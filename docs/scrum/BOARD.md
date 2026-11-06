# Board kerja

Status resmi: `Backlog`, `Ready`, `In Progress`, `Review`, `Done`, `Blocked`. Detail dan kriteria tiap item ada di [product backlog](PRODUCT_BACKLOG.md); board ini adalah ringkasan dan harus diperbarui bersamaan dengannya.

| Status | Item | Alasan/bukti saat ini |
| --- | --- | --- |
| Backlog | B-13 | Sprint 3 belum dimulai. |
| Ready | — | Tidak ada. |
| In Progress | — | Tidak ada. |
| Review | B-05, B-10 | B-05: Ruff tetap tidak ada di cache offline; lint belum dijalankan. B-10: assertion browser setelah semua submit kini menunggu respons dan render selesai; API `no_support` serta reproduksi DOM sesuai kontrak dan 67 uji Python lulus, tetapi Chromium tidak dapat diluncurkan di sandbox ini. Hasil browser penuh di WSL pengguna dan tinjauan tampilan belum tersedia. |
| Done | B-01, B-03, B-04, B-06, B-07, B-08, B-09 | Dokumentasi dan komponen inti diuji; alur API/UI sintetis diperiksa lewat HTTPX dan DOM emulator. Lihat log untuk batas pengujian. |
| Blocked | B-02, B-11, B-12 | PDF/pengetahuan terverifikasi dan kasus berlabel pakar belum tersedia. |

Saat memperbarui status, catat perintah uji, hasil, dan bukti pada [WORK_LOG.md](WORK_LOG.md). `Blocked` berarti dependensi nyata belum tersedia; software sintetis tetap bisa dikerjakan.
