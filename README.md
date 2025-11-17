# 🌱 Grow A Garden

Sebuah aplikasi desktop sederhana untuk manajemen tanaman (contoh
struktur dan prototipe UI). Implementasi prototipe menggunakan Python
dan PyQt5; model dapat disimpan secara lokal menggunakan SQLite.

Singkatnya: folder `src/` berisi model, view, dan controller — cocok untuk
arsitektur MVC sederhana.

Cara menjalankan (singkat)

1. Pastikan Python terpasang.
2. (Opsional) Buat virtual environment dan aktifkan:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Pasang dependency utama:

```powershell
pip install PyQt5
```

4. Jalankan aplikasi:

```powershell
python main.py
```

Struktur folder (penting)

    grow-a-garden/
    │
    ├── src/
    │   ├── models/        # data & logika (mis. Mahasiswa)
    │   ├── views/         # UI (PyQt5)
    │   └── controllers/   # penghubung model & view
    │
    ├── backend/           # helper backend / util (opsional)
    ├── database/          # tempat file SQLite (jika digunakan)
    ├── main.py            # entrypoint aplikasi
    └── README.md

Catatan singkat

- Jika model menggunakan SQLite, tempatkan file DB di `database/garden.db`.
- Jika Anda ingin saya buat skrip inisialisasi database (`init_db.py`),
  saya dapat menambahkannya.

Contribusi

- Buka issue atau kirim pull request untuk fitur dan perbaikan.
