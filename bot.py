import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# قراءة المفاتيح بأمان من متغيرات البيئة في الاستضافة
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# تهيئة عميل OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    chat_id = update.message.chat_id

    # إرسال رسالة بأن البوت جاري العمل على رسم الصورة
    await context.bot.send_message(chat_id=chat_id, text="🎨 جاري توليد الصورة باستخدام DALL-E 3، انتظر قليلاً...")

    try:
        # طلب توليد الصورة من OpenAI
        response = client.images.generate(
            model="dall-e-3",
            prompt=user_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url

        # إرسال الصورة مباشرة للمستخدم في تيليجرام
        await context.bot.send_photo(chat_id=chat_id, photo=image_url, caption=f"✨ النتيجة لوصفك: {user_prompt}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"❌ حدث خطأ أثناء توليد الصورة: {e}")

def main():
    if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
        print("خطأ: يرجى التأكد من ضبط متغيرات البيئة للتوكن ومفتاح OpenAI.")
        return

    # بناء وتشغيل البوت
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # استقبال أي رسالة نصية كأمر لتوليد الصورة
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 البوت يعمل الآن...")
    application.run_polling()

if __name__ == "__main__":
    main()
