# Data pengetahuan

File `demo/knowledge_demo.json` berisi **fixture sintetis**, bukan pengetahuan hama nyata. Folder [demo](demo/README.md) terpisah dari [verified](verified/README.md), yang tetap kosong sampai pengetahuan hama lolos [checklist verifikasi](../docs/knowledge/VERIFICATION_CHECKLIST.md). Jangan membuat `knowledge.json` yang menyiratkan data nyata sudah tersedia. Spesifikasi format ada di [KNOWLEDGE_SPEC.md](../docs/knowledge/KNOWLEDGE_SPEC.md).

Pemilihan dataset harus eksplisit. Mode verified tidak boleh memuat demo sebagai fallback. Kasus pengujian berlabel pakar juga belum tersedia.
