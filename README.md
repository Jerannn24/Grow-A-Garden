# 🌱 Grow A Garden

![Status](https://img.shields.io/badge/Status-Development-green)
![Language](https://img.shields.io/badge/Language-Python_3-blue)
![Framework](https://img.shields.io/badge/Framework-PyQt5-orange)
![Architecture](https://img.shields.io/badge/Architecture-MVC-purple)

**Grow A Garden** adalah aplikasi desktop yang dirancang untuk membantu pengguna, baik pemula maupun ahli dalam melakukan budidaya tanaman. Aplikasi ini bertujuan meningkatkan produktivitas komoditas melalui manajemen perawatan yang terorganisir dan interaksi komunitas.

Aplikasi ini dibangun menggunakan arsitektur **Model-View-Controller (MVC)** untuk memisahkan logika pemrosesan, data, dan antarmuka pengguna, memastikan kode yang bersih dan mudah dikelola.

---

## 👥 (Kelompok 07 - K01)

| NIM          | Nama                    |
| :----------- | :---------------------- |
| **13524005** | Geraldo Artemius        |
| **13524015** | Mahatma Brahmana        |
| **13524045** | Ahmad Zaky Robbani      |
| **13524051** | Mikhael Andrian Yonatan |
| **13524055** | Junior Natra Situmorang |

---

## ✨ Fitur Utama

Berdasarkan spesifikasi desain perangkat lunak (DPPL), aplikasi ini mencakup fitur-fitur berikut:

### 🌿 Manajemen Tanaman (Plant Management)

- **Profil Tanaman:** Menambahkan, memperbarui, dan menghapus profil tanaman lengkap dengan data spesies, media tanam, dan kebutuhan perawatan.
- **Pelacakan Pertumbuhan:** Mencatat data pertumbuhan tanaman seperti tinggi dan fase pertumbuhan.

### ✅ Aktivitas & Perawatan (Tasks & Care)

- **To-Do List Harian:** Menampilkan daftar kegiatan perawatan harian (menyiram, memupuk, dll) berdasarkan jadwal tanaman.
- **Rekaman Aktivitas:** Mencatat aktivitas perawatan yang telah dilakukan pengguna.
- **Pengingat Notifikasi:** Menerima notifikasi untuk tugas yang tertunda (overdue) atau rekomendasi baru.

### 💡 Rekomendasi Cerdas (Smart Insights)

- **Sistem Rekomendasi:** Menerima saran perawatan berdasarkan kondisi tanaman dan riwayat aktivitas pengguna.

### 🤝 Komunitas (Community)

- **Forum Diskusi:** Berbagi postingan tentang perkembangan tanaman ke komunitas.
- **Interaksi Sosial:** Memberikan komentar, like, dan melihat postingan populer.
- **Keamanan:** Fitur pelaporan dan pemblokiran pengguna untuk menjaga komunitas tetap kondusif.

### 🔐 Manajemen Akun

- **Autentikasi Aman:** Registrasi, Login, dan manajemen sesi pengguna.
- **Pengaturan Profil:** Mengubah password dan informasi profil pengguna.

---

## 🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman:** Python
- **GUI Framework:** PyQt5
- **Database:** SQLite
- **Arsitektur:** MVC (Model-View-Controller)

---

## 🚀 Cara Menjalankan Aplikasi

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal Anda:

### 1. Prasyarat

Pastikan **Python 3.x** sudah terinstall di komputer Anda.

### 2. Setup Virtual Environment (Opsional tapi Disarankan)

Disarankan menggunakan virtual environment agar dependencies tidak tercampur.

```powershell
# Buat virtual environment
python -m venv .venv

# Aktifkan environment (Windows)
.\.venv\Scripts\Activate.ps1

# Aktifkan environment (macOS/Linux)
source .venv/bin/activate
```

### 3. Install Dependencies

```powershell
pip install PyQt5
```

### 4. Jalankan Program

```powershell
# Jalankan dari ROOT FOLDER (GROW-A-GARDEN)
python src/main.py
```

## Daftar Modul serta Pembagian

| Nama         | Modul (.py)                                                                                                                               |
| :----------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| **13524005** | PostManager, Post, SharePost, DisplayCommunity, DisplayPost, HomeScreen, MainWindow, CommunityHeader, Sidebar, AppHeader, HomePage        |
| **13524015** | Report, AdminActionForm, AdminReportDisplay, DisplayPost, Post, HomeScreen, MainWindow, ReportForm, create_admin, Sidebar, UserModel      |
| **13524045** | ToDoListManager, Task, ActivityRecordPopUp, ChangePasswordPopUp, DisplaySettings, DisplayToDoList, FlowLayout, AddPlantForm, PlantDetails |
| **13524051** | PlantManager, Plant, AddPlantCard, AppHeader, HomePage, MainWindow, PlantCard, AddPlantForm, PlantDetails, RemovePlantForm                |
| **13524055** | AccountManager, UserModel, MainWindow, Sidebar, DisplayProfile, FormChangePassword, FormChangeProfile, FormLogin, FormRegister            |

## Database

### app.db — Main Application Database

#### 1. users

Menyimpan informasi akun pengguna dan status profil.

| Kolom                   | Tipe Data | Deskripsi                                       |
| ----------------------- | --------- | ----------------------------------------------- |
| userID                  | INTEGER   | Primary Key, Auto Increment. ID unik pengguna.  |
| username                | TEXT      | Username unik.                                  |
| password                | TEXT      | Password (hashed).                              |
| email                   | TEXT      | Email unik.                                     |
| profileInfo             | TEXT      | Informasi bio tambahan (Default: '').           |
| role                    | TEXT      | Peran pengguna (user/admin).                    |
| reportCount             | INTEGER   | Jumlah laporan yang diterima akun.              |
| status                  | TEXT      | Status akun (active/banned/suspended).          |
| suspendedUntil          | TEXT      | Tanggal akhir suspensi (opsional).              |
| location                | TEXT      | Lokasi pengguna (Default: 'unknown').           |
| notificationPreferences | TEXT      | Preferensi notifikasi (Default: 'all').         |
| notificationTime        | TEXT      | Waktu pengiriman notifikasi (Default: '08:00'). |
| timeCreated             | TEXT      | Timestamp pembuatan akun.                       |
| banReason               | TEXT      | Alasan ban (Default: '').                       |

#### 2. plants

| Kolom             | Tipe Data | Deskripsi                     |
| ----------------- | --------- | ----------------------------- |
| plantID           | TEXT      | Primary Key. ID unik tanaman. |
| userID            | TEXT      | ID pemilik tanaman.           |
| plantName         | TEXT      | Nama panggilan tanaman.       |
| plantSpecies      | TEXT      | Spesies tanaman.              |
| plantingStartDate | TEXT      | Tanggal mulai tanam.          |
| plantMedia        | TEXT      | Media tanam.                  |
| plantPhase        | TEXT      | Fase pertumbuhan saat ini.    |
| lightingDuration  | TEXT      | Durasi penyinaran.            |
| height            | REAL      | Tinggi tanaman.               |
| harvestEstim      | TEXT      | Estimasi panen.               |
| problem           | TEXT      | Masalah kesehatan tanaman.    |
| leafColor         | TEXT      | Warna daun saat ini.          |

#### 3. tasks

| Kolom           | Tipe Data | Deskripsi                                  |
| --------------- | --------- | ------------------------------------------ |
| task_id         | INTEGER   | Primary Key, Auto Increment.               |
| user_id         | INTEGER   | ID pemilik tugas.                          |
| plant_id        | TEXT      | ID tanaman terkait.                        |
| action_type     | TEXT      | Jenis tindakan (siram, pupuk, panen, dll). |
| quantity        | INTEGER   | Kuantitas rencana tindakan.                |
| status          | INTEGER   | Status (0 = belum, 1 = selesai).           |
| deadline        | TEXT      | Batas waktu pengerjaan.                    |
| actual_quantity | INTEGER   | Jumlah aktual.                             |
| time_done       | TEXT      | Waktu penyelesaian.                        |

#### 4. postList

| Kolom         | Tipe Data | Deskripsi                                 |
| ------------- | --------- | ----------------------------------------- |
| postID        | INTEGER   | Primary Key, Auto Increment.              |
| userID        | INTEGER   | Pembuat postingan.                        |
| repliedPostID | INTEGER   | Jika komentar, ID postingan induk.        |
| title         | TEXT      | Judul postingan.                          |
| content       | TEXT      | Isi konten.                               |
| media         | TEXT      | Path media.                               |
| timeCreated   | TEXT      | Waktu dibuat.                             |
| viewCount     | INTEGER   | Jumlah dilihat.                           |
| likeCount     | INTEGER   | Jumlah like.                              |
| isAvailable   | INTEGER   | Status ketersediaan (1 aktif, 0 dihapus). |

#### 5. postLikes

| Kolom      | Tipe Data | Deskripsi                              |
| ---------- | --------- | -------------------------------------- |
| id         | INTEGER   | Primary Key, Auto Increment.           |
| postID     | INTEGER   | Post yang dilike.                      |
| userID     | INTEGER   | Pengguna yang melike.                  |
| Constraint | UNIQUE    | Kombinasi (postID, userID) harus unik. |

#### 6. reports

| Kolom             | Tipe Data | Deskripsi                          |
| ----------------- | --------- | ---------------------------------- |
| reportID          | INTEGER   | Primary Key, Auto Increment.       |
| postID            | INTEGER   | Post yang dilaporkan.              |
| reporterID        | INTEGER   | ID pelapor.                        |
| violationType     | TEXT      | Jenis pelanggaran.                 |
| additionalDetails | TEXT      | Detail tambahan.                   |
| timeCreated       | TEXT      | Waktu laporan.                     |
| status            | TEXT      | Status laporan (pending/resolved). |
| adminAction       | TEXT      | Tindakan admin.                    |
| adminID           | INTEGER   | Admin pemroses.                    |
| actionTime        | TEXT      | Waktu tindakan.                    |

### plants.db — Plant Knowledge Base

#### 1. species

| Kolom                | Tipe Data | Deskripsi                 |
| -------------------- | --------- | ------------------------- |
| id                   | INTEGER   | Primary Key.              |
| common_name          | TEXT      | Nama umum.                |
| scientific_name      | TEXT      | Nama ilmiah.              |
| ideal_sunlight_habit | TEXT      | Kebutuhan sinar matahari. |

#### 2. base_care_profiles

| Kolom              | Tipe Data | Deskripsi                                 |
| ------------------ | --------- | ----------------------------------------- |
| id                 | INTEGER   | Primary Key.                              |
| species_id         | INTEGER   | FK ke `species`.                          |
| stage_name         | TEXT      | Tahap tumbuh (Seedling, Vegetative, dll). |
| min_age_weeks      | INTEGER   | Usia minimal.                             |
| max_age_weeks      | INTEGER   | Usia maksimal.                            |
| min_height_cm      | INTEGER   | Tinggi minimal.                           |
| max_height_cm      | INTEGER   | Tinggi maksimal.                          |
| water_freq_days    | INTEGER   | Frekuensi siram (hari).                   |
| water_vol_ml       | INTEGER   | Volume air.                               |
| sunlight_hours_req | INTEGER   | Kebutuhan cahaya.                         |
| fert_freq_days     | INTEGER   | Frekuensi pupuk.                          |
| fert_vol_ml        | INTEGER   | Volume pupuk.                             |

#### 3. harvest_info

| Kolom                    | Tipe Data | Deskripsi                   |
| ------------------------ | --------- | --------------------------- |
| id                       | INTEGER   | Primary Key.                |
| species_id               | INTEGER   | FK ke `species`.            |
| min_time_to_harvest_days | INTEGER   | Hari minimal sebelum panen. |
| max_time_to_harvest_days | INTEGER   | Hari maksimal.              |
| expected_yield_unit      | TEXT      | Satuan hasil panen.         |
| harvest_notes            | TEXT      | Catatan & tips panen.       |

#### 4. diagnostics

| Kolom              | Tipe Data | Deskripsi           |
| ------------------ | --------- | ------------------- |
| id                 | INTEGER   | Primary Key.        |
| symptom_color      | TEXT      | Warna gejala.       |
| action_instruction | TEXT      | Tindakan perbaikan. |
| user_message       | TEXT      | Pesan ke pengguna.  |

#### 5. sunlight_modifiers

| Kolom                 | Tipe Data | Deskripsi              |
| --------------------- | --------- | ---------------------- |
| id                    | INTEGER   | Primary Key.           |
| condition_type        | TEXT      | Jenis kondisi cahaya.  |
| water_evap_multiplier | REAL      | Pengali evaporasi air. |
| note                  | TEXT      | Catatan.               |

#### 6.media_modifiers

| Kolom                 | Tipe Data | Deskripsi                      |
| --------------------- | --------- | ------------------------------ |
| id                    | INTEGER   | Primary Key.                   |
| media_type            | TEXT      | Jenis media (Soil, Leca, dll). |
| water_freq_multiplier | REAL      | Pengali frekuensi siram.       |
| water_vol_multiplier  | REAL      | Pengali volume air.            |
| fert_freq_multiplier  | REAL      | Pengali frekuensi pupuk.       |
| note                  | TEXT      | Catatan.                       |
