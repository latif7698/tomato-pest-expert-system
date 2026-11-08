# Scope produk

## Tujuan dan batas

Pengguna memilih gejala tanaman tomat yang diamati dan tingkat keyakinan pengamatannya. Sistem menghitung dukungan CF positif untuk tiap hama yang memiliki aturan terverifikasi atau, dalam mode demo, aturan sintetis yang diberi label jelas. Keluaran berupa dugaan berperingkat, detail perhitungan, informasi hama, dan sumber yang tersedia. Hasil tidak memastikan penyebab dan tidak menilai akurasi sistem.

MVP mencakup beranda, daftar gejala, formulir konsultasi, perhitungan CF, peringkat dan hasil seri, trace, informasi hama serta sumber, penanda mode dan versi pengetahuan, serta penanganan input salah dan hasil tanpa dukungan. Penyakit non-hama dan kekurangan nutrisi tidak menjadi kelas keluaran.

Di luar MVP: foto/CNN, chatbot, IoT, training ML, login, dashboard admin, database, dan riwayat permanen. Penyimpanan pengetahuan awal direncanakan sebagai JSON. Tidak ada klaim kelayakan penggunaan lapangan sebelum verifikasi pengetahuan dan evaluasi kasus berlabel pakar.

## Status dan batas data

Target awal 3–5 hama serta 10–20 gejala hanyalah perkiraan scope. Snapshot L04 yang diperiksa manusia pada 2026-11-08 memuat lima hama, 10 gejala, dan 11 relasi positif. Status `verified` berarti sumber dan locator diperiksa menurut D-17; ini adaptasi CF positif dari L04, bukan validasi pakar. Penanganan tidak tersedia. Kasus berlabel pakar, evaluasi akurasi lapangan, dan bukti kelayakan penggunaan lapangan belum tersedia; lihat [register sumber](../knowledge/SOURCE_REGISTER.md).
