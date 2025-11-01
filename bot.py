from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

TOKEN = "حط_هنا_توكن_البوت_بتاعك"

ADMIN_ID = 123456789  # حط هنا الـ ID بتاعك من تليجرام

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("👑 لوحة الأدمن", callback_data="admin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("أهلاً بيك في البوت 👋", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "admin":
        if query.from_user.id == ADMIN_ID:
            query.edit_message_text("✅ مرحبًا بك في لوحة الأدمن يا زعيم 👑")
        else:
            query.edit_message_text("🚫 انت مش أدمن يا نجم 😅")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    print("✅ البوت يعمل الآن")
    updater.idle()

if __name__ == "__main__":
    main()
