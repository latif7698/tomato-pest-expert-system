# Spesifikasi pengetahuan

Satu file JSON adalah satu snapshot pengetahuan aktif. Field wajib: `knowledge_version` (string versi yang tidak kosong), `domain` (nilai `tomato_pests`), `mode` (`demo` atau `verified`), `pests` (array), `symptoms` (array), `rules` (array), dan `sources` (array). ID stabil dalam snapshot. Dataset `demo` dan `verified` disimpan di folder berbeda; konfigurasi memilih salah satunya secara eksplisit.

| Entitas | Field wajib | Catatan |
| --- | --- | --- |
| `pests[]` | `id`, `name`, `description`, `source_ids` | `handling` opsional dan hanya boleh dari sumber yang diverifikasi. |
| `symptoms[]` | `id`, `label`, `source_ids` | Label observasi, bukan kesimpulan. |
| `rules[]` | `pest_id`, `symptom_id`, `cf_expert`, `source_id`, `source_locator`, `validation_status` | Satu pasangan hama–gejala sekali dalam MVP. |
| `sources[]` | `id`, `title`, `url`, `access_status` | Locator aturan menunjuk halaman/tabel/bagian yang bisa diperiksa; DOI opsional. |

`validation_status` yang diusulkan: `synthetic` untuk demo dan `verified` hanya sesudah bukti aturan/bobot/locator dicek serta dicatat. Status tersebut tidak menggantikan bukti. `source_ids` dan `source_id` harus menunjuk sumber yang ada. Aturan demo boleh memakai sumber sintetis berlabel, bukan artikel seolah bobotnya berasal dari sana.

## Validasi loader

- ID unik dalam masing-masing koleksi; `pest_id`, `symptom_id`, `source_id`, dan semua `source_ids` harus ada.
- `cf_expert` numerik finite, bukan boolean, pada rentang inklusif 0–1. Pasangan `(pest_id, symptom_id)` tidak boleh duplikat.
- `mode=demo` hanya diizinkan dari lokasi demo dan aturan berstatus `synthetic`; `mode=verified` hanya dari lokasi verified dengan semua aturan berstatus `verified`, bukti sumber/locator, dan tanpa fallback ke demo.
- Data atau relasi yang salah menggagalkan pemuatan secara jelas; tidak diam-diam dilewati. Data nyata baru boleh diberi status `verified` setelah [checklist](VERIFICATION_CHECKLIST.md) selesai per entri.
- Jika sumber menggunakan premis gabungan AND/OR, tahan aturan tersebut untuk kajian model; jangan pecah otomatis menjadi aturan tunggal.

Contoh struktur **sintetis**, bukan data hama tomat nyata:

```json
{
  "knowledge_version": "demo-001",
  "domain": "tomato_pests",
  "mode": "demo",
  "pests": [{"id": "P_SYN_1", "name": "Hama sintetis A", "description": "Hanya contoh uji", "source_ids": ["S_SYN"]}],
  "symptoms": [
    {"id": "G_SYN_1", "label": "Gejala sintetis A", "source_ids": ["S_SYN"]},
    {"id": "G_SYN_2", "label": "Gejala sintetis B", "source_ids": ["S_SYN"]}
  ],
  "rules": [
    {"pest_id": "P_SYN_1", "symptom_id": "G_SYN_1", "cf_expert": 0.8, "source_id": "S_SYN", "source_locator": "fixture sintetis", "validation_status": "synthetic"},
    {"pest_id": "P_SYN_1", "symptom_id": "G_SYN_2", "cf_expert": 0.6, "source_id": "S_SYN", "source_locator": "fixture sintetis", "validation_status": "synthetic"}
  ],
  "sources": [{"id": "S_SYN", "title": "Fixture sintetis, bukan referensi domain", "url": null, "access_status": "synthetic"}]
}
```

Contoh ini hanya mendefinisikan bentuk. Snapshot nyata yang sumbernya diperiksa manusia pada 2026-11-08 ada di [`data/verified/knowledge_verified.json`](../../data/verified/knowledge_verified.json). Definisi `verified` mengikuti D-17 dan [audit manusia](L04_HUMAN_AUDIT_RESOLUTION_2026-11-08.md), tanpa klaim validasi pakar atau akurasi lapangan. Kasus berlabel pakar tetap tertunda.
