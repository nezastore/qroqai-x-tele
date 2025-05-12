import os
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Token Telegram Anda
TELEGRAM_TOKEN = "7899180208:AAH4hSC12ByLARkIhB4MXghv5vSYfPjj6EA"

# API Key dan Secret dari Alibaba Cloud Bailian Anda
# Pastikan tidak ada spasi/tab di akhir string
ALIYUN_ACCESS_KEY_ID = "LTAI5t9sJmre8954kf2tzBJ5".strip()  # Ganti dengan Access Key ID Anda
ALIYUN_ACCESS_KEY_SECRET = "sk-8dbd5b03d3574909b15ea5f81727bfea".strip()  # API key yang Anda berikan

# Endpoint API Bailian yang valid (sesuaikan region Anda)
ALIYUN_API_ENDPOINT = "https://bailian.cn-beijing.aliyuncs.com/v1/chat/completions"

# Daftar model AI yang bisa dipilih pengguna
AVAILABLE_MODELS = [
    "mixtral-8x7b-32768",
    "model-2",
    "model-3"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(model, callback_data=f"model_{model}")]
        for model in AVAILABLE_MODELS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 **NEZA AI Bot**\n"
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
            "messages": [
                {"role": "user", "content": user_message}
            ],
            "model": selected_model,
            "temperature": 0.5,
            "max_tokens": 1024
        }

        headers = {
            "Content-Type": "application/json",
            "x-acs-accesskey-id": ALIYUN_ACCESS_KEY_ID,
            "x-acs-accesskey-secret": ALIYUN_ACCESS_KEY_SECRET,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(ALIYUN_API_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

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

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
