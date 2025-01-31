# 🤖 Telegram AI Bot with Groq API

Bot Telegram cerdas menggunakan Groq API untuk respons cepat dengan model Mixtral/Llama2. Dioptimalkan untuk deployment di VPS.

## Fitur Utama
- Integrasi real-time dengan Groq Cloud
- Tombol salin inline
- Optimasi untuk lingkungan server
- Auto-restart dengan PM2
- Dukungan Ubuntu/Debian

## Prasyarat
- VPS dengan OS Ubuntu 22.04 LTS+
- Akses root/administrator
- Python 3.10+
- Akun [Groq Cloud](https://console.groq.com/)

## Instalasi di VPS

### 1. Update Sistem
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git python3-pip -y

git clone github.com/nezastore/qroqai-x-tele
cd qroqai-x-tele

pip install python-telegram-bot groq

# Install PM2
npm install pm2 -g

# Jalankan bot
pm2 start bot.py --name "groq-bot"

# Monitor status
pm2 monit

# Set auto-start pada reboot
pm2 startup
pm2 save


Lisensi
MIT License - LIHAT LISENSI

🛠️ Maintenance Tips:

Update sistem secara berkala: sudo apt update && sudo apt upgrade

Backup config: pm2 save

Monitor resource: htop

🔐 Keamanan VPS:

Gunakan SSH key authentication

Update password root secara berkala

Hindari menjalankan sebagai user root

📅 Terakhir update: 1 Februaari 2025



