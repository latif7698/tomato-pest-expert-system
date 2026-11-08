# Rencana pengujian

Pengujian unit bagian A, API bagian B, dan alur UI lewat DOM emulator telah dijalankan dengan fixture sintetis; hasil aktual tercatat di [log kerja](../scrum/WORK_LOG.md). Pengguna melaporkan `npm run test:browser` lulus di WSL, termasuk lebar layar dan keyboard, serta telah meninjau screenshot layar lebar dan sempit. Browser tetap tidak dapat diluncurkan dalam sandbox ini. Bagian C menunggu data berlabel pakar. Catat perintah, lingkungan, tanggal, hasil, serta kegagalan; jangan menyatakan PASS hanya karena test dibuat.

## A. Kebenaran perhitungan dan loader

| Kasus | Requirement | Bukti yang diharapkan |
| --- | --- | --- |
| Satu gejala | R-05, R-07 | Perkalian satu aturan dan trace `before=0`, `after=CF_i`. |
| Dua dukungan | R-05, R-07 | `0.8×1.0`, `0.6×0.5` memberi `0.86`; trace akhir sama. |
| Dukungan nol | R-06, R-10 | Aturan bobot 0 tidak menghasilkan kandidat. |
| Input kosong | R-10 | `no_support`, array kosong. |
| Urutan bukti | R-05 | Permutasi input menghasilkan CF sama dalam toleransi `1e-12`; trace stabil. |
| Hasil seri | R-06 | Dua kandidat bernilai sama: rank sama, `is_tied=true`, ID hanya pengurut tampilan. |
| Gejala asing/duplikat | R-04 | Ditolak, tidak dihitung diam-diam. |
| Bobot salah | R-04, R-11 | Non-finite, di luar rentang, boolean, dan `cf_user` tidak dalam skala ditolak. |
| Referensi aturan rusak | R-11 | Loader gagal untuk ID tidak ada, duplikat pasangan, dan status mode tidak cocok. |
| Trace | R-07 | Rangkaian `before`/`after` dan sumber sesuai nilai akhir. |

## B. Fungsi API dan UI

Dengan HTTPX, periksa ketiga endpoint, JSON, 404, 422 tanpa traceback/path, `no_support`, metadata mode/versi, dan tidak ada persistensi riwayat (R-02–R-12). Secara manual atau lewat uji browser yang relevan, periksa beranda (R-01), pilihan gejala dan skala (R-03), pesan validasi, tampilan seri/no_support, trace/sumber, serta label demo dan versi (R-06–R-10). Mode verified yang datanya hilang harus gagal jelas, bukan memuat demo (R-09, R-11).

## C. Evaluasi ketepatan domain

Dataset dengan sumber yang diperiksa manusia sudah tersedia menurut D-17; evaluasi domain tetap tertunda sampai ada kasus berlabel pakar. Gunakan [protokol evaluasi domain](DOMAIN_EVALUATION_PROTOCOL.md) dan template kasus di `data/evaluation/` untuk mencatat asal kasus, label pembanding, prediksi, metrik, serta batas kesimpulan (R-13). Pisahkan kasus evaluasi dari kasus yang dipakai memilih/menyetel bobot; jika pemisahan gagal, jangan laporkan sebagai uji independen. Kelulusan uji A/B tidak membuktikan ketepatan identifikasi lapangan.
