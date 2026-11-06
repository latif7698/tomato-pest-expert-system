async function requestJson(path, options = {}) {
  const response = await fetch(path, options);
  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error("Respons layanan tidak dapat dibaca.");
  }
  if (!response.ok) {
    throw new Error(data?.error?.message || "Permintaan tidak dapat diproses.");
  }
  return data;
}

export function getSymptoms() {
  return requestJson("/symptoms");
}

export function getPest(pestId) {
  return requestJson(`/pests/${encodeURIComponent(pestId)}`);
}

export function postConsultation(observations) {
  return requestJson("/consultations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ observations }),
  });
}
