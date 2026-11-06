# Sprint 2 — Konsultasi web

**Estimasi:** satu minggu, bukan komitmen atau deadline. **Status:** berjalan; B-06–B-09 Done berdasarkan uji API dan DOM, B-10 Review menunggu uji browser sungguhan. Item rencana: B-06, B-07, B-08, B-09, B-10. Tujuan: beranda, form, API, peringkat, trace, informasi hama, dan alur error/no_support yang utuh.

## Planning

Prasyarat: hasil Sprint 1 diuji. Rencanakan route `GET /symptoms`, `GET /pests/{id}`, `POST /consultations`, serta UI statis. Tetapkan pemilik, kapasitas, risiko, dan bukti penerimaan per item. Dataset sintetis tetap diberi label `demo`.

## Catatan harian

Catat tanggal, item, tindakan, bukti, hambatan, langkah berikutnya di [WORK_LOG.md](WORK_LOG.md).

## Review

Tunjukkan alur dari beranda ke hasil; input salah, kosong, seri, detail hama, mode/versi, dan respons API. Lampirkan hasil uji HTTPX/UI aktual. Jangan menganggap lulus uji teknis sebagai validasi domain.

## Retrospective

Sesudah review, catat hal yang berjalan baik, masalah, dan tindakan perbaikan untuk Sprint 3. Tindakan sementara: jalankan server lokal dan `npm run test:browser` saat lingkungan mengizinkan; tinjau screenshot 375/768/1280 piksel dan hasil navigasi keyboard. Skrip sudah dibuat tetapi belum berhasil melewati peluncuran Chromium dalam sandbox ini. Uji DOM bukan pengganti pemeriksaan visual.
