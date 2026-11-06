/* Browser verification against a running local demo app.
 * Run: node tests/browser_flow.cjs
 * Optional: APP_BASE_URL and PLAYWRIGHT_MODULE environment variables.
 * Screenshots are written to /tmp for visual review.
 */
const assert = require("node:assert/strict");
const path = require("node:path");

const playwrightModule = process.env.PLAYWRIGHT_MODULE || "playwright";
const { chromium } = require(playwrightModule);
const baseURL = process.env.APP_BASE_URL || "http://127.0.0.1:8000";

async function submitAndWait(page, action, expectedHttpStatus, expectedUiStatus) {
  const responsePromise = page.waitForResponse((response) =>
    response.url().endsWith("/consultations") && response.request().method() === "POST"
  );
  await action();
  const response = await responsePromise;
  assert.equal(response.status(), expectedHttpStatus);
  await page.locator("#submit-button:not([disabled])").waitFor();
  assert.equal(await page.locator("#form-status").innerText(), expectedUiStatus);
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
    assert.match(await page.locator("#mode-badge").innerText(), /MODE DEMO · DATA SINTETIS/);
    assert.match(await page.locator("#knowledge-version").innerText(), /demo-001/);

    const boxes = page.locator('.symptom-row input[type="checkbox"]');
    assert.equal(await boxes.count(), 2);
    await boxes.nth(0).check();
    await boxes.nth(1).check();
    await page.locator(".symptom-row select").nth(1).selectOption("0.50");
    const firstResponse = await submitAndWait(
      page, () => page.locator("#submit-button").click(), 200, "Perhitungan selesai."
    );
    assert.deepEqual(firstResponse.request().postDataJSON(), {
      observations: [
        { symptom_id: "G_SYN_1", cf_user: 1 },
        { symptom_id: "G_SYN_2", cf_user: 0.5 },
      ],
    });
    assert.match(await page.locator("#result-content").innerText(), /CF 0\.8600/);
    assert.match(await page.locator("#result-content").innerText(), /Fixture sintetis/);
    assert.equal(await page.locator(".trace-block tbody tr").count(), 2);
    assert.equal(await page.locator("#result-section").evaluate((node) => node === document.activeElement), true);

    for (const width of [375, 768, 1280]) {
      await page.setViewportSize({ width, height: 800 });
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
      assert.ok(overflow <= 1, `horizontal overflow at ${width}px: ${overflow}px`);
      await page.screenshot({ path: path.join("/tmp", `tomato-browser-${width}.png`), fullPage: true });
    }

    await boxes.nth(0).uncheck();
    await boxes.nth(1).uncheck();
    const noSupportResponse = await submitAndWait(
      page, () => page.locator("#submit-button").click(), 200, "Perhitungan selesai."
    );
    assert.deepEqual(noSupportResponse.request().postDataJSON(), { observations: [] });
    const noSupport = await noSupportResponse.json();
    assert.equal(noSupport.status, "no_support");
    assert.deepEqual(noSupport.candidates, []);
    assert.match(await page.locator("#result-content").innerText(), /Belum ada dukungan positif/);
    assert.equal(await page.locator(".candidate").count(), 0);

    const tie = await page.evaluate(async () => {
      const response = await fetch("/consultations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ observations: [{ symptom_id: "G_SYN_1", cf_user: 1 }] }),
      });
      return response.json();
    });
    tie.candidates[0].is_tied = true;
    tie.candidates.unshift({ ...tie.candidates[0], pest_id: "P_SYN_0", name: "Hama sintetis B" });
    tie.trace.unshift({ ...tie.trace[0], pest_id: "P_SYN_0" });
    const tiedPest = await page.evaluate(async () => (await fetch("/pests/P_SYN_1")).json());
    tiedPest.pest.id = "P_SYN_0";
    tiedPest.pest.name = "Hama sintetis B";
    await page.route("**/pests/P_SYN_0", async (route) => {
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(tiedPest) });
    });
    await page.route("**/consultations", async (route) => {
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(tie) });
    });
    await boxes.nth(0).check();
    await submitAndWait(page, () => page.locator("#submit-button").click(), 200, "Perhitungan selesai.");
    assert.equal(await page.locator(".candidate .tie").count(), 2);
    assert.equal(await page.locator(".candidate .source-list").count(), 2);
    await page.unroute("**/consultations");
    await page.unroute("**/pests/P_SYN_0");

    await page.route("**/consultations", async (route) => {
      await route.fulfill({
        status: 422,
        contentType: "application/json",
        body: JSON.stringify({ error: { code: "invalid_input", message: "Input konsultasi tidak valid." } }),
      });
    });
    await submitAndWait(page, () => page.locator("#submit-button").click(), 422, "Input konsultasi tidak valid.");
    assert.equal(await page.locator("#result-section").isHidden(), true);
    assert.equal(await page.locator("#submit-button").evaluate((node) => node === document.activeElement), true);
    await page.unroute("**/consultations");

    await page.reload({ waitUntil: "networkidle" });
    await page.locator("#submit-button:not([disabled])").waitFor();
    await page.keyboard.press("Tab");
    assert.equal(await boxes.nth(0).evaluate((node) => node === document.activeElement), true);
    await page.keyboard.press("Space");
    assert.equal(await boxes.nth(0).isChecked(), true);
    await page.keyboard.press("Tab");
    assert.equal(await page.locator(".symptom-row select").first().evaluate((node) => node === document.activeElement), true);
    await page.keyboard.press("ArrowUp");
    assert.equal(await page.locator(".symptom-row select").first().inputValue(), "0.75");
    await page.keyboard.press("Tab");
    await page.keyboard.press("Tab");
    assert.equal(await page.locator("#submit-button").evaluate((node) => node === document.activeElement), true);
    await submitAndWait(page, () => page.keyboard.press("Enter"), 200, "Perhitungan selesai.");
    assert.match(await page.locator("#result-content").innerText(), /CF 0\.6000/);
    assert.equal(await page.locator("#result-section").evaluate((node) => node === document.activeElement), true);
    assert.deepEqual(errors, []);
    console.log("Browser flow passed: consultation, trace/source, no_support, tie, error, widths, keyboard");
  } finally {
    await browser.close();
  }
}

run().catch((error) => { console.error(error); process.exitCode = 1; });
