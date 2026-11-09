# Persistensi PostgreSQL dan deploy Render

## Kontrak data

- JSON L04 yang diperiksa manusia tetap jejak sumber dalam Git. Impor eksplisit hanya menerima mode `verified` dan membuat snapshot tak dapat ditimpa berdasarkan `knowledge_version` dan SHA-256 kanonis; perubahan konten harus memakai versi baru dan audit baru.
- Tabel `knowledge_snapshots`, `knowledge_sources`, `knowledge_pests`, `knowledge_symptoms`, `knowledge_rules` menyimpan isi snapshot dan urutan asli. Pembacaan memvalidasi skema Pydantic dan hash. P11 serta enam relasi negatif tetap di data review, tidak diimpor.
- `consultations` dapat menyimpan UUID internal, waktu, versi snapshot, observasi dan hasil CF (JSONB), tanpa akun, IP, atau nama. Tidak ada API untuk melihat seluruh konsultasi. Penyimpanan konsultasi **mati secara default**, termasuk pada Render; aktif hanya bila `PERSIST_CONSULTATIONS=true` dengan backend PostgreSQL. Data ini **bukan** pengganti kasus evaluasi berlabel pakar. Sampai B-16 selesai, jangan aktifkan opsi tersebut untuk layanan umum tanpa kebijakan retensi/penghapusan.
- Mode demo tetap memakai JSON sintetis. Mode JSON verified juga tetap dapat dipakai untuk pengembangan lokal dan tes browser. Backend PostgreSQL gagal saat versi hilang/berubah atau DB gagal, tanpa fallback.

## Menyiapkan database

Gunakan database pengembangan/tes yang terpisah dari produksi. Dapatkan URL koneksi langsung dan pooled dari Neon; tambahkan driver `postgresql+psycopg://` (alih-alih `postgresql://`) tanpa mengubah host, pengguna, password, nama DB, dan parameter TLS yang diberikan. Jangan menaruh URL itu dalam repository atau log.

```bash
export DATABASE_DIRECT_URL='postgresql+psycopg://USER:PASSWORD@DIRECT_HOST/DB?sslmode=require'
alembic upgrade head
python -m app.db.seed
export DATABASE_URL='postgresql+psycopg://USER:PASSWORD@POOL_HOST/DB?sslmode=require'
export KNOWLEDGE_MODE=verified KNOWLEDGE_BACKEND=postgres
export KNOWLEDGE_VERSION=l04-2026-11-08-v1
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Pastikan URL langsung dan pooled menunjuk **database dan branch Neon yang sama**. Periksa `GET /healthz`, `GET /symptoms`, dan satu POST `/consultations`, lalu cocokkan peringkat/trace terhadap mode JSON. Perintah migrasi **tidak** dijalankan oleh proses web. `downgrade` sengaja tidak menghapus data; lakukan pemulihan dari backup terkontrol jika diperlukan.

## Render dan GitHub

1. Jalankan workflow `.github/workflows/ci.yml` pada PR: Ruff, tes Python dan migrasi/impor/tes di PostgreSQL terisolasi, plus browser verified memakai JSON. Tes browser database terhadap Neon belum otomatis.
2. Buat Neon production branch/database dan jalankan migrasi serta impor dengan URL langsung setelah review. Siapkan backup dan pastikan versi snapshot ada **sebelum** mengaktifkan service dengan backend postgres.
3. Buat layanan Render dari `render.yaml`. Atur `DATABASE_URL` secara rahasia di Render memakai URL pooled Neon. `KNOWLEDGE_VERSION`, mode, dan backend ada pada blueprint. Jangan atur `PERSIST_CONSULTATIONS=true` sampai B-16 selesai. Periksa aturan deploy `checksPass` dan hasil CI sebelum membiarkan `main` deploy otomatis.
4. URL langsung untuk migrasi tidak perlu disimpan pada web service Render. Bila nanti memakai pre-deploy command (tersedia pada paket Render tertentu), kaji urutan dan akses secret khusus migrasi. Untuk layanan tanpa fitur itu, migrasi produksi merupakan langkah operator terpisah dan harus dilakukan sebelum rilis yang membutuhkannya.
5. Pastikan `/healthz` merespons 200 dan uji konsultasi UI mode verified pada URL Render. Periksa log tanpa mencetak URL database. Belum ada tindakan membuat Neon/Render atau deploy production dalam perubahan kode ini.

Render dan Neon dapat memerlukan biaya sesuai paket yang dipilih; periksa pengaturan dan kuota pada akun sebelum membuat sumber daya. Docker tidak diperlukan pada runtime Python native ini. Ketika kode hanya mengubah logika tanpa mengubah schema, deploy otomatis bisa langsung mengikuti CI. Ketika schema berubah, rencanakan migrasi yang kompatibel dengan versi aplikasi yang sedang hidup.

Blueprint memilih paket web `free` secara eksplisit supaya tidak memilih paket berbayar tanpa sengaja. Pada paket ini Render dapat menidurkan layanan setelah tidak aktif; kunjungan berikutnya bisa menunggu startup. Periksa kuota kedua penyedia sebelum mengaktifkan layanan.
