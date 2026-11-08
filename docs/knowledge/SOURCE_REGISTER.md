# Register sumber

| ID | Sumber | Akses saat dokumentasi | Kegunaan/status |
| --- | --- | --- | --- |
| SRC-01 | [Adellia dkk., “Penerapan Metode Certainty Factor pada Sistem Pakar Diagnosa Hama dan Penyakit pada Tanaman Tomat,” JEPIN, DOI 10.26418/jp.v8i3.56178](https://jurnal.untan.ac.id/index.php/jepin/article/view/56178); [PDF resmi](https://jurnal.untan.ac.id/index.php/jepin/article/viewFile/56178/75676595632) | PDF dan 11 relasi yang dimodelkan diperiksa Asep Abdul Latip pada 2026-11-08; [audit manusia](L04_HUMAN_AUDIT_ORIGINAL_2026-11-08.md). | `reviewed` menurut D-17 untuk 11 relasi positif dan label kandidat. Enam relasi negatif serta dua relasi P11 tetap di data review. |
| SRC-02 | [Root-Knot Nematode (Meloidogyne spp.) - Tomato Pest Management Guidelines, UC IPM (UC ANR Publication 3470)](https://ipm.ucanr.edu/agriculture/tomato/root-knot-nematodes/) (A.T. Ploeg (Nematology, UC Riverside); University of California Statewide IPM Program) | Deskripsi P9 diperiksa manusia 2026-11-08: *Description of the Pest*, *Damage*. | `reviewed` untuk deskripsi P9; kesetaraan nama L04 belum dibuktikan. |
| SRC-03 | [Vegetable Leafminer, Liriomyza sativae Blanchard (Insecta: Diptera: Agromyzidae), EENY255 (IN507)](https://edis.ifas.ufl.edu/publication/IN507/pdf) (John L. Capinera; UF/IFAS Extension (EDIS)) | Deskripsi P10 diperiksa manusia 2026-11-08: hal. 2 *Adult*, *Host Plants*; hal. 2–3 *Damage*. | `reviewed` untuk deskripsi P10; padanan nama Indonesia belum dibuktikan. |
| SRC-04 | [Studies on the damage potential of the predator Nesidiocoris tenuis on tomato plants, Bulletin of Insectology 62(1): 41-46](https://archive.bulletinofinsectology.org/pdfarticles/vol62-2009-041-046perdikis.pdf) (D. Perdikis, A. Fantinou, N. Garantonakis, P. Kitsis, D. Maselou, S. Panagakis; Bulletin of Insectology (2009)) | Dibaca 2026-11-07. | Kandidat sumber deskripsi hama (lihat [l04_pest_descriptions_draft.json](../../data/review/l04_pest_descriptions_draft.json)); **belum ditinjau pemeriksa**, bukan referensi hubungan gejala-hama L04. Dipakai untuk deskripsi P11, yang ditahan di review (D-19). |
| SRC-05 | [Melon Fly, Bactrocera cucurbitae (Coquillett) (Insecta: Diptera: Tephritidae), EENY199 (IN356)](https://edis.ifas.ufl.edu/publication/IN356/pdf) (H.V. Weems Jr., J.B. Heppner, T.R. Fasulo; UF/IFAS Extension (EDIS)) | Deskripsi P12 diperiksa manusia 2026-11-08: hal. 1 *Introduction*, *Synonyms*, *Distribution*; hal. 2–3 *Larva*; hal. 4 *Life History*, *Damage*, *Hosts*. | `reviewed` untuk deskripsi P12; ketidakpastian sebagian catatan inang tetap disebutkan. |
| SRC-06 | [CPHST Pest Datasheet for Spodoptera litura](https://caps.ceris.purdue.edu/wp-content/uploads/2025/07/Spodoptera-litura_CPHST-Datasheet_2014.pdf) (M. Sullivan (2007), direvisi staf USDA-APHIS-PPQ-CPHST; USDA-APHIS-PPQ-CPHST) | Deskripsi P13 diperiksa manusia 2026-11-08: hal. 1 taksonomi; hal. 2–3 *Biology and Ecology*; hal. 4 *Damage*; hal. 5 *On tomato*. | `reviewed` untuk deskripsi P13; padanan “ulat grayak” belum dibuktikan. |
| SRC-07 | [Black cutworm (297), Pacific Pests, Pathogens, Weeds and Pesticides fact sheet](https://apps.lucidcentral.org/pppw_v13/pdf/web_full/black_cutworm_297.pdf) (Grahame Jackson (berdasarkan CABI 2013 dan Capinera 2012); Pacific Pests and Pathogens (PestNet, ACIAR)); [halaman lama](https://apps.lucidcentral.org/ppp/text/web_full/entities/black_cutworm_297.htm) | Deskripsi P14 diperiksa manusia 2026-11-08: *Hosts*, *Symptoms & Life Cycle*, *Detection & Inspection*. Halaman lama mengembalikan 403 pada audit. | `reviewed` untuk deskripsi P14 dengan PDF resmi; sumber sekunder dan batas redaksi tercatat. |

Abstrak SRC-01 membahas hama **dan** penyakit serta melaporkan evaluasi dari studi tersebut. Angka evaluasi artikel tidak berlaku sebagai akurasi aplikasi proyek ini. Status halaman artikel tidak membuktikan isi tabel atau bobot dalam PDF.

## Pekerjaan sumber yang tertunda

1. PDF resmi SRC-01 tersedia dan 11 relasi yang dimodelkan serta label Tabel II telah dicocokkan manusia pada 2026-11-08; bukti pada audit manusia. Enam relasi negatif dan dua relasi P11 tetap tercatat untuk penelusuran, bukan aturan aplikasi.
2. Hama dipisah dari penyakit; aturan AND R9–R14 dikaji dan diuraikan per gejala berdasarkan D-12.
3. Konfirmasi arti dan asal bobot dengan sumber/pakar; jangan menyalin angka tanpa konteks atau menganggap bobot dapat diturunkan dari abstrak. Status 2026-11-07: ditunda (D-16); butir ini tetap belum terpenuhi, dan data L04 hanya dapat berstatus verified menurut definisi D-17 dengan batasan tertulis.
4. SRC-02, SRC-03, SRC-05, SRC-06, SRC-07 mendukung deskripsi lima hama. Penanganan tidak diisi karena tidak ada bukti yang dipilih untuk itu.
5. Dapatkan kasus uji dan label pembanding pakar yang independen. Saat ini belum tersedia.

## Status audit SRC-01 (L04)

Audit draf 2026-11-07 tercatat pada [L04_SOURCE_AUDIT.md](L04_SOURCE_AUDIT.md), [L04_METHOD_GAP.md](L04_METHOD_GAP.md), dan [ekstraksi review](../../data/review/l04_extraction.json). Saat itu SRC-02 sampai SRC-07 belum ditinjau pemeriksa dan dataset verified belum ada. Pemeriksaan manusia berikutnya pada 2026-11-08 mengubah status lima sumber yang dipakai; lihat bagian di bawah. Klarifikasi ke penulis/pakar tetap ditunda sesuai D-16.

## Status 2026-11-08

Lima sumber deskripsi dan 11 relasi positif diperiksa Asep Abdul Latip pada 2026-11-08. Status `reviewed` dan mode `verified` di proyek ini berarti bukti sumber diperiksa dan dicatat menurut D-17, bukan konfirmasi pakar atau bukti akurasi lapangan. Lihat [catatan penyelesaian audit](L04_HUMAN_AUDIT_RESOLUTION_2026-11-08.md). P11/SRC-04 tidak masuk dataset; penanganan dan evaluasi kasus berlabel pakar tetap tertunda.
