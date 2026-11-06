# Scope produk

## Tujuan dan batas

Pengguna memilih gejala tanaman tomat yang diamati dan tingkat keyakinan pengamatannya. Sistem menghitung dukungan CF positif untuk tiap hama yang memiliki aturan terverifikasi atau, dalam mode demo, aturan sintetis yang diberi label jelas. Keluaran berupa dugaan berperingkat, detail perhitungan, informasi hama, dan sumber yang tersedia. Hasil tidak memastikan penyebab dan tidak menilai akurasi sistem.

MVP mencakup beranda, daftar gejala, formulir konsultasi, perhitungan CF, peringkat dan hasil seri, trace, informasi hama serta sumber, penanda mode dan versi pengetahuan, serta penanganan input salah dan hasil tanpa dukungan. Penyakit non-hama dan kekurangan nutrisi tidak menjadi kelas keluaran.

Di luar MVP: foto/CNN, chatbot, IoT, training ML, login, dashboard admin, database, dan riwayat permanen. Penyimpanan pengetahuan awal direncanakan sebagai JSON. Tidak ada klaim kelayakan penggunaan lapangan sebelum verifikasi pengetahuan dan evaluasi kasus berlabel pakar.

## Status dan batas data

Target awal 3–5 hama serta 10–20 gejala hanyalah perkiraan scope. Jumlah akhir mengikuti sumber yang dapat diperiksa. Daftar hama, gejala, aturan, bobot CF, penanganan, dan kasus berlabel pakar belum tersedia/terverifikasi; lihat [register sumber](../knowledge/SOURCE_REGISTER.md). Software dapat dibangun dengan fixture sintetis yang jelas berlabel, sedangkan integrasi nyata dan evaluasi domain tetap terblokir.
