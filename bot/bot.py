import os
import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api/v1")

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "👋 **Assalomu alaykum! CustomerInsight AI Botiga xush kelibsiz.**\n\n"
        "📊 Ushbu bot mijozlar xatti-harakati va ketish xavfini (Customer Churn) "
        "monitoring qilish hamda yuqori xavfli mijozlar bo'yicha tezkor ogohlantirish berish uchun mo'ljallangan.\n\n"
        "**Asosiy buyruqlar:**\n"
        "🔹 /link <code> — Web profilingiz bilan bog'lash\n"
        "🔹 /stats — Umumiy mijozlar va churn statistikasi\n"
        "🔹 /metrics — ML modelning aniqlik metrikalari\n"
        "🔹 /alerts — Xavfi yuqori bo'lgan mijozlar ro'yxati\n"
        "🔹 /predict — Yangi mijoz xavfini sinab ko'rish\n"
        "🔹 /help — Yordam va ko'rsatmalar"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistikani ko'rish", callback_data="btn_stats")],
        [InlineKeyboardButton(text="⚠️ Churn Alerts", callback_data="btn_alerts")]
    ])
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=kb)

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "💡 **CustomerInsight Bot Yo'riqnomasi:**\n\n"
        "1. Web platformadagi profilingizdan olingan 8 xonali kod orqali profilingizni botga ulang: `/link ABC12345`\n"
        "2. Tizim Churn xavfi 65% dan yuqori bo'lgan mijozlar aniqlanganda sizga darhol xabar jo'natadi.\n"
        "3. Istalgan vaqtda /stats orqali umumiy metrikalarni kuzatishingiz mumkin."
    )
    await message.answer(help_text, parse_mode="Markdown")

@dp.message(Command("link"))
async def cmd_link(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ Iltimos, ulanish kodini kiriting. Masalan: `/link A1B2C3D4`", parse_mode="Markdown")
        return

    code = args[1].strip().upper()
    chat_id = str(message.chat.id)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/bot/verify-code", params={"code": code, "telegram_chat_id": chat_id}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    await message.answer(f"✅ Muvaffaqiyatli bog'landi! Xush kelibsiz, **{data.get('username', 'Analyst')}**.", parse_mode="Markdown")
                else:
                    await message.answer("❌ Xatolik: Kod yaroqsiz yoki muddati o'tgan.")
        except Exception as e:
            await message.answer(f"⚠️ API bilan bog'lanishda xatolik: {e}")

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_BASE_URL}/dataset/summary") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    text = (
                        "📈 **Mijozlar Bazasi Statistikasi:**\n\n"
                        f"👥 Jami mijozlar: **{data['total_customers']}** ta\n"
                        f"🟢 Faol mijozlar: **{data['active_customers']}** ta\n"
                        f"🔴 Xizmatdan ketgan (Churned): **{data['churned_customers']}** ta\n"
                        f"📉 Churn foizi: **{data['churn_rate']}%**\n"
                        f"💵 O'rtacha oylik to'lov: **${data['avg_monthly_charges']}**\n"
                        f"⏳ O'rtacha mijozlik muddati: **{data['avg_tenure']} oy**\n"
                    )
                    await message.answer(text, parse_mode="Markdown")
                else:
                    await message.answer("❌ Statistikani yuklab bo'lmadi.")
        except Exception as e:
            await message.answer(f"⚠️ API bilan bog'lanishda xatolik: {e}")

@dp.message(Command("metrics"))
async def cmd_metrics(message: types.Message):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_BASE_URL}/predict/metrics") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    text = (
                        f"🧠 **ML Model Natijalari ({data['model_name']}):**\n\n"
                        f"🎯 Aniqlik (Accuracy): **{data['accuracy'] * 100:.1f}%**\n"
                        f"🔍 Precision: **{data['precision'] * 100:.1f}%**\n"
                        f"📡 Recall: **{data['recall'] * 100:.1f}%**\n"
                        f"⚖️ F1-Score: **{data['f1_score'] * 100:.1f}%**\n"
                        f"📊 ROC-AUC: **{data['roc_auc'] * 100:.1f}%**\n\n"
                        f"📦 O'qitish namunalari: {data['train_samples']} ta | Test: {data['test_samples']} ta"
                    )
                    await message.answer(text, parse_mode="Markdown")
                else:
                    await message.answer("❌ Metrikalarni yuklab bo'lmadi.")
        except Exception as e:
            await message.answer(f"⚠️ Xatolik: {e}")

@dp.message(Command("alerts"))
async def cmd_alerts(message: types.Message):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_BASE_URL}/predict/history?limit=10") as resp:
                if resp.status == 200:
                    records = await resp.json()
                    high_risk = [r for r in records if r.get("risk_level") == "High"]
                    if not high_risk:
                        await message.answer("✅ Hozirda oxirgi tahlillarda yuqori xavfli mijozlar aniqlanmagan.")
                        return

                    text = "🚨 **DIQQAT: Churn Xavfi Yuqori Bo'lgan Mijozlar:**\n\n"
                    for r in high_risk[:5]:
                        text += (
                            f"👤 **Mijoz ID:** `{r['customer_id']}`\n"
                            f"⚠️ Xavf: **{round(r['churn_risk_score'] * 100, 1)}%** ({r['risk_level']})\n"
                            f"📋 Shartnoma: {r['contract']} | Oylik: ${r['monthly_charges']}\n"
                            f"-----------------------------\n"
                        )
                    await message.answer(text, parse_mode="Markdown")
                else:
                    await message.answer("❌ Tahlillar tarixini yuklab bo'lmadi.")
        except Exception as e:
            await message.answer(f"⚠️ Xatolik: {e}")

@dp.callback_query(lambda c: c.data == "btn_stats")
async def cb_stats(callback: types.CallbackQuery):
    await callback.answer()
    await cmd_stats(callback.message)

@dp.callback_query(lambda c: c.data == "btn_alerts")
async def cb_alerts(callback: types.CallbackQuery):
    await callback.answer()
    await cmd_alerts(callback.message)

async def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN kiritilmagan. Botni ishga tushirish uchun token kiriting.")
        return
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
