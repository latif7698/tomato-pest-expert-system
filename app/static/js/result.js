import { getPest } from "./api.js";

const section = document.querySelector("#result-section");
const content = document.querySelector("#result-content");

function element(tag, text, className = "") {
  const node = document.createElement(tag);
  node.textContent = text;
  if (className) node.className = className;
  return node;
}

function number(value) {
  return Number(value).toFixed(4);
}

function addSources(container, sources) {
  const heading = element("p", "Sumber informasi:");
  const list = document.createElement("ul");
  list.className = "source-list";
  for (const source of sources) {
    const item = document.createElement("li");
    if (source.url) {
      const link = document.createElement("a");
      link.href = source.url;
      link.textContent = source.title;
      link.rel = "noopener noreferrer";
      link.target = "_blank";
      item.append(link);
    } else {
      item.textContent = source.title;
    }
    list.append(item);
  }
  container.append(heading, list);
}

function addTrace(trace) {
  const block = document.createElement("section");
  block.className = "trace-block";
  block.append(element("h3", "Detail perhitungan CF"));
  const wrapper = document.createElement("div");
  wrapper.className = "trace-wrap";
  const table = document.createElement("table");
  const headers = ["Hama", "Gejala", "CF pakar", "Keyakinan pengamatan", "Dukungan", "Sebelum", "Sesudah", "Sumber/locator"];
  const thead = document.createElement("thead");
  const headingRow = document.createElement("tr");
  for (const header of headers) headingRow.append(element("th", header));
  thead.append(headingRow);
  const tbody = document.createElement("tbody");
  for (const step of trace) {
    const row = document.createElement("tr");
    for (const value of [step.pest_id, step.symptom_id, number(step.cf_expert), number(step.cf_user), number(step.support), number(step.before), number(step.after), `${step.source_id} · ${step.source_locator}`]) {
      row.append(element("td", value));
    }
    tbody.append(row);
  }
  table.append(thead, tbody);
  wrapper.append(table);
  block.append(wrapper, element("p", "CF_i = CF pakar × keyakinan pengamatan; CF gabungan = CF sebelumnya + dukungan × (1 − CF sebelumnya). Angka di tabel dibulatkan hanya untuk tampilan.", "muted"));
  content.append(block);
}

export async function renderResult(result) {
  section.hidden = false;
  content.replaceChildren();
  const mode = result.mode === "demo" ? "DEMO · DATA SINTETIS" : "PENGETAHUAN TERVERIFIKASI";
  content.append(element("p", `${mode} · Versi ${result.knowledge_version}`, "result-meta"));
  if (result.status === "no_support") {
    content.append(element("p", "Belum ada dukungan positif dari gejala yang dipilih. Tidak ada dugaan hama yang dapat ditampilkan."));
    return;
  }
  content.append(element("p", "Peringkat di bawah menunjukkan dukungan CF relatif terhadap aturan yang tersedia. Nilai antar-hama tidak harus berjumlah 100%."));
  for (const candidate of result.candidates) {
    const card = document.createElement("article");
    card.className = "candidate";
    const header = document.createElement("div");
    header.className = "candidate-head";
    const title = element("h3", `#${candidate.rank} · ${candidate.name}`);
    if (candidate.is_tied) title.append(element("span", "Seri", "tie"));
    header.append(title, element("span", `CF ${number(candidate.cf)}`, "cf-value"));
    card.append(header);
    try {
      const details = await getPest(candidate.pest_id);
      card.append(element("p", details.pest.description));
      if (details.pest.handling) card.append(element("p", `Penanganan: ${details.pest.handling}`));
      addSources(card, details.pest.sources);
    } catch {
      card.append(element("p", "Detail hama belum tersedia.", "error"));
    }
    content.append(card);
  }
  addTrace(result.trace);
}
