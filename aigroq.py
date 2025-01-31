from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from groq import Groq

TELEGRAM_TOKEN = "7899180208:AAH4hSC12ByLARkIhB4MXghv5vSYfPjj6EA"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context):
    await update.message.reply_text(
        "🤖 **NEZA AI Bot**\n"
        "Kirim pesan apa saja dan saya akan menjawab menggunakan AI!\n\n"
        "🔹 Gunakan tombol 'Salin' di bawah jawaban untuk menyalin\n"
        "Powered by NEZA Cloud & Airdrop",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context):
    user_message = update.message.text
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}],
            model="mixtral-8x7b-32768",
            temperature=0.5,
            max_tokens=1024
        ).choices[0].message.content
        
        context.user_data['last_response'] = response
        
        keyboard = [
            [InlineKeyboardButton("📋 Salin Jawaban", callback_data='copy_text')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Hanya kirim response murni + tombol
        await update.message.reply_text(
            response,  # <-- Hanya teks response saja
            reply_markup=reply_markup
        )
        
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

async def button_handler(update: Update, context):
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