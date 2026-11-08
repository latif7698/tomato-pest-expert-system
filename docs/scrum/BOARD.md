# Board kerja

Status resmi: `Backlog`, `Ready`, `In Progress`, `Review`, `Done`, `Blocked`. Detail dan kriteria tiap item ada di [product backlog](PRODUCT_BACKLOG.md); board ini adalah ringkasan dan harus diperbarui bersamaan dengannya.

| Status | Item | Alasan/bukti saat ini |
| --- | --- | --- |
| Backlog | — | Tidak ada. |
| Ready | B-16 | Tetapkan kebijakan retensi sebelum layanan umum. |
| In Progress | B-13, B-15 | CI dan Render disiapkan; eksekusi GitHub Actions serta koneksi Neon/Render belum tersedia. B-13 menunggu B-12. |
| Review | — | Tidak ada. |
| Done | B-01, B-02, B-03, B-04, B-05, B-06, B-07, B-08, B-09, B-10, B-11, B-14 | CI PR #3: migrasi/impor pada PostgreSQL 17 terisolasi, 82 tes Python, Ruff, dan browser verified lulus; bukti ada di WORK_LOG. B-11 memakai definisi D-17, tanpa klaim validasi pakar. |
| Blocked | B-12 | Protokol dan template kasus sudah disiapkan; kasus hama berlabel pakar untuk evaluasi independen belum tersedia. |

Saat memperbarui status, catat perintah uji, hasil, dan bukti pada [WORK_LOG.md](WORK_LOG.md). `Blocked` berarti dependensi nyata belum tersedia; software sintetis tetap bisa dikerjakan.

Rencana pengembangan pasca-MVP: [Sprint 4](SPRINT_04.md).
