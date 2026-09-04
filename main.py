import logging
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# إعداد السجلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = "8743057533:AAH8vVWILiPHBm4r2Vjp0vdAGkn4gh_KioM"
WEB_APP_URL = "https://boodym445-rgb.github.io/maxi-doge-app/"
ADMIN_USERNAME = "boodymelpnna"

# --- إعداد قاعدة البيانات (SQLite) ---
def init_db():
    conn = sqlite3.connect("maxi_doge.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            balance INTEGER DEFAULT 0,
            energy INTEGER DEFAULT 1000,
            referred_by INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# تسجيل أو جلب المستخدم من قاعدة البيانات
def get_or_create_user(user_id, first_name, username, referred_by=None):
    conn = sqlite3.connect("maxi_doge.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.execute(
            "INSERT INTO users (user_id, first_name, username, balance, energy, referred_by) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, first_name, username, 0, 1000, referred_by)
        )
        conn.commit()
        # إضافة مكافأة إحالة للشخص الذي دعاه
        if referred_by:
            cursor.execute("UPDATE users SET balance = balance + 1000 WHERE user_id = ?", (referred_by,))
            conn.commit()
            
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.effective_user
    args = context.args
    referred_by = int(args[0]) if args and args[0].isdigit() else None

    # حفظ المستخدم في قاعدة البيانات فوراً
    get_or_create_user(user_data.id, user_data.first_name, user_data.username, referred_by)

    keyboard = [
        [InlineKeyboardButton("🚀 فتح تطبيق التعدين والمهام (Web App)", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_msg = (
        f"مرحباً بك يا {user_data.first_name} في بوت **Maxi Doge ($MAXI)**! 🪙\n\n"
        f"⚡ اضغط على الزر أدناه لدخول تطبيق التعدين، إكمال المهام، وتدوير عجلة الحظ.\n"
        f"📈 سعر الإدراج المتوقع للعملة: **$0.09**"
    )

    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("🚀 البوت وقاعدة البيانات يعملان بنجاح...")
    app.run_polling()
