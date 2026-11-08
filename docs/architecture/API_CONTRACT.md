# Kontrak API rencana MVP

Semua contoh berikut **sintetis**. JSON menggunakan `snake_case`; `mode` adalah `demo` atau `verified`. Respons sukses membawa `knowledge_version` dan `mode`. Status konsultasi hanya `supported` atau `no_support`. Nilai CF mentah dikirim tanpa pembulatan; UI boleh membulatkan untuk tampilan dan harus menyebutnya sebagai dukungan CF, bukan akurasi.

## `GET /symptoms`

`200 OK`:

```json
{
  "knowledge_version": "demo-001",
  "mode": "demo",
  "symptoms": [
    {"id": "G_SYN_1", "label": "Gejala sintetis A"},
    {"id": "G_SYN_2", "label": "Gejala sintetis B"}
  ]
}
```

## `GET /pests/{id}`

`200 OK` untuk `P_SYN_1`:

```json
{
  "knowledge_version": "demo-001",
  "mode": "demo",
  "pest": {
    "id": "P_SYN_1",
    "name": "Hama sintetis A",
    "description": "Hanya fixture pengujian, bukan hama nyata",
    "handling": null,
    "sources": [{"id": "S_SYN", "title": "Fixture sintetis, bukan referensi domain", "url": null}]
  }
}
```

ID hama tidak ditemukan: `404 Not Found` dengan error terkontrol.

## `POST /consultations`

Request (gejala unik; `cf_user` dari skala 0.25/0.50/0.75/1.00):

```json
{
  "observations": [
    {"symptom_id": "G_SYN_1", "cf_user": 1.0},
    {"symptom_id": "G_SYN_2", "cf_user": 0.5}
  ]
}
```

`200 OK` dengan dua aturan sintetis untuk kandidat yang sama (`cf_expert` 0.8 dan 0.6):

```json
{
  "knowledge_version": "demo-001",
  "mode": "demo",
  "status": "supported",
  "candidates": [
    {"pest_id": "P_SYN_1", "name": "Hama sintetis A", "cf": 0.86, "rank": 1, "is_tied": false}
  ],
  "trace": [
    {"pest_id": "P_SYN_1", "symptom_id": "G_SYN_1", "cf_expert": 0.8, "cf_user": 1.0, "support": 0.8, "before": 0.0, "after": 0.8, "source_id": "S_SYN", "source_locator": "fixture sintetis"},
    {"pest_id": "P_SYN_1", "symptom_id": "G_SYN_2", "cf_expert": 0.6, "cf_user": 0.5, "support": 0.3, "before": 0.8, "after": 0.86, "source_id": "S_SYN", "source_locator": "fixture sintetis"}
  ]
}
```

`rank` adalah peringkat kompetisi (seri berbagi peringkat), urutan CF menurun antar kelompok seri; ID hanya mengurutkan kandidat dalam toleransi seri. Seri ditandai `is_tied` bila selisih absolut CF akhir ≤ `1e-12` (toleransi desain untuk floating point). `trace` diurutkan per `pest_id`, lalu `symptom_id` untuk hasil stabil. Hanya kandidat dengan `cf > 0` yang dikembalikan. `CF_user` adalah keyakinan pengamatan, bukan probabilitas.

Request kosong `{"observations": []}` atau input valid tanpa aturan dengan dukungan positif mengembalikan `200 OK`:

```json
{"knowledge_version":"demo-001","mode":"demo","status":"no_support","candidates":[],"trace":[]}
```

## Error dan penyimpanan

Struktur request salah, gejala asing/duplikat, `cf_user` non-finite atau tidak dalam skala: `422 Unprocessable Entity`. Bentuk error aplikasi: `{"error":{"code":"invalid_input","message":"Input konsultasi tidak valid."}}`; detail validasi boleh ditambahkan tanpa traceback atau path internal. Hama tidak ada: `{"error":{"code":"pest_not_found","message":"Hama tidak ditemukan."}}`. Kegagalan pemuatan dataset adalah kegagalan konfigurasi/layanan, tidak boleh fallback diam-diam ke demo. MVP semula tidak memiliki login, database, atau riwayat permanen.

Pengembangan pasca-MVP D-23 menambah backend PostgreSQL eksplisit untuk mode verified. Kontrak `POST /consultations` sukses tetap sama; setelah hitung, input dan hasil ditulis atomik sebagai catatan anonim. Bila penulisan gagal, server memberi `503` dengan `error.code: storage_unavailable` (tidak mengklaim hasil telah tersimpan). Mode JSON tidak menulis catatan. `GET /healthz` memberi `200 {"status":"ok"}` jika proses siap dan DB aktif dapat dihubungi; gangguan DB menghasilkan `503`. Tidak ada endpoint baca riwayat publik.
