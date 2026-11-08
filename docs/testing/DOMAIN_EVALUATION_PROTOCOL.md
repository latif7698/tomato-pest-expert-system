# Protokol evaluasi domain B-12

Status: **belum dijalankan**. Template kosong ada di [data/evaluation/cases_template.csv](../../data/evaluation/cases_template.csv). Belum ada kasus hama berlabel pakar; jangan menulis angka ketepatan sistem dari uji software atau dari 90% hasil artikel L04.

## Pengumpulan kasus

Setiap baris template mewakili satu kasus independen. Catat ID kasus, asal dan tanggal pengamatan, label hama dari pakar (P9, P10, P12, P13, P14), identitas/rujukan penilai, dan gejala yang benar-benar diamati. `observations_json` berisi daftar objek `symptom_id` dan `cf_user` sesuai kontrak konsultasi. Catat alasan pemilihan tingkat keyakinan; skala 0.25/0.50/0.75/1.00 adalah keputusan proyek, belum divalidasi terhadap pengguna.

Label harus ditetapkan tanpa melihat keluaran aplikasi. Catat apakah kasus pernah dipakai menetapkan aturan, bobot, atau keputusan scope; pisahkan kasus semacam itu dari evaluasi independen. Kasus dengan label di luar lima hama tidak dimasukkan ke penyebut metrik utama dan dilaporkan terpisah sebagai batas cakupan. Jangan mengubah label, aturan, atau bobot setelah melihat prediksi tanpa mencatat bahwa evaluasi berikutnya tidak lagi independen.

## Penilaian

Jalankan aplikasi dalam `KNOWLEDGE_MODE=verified` dengan versi pengetahuan yang dicatat. Untuk setiap kasus dalam scope, simpan status, daftar kandidat peringkat pertama, penanda seri, dan CF yang ditampilkan. Jika `no_support`, daftar peringkat pertama kosong.

- **Ketepatan peringkat pertama ketat:** jumlah kasus berlabel pakar yang menjadi **satu-satunya** kandidat peringkat pertama dibagi jumlah kasus berlabel dalam scope. Hasil seri dan `no_support` dihitung tidak tepat.
- **Kecocokan himpunan peringkat pertama:** jumlah kasus yang label pakarnya terdapat dalam himpunan kandidat peringkat pertama dibagi jumlah kasus berlabel dalam scope. Seri dapat dihitung cocok di sini, tetapi jumlah seri dilaporkan terpisah.
- **Cakupan dukungan:** jumlah kasus dalam scope dengan status `supported` dibagi jumlah kasus berlabel dalam scope. Ini bukan ukuran ketepatan.

Laporkan pembilang, penyebut, daftar kasus keliru, jumlah seri, jumlah `no_support`, dan jumlah kasus di luar scope. Jangan menyebut CF sebagai probabilitas atau angka ketepatan. Jika jumlah kasus kecil, sumber kasus tidak beragam, atau label pakar tidak independen, nyatakan batas itu pada laporan. Simpan data kasus berizin dan hindari informasi pribadi petani yang tidak diperlukan.

## Kriteria selesai

B-12 tetap Blocked sampai kasus dan label pembanding nyata tersedia. Setelah data diperoleh, pemeriksaan meliputi validasi format, eksekusi setiap kasus terhadap snapshot verified yang tetap, hitungan metrik sesuai definisi di atas, dan tinjauan hasil oleh pemeriksa manusia. Dokumentasikan jumlah kasus, hasil, kesalahan, serta batas kesimpulan di WORK_LOG dan laporan evaluasi.
