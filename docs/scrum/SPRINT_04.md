# Sprint 4 — Persistensi dan deploy

Status: berjalan 2026-11-08. Ini pengembangan setelah MVP, bukan perubahan definisi B-12.

1. B-14: migrasi PostgreSQL, impor snapshot `verified` yang tidak dapat ditimpa, versi pin, uji kesetaraan API/CF, serta catatan konsultasi tanpa identitas.
2. B-15: CI Ruff, Python, PostgreSQL terisolasi, browser; deploy Render native Python dengan Neon setelah migrasi dan impor terkontrol.
3. B-16: tetapkan masa simpan dan pembersihan rutin catatan konsultasi sebelum layanan umum.

Review: bandingkan hasil JSON dengan database; catat keluaran CI serta health check Render. B-12 tetap menunggu kasus berlabel pakar, bukan data konsultasi anonim.
