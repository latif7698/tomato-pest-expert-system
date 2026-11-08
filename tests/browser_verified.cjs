/* Run against a server started with KNOWLEDGE_MODE=verified. */
const assert = require("node:assert/strict");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");

const baseURL = process.env.APP_BASE_URL || "http://127.0.0.1:8000";

async function submit(page) {
  const responsePromise = page.waitForResponse((response) =>
    response.url().endsWith("/consultations") && response.request().method() === "POST"
  );
  await page.locator("#submit-button").click();
  const response = await responsePromise;
  assert.equal(response.status(), 200);
  await page.locator("#submit-button:not([disabled])").waitFor();
  assert.equal(await page.locator("#form-status").innerText(), "Perhitungan selesai.");
  return response;
}

async function run() {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    const errors = [];
    page.on("pageerror", (error) => errors.push(error.message));
    await page.goto(baseURL, { waitUntil: "networkidle" });
    await page.locator("#submit-button:not([disabled])").waitFor();
    assert.equal(await page.locator("#mode-badge").innerText(), "SUMBER DIPERIKSA");
    assert.match(await page.locator("#knowledge-version").innerText(), /l04-2026-11-08-v1/);
    assert.match(await page.locator("#mode-explanation").innerText(), /AND diuraikan per gejala/);
    assert.match(await page.locator("#mode-explanation").innerText(), /relasi negatif tidak dihitung/);
    assert.match(await page.locator("#mode-explanation").innerText(), /belum divalidasi/);
    assert.match(await page.locator("#mode-explanation").innerText(), /belum ada bukti akurasi khusus hama/);

    const rows = page.locator(".symptom-row");
    assert.equal(await rows.count(), 10);
    for (const id of ["G30", "G31", "G32"]) {
      await rows.locator(`input[value="${id}"]`).check();
    }
    const response = await submit(page);
    const result = await response.json();
    assert.equal(result.mode, "verified");
    assert.equal(result.candidates[0].pest_id, "P12");
    assert.equal(result.candidates[0].cf, 0.952);
    assert.match(await page.locator("#result-content").innerText(), /CF 0\.9520/);
    assert.match(await page.locator("#result-content").innerText(), /SUMBER DIPERIKSA · BUKAN VALIDASI PAKAR/);
    assert.match(await page.locator(".candidate").first().innerText(), /Sumber diperiksa:/);
    assert.equal(await page.locator(".candidate").first().locator(".source-list li").count(), 2);
    assert.equal(await page.locator(".trace-block tbody tr").count(), 4);
    assert.match(await page.locator(".trace-block").innerText(), /SRC-01 · hal\. cetak 455/);

    for (const width of [375, 768, 1280]) {
      await page.setViewportSize({ width, height: 800 });
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
      assert.ok(overflow <= 1, `horizontal overflow at ${width}px: ${overflow}px`);
    }

    for (const id of ["G30", "G31", "G32"]) {
      await rows.locator(`input[value="${id}"]`).uncheck();
    }
    const empty = await submit(page);
    assert.equal((await empty.json()).status, "no_support");
    assert.match(await page.locator("#result-content").innerText(), /Belum ada dukungan positif/);
    assert.deepEqual(errors, []);
    console.log("Verified browser flow passed: mode, limits, consultation, sources, trace, no_support, widths");
  } finally {
    await browser.close();
  }
}

run().catch((error) => { console.error(error); process.exitCode = 1; });
