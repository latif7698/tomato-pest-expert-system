# Log keputusan dan ketidakpastian

| ID | Jenis | Isi | Dasar/status |
| --- | --- | --- | --- |
| D-01 | Keputusan scope | Keluaran hanya hama tomat; penyakit non-hama dan kekurangan nutrisi dikecualikan. | Instruksi produk. |
| D-02 | Keputusan metode | MVP memakai dukungan CF positif dan aturan satu hubungan gejala–hama. | Kontrak proyek; aturan sumber gabungan perlu kajian. |
| D-03 | Keputusan arsitektur | Python, FastAPI, Uvicorn, Pydantic, UI HTML/CSS/JS tanpa framework, JSON awal; mesin CF terpisah. | Rencana teknologi; versi belum dipilih. |
| D-04 | Keputusan MVP | Tanpa login, admin, database, riwayat permanen, foto/CNN, chatbot, IoT, atau training ML. | Batas scope. |
| D-05 | Usulan desain | Skala `cf_user` 0.25/0.50/0.75/1.00 dan toleransi seri absolut `1e-12`. | Untuk UX/numerik; skala belum divalidasi terhadap pengguna/pakar. |
| D-06 | Keputusan keselamatan klaim | CF bukan akurasi/probabilitas pasti; tidak ada ambang diagnosis; hasil seri diberi penanda. | Makna metode dan batas produk. |
| D-07 | Keputusan data | Mode `demo` dan `verified` terpisah; verified gagal jelas bila data sah tak ada, tanpa fallback. | Mencegah demo disalahartikan nyata. |
| D-08 | Asumsi perencanaan | 3–5 hama, 10–20 gejala, estimasi satu minggu/sprint. | Perkiraan awal saja; jumlah akhir mengikuti sumber. |
| D-09 | Belum diverifikasi | Hama, gejala, aturan, bobot, penanganan, dan kasus berlabel pakar. | PDF belum ditelaah; lihat [register sumber](../knowledge/SOURCE_REGISTER.md). |
| D-10 | Keputusan pengujian | Pisahkan ketepatan hitung, fungsi API/UI, dan evaluasi terhadap label pakar. | Cegah uji software dipakai sebagai klaim lapangan. |

Perubahan keputusan harus menyebut alasan, bukti, dan dampaknya pada kontrak, backlog, serta pengujian.
