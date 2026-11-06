# Struktur kode yang direncanakan

Struktur di bawah kini diimplementasikan untuk Sprint 1 dan Sprint 2, termasuk API/UI, berkas uji API, dan data demo sintetis. Berkas `data/verified/knowledge_verified.json` tetap belum tersedia. Tidak perlu file kode kosong.

```text
app/
  __init__.py
  main.py                 # Buat aplikasi FastAPI, pasang route dan static files
  config.py               # Pilih mode/path dataset secara eksplisit
  api/
    __init__.py
    routes.py             # Endpoint, status HTTP, translasi error
  schemas/
    __init__.py
    knowledge.py          # Model dan validasi pengetahuan
    consultation.py       # Model request/response konsultasi
  services/
    __init__.py
    knowledge_loader.py   # Baca JSON dan validasi referensi/integritas
    cf_engine.py          # Hitung CF positif dan trace, tanpa I/O/server
    consultation_service.py # Orkestrasi seleksi aturan, ranking, metadata
  static/
    index.html            # Beranda, form, hasil
    css/styles.css        # Tampilan dan status demo
    js/api.js             # Panggilan HTTP serta error terkontrol
    js/consultation.js    # Gejala dan input keyakinan
    js/result.js          # Ranking, seri, trace, mode, sumber
tests/
  conftest.py             # Fixture bersama
  fixtures/knowledge_sample.json # Data sintetis berlabel untuk uji
  test_knowledge_loader.py
  test_cf_engine.py
  test_api.py
```

`routes.py` bergantung pada `consultation_service.py` dan skema; layanan bergantung pada loader serta `cf_engine.py`; loader bergantung pada skema pengetahuan. `cf_engine.py` menerima data numerik yang sudah divalidasi dan mengembalikan hasil numerik/trace. UI hanya bergantung pada kontrak HTTP. Mesin wajib bisa diuji dengan pytest tanpa Uvicorn. Paket Python/FastAPI/Uvicorn/Pydantic/pytest/HTTPX/Ruff, lingkungan virtual lokal, dan versi terkunci ditetapkan pada implementasi setelah kompatibilitas diperiksa.
