# L04: Selisih Metode Artikel vs Implementasi

> Analisis metode awal disusun sebelum pemeriksaan manusia. Sebelas relasi positif dan lima deskripsi diperiksa Asep Abdul Latip pada 2026-11-08; koreksi dan batasannya ada pada [catatan penyelesaian audit](L04_HUMAN_AUDIT_RESOLUTION_2026-11-08.md). Algoritma CF tetap memakai adaptasi positif D-11/D-12.

## 0. Dasar dan batas pemeriksaan

- Dibaca langsung dari salinan lokal repo: `AGENTS.md`, `docs/product/SCOPE.md`, `docs/decisions/DECISION_LOG.md`, `docs/scrum/BOARD.md`, `docs/scrum/SPRINT_03.md`, `KNOWLEDGE_SPEC.md`, `SOURCE_REGISTER.md`, `VERIFICATION_CHECKLIST.md`, `docs/method/CERTAINTY_FACTOR.md`, `app/schemas/knowledge.py`, `app/services/cf_engine.py`, `data/demo/knowledge_demo.json`, `data/verified/README.md`.
- Repo diakses dari berkas zip yang diunggah, bukan dari URL GitHub (sandbox tanpa jaringan). Isi zip tidak dibandingkan dengan GitHub.
- Uji repo **tidak dijalankan** (pydantic dan pytest tidak terpasang, sandbox offline). Angka contoh di bawah dihitung dengan mereplikasi rumus `cf_engine.py` yang dibaca, bukan dengan menjalankan mesin itu.

## 1. Metode L04 (ringkas, locator ada di audit)

| Aspek | L04 |
|---|---|
| CF per gejala | CF = MB − MD, dapat negatif (pers. 1, hal. 453; Tabel IV) |
| Penggabungan | contoh CF1 + CF2·(1−CF1) berurutan (hal. 456); pers. (2) tercetak tidak konsisten |
| Aturan | satu aturan per hama, `IF .. AND .. THEN` (Tabel VI, hal. 455), tetapi dihitung dengan kombinasi aditif |
| Input pengguna | checklist biner (Gambar 5); tanpa pengali keyakinan pengguna |
| Keluaran | persentase (0.904 → 90.4%) |

## 2. Kontrak repo saat ini (dari berkas)

| Aspek | Repo | Sumber |
|---|---|---|
| Model | dukungan CF positif; satu hubungan hama–gejala | `CERTAINTY_FACTOR.md`, D-02 |
| CF per aturan | CF_i = cf_expert × cf_user; gabung CF_prev + CF_i·(1−CF_prev) per hama | `CERTAINTY_FACTOR.md`, `cf_engine.py` |
| Skala `cf_user` | 0.25 / 0.50 / 0.75 / 1.00 (usulan desain, belum divalidasi) | D-05, `cf_engine.py` |
| `cf_expert` | harus finite dan dalam [0, 1]; di luar itu schema melempar error | `Rule.check_cf_expert` |
| Pasangan hama–gejala | sekali saja; duplikat ditolak | `KnowledgeBase.check_integrity` |
| Gejala tak dipilih | bukan bukti negatif; hanya gejala terpilih yang memberi dukungan; skor parsial diizinkan | `CERTAINTY_FACTOR.md`, `cf_engine.py` |
| Premis AND/OR | harus dikaji dulu, tidak boleh dipecah otomatis; mode verified tidak boleh memuat demo | `AGENTS.md`, `KNOWLEDGE_SPEC.md` |
| Hama | `description` wajib tidak kosong; `handling` hanya untuk mode verified | `Pest`, `check_integrity` |
| Sumber verified | harus `reviewed` dan memiliki URL; semua aturan `verified` | `check_integrity` |

## 3. Perbedaan yang berpengaruh pada hasil

**a. CF pakar negatif.** 6 dari 19 relasi hama bernilai MB−MD negatif (P9–G7 −0.2, P9–G12 −0.4, P10–G17 −0.4, P11–G29 −0.4, P13–G33 −0.2, P14–G35 −0.2). Pada repo, `cf_expert` negatif **ditolak schema**, sehingga pemuatan dataset gagal. Mengubahnya ke 0, mutlak, atau positif memalsukan sumber, jadi tidak dilakukan. Contoh: hanya G35 terpilih untuk P14 bernilai −0.2 di artikel (bukti yang melemahkan). Pada repo, relasi itu tidak bisa ada, sehingga hasilnya `no_support`.

**b. Penggabungan nilai campuran tidak didefinisikan artikel.** Contoh P9 dengan keempat gejala terpilih (MB−MD: G7 −0.2, G12 −0.4, G23 0.8, G24 0.8). Hitungan ilustrasi, bukan dari artikel:

| Cara hitung | Hasil |
|---|---|
| Rumus contoh artikel diterapkan harfiah pada semua nilai (komutatif, urutan tidak berpengaruh) | 0.9328 |
| Hanya yang positif (G23, G24), setara hasil mesin repo dengan `cf_user` = 1.0 | 0.96 |
| Gabungan campuran gaya MYCIN klasik [anotasi auditor, bukan dari artikel] | 0.9167 |

Artikel tidak menentukan mana yang benar. Angka di atas adalah skenario ilustratif; hasil aplikasi tidak dapat dibandingkan secara pasti dengan hasil artikel untuk bukti bertanda campuran.

**c. Premis AND.** R9–R14 berbentuk AND, tetapi contoh hitung artikel menjumlahkan bukti tiap gejala (kombinasi aditif), bukan min dan bukan syarat semua gejala. Bila AND ditafsirkan sebagai min, P9 dengan keempat gejala menjadi −0.4. Mesin repo juga tidak mensyaratkan semua gejala (skor parsial diizinkan). Pada data L04, penguraian per gejala dengan CF positif memberi aritmetika yang sama dengan contoh artikel untuk relasi positif. Ini tafsir auditor, bukan pernyataan artikel, dan menurut `AGENTS.md` perlu keputusan Anda sebelum aturan dimasukkan.

**d. Skala `cf_user`.** Repo mengalikan dengan 0.25–1.00; artikel tidak punya pengali. Hasil hanya sebanding dengan artikel pada `cf_user` = 1.0. Contoh P12 (G30, G31, G32 = 0.8, 0.4, 0.6): `cf_user` 1.0 untuk semua memberi 0.952; 0.5 untuk semua memberi 0.664. Peran Tabel III di artikel masih belum jelas.

**e. Gejala bersama dan seri.** G31 dipakai P12 dan P13 dengan nilai sama (0.4); bila hanya G31 terpilih, kedua hama seri dan mesin menandai `is_tied`. G25 dan G33 nyaris duplikat.

**f. Sumber deskripsi.** L04 tidak memuat deskripsi atau penanganan hama. Lima deskripsi diambil dari SRC-02, SRC-03, SRC-05, SRC-06, dan SRC-07, lalu diperiksa manusia pada 2026-11-08. Penanganan tetap kosong.

**g. Evaluasi.** 90% (18/20) gabungan hama+penyakit, tidak berlaku untuk aplikasi pada opsi mana pun.

## 4. Opsi keputusan

### Opsi A: replikasi L04 sedekat mungkin
- Kontrak: mengubah D-02 (dukungan positif) dengan alasan, bukti, dan dampak ke kontrak, backlog, serta pengujian (aturan `DECISION_LOG.md`); memperbarui `CERTAINTY_FACTOR.md` dan `API_CONTRACT.md`.
- Kode: `Rule.check_cf_expert` menjadi [−1, 1] (atau field `mb`/`md`); `cf_engine.py` menerima dukungan negatif dengan rumus gabung tertulis untuk tanda campuran; skema konsultasi/UI menyesuaikan skala (checklist biner atau pemetaan Tabel III).
- Pengujian: `tests/test_cf_engine.py`, `tests/test_knowledge_loader.py`, fixture dan `tests/browser_flow.cjs` perlu diperluas (contoh R1 0.84/0.904 sebagai uji fungsi gabung, kasus negatif, batas −1/+1, skor parsial).
- Ilmiah: mempertahankan 19 relasi; tetap ada asumsi pada tanda campuran dan AND yang artikel tidak definisikan, jadi "replikasi" tidak penuh. Klaim akurasi L04 tetap tidak berlaku.
- Teknis: cakupan perubahan besar dan menyentuh kontrak yang sudah Done (B-01, B-03 sampai B-09).

### Opsi B: adaptasi MVP dengan dukungan positif
- Tidak dapat dipakai langsung: 6 relasi negatif di atas (32% dari 19). Tidak diubah menjadi 0/mutlak/positif; dicatat sebagai "tidak dimodelkan" di audit dan JSON review, bukan dihapus diam-diam.
- Dapat dipakai (13 relasi, `cf_expert` = MB−MD dari Tabel IV, pers. 1): P9 (G23, G24), P10 (G25, G26), P11 (G27, G28), P12 (G30, G31, G32), P13 (G31, G34), P14 (G36, G37).
- Tidak ada perubahan mesin, schema, atau UI. Perlu keputusan tertulis baru di `DECISION_LOG.md` tentang penguraian aturan AND menjadi relasi per gejala (lihat 3c).
- Dampak: enam bukti negatif tidak dihitung. Skor adaptasi dapat berbeda dari artikel, tetapi arah selisihnya tidak dapat dipastikan karena artikel tidak mendefinisikan penggabungan bukti negatif/campuran. P9 hanya punya dua gejala pendukung; `cf_user` di bawah 1.0 juga mengubah hasil dari contoh artikel.
- Pernyataan keterbatasan wajib: bukan replikasi L04; 6 relasi negatif tidak dimodelkan; AND diuraikan per gejala atas keputusan proyek; skala `cf_user` belum divalidasi; akurasi L04 tidak boleh dikutip sebagai akurasi aplikasi.
- Mode `verified` menurut D-17 dapat diaktifkan setelah pemeriksaan sumber manusia dan pencatatan bukti; ini tidak membuktikan validasi pakar atau akurasi lapangan.

### Rekomendasi: Opsi B
Ini **mengubah** rekomendasi saya sebelumnya (Opsi A) setelah membaca repo. Alasannya: (1) pada artikel, replikasi "sedekat mungkin" tidak terdefinisi untuk 6 relasi negatif karena penggabungan tanda campuran tidak ada, sehingga Opsi A tetap bergantung pada asumsi saya sendiri; (2) Opsi A mengubah kontrak D-02 dan menyentuh schema, mesin, API, UI, dan tes yang sudah Done; (3) Opsi B sesuai kontrak MVP dan, untuk relasi positif dengan `cf_user` = 1.0, memberi aritmetika yang sama dengan contoh artikel. Syaratnya: keterbatasan di atas dinyatakan, 6 relasi negatif tetap tercatat, dan klarifikasi ke penulis/pakar (pers. 2, penggabungan negatif, AND, Tabel III) dijalankan agar Opsi A bisa dinilai ulang. Opsi B dipilih pengguna pada 2026-11-07 (lihat bagian 5).

## 5. Keputusan (status 2026-11-07)

| No | Keputusan | Status |
|---|---|---|
| 1 | Opsi A atau B | Opsi B dipilih (D-11) |
| 2 | Aturan AND R9–R14 diuraikan per gejala | Disetujui (D-12) |
| 3 | P9 Nematoda Akar | Tetap masuk scope (D-13) |
| 4 | Sumber deskripsi/penanganan hama | Sumber tambahan akan dicari; belum ada sumber ditetapkan (D-15) |
| 5 | Redaksi G25/G27 | Memakai teks Tabel II (D-14) |
| 6 | Klarifikasi ke penulis/pakar | Ditunda, tidak dilakukan; menjadi batasan sistem (D-16) |
| 7 | Status verified | V1: bukti sumber diperiksa dan dicatat, bukan konfirmasi pakar (D-17) |
| 8 | Pemeriksa | Manusia; LLM tidak dipakai (D-18); pengguna sendiri (D-21) |
| 9 | P11 Kepik Tomat | Ditahan di review (D-19) |
| 10 | P12 Lalat Buah | Tetap masuk dengan catatan di deskripsi (D-20) |

## 6. Pernyataan keterbatasan (draf teks untuk dokumentasi/UI nanti)

1. Pengetahuan adalah adaptasi dari L04 (Adellia dkk., 2022), bukan replikasi metode artikel.
2. Enam dari 19 relasi hama (CF pakar negatif) tidak dimodelkan. Skor adaptasi dapat berbeda dari artikel, tetapi arah perbedaannya tidak dapat dipastikan tanpa aturan penggabungan nilai negatif/campuran dari artikel. P9 hanya memakai 2 dari 4 relasinya.
3. Aturan AND diuraikan per gejala atas keputusan proyek; skor parsial diizinkan.
4. Persamaan (2), penggabungan CF negatif, arti AND, peran Tabel III, dan asal MB/MD belum dikonfirmasi ke penulis/pakar.
5. Skala `cf_user` 0.25–1.00 adalah keputusan desain proyek, bukan dari L04.
6. Label gejala memakai Tabel II; redaksi G25 dan G27 berbeda dengan aturan R10 dan R11.
7. Nilai CF bukan akurasi atau probabilitas; akurasi 90% L04 gabungan hama+penyakit dan tidak berlaku untuk aplikasi.
8. Lima deskripsi telah diperiksa manusia pada 2026-11-08; penanganan hama tidak tersedia. Status `verified` berarti pemeriksaan sumber sesuai D-17, bukan validasi pakar.

## 7. Bukti status verified (V1, D-17)

1. Tabel IV dicocokkan manusia dengan PDF untuk 11 relasi yang dimodelkan; enam negatif dan dua relasi P11 tetap di review.
2. Scope P11 dan P12 diputuskan melalui D-19/D-20.
3. SRC-02, SRC-03, SRC-05, SRC-06, SRC-07 ditinjau Asep Abdul Latip pada 2026-11-08; SRC-04 tetap tidak dipakai.
4. Dataset aplikasi dibentuk dari kandidat yang dikoreksi dan diuji melalui loader serta alur konsultasi verified. Hasil uji dicatat di WORK_LOG.
5. Pemeriksa, tanggal, locator, keputusan, dan batasan D-16 dicatat di audit manusia serta catatan penyelesaian. Pemeriksaan ini bukan validasi pakar.

## 8. Dampak keputusan P11 dan P12 pada dataset MVP

Dataset MVP setelah pemeriksaan sumber: 5 hama (P9, P10, P12, P13, P14), 11 relasi, 10 gejala. Relasi: P9 (G23, G24), P10 (G25, G26), P12 (G30, G31, G32), P13 (G31, G34), P14 (G36, G37). Tidak dimodelkan: 6 relasi negatif (D-11) dan 2 relasi P11 yang ditahan (G27, G28). G31 dipakai bersama oleh P12 dan P13 dengan nilai sama, sehingga hasil seri bila hanya G31 terpilih. Angka ini dihitung dari `data/review/l04_extraction.json`.
