# Sistem Pakar Identifikasi Hama pada Tanaman Tomat Menggunakan Certainty Factor Berbasis Web

Proyek tugas kuliah untuk mengidentifikasi **dugaan hama** tanaman tomat dari gejala yang dimasukkan manual. MVP yang direncanakan memakai Certainty Factor (CF) dukungan positif, menampilkan peringkat dugaan dan jejak hitung. Nilai CF bukan identifikasi pasti, probabilitas terkalibrasi, atau ukuran akurasi.

**Status:** aplikasi menyediakan mode demo sintetis dan mode verified dengan lima hama, 10 gejala, dan 11 relasi positif dari L04. `verified` berarti sumber diperiksa manusia pada 2026-11-08 menurut D-17, bukan validasi pakar. Ini adaptasi CF positif: aturan AND diuraikan per gejala dan enam relasi negatif tidak dihitung. Skala keyakinan pengguna belum divalidasi; belum ada bukti akurasi khusus hama atau kelayakan lapangan.

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
4. Pemeriksaan sumber manusia dan integrasi data nyata Sprint 3 telah dilakukan; lihat [audit](docs/knowledge/L04_HUMAN_AUDIT_RESOLUTION_2026-11-08.md). Evaluasi kasus berlabel pakar masih tertunda.

Instruksi sesi implementasi ada di [AGENTS.md](AGENTS.md).

## Menjalankan prototipe dan uji pada lingkungan dengan akses dependency

Gunakan Python 3.12, buat `.venv`, instal dependensi terpin dari `requirements-dev.txt`, lalu jalankan `KNOWLEDGE_MODE=verified uvicorn app.main:app` dan buka `http://127.0.0.1:8000/`. Mode verified membaca `data/verified/knowledge_verified.json`; mode default `demo` membaca `data/demo/knowledge_demo.json`. Loader menolak mode yang tidak cocok dan tidak beralih otomatis ke demo. Jalankan `python -m pytest tests` dan `ruff check app tests`. Versi runtime terpasang dicatat dalam `requirements-lock.txt`. Hasil pemeriksaan aktual ada di [log kerja](docs/scrum/WORK_LOG.md).

Untuk pemeriksaan browser di lingkungan yang mengizinkan localhost, instal dependency pengujian Node dari `package.json` dan sediakan Chromium Playwright. Jalankan server verified di atas lalu `npm run test:browser:verified`; skrip ini memeriksa label mode, batas metode, konsultasi, sumber, jejak, kondisi tanpa dukungan, dan lebar layar. Untuk mode demo, jalankan server tanpa `KNOWLEDGE_MODE` lalu `npm run test:browser`. Hasil aktual dan batas lingkungan dicatat di [log kerja](docs/scrum/WORK_LOG.md).
