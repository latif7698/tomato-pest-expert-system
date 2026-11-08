# Data pengetahuan

File `demo/knowledge_demo.json` berisi **fixture sintetis**, bukan pengetahuan hama nyata. Folder [verified](verified/README.md) memuat snapshot L04 yang sumbernya diperiksa manusia pada 2026-11-08 menurut D-17. Data review dan delapan relasi yang tidak dimodelkan tetap terpisah di [review](review/l04_extraction.json). Spesifikasi format ada di [KNOWLEDGE_SPEC.md](../docs/knowledge/KNOWLEDGE_SPEC.md).

Pemilihan dataset harus eksplisit. Mode verified tidak memuat demo sebagai fallback. Kasus pengujian berlabel pakar dan evaluasi akurasi lapangan belum tersedia.
