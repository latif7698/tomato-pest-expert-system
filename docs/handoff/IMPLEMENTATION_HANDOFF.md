# Handoff langsung untuk Sprint 1

**Catatan sejarah Sprint 1:** isi handoff di bawah menggambarkan keadaan awal implementasi. Status terkini: mode verified L04 aktif menurut D-17 setelah pemeriksaan manusia 2026-11-08; lihat [board](../scrum/BOARD.md), [audit](../knowledge/L04_HUMAN_AUDIT_RESOLUTION_2026-11-08.md), dan [WORK_LOG](../scrum/WORK_LOG.md). B-05 masih Review karena enam temuan Ruff lama, bukan karena Ruff belum tersedia. Untuk melanjutkan, baca [AGENTS.md](../../AGENTS.md), [scope](../product/SCOPE.md), [keputusan](../decisions/DECISION_LOG.md), [Sprint 3](../scrum/SPRINT_03.md), [spesifikasi pengetahuan](../knowledge/KNOWLEDGE_SPEC.md), dan [metode CF](../method/CERTAINTY_FACTOR.md).

## Urutan kerja

1. Periksa versi Python yang tersedia dan kompatibilitas paket. Buat `.venv` lokal; tentukan lalu kunci versi dependency runtime (FastAPI, Uvicorn, Pydantic) dan pengembangan (pytest, HTTPX, Ruff). Jangan menebak versi terbaru. Tidak perlu NumPy, pandas, scikit-learn, atau GPU.
2. Buat hanya modul Sprint 1 dari [struktur rencana](../architecture/PROJECT_STRUCTURE.md): `app/__init__.py`, `app/schemas/__init__.py`, `app/schemas/knowledge.py`, `app/services/__init__.py`, `app/services/knowledge_loader.py`, `app/services/cf_engine.py`, `tests/conftest.py`, `tests/fixtures/knowledge_sample.json`, `tests/test_knowledge_loader.py`, dan `tests/test_cf_engine.py`. Berkas konfigurasi dependency dibuat sesuai pilihan yang diverifikasi. Jangan buat API/UI atau modul kosong lain sekadar melengkapi pohon.
3. Gunakan fixture **sintetis** yang jelas berlabel `mode=demo`; pisahkan dari `data/verified/`. Loader menolak ID/referensi rusak, duplikat aturan, bobot non-finite/di luar rentang, status validasi tidak cocok, dan fallback demo pada mode verified.
4. Buat `cf_engine` murni yang menerima data tervalidasi, menghitung dukungan positif, ranking/seri, dan trace tanpa server atau I/O. Batasi pembulatan pada tampilan. Konsisten dengan [kontrak API](../architecture/API_CONTRACT.md) untuk nama field hasil.
5. Jalankan pytest relevan dan Ruff; catat perintah serta hasil aktual di [WORK_LOG.md](../scrum/WORK_LOG.md). Perbarui [backlog](../scrum/PRODUCT_BACKLOG.md) dan [board](../scrum/BOARD.md) hanya menurut bukti.

## Uji wajib dan selesai

Uji minimal: satu gejala, dua dukungan menghasilkan 0.86, bobot nol, input kosong, hasil seri, duplikat/ID asing, bobot non-finite dan di luar rentang, referensi rusak, permutasi bukti dalam toleransi `1e-12`, trace yang merekonstruksi hasil, serta mode/versi dataset. B-03–B-05 `Done` hanya bila pengujian relevan benar-benar dijalankan dan lulus, linting relevan selesai, dan batas demo jelas. Kegagalan atau bagian belum diuji dicatat apa adanya.

## Batas Sprint 1

Tidak mengerjakan endpoint, UI, pengetahuan hama nyata, penanganan, atau evaluasi domain. Jangan mengubah aturan premis AND/OR dari sumber tanpa kajian. Jangan deploy, commit, atau push tanpa instruksi pengguna. B-11/B-12 tetap `Blocked` sampai sumber dan label pakar tersedia.
