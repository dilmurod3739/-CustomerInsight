# CustomerInsight — Mijozlar Xatti-Harakati va Churn Tahlili Platformasi

> **Universitet 4-amaliy topshirig‘i:** Datasetlar bilan ishlash bo‘yicha IT loyiha (Frontend • Backend • Database • Dataset • Machine Learning • Telegram Bot).

---

## 📌 1. Loyiha haqida va Maqsad

**CustomerInsight** — telekommunikatsiya kompaniyasi mijozlarining xizmatdan ketish xavfini (**Customer Churn**) o‘rganish, mijozlar xatti-harakatlarini segmentlash hamda Machine Learning yordamida ketish ehtimolini oldindan bashorat qiluvchi to‘liq sikldagi (Full-Stack) tahliliy tizim.

Biznesda mavjud mijozni saqlab qolish yangi mijoz jalb qilishdan 5–7 barobar arzon tushadi. Ushbu platforma qaysi mijozlar xavf ostida ekanini aniqlab, ularga mos saqlab qolish choralarini (retention strategies) tavsiya qiladi.

---

## 🏗️ 2. Loyiha Arxitekturasi va Texnologik Stack

Loyihada quyidagi zamonaviy texnologik asos tanlangan:

* **Frontend:** React 19, TypeScript, Tailwind CSS v4, Lucide Icons, Vite
* **Backend:** Python 3.15, FastAPI (Asinxron REST API), Pydantic v2
* **Data Science & ML:** Pandas, NumPy, Scikit-learn, Joblib
* **Database:** SQLAlchemy ORM (standart holatda SQLite, osonlik bilan PostgreSQL ga o‘tish imkoni)
* **Telegram Bot:** Python, Aiogram 3 (Asinxron Telegram bot)
* **Xavfsizlik:** JWT tokenlar, parollarni bcrypt orqali xeshlash, CORS himoyasi, Pydantic ma'lumotlar validatsiyasi

---

## 📊 3. Dataset Tafsilotlari (Telco Customer Churn)

Tizim IBM / Kaggle ochiq manbasidagi **Telco Customer Churn** datasetidan foydalanadi (7,043 ta mijoz yozuvi):

* **Demografik belgilar:** Jinsi, yoshi (Senior Citizen), oilaviy holati (Partner, Dependents).
* **Xizmat turlari:** Telefon xizmati, bir nechta liniyalar, Internet xizmati (DSL, Fiber optic), Online Security, Tech Support, Streaming TV va Movies.
* **Shartnoma va to‘lov:** Shartnoma turi (Month-to-month, One year, Two year), To‘lov usuli (Electronic check, Mailed check, Bank transfer, Credit card), Oylik to‘lov (Monthly Charges), Jami to‘lov (Total Charges).
* **Maqsad belgisi (Target):** `Churn` (Yes — mijoz ketgan, No — mijoz qolgan).

### 🔍 Muhim Statistik Xulosalar:
1. **Shartnoma turi ta'siri:** Oylik (Month-to-month) shartnomadagi mijozlarning **42.7%** qismi ketmoqda. Uzoq muddatli (2 yillik) shartnomalarda bu ko‘rsatkich atigi **2.8%** ni tashkil etadi.
2. **Optik tola (Fiber Optic):** Optik toladan foydalanuvchilar orasida churn **41.9%** (yuqori oylik to‘lov va texnik yordam yetishmovchiligi sababli).
3. **Elektron chek:** Electronic check orqali to‘lov qiluvchilar eng beqaror segment hisoblanadi.

---

## 🧠 4. Machine Learning Modeli va Metrikalar

Mijoz ketishini bashorat qilish uchun **Random Forest Classifier (Class Balanced)** modeli tanlangan.

* **Ma'lumotlarni qayta ishlash:** 
  - Kategorik ustunlar uchun `OneHotEncoder(handle_unknown='ignore')`
  - Raqamli ustunlar uchun `StandardScaler`
  - Train/Test bo‘linishi: 80% o‘qitish, 20% testlash (Stratified)
* **Metrikalar:**
  - **Accuracy (Aniqlik):** ~79.3%
  - **Recall (Ketuvchilarni qamrab olish):** ~74.8% *(Biznesda ketayotgan mijozni o‘tkazib yubormaslik eng muhim bo‘lgani uchun Recall ustuvor)*
  - **ROC-AUC:** ~84.6%
* **Feature Importance (Eng muhim omillar):**
  1. `tenure` — Mijozning kompaniya bilan birga bo‘lgan oylari
  2. `TotalCharges` — Kompaniyaga to‘langan jami summa
  3. `MonthlyCharges` — Oylik to‘lov miqdori
  4. `Contract_Month-to-month` — Qisqa muddatli shartnoma
  5. `OnlineSecurity_No` & `TechSupport_No` — Qo‘shimcha xizmatlar yo‘qligi

---

## 🚀 5. O‘rnatish va Ishga Tushirish

### 1) Repozitoriyni tayyorlash va .env sozlash
```bash
cp .env.example .env
```

### 2) Backendni ishga tushirish (FastAPI)
```bash
# Virtual muhitni faollashtirish
.venv\Scripts\activate

# Backendni ishga tushirish
py -m uvicorn backend.main:app --reload --port 8000
```
API va Swagger interfeysi: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3) Frontendni ishga tushirish (React)
```bash
cd frontend
npm run dev
```
Web ilova: [http://localhost:5173](http://localhost:5173)

### 4) Telegram Botni ishga tushirish (Aiogram 3)
```bash
# .env fayliga TELEGRAM_BOT_TOKEN qo'yilgach:
py bot/bot.py
```

---

## 🤖 6. Telegram Bot Imkoniyatlari

* `/start` — Botni faollashtirish va asosiy boshqaruv tugmalarini ochish.
* `/link <code>` — Web platformadan olingan xavfsiz kod orqali tahlilchi profilini bog‘lash.
* `/stats` — Umumiy mijozlar soni, faol va ketgan mijozlar foizi, o‘rtacha to‘lov bo‘yicha tezkor hisobot.
* `/metrics` — ML modelining Accuracy, Precision, Recall, ROC-AUC natijalarini ko‘rish.
* `/alerts` — Tizim tomonidan aniqlangan eng yuqori xavfli (Churn risk > 65%) mijozlar ro‘yxati va ularni saqlab qolish tavsiyalari.

---

## 🛡️ 7. Muhandislik va Xavfsizlik Standartlari (AGENTS.md)

* **Parollar:** bcrypt orqali mustahkam xeshlangan.
* **Tokenlar:** HS256 algoritmli JWT (JSON Web Tokens).
* **Validatsiya:** Barcha kiruvchi parametrlar Pydantic modellari orqali tekshiriladi.
* **Secret boshqaruvi:** Hech qanday maxfiy token yoki kalit kod ichida qattiq yozilmagan (`.env` orqali o‘qiladi).
