# 🤖 Crypto News Summarizer Bot

Auto-scrape berita crypto terbaru dari CoinDesk & CoinTelegraph,
analisis sentimen dengan AI, dan kirim ringkasan ke Telegram — otomatis.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Groq](https://img.shields.io/badge/LLM-Groq%20LLaMA3.1-orange)
![Telegram](https://img.shields.io/badge/Delivery-Telegram-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Demo

![demo](assets/demo.gif)

---

## 🚀 Fitur

- 📡 **Multi-source** — scraping CoinDesk + CoinTelegraph sekaligus
- 🧠 **AI Summarizer** — ringkasan 2-3 kalimat per artikel (Groq LLaMA 3.1)
- 🟢 **Sentiment Analysis** — label BULLISH / BEARISH / NEUTRAL otomatis
- 💬 **Telegram Commands** — /news, /filter, /status, /start
- 🔍 **Keyword Filter** — /filter btc eth → hanya berita relevan
- ⏰ **Scheduler** — otomatis tiap 08:00 & 20:00
- 📝 **Error Logging** — log ke file + notif Telegram kalau ada masalah

---

## 🛠️ Tech Stack

| Komponen | Library |
|---|---|
| Scraping | `requests` + `BeautifulSoup4` |
| AI Summarizer | `groq` (LLaMA 3.1 8B Instant) |
| Telegram | `python-telegram-bot` |
| Scheduler | `schedule` |
| Config | `python-dotenv` |

---

## ⚡ Quick Start

### 1. Clone repo

```bash
git clone https://github.com/ABDI28-pro/crypto-news-bot
cd crypto-news-bot
```

### 2. Install dependencies

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```
### 3. Setup `.env`

Buat file `.env` di root project:
GROQ_API_KEY=gsk_xxxx

TELEGRAM_BOT_TOKEN=xxxx

TELEGRAM_CHAT_ID=xxxx

Cara dapat `TELEGRAM_CHAT_ID`:
1. Kirim `/start` ke bot kamu di Telegram
2. Buka `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Lihat nilai `chat.id` di response JSON

### 4. Jalankan

```bash
# Jalankan sekali (test)
python main.py

# Jalankan bot interaktif (Telegram commands)
python main.py --bot

# Jalankan dengan scheduler otomatis
python main.py --schedule
```

---

## 💬 Telegram Commands

| Command | Fungsi |
|---|---|
| `/start` | Tampilkan menu |
| `/news` | Ambil & rangkum berita sekarang |
| `/filter btc eth` | Filter berita by keyword |
| `/filter clear` | Hapus filter |
| `/status` | Cek filter aktif |

---

## 📁 Struktur Project
crypto-news-bot/

├── main.py          # Entry point + scheduler

├── scraper.py       # Scraping CoinDesk & CoinTelegraph

├── summarizer.py    # Summarize + sentiment analysis

├── telegram_bot.py  # Kirim pesan ke Telegram

├── bot_commands.py  # Handler Telegram commands

├── requirements.txt

└── .env             # API keys (tidak di-commit)

---

## 📤 Contoh Output Telegram
🟢 BULLISH
📰 Bitcoin surges past $70,000 as institutional demand grows
📝 Bitcoin menembus level $70.000 didorong oleh meningkatnya

permintaan institusional dan sentimen pasar yang positif pasca

halving. Analis memperkirakan momentum ini akan berlanjut.
💡 Momentum bullish kuat — pertimbangkan hold atau akumulasi

bertahap di level support.
📡 Sumber: CoinDesk

🔗 Baca selengkapnya

---

## 💼 Use Cases untuk Bisnis

- 📨 **Newsletter crypto otomatis** untuk komunitas trader
- 📊 **Daily briefing** untuk fund manager atau analis
- 🔔 **Alert sistem** untuk monitor berita token tertentu
- 🤖 **White-label bot** untuk platform crypto lokal

---

## ⚙️ Customisasi

| File | Yang bisa diubah |
|---|---|
| `scraper.py` | Tambah sumber berita baru |
| `main.py` | Ubah jadwal otomatis |
| `summarizer.py` | Ubah bahasa / format ringkasan |
| `bot_commands.py` | Tambah command Telegram baru |

---

## 📄 License

MIT — bebas digunakan dan dimodifikasi.

---

> Built by [ABDI28-PRO](https://github.com/ABDI28-pro) · Powered by Groq + python-telegram-bot

### 3. Setup `.env`

Buat file `.env` di root project:
