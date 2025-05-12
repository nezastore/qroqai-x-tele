import os
import json
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Ganti dengan token Telegram Anda
TELEGRAM_TOKEN = "7899180208:AAH4hSC12ByLARkIhB4MXghv5vSYfPjj6EA"

# Ganti dengan API Key dan Secret dari Alibaba Cloud Bailian Anda
ALIYUN_ACCESS_KEY_ID = "7899180208:AAH4hSC12ByLARkIhB4MXghv5vSYfPjj6EA"
ALIYUN_ACCESS_KEY_SECRET = "sk-8dbd5b03d3574909b15ea5f81727bfea"
ALIYUN_API_ENDPOINT = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"  # Contoh endpoint, sesuaikan dengan dokumentasi resmi

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **NEZA AI Bot**\n"
        "Kirim pesan apa saja dan saya akan menjawab menggunakan AI!\n\n"
        "🔹 Gunakan tombol 'Salin' di bawah jawaban untuk menyalin\n"
        "Powered by NEZA Cloud Team",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Membuat payload request sesuai dokumentasi API Bailian
        payload = {
            "messages": [
                {"role": "user", "content": user_message}
            ],
            "model": "mixtral-8x7b-32768",  # Sesuaikan model jika perlu
            "temperature": 0.5,
            "max_tokens": 1024
        }

        # Header autentikasi dan content-type
        headers = {
            "Content-Type": "application/json",
            "x-acs-accesskey-id": ALIYUN_ACCESS_KEY_ID,
            "x-acs-accesskey-secret": ALIYUN_ACCESS_KEY_SECRET,
            # Tambahkan header lain jika diperlukan oleh API Bailian
        }

        # Mengirim request POST ke API Bailian
        async with httpx.AsyncClient() as client:
            response = await client.post(ALIYUN_API_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        # Parsing response, sesuaikan dengan struktur response API Bailian
        # Contoh asumsi response:
        # {
        #   "choices": [
        #       {
        #           "message": {
        #               "content": "Jawaban AI di sini"
        #           }
        #       }
        #   ]
        # }
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

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("✅ Teks siap disalin!")
    await query.edit_message_reply_markup(reply_markup=None)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
