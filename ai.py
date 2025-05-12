import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes, CallbackQueryHandler
)

# Token Telegram Anda
TELEGRAM_TOKEN = "7899180208:AAH4hSC12ByLARkIhB4MXghv5vSYfPjj6EA"

# API Key Groq Anda
GROQ_API_KEY = "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"

# Endpoint API Groq
GROQ_API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

# Daftar model AI Groq yang bisa dipilih pengguna
AVAILABLE_MODELS = [
    "llama3-8b-8192",
    "llama3-70b-8192",
    "gemma-7b-it",
    "mixtral-8x7b-32768"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(model, callback_data=f"model_{model}")]
        for model in AVAILABLE_MODELS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 **Groq AI Bot**\n"
        "Silakan pilih model AI yang ingin Anda gunakan:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data.startswith("model_"):
        selected_model = data[len("model_"):]
        context.user_data['selected_model'] = selected_model
        await query.answer(f"Model AI dipilih: {selected_model}")
        await query.edit_message_text(
            f"✅ Anda telah memilih model AI: *{selected_model}*\n\n"
            "Sekarang kirim pesan apa saja dan saya akan menjawab menggunakan model ini.",
            parse_mode="Markdown"
        )
    elif data == 'copy_text':
        await query.answer("✅ Teks siap disalin!")
        await query.edit_message_reply_markup(reply_markup=None)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    selected_model = context.user_data.get('selected_model')

    if not selected_model:
        await update.message.reply_text(
            "⚠️ Anda belum memilih model AI.\n"
            "Silakan gunakan perintah /start untuk memilih model terlebih dahulu."
        )
        return

    try:
        payload = {
            "model": selected_model,
            "messages": [
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.5,
            "max_tokens": 1024
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }

        response = requests.post(GROQ_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Struktur respons Groq mirip OpenAI: ambil konten jawaban
        ai_response = data["choices"][0]["message"]["content"]

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
        await update.message.reply_text(f"⚠️ HTTP error: {http_err.response.status_code} - {http_err.response.text}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot berjalan... Tekan Ctrl+C untuk berhenti.")
    app.run_polling()

if __name__ == "__main__":
    main()
