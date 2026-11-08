# Checklist verifikasi pengetahuan

Isi per entri, sertakan bukti dan pemeriksa. Centang hanya butir yang didukung pemeriksaan manusia atau uji aktual; batasan yang belum terpenuhi tetap dicatat.

- [x] PDF sumber diperoleh, dibaca, dan versi/tautan dicatat.
- [x] Kelas hama dipisahkan dari penyakit/kekurangan nutrisi; setiap nama dan deskripsi punya locator sumber.
- [x] Setiap gejala memiliki definisi/label dan locator sumber yang jelas.
- [x] Setiap aturan hama–gejala memiliki asal `cf_expert` dan locator tepat; skala serta batas maknanya dicatat.
- [x] Premis AND/OR pada sumber diperiksa dan tidak diubah menjadi aturan tunggal tanpa kajian.
- [ ] Penanganan, jika ditampilkan, diperiksa per hama dan sumbernya dicatat.
- [x] ID/referensi/bobot/duplikat divalidasi oleh loader; mode verified menolak data demo.
- [x] Pemeriksa, tanggal, keputusan, dan bukti dicatat untuk tiap perubahan status ke `verified`.
- [ ] Kasus evaluasi memiliki label pakar dan terpisah dari penetapan/penyetelan bobot.

Format catatan entri: `ID entri | jenis | sumber | locator | kutipan/parafrasa singkat | keputusan | pemeriksa | tanggal`. Jangan masukkan data nyata hanya berdasarkan asumsi atau contoh sintetis.

## Catatan status per butir (2026-11-08)

Dasar: [audit manusia asli](L04_HUMAN_AUDIT_ORIGINAL_2026-11-08.md), [penyelesaian audit](L04_HUMAN_AUDIT_RESOLUTION_2026-11-08.md), [selisih metode](L04_METHOD_GAP.md), dan [DECISION_LOG](../decisions/DECISION_LOG.md) D-11 sampai D-22. Cakupan checked adalah lima hama, 10 gejala, dan 11 relasi positif pada `data/verified/knowledge_verified.json`.

1. URL PDF resmi SRC-01 dan snapshot kandidat sebelum koreksi dicatat di penyelesaian audit.
2. Lima hama ditinjau dengan SRC-02, SRC-03, SRC-05, SRC-06, SRC-07; P11/SRC-04 tetap ditahan. Flag kesetaraan nama dan keraguan inang P12 tetap berlaku.
3. Label 10 gejala dari Tabel II diperiksa manusia; locator halaman cetak 454 dicatat di audit.
4. MB, MD, dan CF untuk 11 aturan cocok dengan Tabel IV menurut audit manusia. Asal penetapan MB/MD dan peran Tabel III belum diklarifikasi; status `verified` di sini berarti pemeriksaan sumber menurut D-17.
5. Premis AND dikaji dan diuraikan per gejala sesuai D-12; ini adaptasi metode, bukan replikasi persis L04.
6. `handling` kosong pada kelima hama; butir penanganan tidak berlaku untuk snapshot ini.
7. Loader mode verified dan pemisahan dari demo diuji dalam `tests/test_knowledge_verified.py`; hasil aktual ada di [WORK_LOG](../scrum/WORK_LOG.md).
8. Pemeriksa Asep Abdul Latip dan tanggal 2026-11-08 tercatat pada audit manusia serta catatan penyelesaiannya. Schema aplikasi tidak menyimpan identitas pemeriksa pada tiap entri.
9. Kasus berlabel pakar dan evaluasi lapangan belum ada; butir ini tetap terbuka untuk B-12, bukan syarat D-17.
