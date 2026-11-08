# Product backlog

Status yang dipakai: **Backlog**, **Ready**, **In Progress**, **Review**, **Done**, **Blocked**. `Done` membutuhkan bukti pada [kriteria penerimaan](../testing/ACCEPTANCE_CRITERIA.md). Sprint adalah rencana, bukan tanda pekerjaan telah dimulai. Satu minggu per sprint hanya estimasi.

| ID | User story/tujuan | Prioritas | Req. | Acceptance criteria ringkas | Dependensi | Target | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B-01 | Sebagai tim, saya memiliki scope, keputusan, kontrak, dan gap sumber yang tercatat. | Tinggi | R-01–R-13 | Dokumen saling konsisten dan tautan valid. | Tidak ada | Persiapan | Done |
| B-02 | Sebagai tim, saya dapat menelusuri PDF dan memisahkan data hama dari penyakit. | Tinggi | R-08, R-11, R-13 | Locator sumber tiap entri dan status verifikasi tercatat. | Akses/telaah PDF, bukti pemeriksa manusia | Persiapan/Sprint 3 | Done |
| B-03 | Sebagai developer, saya dapat memuat dan memvalidasi JSON pengetahuan. | Tinggi | R-09, R-11 | ID, referensi, bobot, duplikat, mode, versi diuji. | B-01 | Sprint 1 | Done |
| B-04 | Sebagai developer, saya dapat menghitung CF tanpa server. | Tinggi | R-05, R-06, R-07, R-10 | Uji angka 0.86, nol, seri, urutan, trace. | B-01, B-03 | Sprint 1 | Done |
| B-05 | Sebagai developer, saya mempunyai fixture dan pengujian unit yang dapat diulang. | Tinggi | R-05–R-07, R-10, R-11 | pytest menjalankan kasus A yang relevan dan mencatat hasil aktual; Ruff dijalankan. | B-03, B-04 | Sprint 1 | Done |
| B-06 | Sebagai pengguna, saya melihat beranda dan daftar gejala aktif. | Tinggi | R-01, R-02, R-09 | UI dan `GET /symptoms` konsisten, mode/versi terlihat. | B-03 | Sprint 2 | Done |
| B-07 | Sebagai pengguna, saya mengirim observasi dengan keyakinan dan menerima hasil aman. | Tinggi | R-03, R-04, R-05, R-10, R-12 | POST valid/invalid/no_support diuji; tanpa persistensi. | B-04, B-05 | Sprint 2 | Done |
| B-08 | Sebagai pengguna, saya melihat peringkat, seri, dan trace yang dapat dijelaskan. | Tinggi | R-06, R-07, R-09 | Ranking/trace/sumber/mode/versi tampil, cocok dengan API. | B-07 | Sprint 2 | Done |
| B-09 | Sebagai pengguna, saya membuka detail hama beserta sumbernya. | Sedang | R-08 | Detail dan 404 diuji; penanganan tanpa bukti tidak tampil. | B-03, B-06 | Sprint 2 | Done |
| B-10 | Sebagai tim, saya menguji API dan UI pada alur utama serta error. | Tinggi | R-01–R-12 | Semua pemeriksaan B pada test plan dijalankan dan dicatat. | B-06–B-09 | Sprint 2 | Done |
| B-11 | Sebagai tim, saya mengaktifkan pengetahuan hama terverifikasi. | Tinggi | R-02, R-08, R-09, R-11 | Checklist per entri, loader verified, tanpa fallback demo. | B-02, B-03 | Sprint 3 | Done |
| B-12 | Sebagai tim, saya mengukur ketepatan terhadap label pakar secara jujur. | Tinggi | R-13 | Jumlah kasus, label, kesalahan, batas kesimpulan dilaporkan; data independen. | B-11, kasus berlabel pakar | Sprint 3 | Blocked |
| B-13 | Sebagai tim, saya menyelaraskan dokumentasi akhir dengan implementasi. | Sedang | R-01–R-13 | Kontrak, cara jalan, bukti uji, dan keterbatasan diperbarui. | B-10–B-12 | Sprint 3 | In Progress |

`B-02` dan `B-11` selesai menurut pemeriksaan sumber D-17 pada 2026-11-08, bukan karena fixture sintetis. `B-12` menunggu kasus berlabel pakar. B-13 mendokumentasikan keterbatasan tanpa menyebut produk tervalidasi untuk lapangan.
