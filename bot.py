import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

# قراءة التوكن و الايدي من المتغيرات (من Railway)
TOKEN = os.getenv("8355553542:AAGaJQqMDrNzhkgwk3xFXWuNvCqFOgRI--w")
ADMIN_ID = int(os.getenv("7717740661", 0))

# إنشاء قاعدة البيانات (لو مش موجودة)
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

# إنشاء جدول المستخدمين
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT
)
""")
conn.commit()


# دالة /start
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
                   (user.id, user.username, user.first_name))
    conn.commit()
    update.message.reply_text("👋 أهلاً بك! تم تسجيلك في قاعدة البيانات.")


# دالة /admin
def admin(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("❌ غير مصرح لك بالدخول.")
        return

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    keyboard = [
        [InlineKeyboardButton("📊 عدد المستخدمين", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"👮‍♂️ لوحة الأدمن\nالمستخدمين المسجلين: {total_users}", reply_markup=reply_markup)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("admin", admin))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
