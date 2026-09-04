import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# إعداد السجلات لتتبع العمليات في الـ CMD
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN_NAME = "Maxi Doge ($MAXI)"
BOT_TOKEN = "8743057533:AAH8vVWILiPHBm4r2Vjp0vdAGkn4gh_KioM"

# ضع هنا رابط موقعك المرفوع على GitHub Pages
WEB_APP_URL = "https://YOUR-USERNAME.github.io/maxi-doge-app/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name

    # إنشاء زر يفتح التطبيق التفاعلي (Web App)
    keyboard = [
        [InlineKeyboardButton("🚀 فتح تطبيق التعدين (Web App)", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = (
        f"مرحباً بك يا {user_first_name} في تطبيق تعدين **{TOKEN_NAME}**! 🚀\n\n"
        f"اضغط على الزر أدناه لفتح واجهة التعدين التفاعلية وابدأ بجمع العملات قبل موعد الإدراج في أواخر 2026."
    )
    
    await update.message.reply_text(caption, reply_markup=reply_markup, parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("🚀 البوت يعمل الآن بنجاح عبر الـ CMD...")
    app.run_polling()
