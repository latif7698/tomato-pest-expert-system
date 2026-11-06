# Instruksi kerja Codex

- Sebelum bekerja, baca [scope](docs/product/SCOPE.md), [keputusan](docs/decisions/DECISION_LOG.md), [board](docs/scrum/BOARD.md), dan dokumen sprint aktif.
- Implementasikan hanya pekerjaan yang diminta pengguna dan jaga pekerjaan yang sudah ada. Kerjakan tanpa subagent.
- Pisahkan algoritma CF dari API, UI, dan data domain. Mesin CF harus bisa diuji tanpa server.
- Jangan mengarang daftar hama, gejala, bobot pakar, sumber, atau rekomendasi penanganan. Data sintetis harus diberi label demo/fixture dan dipisahkan dari data terverifikasi.
- Jangan menyebut nilai CF sebagai akurasi, probabilitas terkalibrasi, atau diagnosis pasti.
- Jalankan pengujian yang relevan sebelum menyatakan pekerjaan selesai; jangan menulis PASS tanpa eksekusi. Perbarui board dan log berdasarkan bukti, bukan karena file sudah dibuat.
- Jangan deploy, commit, atau push tanpa instruksi pengguna. Jangan masukkan `.venv`, cache, atau secrets ke Git.
- Jika sumber memakai premis AND/OR, kaji kesesuaiannya dengan model MVP sebelum memasukkan aturan. Mode terverifikasi tidak boleh diam-diam memuat data demo.
- Untuk eksplorasi struktural codebase, gunakan skill `codebase-memory` yang terpasang; jika indeks tidak mencakup workspace, periksa berkas secara langsung.
