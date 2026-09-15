import asyncio
import json
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

BOT_TOKEN = "8802997290:AAHoyFMjxplWtGjVDmJGUzY1nf6lQEtR_hA"
ADMIN_GROUP_ID = -1004452412169

# موقتاً لینک نتlify را می‌گذاریم، بعد از گرفتن دامنه Railway عوض می‌کنیم
WEBAPP_URL = "https://gerdoobot-production.up.railway.app/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def send_to_group(data: dict, user=None):
    text = f"""🆕 ثبت‌نام جدید

👤 نام: {data.get('firstName', '')} {data.get('lastName', '')}
🆔 کد ملی: {data.get('nationalId', '')}
📅 تولد: {data.get('birthDate', '')}
⚧ جنسیت: {data.get('gender', '')}
📱 موبایل: {data.get('mobile', '')}
📧 ایمیل: {data.get('email', 'ندارد')}
👨‍👩‍👧 والد: {data.get('parentName', 'ندارد')}
📞 موبایل والد: {data.get('parentMobile', '')}
🎓 مقطع: {data.get('education', '')}
📚 دوره: {data.get('course', '')}
📊 سطح: {data.get('level', '')}
📝 توضیحات: {data.get('notes', 'ندارد')}
"""
    if user:
        text += f"\nکاربر تلگرام: @{user.username or 'ندارد'}\nآیدی: {user.id}"

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": ADMIN_GROUP_ID, "text": text}
        )


@dp.message(Command("start"))
async def start(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(
            text="📝 ثبت‌نام در آکادمی گردو",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]],
        resize_keyboard=True
    )
    await message.answer(
        "سلام! 👋\nبرای ثبت‌نام روی دکمه زیر بزن:",
        reply_markup=kb
    )


@dp.message(F.web_app_data)
async def webapp_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        await send_to_group(data, message.from_user)
        await message.answer("✅ ثبت‌نام شما با موفقیت انجام شد و برای رئسا ارسال گردید.")
    except Exception as e:
        await message.answer("خطا در پردازش فرم.")
        print("ERROR webapp:", e)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(dp.start_polling(bot))
    yield
    task.cancel()
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def home():
    return FileResponse("index.html")


@app.post("/submit")
async def submit(request: Request):
    data = await request.json()
    await send_to_group(data)
    return JSONResponse({"ok": True, "message": "ثبت‌نام با موفقیت انجام شد"})
