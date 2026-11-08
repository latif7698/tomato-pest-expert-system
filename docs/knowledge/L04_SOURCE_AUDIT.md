# Audit Sumber L04

> Transkripsi awal dibuat 2026-11-07. Sebelas relasi yang dimodelkan dan label Tabel II diperiksa Asep Abdul Latip pada 2026-11-08; delapan relasi lain tetap tercatat hanya di review. Lihat [audit manusia](L04_HUMAN_AUDIT_ORIGINAL_2026-11-08.md) dan [penyelesaiannya](L04_HUMAN_AUDIT_RESOLUTION_2026-11-08.md). Ini pemeriksaan sumber menurut D-17, bukan validasi pakar.
> Dasar: teks dan halaman PDF L04 (8 halaman, sumber SRC-01 pada [register sumber](SOURCE_REGISTER.md)). Perbandingan dengan implementasi repo ada di [L04_METHOD_GAP.md](L04_METHOD_GAP.md).
> Draf JSON: [../../data/review/l04_extraction.json](../../data/review/l04_extraction.json)

Legenda: **[Cetak]** = kutipan/transkripsi sumber; **[Hitung]** = hasil perhitungan; **[Interpretasi]** = pendapat auditor.

## 1. Identitas sumber

| Item | Nilai | Jenis |
|---|---|---|
| Judul | Penerapan Metode *Certainty Factor* pada Sistem Pakar Diagnosa Hama dan Penyakit pada Tanaman Tomat | Cetak |
| Penulis | Dila Adellia, Alda Cendekia Siregar, Syarifah Putri Alkadri (Teknik Informatika, Universitas Muhammadiyah Pontianak) | Cetak |
| Jurnal | JEPIN (Jurnal Edukasi dan Penelitian Informatika), Vol. 8, No. 3, Desember 2022; ISSN(e) 2548-9364 / ISSN(p) 2460-0741 | Cetak |
| Tanggal | Submitted 13-07-2022; Revised 29-08-2022; Accepted 10-12-2022 | Cetak (hal. 451) |
| DOI | 10.26418/jp.v8i3.56178, dicatat pada `SOURCE_REGISTER.md` SRC-01 dari halaman jurnal (diakses 2026-11-05). **Tidak tercetak pada PDF** dan tidak dapat diverifikasi dari PDF. | Dari register repo |
| URL halaman artikel | https://jurnal.untan.ac.id/index.php/jepin/article/view/56178 | Dari pengguna |
| URL PDF | https://jurnal.untan.ac.id/index.php/jepin/article/viewFile/56178/75676595632 | Dicatat dari pemeriksaan manusia 2026-11-08 |
| Halaman | Cetak 451–458 = PDF hal. 1–8; PDF hal. = cetak − 450 | Interpretasi (urutan halaman) |
| Pakar | Dr.Ir. Fadjar Rianto, MS (satu pakar; hal. 453 dan ucapan terima kasih hal. 457) | Cetak |

## 2. Cakupan: hama saja

- Tabel I (hal. 453) memuat 14 entitas (P1–P14) dan tidak memisahkan hama dari penyakit. Jumlah sesuai klaim hal. 452 (14 data hama dan penyakit, 37 gejala).
- **Klasifikasi hama diambil dari label pada Tabel VI**: R1–R8 berlabel "Penyakit", R9–R14 berlabel "Hama". Jadi hama = **P9–P14 (6 entitas)**. Ini [Interpretasi] berbasis label aturan; Tabel I sendiri tidak melabeli.
- P9 Nematoda Akar berlabel "Hama" oleh artikel walau nematoda bukan serangga; diputuskan pengguna tetap masuk scope (D-13).
- P1–P8 (penyakit) tidak ditranskripsi.

## 3. Tabel hama (6)

| Kode | Nama persis (Tabel I, cetak 453) | Label di Tabel VI | Aturan | Usulan nama umum UI | Usulan nama ilmiah (INTERPRETASI) |
|---|---|---|---|---|---|
| P9 | Nematoda Akar (Heterodera marioni/ Meloidogyne javanice) | Hama | R9 | Nematoda Akar | Meloidogyne javanica (tercetak 'javanice'); 'Heterodera marioni' nama lama |
| P10 | Penggerek Daun (Liriomyza sative Blancard (Diptera : Asgromyzidae)) | Hama | R10 | Penggerek Daun | Liriomyza sativae Blanchard (Diptera: Agromyzidae) |
| P11 | Kepik Tomat (Nesidiocoris (Crytopeltis) tenuis (Hemiptera : Miridae)) | Hama | R11 | Kepik Tomat | Nesidiocoris tenuis (sinonim Cyrtopeltis tenuis) (Hemiptera: Miridae) |
| P12 | Lalat Buah (Bactocera cucurbitae (Coquillet) (Diptera : Tephritidae)) | Hama | R12 | Lalat Buah | Bactrocera cucurbitae (Coquillett) (Diptera: Tephritidae) |
| P13 | Ulat Grayak (Spodoptera liture F.) | Hama | R13 | Ulat Grayak | Spodoptera litura (F.) |
| P14 | Ulat Tanah (Agrotis ipsilon) | Hama | R14 | Ulat Tanah | Agrotis ipsilon (tidak perlu diubah) |

- Deskripsi/penanganan: **tidak ada** untuk P9–P14 (lihat bagian 8).
- Kolom nama ilmiah usulan adalah koreksi ejaan taksonomi oleh auditor dan **belum diverifikasi** terhadap rujukan taksonomi. Nama tercetak harus disimpan apa adanya (typo seperti "Asgromyzidae", "Crytopeltis", "Bactocera", "liture", "Coquillet").
- Status semua entri: draf belum diverifikasi.

## 4. Tabel gejala yang berkaitan dengan hama (18 dari 37)

Himpunan gejala = gejala pada relasi P9–P14 di Tabel IV (cocok dengan antecedent R9–R14): G7, G12, G17, G23–G37. Tidak semua gejala artikel berkaitan dengan semua hama; peta gejala→hama ada di kolom "Hama".

| Kode | Teks Tabel II persis (cetak 454) | Teks pada Tabel VI (cetak 455) | Hama | Pakai juga di penyakit | Catatan redaksi | Usulan teks UI |
|---|---|---|---|---|---|---|
| G7 | Tanaman roboh | tanaman roboh | P9 | P3 | identik | Tanaman roboh |
| G12 | Tanaman layu | tanaman layu | P9 | P5, P7 | identik (Tabel II ada spasi akhir) | Tanaman layu |
| G17 | Daun mengering | daun mengering | P10 | P6 | identik | Daun mengering |
| G23 | Tanaman kerdil | tanaman kerdil | P9 | P8 | identik | Tanaman kerdil |
| G24 | Akar serabut tidak normal dan terdapat bulatan kecil seperti bisul berwarna putih | akar serabut tidak normal dan terdapat bulatan kecil seperti bisul berwarna putih | P9 | - | identik | Akar serabut tidak normal dan terdapat bulatan kecil seperti bisul berwarna putih |
| G25 | Daun tanaman terdapat bercak putih | daun tanaman lebih kecil dan terdapat bercak putih | P10 | - | BERBEDA: R10 menambah 'lebih kecil' yang tidak ada di G25 (dua gejala jadi satu?) | Daun tanaman terdapat bercak putih |
| G26 | Terdapat larva dibagian tepi daun | terdapat larva dibagian tepi daun | P10 | - | identik (ejaan 'dibagian' tercetak) | Terdapat larva di bagian tepi daun |
| G27 | Ujung ranting terdapat tusukan berwarna coklat | ujung ranting terdapat tusukan melingkar berwarna coklat | P11 | - | BERBEDA: R11 menambah 'melingkar' | Ujung ranting terdapat tusukan berwarna coklat |
| G28 | Pucuk tanaman kering | pucuk tanaman kering | P11 | - | identik | Pucuk tanaman kering |
| G29 | Bunga layu dan menghitam | bunga layu dan menghitam | P11 | - | identik | Bunga layu dan menghitam |
| G30 | Buah busuk dan terdapat larva | buah membusuk dan terdapat larva | P12 | - | beda kecil: 'busuk' vs 'membusuk' | Buah busuk dan terdapat larva |
| G31 | Buah berlubang | buah berlubang | P12, P13 | - | identik | Buah berlubang |
| G32 | Buah rontok | buah rontok | P12 | - | identik | Buah rontok |
| G33 | Terdapat bercak putih pada daun | terdapat bercak putih pada daun | P13 | - | identik; nyaris duplikat G25 | Terdapat bercak putih pada daun |
| G34 | Daun berlubang | daun berlubang | P13 | - | identik | Daun berlubang |
| G35 | Terdapat bekas gigitan dipermukaan daun | terdapat bekas gigitan dipermukaan daun | P14 | - | identik (ejaan 'dipermukaan') | Terdapat bekas gigitan di permukaan daun |
| G36 | Pangkal batang terdapat bekas gigitan | pangkal batang terdapat bekas gigitan | P14 | - | identik | Pangkal batang terdapat bekas gigitan |
| G37 | Terdapat ulat menggulung disekitar tanaman | terdapat ulat menggulung disekitar tanaman | P14 | - | identik (ejaan 'disekitar') | Terdapat ulat menggulung di sekitar tanaman |

Catatan:
- G7, G12, G17, G23 juga muncul pada penyakit (P3; P5, P7; P6; P8). Gejala ini tidak spesifik hama.
- G31 dipakai dua hama (P12 dan P13), dengan MB/MD identik (0.8/0.4).
- G25 dan G33 hampir duplikat ("bercak putih pada daun") dengan kode berbeda; R10 menambah "lebih kecil". [Interpretasi] kemungkinan G25 mencampur dua gejala; perlu klarifikasi sebelum teks UI ditetapkan.
- G27: "melingkar" hanya ada pada R11, tidak pada G27.

## 5. Matriks relasi hama–gejala–aturan (19 relasi)

Aturan: satu aturan per hama (R9→P9 … R14→P14), bentuk `IF (...) AND (...) AND (...) THEN (Hama ...)`. Teks aturan persis ada di JSON (`rules[].text_printed`). Kolom "(urutan)" = posisi antecedent pada teks aturan; urutan pada R9 (G23, G24, G12, G7) dan R10 (G25, G17, G26) **berbeda** dari urutan Tabel IV.

| ID | Hama | Gejala | Aturan (urutan) | MB | MD | MB−MD (hitung) | Hal. cetak/PDF | Locator | Catatan |
|---|---|---|---|---|---|---|---|---|---|
| L04-REL-01 | P9 | G7 | R9 (4) | 0.4 | 0.6 | **-0.2** | 454/4 | Tabel IV, kelompok P9, baris G7 | nilai MB-MD negatif; semantik penggabungan tidak didefinisikan artikel |
| L04-REL-02 | P9 | G12 | R9 (3) | 0.4 | 0.8 | **-0.4** | 454/4 | Tabel IV, kelompok P9, baris G12 | nilai MB-MD negatif; semantik penggabungan tidak didefinisikan artikel |
| L04-REL-03 | P9 | G23 | R9 (1) | 1 | 0.2 | **0.8** | 454/4 | Tabel IV, kelompok P9, baris G23 |  |
| L04-REL-04 | P9 | G24 | R9 (2) | 1 | 0.2 | **0.8** | 454/4 | Tabel IV, kelompok P9, baris G24 |  |
| L04-REL-05 | P10 | G17 | R10 (2) | 0.4 | 0.8 | **-0.4** | 454/4 | Tabel IV, kelompok P10, baris G17 | nilai MB-MD negatif; semantik penggabungan tidak didefinisikan artikel |
| L04-REL-06 | P10 | G25 | R10 (1) | 1 | 0.2 | **0.8** | 454/4 | Tabel IV, kelompok P10, baris G25 |  |
| L04-REL-07 | P10 | G26 | R10 (3) | 0.6 | 0.2 | **0.4** | 454/4 | Tabel IV, kelompok P10, baris G26 |  |
| L04-REL-08 | P11 | G27 | R11 (1) | 1 | 0.2 | **0.8** | 454/4 | Tabel IV, kelompok P11, baris G27 |  |
| L04-REL-09 | P11 | G28 | R11 (2) | 0.6 | 0.4 | **0.2** | 455/5 | Tabel IV, kelompok P11, baris G28 | data tabel terpecah antar halaman 454/455 |
| L04-REL-10 | P11 | G29 | R11 (3) | 0.4 | 0.8 | **-0.4** | 455/5 | Tabel IV, kelompok P11, baris G29 | nilai MB-MD negatif; semantik penggabungan tidak didefinisikan artikel; data tabel terpecah antar halaman 454/455 |
| L04-REL-11 | P12 | G30 | R12 (1) | 1 | 0.2 | **0.8** | 455/5 | Tabel IV, kelompok P12, baris G30 |  |
| L04-REL-12 | P12 | G31 | R12 (2) | 0.8 | 0.4 | **0.4** | 455/5 | Tabel IV, kelompok P12, baris G31 |  |
| L04-REL-13 | P12 | G32 | R12 (3) | 0.8 | 0.2 | **0.6** | 455/5 | Tabel IV, kelompok P12, baris G32 |  |
| L04-REL-14 | P13 | G31 | R13 (1) | 0.8 | 0.4 | **0.4** | 455/5 | Tabel IV, kelompok P13, baris G31 |  |
| L04-REL-15 | P13 | G33 | R13 (2) | 0.4 | 0.6 | **-0.2** | 455/5 | Tabel IV, kelompok P13, baris G33 | nilai MB-MD negatif; semantik penggabungan tidak didefinisikan artikel |
| L04-REL-16 | P13 | G34 | R13 (3) | 0.6 | 0.2 | **0.4** | 455/5 | Tabel IV, kelompok P13, baris G34 |  |
| L04-REL-17 | P14 | G35 | R14 (1) | 0.4 | 0.6 | **-0.2** | 455/5 | Tabel IV, kelompok P14, baris G35 | nilai MB-MD negatif; semantik penggabungan tidak didefinisikan artikel |
| L04-REL-18 | P14 | G36 | R14 (2) | 1 | 0.2 | **0.8** | 455/5 | Tabel IV, kelompok P14, baris G36 |  |
| L04-REL-19 | P14 | G37 | R14 (3) | 1 | 0.2 | **0.8** | 455/5 | Tabel IV, kelompok P14, baris G37 |  |

Ringkasan [Hitung]: 19 relasi; 13 bernilai MB−MD > 0; **6 bernilai negatif**: P9–G7 (−0.2), P9–G12 (−0.4), P10–G17 (−0.4), P11–G29 (−0.4), P13–G33 (−0.2), P14–G35 (−0.2). Nilai negatif ditranskripsi apa adanya; tidak diubah ke nol, mutlak, atau positif. Tidak ada nilai yang tidak terbaca.
(Di luar scope hama: P3–G6 juga negatif, 0.4−0.6=−0.2.)

Catatan keterbacaan: transkripsi awal dibaca dari lapisan teks PDF per kolom. Asep Abdul Latip mencocokkan MB/MD untuk 11 relasi yang dimodelkan terhadap Tabel IV pada 2026-11-08; semuanya sesuai kandidat. Enam relasi negatif dan dua relasi positif P11 tetap ada di ekstraksi, tetapi tidak dipakai dataset aplikasi. Tabel P11 terpecah antar halaman (G27 di hal. 454; G28–G29 di hal. 455).

## 6. Rumus dan contoh hitung dalam artikel

- [Cetak] Pers. (1) hal. 453: CF[H,E] = MB[H,E] − MD[H,E].
- [Cetak] Pers. (2) hal. 453: `CF(H)=CF(H)CF(R1) + CF(R2) + [CF(R1) * CF(R2)]`. **Tidak konsisten** dengan contoh hal. 456 (bentuk CF1 + CF2·(1−CF1)). Jika dipakai harfiah pada contoh, 0.8 + 0.2 + 0.16 = 1.16 (>1). Tandai: **perlu klarifikasi**; tidak diperbaiki diam-diam.
- [Cetak] Contoh R1 hal. 456: 0.8 + 0.2·(1−0.8) = 0.84; 0.84 + 0.4·(1−0.84) = 0.904. [Hitung] aritmetika cocok (0.84 dan 0.904).
- Contoh hanya untuk penyakit (R1/P1). **Tidak ada contoh hitung hama.** Hasil di Gambar 6: P1 "90.4 % (0.904)".
- Penggabungan nilai negatif tidak dijelaskan.
- Tabel III (hal. 454) "Bobot Nilai CF": Sangat Yakin 1; Yakin 0.8; Cukup Yakin 0.6; Sedikit Yakin 0.4; Tidak Yakin 0.2; Tidak 0. Artikel tidak menyebutnya skala keyakinan pengguna. Semua MB/MD Tabel IV memakai nilai skala ini, dan contoh hitung tidak mengalikan input pengguna. Gambar 5 (hal. 456) menampilkan checklist gejala (kotak centang). [Interpretasi] skala ini kemungkinan skala pakar untuk MB/MD, bukan skala input pengguna; **perlu klarifikasi**.
- Cara pakar menetapkan tiap nilai MB/MD tidak dijelaskan.
- Pohon keputusan (Gambar 3) dan mekanisme forward chaining untuk skor parsial tidak dijelaskan dalam teks; Gambar 3 tidak ditranskripsi.

## 7. Evaluasi (hal. 457)

- 20 data kasus lapangan (wawancara petani, dinilai oleh satu pakar), 18 benar, 2 salah (kasus ke-6 dan ke-12), akurasi 90% (Tabel VIII).
- Metrik: akurasi saja. Tidak ada rincian per hama/penyakit, daftar gejala per kasus, distribusi kelas, confusion matrix, atau identitas 2 kasus salah.
- Data uji gabungan hama dan penyakit. **90% tidak boleh diklaim sebagai akurasi khusus hama maupun akurasi aplikasi kita.**
- Pengujian black box (Tabel VII, 11 item "Valid") bersifat fungsional, bukan bukti kebenaran pengetahuan.

## 8. Penanganan

Tabel V (hal. 455) hanya memuat solusi **P1** (penyakit Busuk). Teks hal. 453 menyatakan tiap data penyakit punya rekomendasi solusi, tetapi isinya tidak ditampilkan. **Tidak ada penanganan untuk P9–P14.** Jangan mengisi penanganan dari sumber ini.

## 9. Ambiguitas

Status 2026-11-07: klarifikasi ke penulis/pakar ditunda ([D-16](../decisions/DECISION_LOG.md)); A2, A3, A4, A5, dan A14 menjadi batasan sistem. Teks G25/G27 memakai Tabel II (D-14).

| ID | Isi | Letak |
|---|---|---|
| A1 | Klasifikasi hama vs penyakit hanya tersirat dari label Tabel VI | Tabel I vs VI |
| A2 | Pers. (2) tercetak tidak sama dengan rumus pada contoh | hal. 453 vs 456 |
| A3 | Penggabungan CF negatif tidak didefinisikan | hal. 453–456 |
| A4 | Aturan AND tetapi dihitung dengan CF kombinasi; tidak jelas apakah aturan aktif bila hanya sebagian gejala dipilih | Tabel VI, hal. 456, Gambar 3 |
| A5 | Peran Tabel III (skala pakar atau skala pengguna) | hal. 454, Gambar 5 |
| A6 | Pembacaan kolom MB/MD dari lapisan teks; perlu cek visual | Tabel IV |
| A7 | Redaksi G25, G27, G30 berbeda dengan R10, R11, R12 | Tabel II vs VI |
| A8 | G25 dan G33 nyaris duplikat | Tabel II |
| A9 | Tabel IV P11 terpecah antar halaman | hal. 454/455 |
| A10 | Tidak ada penanganan hama | Tabel V |
| A11 | Evaluasi gabungan, tanpa rincian | Tabel VIII |
| A12 | Banyak salah ketik nama ilmiah pada Tabel I | Tabel I |
| A13 | DOI tidak tercetak pada PDF; URL PDF resmi dicatat 2026-11-08 | PDF dan register SRC-01 |
| A14 | Sumber nilai MB/MD per sel dan cara penentuannya tidak dijelaskan | hal. 453–454 |
| A15 | Gambar 6 hanya memperlihatkan satu hasil; urutan, ambang batas, dan penanganan banyak hasil tidak dijelaskan | hal. 456 |

## 10. Hasil pemeriksaan dan batasan yang tersisa

1. Sebelas relasi positif kandidat dan label 10 gejala diperiksa manusia terhadap PDF pada 2026-11-08. Tidak ada perubahan MB, MD, atau CF. Jumlah ekstraksi tetap 19 relasi: 11 dimodelkan, 6 negatif, 2 positif P11 ditahan.
2. Delapan relasi yang tidak dimodelkan tetap di review; perlu pemeriksaan tersendiri bila kelak akan dipakai. P11 tetap ditahan menurut D-19.
3. Pers. (2), penggabungan negatif, peran AND dan Tabel III, serta asal MB/MD tidak diklarifikasi ke penulis/pakar menurut D-16. Ini batasan interpretasi, bukan penghalang status D-17.
4. Kesetaraan beberapa nama ilmiah dan padanan nama umum Indonesia belum dibuktikan; flag terkait dipertahankan. Penanganan hama tidak diisi.
5. Kasus berlabel pakar dan evaluasi akurasi khusus hama belum tersedia. Pemeriksaan sumber oleh manusia tidak sama dengan validasi pakar atau kelayakan lapangan.

## 11. Implikasi terhadap checklist dan schema repo

Per [VERIFICATION_CHECKLIST.md](VERIFICATION_CHECKLIST.md), PDF resmi, 11 bobot positif, label gejala, deskripsi lima hama, dan locator telah diperiksa manusia. Aturan AND diuraikan menurut D-12. Sumber deskripsi berasal dari SRC-02, SRC-03, SRC-05, SRC-06, SRC-07; penanganan tidak tersedia. Pemeriksa, tanggal, dan bukti ada pada audit manusia dan catatan penyelesaiannya. Kasus evaluasi berlabel pakar tetap di luar cakupan pemeriksaan ini.

Schema mewajibkan deskripsi hama tidak kosong; lima deskripsi dari sumber tambahan memenuhi kebutuhan itu setelah pemeriksaan manusia. Status `verified` berarti bukti sumber diperiksa menurut D-17, bukan validasi pakar domain.
