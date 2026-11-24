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
        "👋 **Assalomu alaykum! CustomerInsight AI Telegram Botiga xush kelibsiz.**\n\n"
        "📊 Ushbu bot mijozlar xatti-harakati va ketish xavfini (Customer Churn) "
        "monitoring qilish hamda yuqori xavfli mijozlar bo'yicha mas'ul xodimlarga tezkor xabar berish uchun mo'ljallangan.\n\n"
        "**Asosiy integratsiya buyruqlari:**\n"
        "🔍 `/customer <id>` — Mijoz ID bo'yicha tahlil va Churn natijasini olish (Masalan: `/customer 7590-VHVEG`)\n"
        "🚨 `/alerts` — Churn xavfi yuqori bo'lgan mijozlar haqida mas'ul xodimga ogohlantirish\n"
        "📑 `/weekly_report` — Haftalik mijozlar segmentatsiyasi hisobotini olish\n"
        "📈 `/stats` — Umumiy mijozlar bazasi ko'rsatkichlari\n"
        "🧠 `/metrics` — ML modelining aniqlik metrikalari (Accuracy, Recall, ROC-AUC)\n"
        "🔗 `/link <code>` — Web profilingiz bilan bog'lash\n"
        "💡 `/help` — Yordam va ko'rsatmalar"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Mijozni tekshirish", callback_data="btn_check_sample")],
        [InlineKeyboardButton(text="🚨 Yuqori Xavfli Mijozlar (Alerts)", callback_data="btn_alerts")],
        [InlineKeyboardButton(text="📑 Haftalik Segmentatsiya Hisoboti", callback_data="btn_weekly")],
        [InlineKeyboardButton(text="📊 Umumiy Statistika", callback_data="btn_stats")]
    ])
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=kb)

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "💡 **CustomerInsight Bot Imkoniyatlari:**\n\n"
        "1. **Mijoz tahlili:** `/customer 7590-VHVEG` yoki istalgan mijoz ID sini yuborsangiz, model uning ketish ehtimolini hisoblab beradi.\n"
        "2. **Xavfli mijozlar signali:** `/alerts` buyrug'i orqali xavfi 65% dan yuqori bo'lgan mijozlar ro'yxati va ularni saqlab qolish choralari chiqadi.\n"
        "3. **Haftalik hisobot:** `/weekly_report` orqali shartnoma turlari va xizmatlar kesimidagi xavf taqsimoti beriladi."
    )
    await message.answer(help_text, parse_mode="Markdown")

@dp.message(Command("customer"))
async def cmd_customer(message: types.Message):
    """Mijoz identifikatori bo'yicha tahlil natijasini olish"""
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "⚠️ Iltimos, mijoz identifikatorini kiriting.\n"
            "Misol uchun: `/customer 7590-VHVEG` yoki `/customer 9237-HQITU`",
            parse_mode="Markdown"
        )
        return

    cust_id = args[1].strip()
    await analyze_and_send_customer(message, cust_id)

async def analyze_and_send_customer(message: types.Message, cust_id: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_BASE_URL}/dataset/customer/{cust_id}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    analysis = data["analysis"]
                    cust = data["customer"]

                    prob_pct = round(analysis["churn_probability"] * 100, 1)
                    risk_badge = "🔴 YUQORI (HIGH)" if analysis["risk_level"] == "High" else "🟡 O'RTA" if analysis["risk_level"] == "Medium" else "🟢 PAST (LOW)"

                    text = (
                        f"👤 **MIJOZ TAHLILI: `{analysis['customerID']}`**\n"
                        f"----------------------------------------\n"
                        f"📊 **Ketish xavfi (Churn Risk):** **{prob_pct}%**\n"
                        f"🛡️ **Xavf darajasi:** {risk_badge}\n"
                        f"🎯 **Model qarori:** **{analysis['churn_prediction']}** ({'Xizmatdan ketishi kutilmoqda' if analysis['churn_prediction'] == 'Yes' else 'Xizmatda qoladi'})\n\n"
                        f"📋 **Mijoz parametrlari:**\n"
                        f"• Shartnoma: {cust.get('Contract')}\n"
                        f"• Internet: {cust.get('InternetService')}\n"
                        f"• Oylik to'lov: ${cust.get('MonthlyCharges')}\n"
                        f"• Mijozlik davri: {cust.get('tenure')} oy\n"
                        f"• To'lov usuli: {cust.get('PaymentMethod')}\n\n"
                        f"⚠️ **Aniqlangan asosiy omillar:**\n"
                    )
                    for factor in analysis["key_factors"]:
                        text += f"• {factor}\n"

                    text += f"\n💡 **Mas'ul xodim uchun tavsiyalar:**\n"
                    for rec in analysis["retention_recommendations"]:
                        text += f"✅ {rec}\n"

                    await message.answer(text, parse_mode="Markdown")
                elif resp.status == 404:
                    await message.answer(f"❌ Kechirasiz, `{cust_id}` identifikatorli mijoz datasetda topilmadi.", parse_mode="Markdown")
                else:
                    await message.answer("❌ Serverda xatolik yuz berdi.")
        except Exception as e:
            await message.answer(f"⚠️ API bilan bog'lanishda xatolik: {e}")

@dp.message(Command("alerts"))
async def cmd_alerts(message: types.Message):
    """Churn xavfi yuqori bo'lgan mijozlar haqida mas'ul xodimga xabar berish"""
    async with aiohttp.ClientSession() as session:
        try:
            # Namuna uchun datasetdan yuqori xavfli mijozlarni olamiz
            async with session.get(f"{API_BASE_URL}/dataset/sample?limit=10&churn=Yes") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    customers = data.get("data", [])

                    text = (
                        "🚨 **DIQQAT: Churn Xavfi Yuqori Bo'lgan Mijozlar Monitoringi**\n"
                        "Mas'ul xodim (Menejer) uchun tezkor xabarnoma:\n"
                        "----------------------------------------\n\n"
                    )

                    for c in customers[:5]:
                        text += (
                            f"👤 **Mijoz ID:** `{c['customerID']}`\n"
                            f"⚠️ Holat: **Xavf darajasi: YUQORI (Churn kutilmoqda)**\n"
                            f"📄 Shartnoma: {c['Contract']} | Oylik: ${c['MonthlyCharges']}\n"
                            f"⏳ Muddat: {c['tenure']} oy | Internet: {c['InternetService']}\n"
                            f"👉 *Tavsiya:* 1 yillik shartnomaga o'tish chegirmasi taklif qiling.\n"
                            f"----------------------------------------\n"
                        )

                    text += "\n💡 *Batafsil ma'lumot olish uchun: `/customer <ID>`*"
                    await message.answer(text, parse_mode="Markdown")
                else:
                    await message.answer("❌ Ogohlantirishlar ma'lumotini yuklab bo'lmadi.")
        except Exception as e:
            await message.answer(f"⚠️ Xatolik: {e}")

@dp.message(Command("weekly_report"))
async def cmd_weekly_report(message: types.Message):
    """Haftalik mijozlar segmentatsiyasi hisobotini yuborish"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_BASE_URL}/dataset/weekly-report") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    text = (
                        "📑 **HAFTALIK MIJOZLAR SEGMENTATSIYASI HISOBOTI**\n"
                        f"📅 Davr: {data['period']}\n"
                        f"👥 Jami mijozlar bazasi: **{data['total_customers']}** ta\n"
                        f"📉 Umumiy Churn darajasi: **{data['overall_churn_rate']}%**\n"
                        "----------------------------------------\n\n"
                        "📊 **Asosiy Segmentlar Tahlili:**\n\n"
                    )

                    for seg in data["critical_segments"]:
                        text += (
                            f"🔸 **{seg['segment']}**\n"
                            f"• Mijozlar soni: {seg['customers']} ta\n"
                            f"• Churn darajasi: **{seg['churn_rate']}%** ({seg['risk_level']})\n"
                            f"• Harakat rejasi: {seg['priority_action']}\n\n"
                        )

                    text += "🎯 *Xulosa: Oylik shartnomadagi mijozlarni yillik paketlarga o'tkazish churn darajasini 30% ga kamaytiradi.*"
                    await message.answer(text, parse_mode="Markdown")
                else:
                    await message.answer("❌ Haftalik hisobotni yuklab bo'lmadi.")
        except Exception as e:
            await message.answer(f"⚠️ Xatolik: {e}")

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
                        f"🔴 Ketganlar (Churn): **{data['churned_customers']}** ta\n"
                        f"📉 Churn ko'rsatkichi: **{data['churn_rate']}%**\n"
                        f"💵 O'rtacha oylik to'lov: **${data['avg_monthly_charges']}**\n"
                        f"⏳ O'rtacha muddat: **{data['avg_tenure']} oy**\n"
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
                        f"📡 Recall (Qamrab olish): **{data['recall'] * 100:.1f}%**\n"
                        f"⚖️ F1-Score: **{data['f1_score'] * 100:.1f}%**\n"
                        f"📊 ROC-AUC: **{data['roc_auc'] * 100:.1f}%**\n\n"
                        f"📦 Train: {data['train_samples']} ta | Test: {data['test_samples']} ta\n"
                        f"⚙️ Metod: OneHotEncoding + Balanced Random Forest"
                    )
                    await message.answer(text, parse_mode="Markdown")
                else:
                    await message.answer("❌ Metrikalarni yuklab bo'lmadi.")
        except Exception as e:
            await message.answer(f"⚠️ Xatolik: {e}")

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

# Agar foydalanuvchi to'g'ridan-to'g'ri ID yuborsa
@dp.message()
async def default_handler(message: types.Message):
    text = message.text.strip()
    if text.startswith("/"):
        return
    # Agar 4-15 belgili ID kelsa, mijoz deb tekshirib ko'ramiz
    if 4 <= len(text) <= 15 and "-" in text:
        await analyze_and_send_customer(message, text)
    else:
        await message.answer(
            f"ℹ️ Mijozni tekshirish uchun uning identifikatorini yuboring. Masalan: `7590-VHVEG`\n"
            f"Barcha buyruqlar uchun: `/help`",
            parse_mode="Markdown"
        )

# Callback tugmalar
@dp.callback_query(lambda c: c.data == "btn_check_sample")
async def cb_check_sample(callback: types.CallbackQuery):
    await callback.answer()
    await analyze_and_send_customer(callback.message, "7590-VHVEG")

@dp.callback_query(lambda c: c.data == "btn_alerts")
async def cb_alerts(callback: types.CallbackQuery):
    await callback.answer()
    await cmd_alerts(callback.message)

@dp.callback_query(lambda c: c.data == "btn_weekly")
async def cb_weekly(callback: types.CallbackQuery):
    await callback.answer()
    await cmd_weekly_report(callback.message)

@dp.callback_query(lambda c: c.data == "btn_stats")
async def cb_stats(callback: types.CallbackQuery):
    await callback.answer()
    await cmd_stats(callback.message)

async def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN kiritilmagan. Botni ishga tushirish uchun .env ga token kiriting.")
        return
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
