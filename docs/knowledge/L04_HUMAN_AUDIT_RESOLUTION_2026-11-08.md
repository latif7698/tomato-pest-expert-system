# Penyelesaian audit manusia L04, 2026-11-08

Pemeriksa sumber: **Asep Abdul Latip** (pengguna sendiri), 2026-11-08. Pemeriksaan ini memenuhi definisi D-17: bukti sumber diperiksa dan dicatat. Ini bukan validasi pakar domain, diagnosis pasti, atau evaluasi akurasi lapangan.

## Jejak versi

| Artefak | SHA-256 | Keterangan |
| --- | --- | --- |
| [Audit manusia asli](L04_HUMAN_AUDIT_ORIGINAL_2026-11-08.md) | `6b681eb2f77c40cbacfb9bad33b8596983d3af34344655cbad7b730a0dad4403` | Salinan utuh dari `for codex/audit-hasil-lanjutkan_terisi.md` di folder saudara. |
| [Kandidat yang diperiksa](../../data/review/l04_candidate_knowledge_pre_audit_2026-11-08.json) | `d43e1924e18dd07f2661f2a669f74015fda09e0c7a984e1a236c9620d3d0d944` | Snapshot sebelum koreksi, karena audit asli belum mengisi versi/commit kandidat. |
| [Kandidat setelah koreksi](../../data/review/l04_candidate_knowledge.json) | `712578bb666cb75d9b871455f3e9b4af522a769aa5234e70c636402e02e54c5a` | Tetap format review; aturan berstatus `candidate`. |
| [Dataset aplikasi](../../data/verified/knowledge_verified.json) | `45d775c29a7fa02c594cf988d1c6cca7a2169e1ee98dc3bb45538e43c9f8d1a5` | Mode `verified`, versi `l04-2026-11-08-v1`. |

Audit asli menandai temuan sebagai “Selesai”, tetapi alasan keputusan masih menyebut enam temuan terbuka dan tiga pemeriksaan tambahan belum ditandai. Catatan ini menganggap kalimat alasan tersebut sebagai keadaan **sebelum koreksi**: bagian 1 audit asli sudah menandai ketiga pemeriksaan tambahan “Ya”; koreksi nyata di bawah diterapkan setelah audit. Status akhir tiap temuan tercatat di sini, tanpa mengubah dokumen asli.

## Temuan dan penerapan

| Temuan | Penerapan dan dasar | Status akhir |
| --- | --- | --- |
| P9-NAMA | Flag perbedaan nama L04 dan *Meloidogyne spp.* tetap di draf; tidak menyatakan kesetaraan taksonomi yang belum terbukti. | Dicatat sebagai batas interpretasi |
| P12-LOKATOR | Locator SRC-05 untuk *Larva* menjadi hal. 2–3, sesuai audit manusia. | Diterapkan |
| P12-REDAKSI | Klaim hama penting dalam wilayah sebaran dipisah dari fakta sebaran di Indonesia; tidak menyiratkan bukti kepentingan khusus di Indonesia. | Diterapkan |
| P12-FLAG | Flag mengikuti *Damage* dan *Hosts* SRC-05: melon/tanaman terkait paling terdampak; tomat tercatat sebagai inang; sebagian catatan inang dapat berasal dari pengamatan imago pada tumbuhan bukan inang. Catatan keraguan pada deskripsi dipertahankan. | Diterapkan |
| P13-FLAG | Flag bahwa padanan nama “ulat grayak” tidak dibuktikan oleh SRC-06 ditambahkan; locator biologi dirinci hal. 2–3. | Diterapkan |
| P14-REDAKSI | Frasa “pada siang hari” yang tersirat dihapus; locator menambahkan *Detection & Inspection* untuk klaim tanaman muda. PDF resmi SRC-07 dipakai sebagai URL aktif karena halaman lama mengembalikan 403 pada audit. | Diterapkan |
| DOK-REGISTER | [PDF resmi L04](https://jurnal.untan.ac.id/index.php/jepin/article/viewFile/56178/75676595632) dicatat pada SRC-01 dan metadata ekstraksi. | Diterapkan |
| Perbandingan skor | Klaim arah selisih skor di D-11 dan L04_METHOD_GAP diperhalus: hasil adaptasi dapat berbeda, tetapi arah perbandingan dengan artikel tidak dapat dipastikan tanpa metode gabungan bukti negatif/campuran. | Diterapkan |

## Bukti per entri yang dipromosikan

Sebelas pasangan pada tabel berikut dibaca pemeriksa dari Tabel IV PDF L04 dan cocok dengan kandidat sebelum koreksi; angka MB, MD, dan CF tidak diubah. Semua aturan memakai sumber SRC-01 dan locator kelompok baris Tabel IV di dataset.

| Hama–gejala | MB | MD | CF | Halaman cetak |
| --- | ---: | ---: | ---: | ---: |
| P9–G23 | 1 | 0.2 | 0.8 | 454 |
| P9–G24 | 1 | 0.2 | 0.8 | 454 |
| P10–G25 | 1 | 0.2 | 0.8 | 454 |
| P10–G26 | 0.6 | 0.2 | 0.4 | 454 |
| P12–G30 | 1 | 0.2 | 0.8 | 455 |
| P12–G31 | 0.8 | 0.4 | 0.4 | 455 |
| P12–G32 | 0.8 | 0.2 | 0.6 | 455 |
| P13–G31 | 0.8 | 0.4 | 0.4 | 455 |
| P13–G34 | 0.6 | 0.2 | 0.4 | 455 |
| P14–G36 | 1 | 0.2 | 0.8 | 455 |
| P14–G37 | 1 | 0.2 | 0.8 | 455 |

Label 10 gejala dicocokkan pemeriksa dengan Tabel II (hal. cetak 454). Lima deskripsi dicocokkan dengan locator berikut; `source_ids` pada dataset menunjuk sumber tersebut. `P11` dan SRC-04 tetap di review.

| Hama | Sumber | Locator yang diperiksa |
| --- | --- | --- |
| P9 | SRC-02 | *Description of the Pest*, *Damage* |
| P10 | SRC-03 | hal. 2 *Adult*, *Host Plants*; hal. 2–3 *Damage* |
| P12 | SRC-05 | hal. 1 *Introduction*, *Synonyms*, *Distribution*; hal. 2–3 *Larva*; hal. 4 *Life History*, *Damage*, *Hosts* |
| P13 | SRC-06 | hal. 1 taksonomi; hal. 2–3 *Biology and Ecology*; hal. 4 *Damage*; hal. 5 *On tomato* |
| P14 | SRC-07 | *Hosts*, *Symptoms & Life Cycle*, *Detection & Inspection* |

Schema aplikasi menyimpan status aturan, status sumber, URL, dan locator aturan. Nama pemeriksa, tanggal, serta locator deskripsi dicatat di sini dan di audit asli karena schema tidak memiliki field tersebut. `handling` tidak diisi.

## Batas yang tetap terbuka

- Enam relasi negatif dan dua relasi positif P11 tetap di `data/review/l04_extraction.json`, di luar dataset aplikasi.
- Kesetaraan beberapa nama ilmiah L04 dan padanan nama umum Indonesia belum dibuktikan; flag draf tetap berlaku.
- Klarifikasi kepada penulis L04 tentang persamaan (2), penggabungan negatif/campuran, AND, Tabel III, dan asal MB/MD ditunda sesuai D-16.
- Skala keyakinan pengguna belum divalidasi. Belum ada kasus hama berlabel pakar, evaluasi akurasi lapangan, atau bukti kelayakan penggunaan lapangan.
- Tidak ada sumber penanganan hama yang dipilih; penanganan tetap kosong.
