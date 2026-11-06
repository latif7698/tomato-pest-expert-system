# Kontrak Certainty Factor MVP

Model MVP memakai **dukungan positif**. Satu hubungan hama–gejala menyumbang satu dukungan bila gejala dipilih. Untuk aturan cocok ke-`i`:

```text
CF_i = CF_expert_i × CF_user_i
CF_combined = CF_previous + CF_i × (1 - CF_previous)
```

Mulai `CF_previous = 0` **untuk setiap kandidat hama**. Akumulasikan seluruh dukungan kandidat tersebut. Semua bobot harus finite dan berada dalam 0–1. Jangan membulatkan di setiap langkah; pembulatan hanya untuk tampilan. Input gejala duplikat ditolak agar satu aturan tidak dihitung dua kali. Untuk trace yang stabil, proses aturan menurut `symptom_id` setelah validasi; hasil matematis tetap sama saat urutan input berubah, dengan toleransi galat floating point.

Gejala yang tidak dipilih atau yang pengamatannya belum diketahui tidak memberi dukungan; tidak dipilih bukan bukti negatif. ID gejala asing dalam request adalah input tidak valid dan ditolak. Kandidat tanpa dukungan positif tidak ditampilkan. Jika tidak ada dukungan, keluarkan `no_support`, bukan diagnosis kosong dengan nilai nol. CF antar-hama tidak harus berjumlah 100%; hasil tertinggi bukan penyebab pasti. Seri pada nilai akhir dalam toleransi numerik yang terdokumentasi ditandai `is_tied`; ID hanya untuk urutan tampilan seri. Jangan menetapkan ambang diagnosis tanpa dasar.

Skala usulan `CF_user`: `0.25`, `0.50`, `0.75`, `1.00` (label UI perlu dijelaskan pada implementasi). Ini **keputusan desain yang belum divalidasi**, bukan bobot dari jurnal. Nilai nol hanya dapat muncul dari bobot pakar 0 dalam data dan tidak memberi dukungan. Permintaan kosong valid. ID asing atau `CF_user` di luar skala ditolak. Jika sumber memakai premis gabungan AND/OR, jangan mengubahnya menjadi aturan gejala tunggal tanpa kajian.

## Contoh sintetis

`0.8 × 1.0 = 0.8`; `0.6 × 0.5 = 0.3`; gabungan `0.8 + 0.3 × (1 - 0.8) = 0.86`. Angka tersebut hanya fixture uji, bukan bobot hama nyata.

Setiap langkah trace memuat `symptom_id`, `cf_expert`, `cf_user`, `support`, `before`, `after`, `source_id`, dan `source_locator`. Trace kandidat akhir harus bisa direkonstruksi sampai CF yang dikembalikan. Lihat [kontrak API](../architecture/API_CONTRACT.md).
