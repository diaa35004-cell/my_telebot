import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

TOKEN = "8355553542:AAGaJQqMDrNzhkgwk3xFXWuNvCqFOgRI--w"
ADMIN_ID = 7717740661  # حط هنا الايدي بتاعك

# إنشاء قاعدة البيانات
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT
)
""")
conn.commit()

def start(update: Update, context):
    user = update.effective_user

    # تسجيل المستخدم في قاعدة البيانات
    cursor.execute("INSERT OR IGNORE INTO users (id, username, first_name) VALUES (?, ?, ?)",
                   (user.id, user.username, user.first_name))
    conn.commit()

    keyboard = [
        [InlineKeyboardButton("👑 اضغط هنا", callback_data='button_click')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("مرحبًا بك في البوت ✅", reply_markup=reply_markup)

def button(update: Update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="تم الضغط 👌")

def show_users(update: Update, context):
    if update.effective_user.id == ADMIN_ID:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        if not users:
            update.message.reply_text("لا يوجد مستخدمين بعد 😅")
        else:
            text = "\n".join([f"{u[2]} (@{u[1]}) - {u[0]}" for u in users])
            update.message.reply_text(f"📋 قائمة المستخدمين:\n{text}")
    else:
        update.message.reply_text("❌ ليس لديك صلاحية للوصول")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("users", show_users))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
