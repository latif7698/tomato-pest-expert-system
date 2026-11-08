import { getSymptoms, postConsultation } from "./api.js";
import { renderResult } from "./result.js";

const form = document.querySelector("#consultation-form");
const list = document.querySelector("#symptom-list");
const button = document.querySelector("#submit-button");
const status = document.querySelector("#form-status");
const modeBadge = document.querySelector("#mode-badge");
const version = document.querySelector("#knowledge-version");
const modeExplanation = document.querySelector("#mode-explanation");
const footerNote = document.querySelector("#footer-note");

function setStatus(message, isError = false) {
  status.textContent = message;
  status.classList.toggle("error", isError);
}

function renderSymptoms(symptoms) {
  list.replaceChildren();
  for (const symptom of symptoms) {
    const row = document.createElement("div");
    row.className = "symptom-row";

    const label = document.createElement("label");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = symptom.id;
    checkbox.name = "symptom";
    label.append(checkbox, document.createTextNode(`${symptom.label} (${symptom.id})`));

    const select = document.createElement("select");
    select.setAttribute("aria-label", `Keyakinan pengamatan ${symptom.label}`);
    select.disabled = true;
    for (const [value, text] of [
      ["0.25", "Rendah · 0,25"],
      ["0.50", "Sedang · 0,50"],
      ["0.75", "Tinggi · 0,75"],
      ["1.00", "Sangat yakin · 1,00"],
    ]) {
      const option = new Option(text, value);
      select.add(option);
    }
    select.value = "1.00";
    checkbox.addEventListener("change", () => { select.disabled = !checkbox.checked; });
    row.append(label, select);
    list.append(row);
  }
}

async function initialize() {
  try {
    const data = await getSymptoms();
    modeBadge.className = `mode-badge ${data.mode}`;
    if (data.mode === "demo") {
      modeBadge.textContent = "MODE DEMO · DATA SINTETIS";
      modeExplanation.textContent = "Data demo sepenuhnya sintetis dan hanya untuk mencoba alur aplikasi.";
    } else {
      modeBadge.textContent = "SUMBER DIPERIKSA";
      modeExplanation.textContent = "Data ini adaptasi CF positif dari L04: aturan AND diuraikan per gejala dan enam relasi negatif tidak dihitung. Skala keyakinan pengamatan belum divalidasi. Sumber diperiksa manusia, bukan divalidasi pakar; belum ada bukti akurasi khusus hama.";
      footerNote.textContent = "Prototipe tugas kuliah. Sumber diperiksa; hasil bukan diagnosis pasti dan belum diuji terhadap kasus hama berlabel pakar.";
    }
    version.textContent = `Versi pengetahuan: ${data.knowledge_version}`;
    renderSymptoms(data.symptoms);
    button.disabled = false;
    setStatus("");
  } catch (error) {
    list.textContent = "Daftar gejala belum tersedia.";
    setStatus(error.message, true);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const observations = [...list.querySelectorAll(".symptom-row")]
    .filter((row) => row.querySelector('input[type="checkbox"]').checked)
    .map((row) => ({
      symptom_id: row.querySelector('input[type="checkbox"]').value,
      cf_user: Number(row.querySelector("select").value),
    }));
  button.disabled = true;
  document.querySelector("#result-section").hidden = true;
  setStatus("Menghitung…");
  let succeeded = false;
  try {
    const result = await postConsultation(observations);
    await renderResult(result);
    setStatus("Perhitungan selesai.");
    document.querySelector("#result-section").focus();
    succeeded = true;
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    button.disabled = false;
    if (!succeeded) button.focus();
  }
});

initialize();
