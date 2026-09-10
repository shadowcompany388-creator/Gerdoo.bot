import asyncio
import json
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

BOT_TOKEN = "8802997290:AAHoyFMjxplWtGjVDmJGUzY1nf6lQEtR_hA"
ADMIN_GROUP_ID = -1004452412169
WEBAPP_URL = "https://quiet-scone-893311.netlify.app/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📝 ثبت‌نام در آکادمی گردو", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True
    )
    await message.answer("سلام! 👋\nبرای ثبت‌نام روی دکمه زیر بزن:", reply_markup=kb)

@dp.message(F.web_app_data)
async def webapp_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)

        text = (
            "🆕 ثبت‌نام جدید\n\n"
            f"👤 نام: {data.get('firstName', '')} {data.get('lastName', '')}\n"
            f"🆔 کد ملی: {data.get('nationalId', '')}\n"
            f"📅 تولد: {data.get('birthDate', '')}\n"
            f"⚧ جنسیت: {data.get('gender', '')}\n"
            f"📱 موبایل: {data.get('mobile', '')}\n"
            f"📧 ایمیل: {data.get('email', 'ندارد')}\n"
            f"👨‍👩‍👧 والد: {data.get('parentName', 'ندارد')}\n"
            f"📞 موبایل والد: {data.get('parentMobile', '')}\n"
            f"🎓 مقطع: {data.get('education', '')}\n"
            f"📚 دوره: {data.get('course', '')}\n"
            f"📊 سطح: {data.get('level', '')}\n"
            f"📝 توضیحات: {data.get('notes', 'ندارد')}\n\n"
            f"کاربر: @{message.from_user.username or 'ندارد'}\n"
            f"آیدی: {message.from_user.id}"
        )

        await bot.send_message(ADMIN_GROUP_ID, text)
        await message.answer("✅ ثبت‌نام شما با موفقیت انجام شد و برای رئسا ارسال گردید.")

    except Exception as e:
        await message.answer("خطا در پردازش فرم. دوباره تلاش کنید.")
        print("ERROR:", e)

async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())