# Sistem Pakar Identifikasi Hama pada Tanaman Tomat Menggunakan Certainty Factor Berbasis Web

Proyek tugas kuliah untuk mengidentifikasi **dugaan hama** tanaman tomat dari gejala yang dimasukkan manual. MVP yang direncanakan memakai Certainty Factor (CF) dukungan positif, menampilkan peringkat dugaan dan jejak hitung. Nilai CF bukan identifikasi pasti, probabilitas terkalibrasi, atau ukuran akurasi.

**Status:** inti Sprint 1 dan alur web Sprint 2 sudah dibuat dengan data demo sintetis. Uji unit/API dan alur DOM telah dijalankan; browser sungguhan serta Ruff belum dapat dijalankan dalam sandbox ini. Pengetahuan hama nyata belum diverifikasi. Artikel awal mencakup hama serta penyakit; proyek membatasi kelas keluaran pada hama. Jumlah awal 3–5 hama dan 10–20 gejala adalah perkiraan, bukan target data yang sudah terpenuhi.

## Peta dokumen

- Produk: [scope](docs/product/SCOPE.md), [requirements](docs/product/REQUIREMENTS.md).
- Rancangan: [overview](docs/architecture/OVERVIEW.md), [struktur proyek](docs/architecture/PROJECT_STRUCTURE.md), [kontrak API](docs/architecture/API_CONTRACT.md), [metode CF](docs/method/CERTAINTY_FACTOR.md).
- Pengetahuan: [spesifikasi](docs/knowledge/KNOWLEDGE_SPEC.md), [register sumber](docs/knowledge/SOURCE_REGISTER.md), [daftar verifikasi](docs/knowledge/VERIFICATION_CHECKLIST.md), [status data](data/README.md).
- Mutu: [rencana uji](docs/testing/TEST_PLAN.md), [kriteria penerimaan](docs/testing/ACCEPTANCE_CRITERIA.md).
- Kerja: [backlog](docs/scrum/PRODUCT_BACKLOG.md), [board](docs/scrum/BOARD.md), [Sprint 1](docs/scrum/SPRINT_01.md), [Sprint 2](docs/scrum/SPRINT_02.md), [Sprint 3](docs/scrum/SPRINT_03.md), [log kerja](docs/scrum/WORK_LOG.md), [keputusan](docs/decisions/DECISION_LOG.md), [handoff implementasi](docs/handoff/IMPLEMENTATION_HANDOFF.md).

## Urutan pengerjaan

1. Telaah scope, keputusan, backlog, dan sprint aktif; tentukan mode demo atau terverifikasi.
2. Sprint 1: skema pengetahuan, loader, mesin CF murni, dan pengujian unit dengan fixture sintetis. Kode inti sudah ada; lihat [board](docs/scrum/BOARD.md) untuk bukti dan status terkini.
3. Sprint 2: API, antarmuka, dan alur konsultasi lengkap. Implementasi tersedia; lihat [board](docs/scrum/BOARD.md) untuk status verifikasi.
4. Verifikasi sumber dan pengetahuan hama; lanjutkan Sprint 3 untuk integrasi data nyata dan evaluasi kasus berlabel pakar. Bagian ini tetap terblokir sampai bukti tersedia.

Instruksi sesi implementasi ada di [AGENTS.md](AGENTS.md). Tidak ada data hama nyata yang disediakan pada tahap ini.

## Menjalankan prototipe dan uji pada lingkungan dengan akses dependency

Gunakan Python 3.12, buat `.venv`, instal dependensi terpin dari `requirements-dev.txt`, lalu jalankan `uvicorn app.main:app` dan buka `http://127.0.0.1:8000/`. Mode default `demo` membaca `data/demo/knowledge_demo.json`. Set `KNOWLEDGE_MODE=verified` hanya setelah dataset terverifikasi tersedia; mode ini gagal jelas bila berkas tidak ada. Jalankan `python -m pytest tests` dan `ruff check app tests`. Versi runtime terpasang dicatat dalam `requirements-lock.txt`. Di sandbox saat ini, pytest/HTTPX dijalankan dari instalasi lokal lain; server tidak dapat bind ke localhost dan browser tidak dapat diluncurkan. Lihat [log kerja](docs/scrum/WORK_LOG.md).

Untuk pemeriksaan browser di lingkungan yang mengizinkan localhost, instal dependency pengujian Node dari `package.json`, sediakan browser Chromium Playwright, jalankan server di atas, lalu jalankan `npm run test:browser`. Skrip di `tests/browser_flow.cjs` memeriksa alur konsultasi nyata, lebar 375/768/1280 piksel, dan navigasi keyboard; skenario seri/error pada UI memakai respons sintetis yang disisipkan oleh tes. Hasil screenshot disimpan di `/tmp` untuk tinjauan visual. Skrip tersebut belum berhasil dieksekusi dalam sandbox ini.
