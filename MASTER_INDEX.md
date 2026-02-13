# 📚 Web Shell Scanner - Master Index

Dokumentasi lengkap untuk **Web Shell Scanner v1.0 & v2.0 (Telegram)**

---

## 🚀 QUICK START (Pilih Salah Satu)

### Option 1: Basic Version (Tanpa Telegram)
```bash
pip install -r requirements.txt
python webshell_scanner.py -u https://example.com
```

### Option 2: Telegram Version (Dengan Notifikasi)
```bash
pip install -r requirements.txt
python webshell_scanner_telegram.py -u https://example.com \
  -tb "YOUR_BOT_TOKEN" -tc "YOUR_CHAT_ID"
```

---

## 📁 FILE STRUCTURE

### 🔴 SCRIPT FILES (PALING PENTING)

| File | Versi | Ukuran | Deskripsi |
|------|-------|--------|-----------|
| **webshell_scanner.py** | v1.0 | 11KB | ⭐ Script dasar tanpa notifikasi |
| **webshell_scanner_telegram.py** | v2.0 | 18KB | ⭐ Script dengan Telegram alerts |

**Gunakan salah satu!** Telegram version bisa jalan tanpa Telegram juga.

---

### 📘 DOKUMENTASI UTAMA

#### Untuk Basic Version (v1.0)
| File | Untuk Apa? |
|------|-----------|
| **README.md** | Dokumentasi lengkap versi basic |
| **QUICK_START.md** | Panduan cepat 5 menit |
| **DEMO_OUTPUT.txt** | Contoh output scanning |

#### Untuk Telegram Version (v2.0)
| File | Untuk Apa? |
|------|-----------|
| **README_TELEGRAM.md** | Dokumentasi lengkap Telegram version |
| **TELEGRAM_SETUP.txt** | Setup Telegram bot (5 langkah) |
| **VERSION_COMPARISON.md** | Perbandingan v1.0 vs v2.0 |

---

### 📄 DOCUMENTATION FILES (Lengkap)

| File | Ukuran | Deskripsi |
|------|--------|-----------|
| MASTER_INDEX.md | (ini) | Index master semua file |
| INDEX.txt | 4.4K | Navigasi cepat ASCII |
| VERSION_COMPARISON.md | 6.7K | Basic vs Telegram comparison |
| QUICK_START.md | 2.9K | Mulai dalam 5 menit |
| TELEGRAM_SETUP.txt | 12K | Setup Telegram step-by-step |
| README.md | 4.6K | Dokumentasi Basic version |
| README_TELEGRAM.md | 8.8K | Dokumentasi Telegram version |
| DEMO_OUTPUT.txt | 3.2K | Contoh output scan |

---

### 🔧 CONFIGURATION FILES

| File | Deskripsi |
|------|-----------|
| requirements.txt | Python dependencies (requests) |
| config.example.json | Contoh konfigurasi Telegram |

---

## 🎯 READING GUIDE

### Saya Pemula, Baca Apa?

**Step 1:** Baca **INDEX.txt** atau **MASTER_INDEX.md** (file ini)
**Step 2:** Pilih versi:
  - Tanpa notifikasi → Baca **README.md** + **QUICK_START.md**
  - Dengan Telegram → Baca **README_TELEGRAM.md** + **TELEGRAM_SETUP.txt**
**Step 3:** Lihat **DEMO_OUTPUT.txt** untuk contoh
**Step 4:** Jalankan script!

### Saya Sudah Paham, Mau Cepat?

```bash
# Basic version
python webshell_scanner.py -u https://example.com

# Telegram version (setelah setup bot)
python webshell_scanner_telegram.py -u https://example.com \
  -tb "TOKEN" -tc "CHAT_ID"
```

### Saya Mau Setup Telegram, Baca Apa?

**Prioritas:**
1. **TELEGRAM_SETUP.txt** ← Mulai dari sini!
2. **README_TELEGRAM.md** ← Detail lengkap
3. **config.example.json** ← Contoh config

### Saya Ragu Pakai Versi Mana?

Baca: **VERSION_COMPARISON.md**

**TL;DR:**
- Personal use, manual scan → **Basic (v1.0)**
- Team monitoring, automated → **Telegram (v2.0)**

---

## 📊 FEATURE MATRIX

| Feature | Basic v1.0 | Telegram v2.0 |
|---------|------------|---------------|
| Web shell detection | ✅ | ✅ |
| Multi-threading | ✅ | ✅ |
| Console output | ✅ | ✅ |
| Real-time alerts | ❌ | ✅ Telegram |
| Mobile notifications | ❌ | ✅ Telegram |
| Team collaboration | ❌ | ✅ Group chat |
| Summary reports | ❌ | ✅ Telegram |

---

## 🔍 FILE PURPOSE SUMMARY

### Must Read Files (Wajib Baca)

**Untuk Basic Version:**
1. ✅ README.md - Cara pakai, fitur, limitasi
2. ✅ QUICK_START.md - Panduan cepat

**Untuk Telegram Version:**
1. ✅ README_TELEGRAM.md - Dokumentasi lengkap
2. ✅ TELEGRAM_SETUP.txt - Setup bot (PENTING!)

### Optional Files (Baca Jika Perlu)

- VERSION_COMPARISON.md - Jika ragu pilih versi mana
- DEMO_OUTPUT.txt - Jika ingin lihat contoh output
- INDEX.txt - Alternative navigation guide
- config.example.json - Jika mau pakai config file

---

## 📋 QUICK COMMANDS REFERENCE

### Installation
```bash
pip install -r requirements.txt
```

### Basic Scan
```bash
python webshell_scanner.py -u https://example.com
```

### Telegram Scan
```bash
python webshell_scanner_telegram.py \
  -u https://example.com \
  -tb "123456789:ABCdefGHIjklMNOpqrsTUVwxyz" \
  -tc "123456789"
```

### Test Telegram
```bash
python webshell_scanner_telegram.py --test-telegram \
  -tb "YOUR_TOKEN" -tc "YOUR_CHAT_ID"
```

### Advanced Options
```bash
# Custom timeout & workers
python webshell_scanner_telegram.py \
  -u https://example.com \
  -tb "TOKEN" -tc "CHAT_ID" \
  -t 30 -w 20
```

---

## 🎓 LEARNING PATH

### Path 1: Quick Start (15 menit)
1. Install dependencies
2. Baca QUICK_START.md
3. Run basic scan
4. Done!

### Path 2: Production Setup (1 jam)
1. Baca README_TELEGRAM.md
2. Setup Telegram bot (TELEGRAM_SETUP.txt)
3. Test connection
4. Configure automated scanning
5. Deploy!

### Path 3: Complete Understanding (2 jam)
1. Baca semua README files
2. Pahami VERSION_COMPARISON.md
3. Explore config options
4. Test both versions
5. Choose best for your needs

---

## 🔐 SECURITY NOTES

**PENTING - Baca Ini:**

1. **Legal:** HANYA gunakan pada website Anda sendiri atau dengan izin tertulis
2. **Bot Token:** Jangan commit ke Git, gunakan environment variables
3. **False Positives:** Scanner tidak 100% akurat, manual check tetap perlu
4. **Server Load:** Adjust workers (-w) untuk avoid overwhelming server

---

## 💡 PRO TIPS

### Tip 1: Start Simple
Mulai dengan Basic version untuk testing, upgrade ke Telegram jika perlu.

### Tip 2: Use Config File
Simpan credentials di config.json (add to .gitignore):
```json
{
  "telegram_bot_token": "YOUR_TOKEN",
  "telegram_chat_id": "YOUR_CHAT_ID"
}
```

### Tip 3: Scheduled Scanning
Setup cron job untuk scan otomatis:
```bash
0 2 * * * python3 /path/to/webshell_scanner_telegram.py \
  -u https://mysite.com -tb "TOKEN" -tc "CHAT_ID"
```

### Tip 4: Multiple Sites
Scan multiple websites dengan loop:
```bash
for site in site1.com site2.com site3.com; do
  python webshell_scanner_telegram.py -u https://$site \
    -tb "TOKEN" -tc "CHAT_ID"
done
```

---

## 🆘 TROUBLESHOOTING QUICK LINKS

| Problem | Read This |
|---------|-----------|
| Don't know which version to use | VERSION_COMPARISON.md |
| How to setup Telegram | TELEGRAM_SETUP.txt |
| Script not working | README.md (Troubleshooting) |
| Telegram not sending | README_TELEGRAM.md (Troubleshooting) |
| Want to see example output | DEMO_OUTPUT.txt |

---

## 📞 SUPPORT RESOURCES

**Telegram Bot Setup:**
- Official Bot API: https://core.telegram.org/bots/api
- BotFather: https://t.me/botfather
- Get Chat ID: @userinfobot or @getidsbot

**Python Help:**
- Requests library: https://requests.readthedocs.io/

---

## 📈 VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | - | Basic web shell scanner |
| v2.0 | - | + Telegram notifications |
| | | + Real-time alerts |
| | | + Summary reports |

---

## ✅ QUICK DECISION TREE

```
Need web shell scanner?
    │
    ├─ One-time scan? ─────────────────────► Use Basic (v1.0)
    │
    ├─ Need mobile alerts? ────────────────► Use Telegram (v2.0)
    │
    ├─ Team monitoring? ───────────────────► Use Telegram (v2.0)
    │
    ├─ Automated scanning? ────────────────► Use Telegram (v2.0)
    │
    └─ Not sure? ──────────────────────────► Read VERSION_COMPARISON.md
```

---

## 🎯 FILE PRIORITY FOR DIFFERENT USERS

### Security Professional
**Priority:**
1. README_TELEGRAM.md
2. TELEGRAM_SETUP.txt
3. VERSION_COMPARISON.md

### System Administrator
**Priority:**
1. QUICK_START.md
2. README.md
3. DEMO_OUTPUT.txt

### Developer
**Priority:**
1. README.md
2. webshell_scanner.py (read code)
3. requirements.txt

### Manager
**Priority:**
1. VERSION_COMPARISON.md
2. DEMO_OUTPUT.txt
3. README_TELEGRAM.md

---

## 📦 PACKAGE CONTENTS SUMMARY

**Total Files:** 25
**Total Size:** ~188KB
**Scripts:** 2 (Basic + Telegram)
**Documentation:** 10+ files
**Dependencies:** requests only

**All-in-one package** - everything you need! 🎉

---

## 🔗 NAVIGATION

- **New User?** → Start with INDEX.txt
- **Want Basic?** → README.md + QUICK_START.md
- **Want Telegram?** → README_TELEGRAM.md + TELEGRAM_SETUP.txt
- **Compare Versions?** → VERSION_COMPARISON.md
- **See Example?** → DEMO_OUTPUT.txt

---

**Happy Scanning! 🔒**

*Security is a journey, not a destination.*

---

**Last Updated:** 2024
**Package Version:** 2.0 Complete
**Documentation Status:** ✅ Complete

