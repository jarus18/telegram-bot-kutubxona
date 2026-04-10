import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Logging sozlash
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- /start buyrug'i ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("✅ Ha", callback_data="yes"),
            InlineKeyboardButton("❌ Yo'q", callback_data="no"),
        ],
        [
            InlineKeyboardButton("ℹ️ Ma'lumot", callback_data="info"),
            InlineKeyboardButton("⚙️ Sozlamalar", callback_data="settings"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Assalomu alaykum! Quyidagi tugmalardan birini tanlang:",
        reply_markup=reply_markup
    )


# --- Tugma bosilganda ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Telegram'ga "OK" signali yuborish

    data = query.data

    if data == "yes":
        text = "✅ Siz 'Ha' ni tanladingiz!"
    elif data == "no":
        text = "❌ Siz 'Yo'q' ni tanladingiz!"
    elif data == "info":
        text = "ℹ️ Bu bot python-telegram-bot kutubxonasi bilan yaratilgan."
    elif data == "settings":
        # Sozlamalar uchun yangi inline keyboard
        keyboard = [
            [InlineKeyboardButton("🔔 Bildirishnomalar", callback_data="notif")],
            [InlineKeyboardButton("🌐 Til", callback_data="language")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("⚙️ Sozlamalar:", reply_markup=reply_markup)
        return
    elif data == "back":
        # Bosh menyuga qaytish
        keyboard = [
            [
                InlineKeyboardButton("✅ Ha", callback_data="yes"),
                InlineKeyboardButton("❌ Yo'q", callback_data="no"),
            ],
            [
                InlineKeyboardButton("ℹ️ Ma'lumot", callback_data="info"),
                InlineKeyboardButton("⚙️ Sozlamalar", callback_data="settings"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "👋 Salom! Quyidagi tugmalardan birini tanlang:",
            reply_markup=reply_markup
        )
        return
    elif data == "notif":
        text = "🔔 Bildirishnomalar yoqilgan!"
    elif data == "language":
        text = "🌐 Til: O'zbek"
    else:
        text = "❓ Noma'lum buyruq."

    await query.edit_message_text(text=text)


# --- /help buyrug'i ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📖 Yordam:\n"
        "/start - Botni boshlash\n"
        "/help - Yordam olish"
    )


# --- Asosiy funksiya ---
def main() -> None:
    TOKEN = "8598309632:AAEihm3OI0I6V4lLFJx6I3s1ohH7TTIiXEE"  # @BotFather dan oling

    app = Application.builder().token(TOKEN).build()

    # Handler'larni qo'shish
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot ishga tushdi... ✅")
    app.run_polling()


if __name__ == "__main__":
    main()
