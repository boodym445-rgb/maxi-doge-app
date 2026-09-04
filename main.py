import sqlite3
import random
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعداد التسجيل (Logging)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# التوكن والربط
TOKEN = "8743057533:AAHU2_LzpD2fr27fN0MhxgZT2HGsOk4fRPM"
WEB_APP_URL = "https://boodym445-rgb.github.io/maxi-doge-app/"

# إعداد قاعدة البيانات SQLite بتصميم احترافي وآمن
def init_db():
    conn = sqlite3.connect("maxi_doge.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance INTEGER DEFAULT 0,
            energy INTEGER DEFAULT 1000
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_or_create_user(user_id, username):
    conn = sqlite3.connect("maxi_doge.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance, energy FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    
    if not row:
        cursor.execute("INSERT INTO users (user_id, username, balance, energy) VALUES (?, ?, 0, 1000)", (user_id, username))
        conn.commit()
        balance, energy = 0, 1000
    else:
        balance, energy = row
        
    conn.close()
    return balance, energy

def update_user_balance(user_id, amount):
    conn = sqlite3.connect("maxi_doge.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    new_balance = cursor.fetchone()[0]
    conn.close()
    return new_balance

# أمر البدء بتصميم واجهة احترافية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    balance, energy = get_or_create_user(user.id, user.username or user.first_name)
    
    # واجهة أزرار احترافية ومنسقة
    keyboard = [
        [InlineKeyboardButton("🚀 إطلاق تطبيق Maxi Doge Mini App", web_app=WebAppInfo(url=WEB_APP_URL))],
        [
            InlineKeyboardButton("🎡 عجلة الحظ", callback_data="spin_wheel"),
            InlineKeyboardButton("💼 حسابي والرصيد", callback_data="profile")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"🌟 **مرحباً بك يا {user.first_name} في عالم Maxi Doge!** 🐾\n\n"
        f"💎 المنصة الرسمية لتعدين وكسب عملات **$MAXI**.\n"
        f"🎯 **هدف الإدراج:** $0.09\n\n"
        f"📊 **حسابك الحالي:**\n"
        f"• الرصيد: `{balance:,} $MAXI`\n"
        f"• الطاقة: `{energy} / 1000` ⚡\n\n"
        f"اختر أحد الخيارات أدناه للبدء في ربح العملات فوراً 👇"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# لوحة عرض الملف الشخصي
async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    balance, energy = get_or_create_user(user.id, user.username or user.first_name)
    
    profile_text = (
        f"👤 **لوحة بيانات المستخدم الاحترافية**\n\n"
        f"🆔 المعرف: `{user.id}`\n"
        f"💰 إجمالي الأرباح: `{balance:,} $MAXI`\n"
        f"⚡ الطاقة المتاحة: `{energy} / 1000`\n\n"
        f"استمر في التعدين عبر التطبيق أو تدوير العجلة لزيادة أرباحك!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🚀 فتح التطبيق", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(profile_text, reply_markup=reply_markup, parse_mode="Markdown")

# العودة للقائمة الرئيسية
async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    balance, energy = get_or_create_user(user.id, user.username or user.first_name)
    
    keyboard = [
        [InlineKeyboardButton("🚀 إطلاق تطبيق Maxi Doge Mini App", web_app=WebAppInfo(url=WEB_APP_URL))],
        [
            InlineKeyboardButton("🎡 عجلة الحظ", callback_data="spin_wheel"),
            InlineKeyboardButton("💼 حسابي والرصيد", callback_data="profile")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    menu_text = (
        f"🌟 **القائمة الرئيسية - Maxi Doge** 🐾\n\n"
        f"📊 رصيدك الحالي: `{balance:,} $MAXI`\n"
        f"اختر ما يناسبك أدناه 👇"
    )
    await query.edit_message_text(menu_text, reply_markup=reply_markup, parse_mode="Markdown")

# التعامل مع الأزرار وتدوير عجلة الحظ مع تأثير حركي
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    if query.data == "profile":
        await profile_handler(update, context)
        return
    elif query.data == "main_menu":
        await main_menu_handler(update, context)
        return
        
    if query.data == "spin_wheel":
        # تأثير حركة تشويقية لتوريد عجلة الحظ
        spin_steps = [
            "🎡 ⟨ 🔄 جاري تدوير عجلة الحظ... ⟩",
            "🎡 ⟨ ⚡ العجلة تدور بسرعة فائقة... ⟩",
            "🎡 ⟨ 🎯 اقتربت العجلة من الاستقرار... ⟩"
        ]
        
        for step in spin_steps:
            try:
                await query.edit_message_text(text=step)
                await asyncio.sleep(0.7)
            except Exception:
                pass

        # جوائز العجلة
        prizes = [
            {"text": "🎉 مبروك! فزت بـ 100 عملة $MAXI", "amount": 100},
            {"text": "🎁 رائع! فزت بـ 500 عملة $MAXI", "amount": 500},
            {"text": "🔥 مميز! فزت بـ 1,000 عملة $MAXI", "amount": 1000},
            {"text": "💎 الجائزة الكبرى! فزت بـ 5,000 عملة $MAXI", "amount": 5000}
        ]
        weights = [48, 48, 2, 2]
        
        won_prize = random.choices(prizes, weights=weights, k=1)[0]
        new_balance = update_user_balance(user.id, won_prize["amount"])
        
        result_text = (
            f"✨ **نتيجة عجلة الحظ الاحترافية** ✨\n\n"
            f"{won_prize['text']}\n\n"
            f"💰 رصيدك الإجمالي المحدث: `{new_balance:,} $MAXI`"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔄 تدوير مرة أخرى", callback_data="spin_wheel")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Professional Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
