# Kriteria penerimaan

Dokumen ini merinci bukti penerimaan untuk [requirements](../product/REQUIREMENTS.md). Uji Python, API, dan alur browser verified dijalankan pada 2026-11-08; bukti ada di [log kerja](../scrum/WORK_LOG.md). Ruff pada seluruh `app tests` berjalan dan menemukan enam temuan lama; berkas Python Tahap 2 lolos lint. Evaluasi domain berlabel pakar belum tersedia.

| Requirement | Pemeriksaan penerimaan | Bukti |
| --- | --- | --- |
| R-01 | Buka beranda; lihat batas hama, sifat dugaan, mode, versi. | Pemeriksaan UI. |
| R-02 | `GET /symptoms` dan UI memakai dataset aktif yang sama. | Uji API + UI. |
| R-03 | Form menerima pilihan unik dengan empat tingkat keyakinan dan input kosong. | Uji UI + request. |
| R-04 | Kirim struktur salah, ID asing, duplikat, non-finite, dan nilai di luar skala. | `422` aman; uji API. |
| R-05 | Hitung satu aturan, dua aturan (`0.86`), dan permutasi input. | Uji mesin CF. |
| R-06 | Periksa kandidat nol terbuang, ranking menurun, seri berbagi rank dan ditandai. | Uji mesin/layanan/API. |
| R-07 | Rekonstruksi hasil akhir dari trace termasuk sumber. | Uji mesin/API. |
| R-08 | Buka detail hama dan minta ID asing; penanganan tanpa bukti tidak tampil. | Uji API + UI. |
| R-09 | Periksa `mode`/`knowledge_version` di respons dan UI; demo jelas. | Uji API + UI. |
| R-10 | Kirim input kosong dan input valid tanpa aturan positif. | `no_support`, dua array kosong. |
| R-11 | Muat dataset cacat dan verified tanpa data yang sah. | Loader gagal tanpa fallback demo. |
| R-12 | Lakukan konsultasi dan periksa tidak ada mekanisme simpan permanen/riwayat. | Review arsitektur + uji alur. |
| R-13 | Evaluasi dengan kasus berlabel pakar yang terpisah dari penetapan bobot. | Laporan jumlah kasus, label, kesalahan, keterbatasan; saat ini Blocked. |

`Done` hanya diberikan sesudah pemeriksaan sesuai butir dijalankan dan hasilnya tercatat. Kriteria teknis R-01–R-12 dapat diuji dengan fixture sintetis; itu tidak mengubah status R-13.
