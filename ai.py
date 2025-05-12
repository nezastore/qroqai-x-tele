import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes, CallbackQueryHandler
)

# Token Telegram Anda (tidak diubah)
TELEGRAM_TOKEN = "7899180208:AAH4hSC12ByLARkIhB4MXghv5vSYfPjj6EA"

# API Key Cohere Anda (ganti dengan API Key Anda sendiri dari https://dashboard.cohere.com/)
COHERE_API_KEY = "hdCYDWeT0DWdHHaS3rhejoTJWqDqqWGr0GVip8AS"

# Endpoint API Cohere untuk generate teks
COHERE_API_ENDPOINT = "https://api.cohere.ai/generate"

# Daftar model AI Cohere yang bisa dipilih pengguna (contoh model yang umum tersedia)
AVAILABLE_MODELS = [
    "command-xlarge-nightly",
    "command-large",
    "command-medium",
    "command-small",
    "xlarge",
    "large",
    "medium",
    "small"
]

# Membuat tombol model dengan tampilan 2 kolom agar lebih menarik
def build_model_keyboard():
    keyboard = []
    row = []
    for i, model in enumerate(AVAILABLE_MODELS, 1):
        row.append(InlineKeyboardButton(model, callback_data=f"model_{model}"))
        if i % 2 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = build_model_keyboard()
    await update.message.reply_text(
        "🤖 **Cohere AI Bot**\n"
        "Halo! Silakan pilih model AI yang ingin kamu gunakan ya:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data.startswith("model_"):
        selected_model = data[len("model_"):]
        context.user_data['selected_model'] = selected_model
        await query.answer(f"Kamu memilih model AI: {selected_model}")
        await query.edit_message_text(
            f"✅ Model AI *{selected_model}* sudah dipilih.\n\n"
            "Sekarang, kirimkan pesan apa saja, dan aku akan menjawab menggunakan model ini ya!",
            parse_mode="Markdown"
        )
    elif data == 'copy_text':
        await query.answer("✅ Teks sudah siap untuk disalin!")
        await query.edit_message_reply_markup(reply_markup=None)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    selected_model = context.user_data.get('selected_model')

    if not selected_model:
        await update.message.reply_text(
            "⚠️ Kamu belum memilih model AI nih.\n"
            "Yuk, ketik /start dulu untuk memilih model yang kamu mau."
        )
        return

    try:
        payload = {
            "model": selected_model,
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

        context.user_data['last_response'] = ai_response

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
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot sudah berjalan... Tekan Ctrl+C untuk berhenti.")
    app.run_polling()

if __name__ == "__main__":
    main()
