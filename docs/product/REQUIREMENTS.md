# Requirements MVP

ID stabil di bawah dipakai oleh [backlog](../scrum/PRODUCT_BACKLOG.md) dan [rencana uji](../testing/TEST_PLAN.md). Semua kriteria diuji dengan data sintetis sampai pengetahuan nyata diverifikasi.

| ID | Requirement | Kriteria penerimaan yang dapat diperiksa |
| --- | --- | --- |
| R-01 | Beranda | Menjelaskan tujuan, batas keluaran hama, dan sifat dugaan CF; menampilkan mode dan `knowledge_version`. |
| R-02 | Daftar gejala | `GET /symptoms` dan UI menampilkan ID serta label gejala dari dataset aktif; tidak menggabungkan mode. |
| R-03 | Form konsultasi | Pengguna dapat memilih gejala unik dan `cf_user` dari skala usulan 0.25/0.50/0.75/1.00; pilihan kosong diperbolehkan. |
| R-04 | Validasi input | Struktur salah, ID gejala asing, duplikat, bobot di luar skala, atau non-finite menghasilkan error validasi tanpa traceback/path internal. |
| R-05 | Perhitungan CF | Setiap aturan positif menghitung perkalian dan kombinasi sesuai kontrak; tanpa pembulatan antara langkah; hasil tidak bergantung pada urutan bukti di luar toleransi numerik. |
| R-06 | Peringkat dugaan | Hanya kandidat dengan dukungan positif tampil; urut CF menurun, hasil seri ditandai dan ID hanya mengurutkan tampilan; tanpa ambang diagnosis. |
| R-07 | Detail perhitungan | Trace untuk tiap dukungan memuat gejala, bobot pakar/pengguna, dukungan, nilai sebelum/sesudah, dan sumber; nilai akhir cocok dengan trace. |
| R-08 | Informasi hama/sumber | `GET /pests/{id}` menampilkan informasi yang bersumber; ID tidak dikenal menghasilkan 404; penanganan hanya tampil jika tervalidasi. |
| R-09 | Mode dan versi | Semua respons relevan dan UI hasil menampilkan `mode` serta `knowledge_version`; demo diberi label jelas. |
| R-10 | Tanpa dukungan | Input kosong valid atau tidak ada aturan yang memberi dukungan menghasilkan `status: no_support`, `candidates: []`, `trace: []`, dan pesan netral. |
| R-11 | Integritas pengetahuan | Loader menolak ID/referensi/duplikat/bobot/status validasi yang tidak sah; mode terverifikasi hanya menerima data terverifikasi. |
| R-12 | Privasi MVP | Konsultasi diproses per permintaan tanpa riwayat permanen, login, atau database. |
| R-13 | Evaluasi domain | Sebelum klaim validasi lapangan, laporan menyebut jumlah kasus, label pakar, kesalahan, dan batas kesimpulan; kasus evaluasi tidak dipakai menyetel bobot. |

R-13 adalah gerbang evaluasi Sprint 3, bukan klaim bahwa evaluasi sudah dapat dilakukan. Rincian skenario ada di [kriteria penerimaan](../testing/ACCEPTANCE_CRITERIA.md).
