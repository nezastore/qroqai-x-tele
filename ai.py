import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes
)

# Token Telegram Anda (tidak diubah)
TELEGRAM_TOKEN = "7899180208:AAH4hSC12ByLARkIhB4MXghv5vSYfPjj6EA"

# API Key Cohere Anda (ganti dengan API Key Anda sendiri dari https://dashboard.cohere.com/)
COHERE_API_KEY = "hdCYDWeT0DWdHHaS3rhejoTJWqDqqWGr0GVip8AS"

# Endpoint API Cohere untuk generate teks
COHERE_API_ENDPOINT = "https://api.cohere.ai/generate"

# Model AI Cohere yang digunakan secara lokal (hardcoded)
SELECTED_MODEL = "command-large"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Cohere AI Bot\n"
        "Halo! Silakan kirim pesan apa saja, dan aku akan menjawab menggunakan model AI yang sudah dipilih."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        payload = {
            "model": SELECTED_MODEL,
            "prompt": user_message,
            "max_tokens": 300,
            "temperature": 0.7,
            "k": 0,
            "p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop_sequences": []
        }

        headers = {
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(COHERE_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Ambil teks hasil generate dari Cohere
        ai_response = data["generations"][0]["text"].strip()

        keyboard = [
            [InlineKeyboardButton("📋 Salin Jawaban", callback_data='copy_text')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            ai_response,
            reply_markup=reply_markup
        )

    except requests.HTTPError as http_err:
        await update.message.reply_text(
            f"⚠️ Aduh, ada masalah HTTP nih: {http_err.response.status_code} - {http_err.response.text}\n"
            "Coba cek lagi ya."
        )
    except Exception as e:
        await update.message.reply_text(
            f"⚠️ Wah, ada error nih: {str(e)}\n"
            "Coba ulangi lagi ya."
        )

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot sudah berjalan... Tekan Ctrl+C untuk berhenti.")
    app.run_polling()

if __name__ == "__main__":
    main()
