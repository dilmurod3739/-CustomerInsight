import { useState } from 'react';
import { Calculator, CheckCircle2, ShieldAlert, Sparkles } from 'lucide-react';
import type { CustomerFeatures, PredictionResult } from '../types';

export const PredictCalculator: React.FC = () => {
  const [formData, setFormData] = useState<CustomerFeatures>({
    customerID: 'CUST-' + Math.floor(1000 + Math.random() * 9000),
    gender: 'Female',
    SeniorCitizen: 0,
    Partner: 'No',
    Dependents: 'No',
    tenure: 6,
    PhoneService: 'Yes',
    MultipleLines: 'No',
    InternetService: 'Fiber optic',
    OnlineSecurity: 'No',
    OnlineBackup: 'No',
    DeviceProtection: 'No',
    TechSupport: 'No',
    StreamingTV: 'No',
    StreamingMovies: 'No',
    Contract: 'Month-to-month',
    PaperlessBilling: 'Yes',
    PaymentMethod: 'Electronic check',
    MonthlyCharges: 75.5,
    TotalCharges: 450.0,
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch('/api/v1/predict/single', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Bashorat qilishda xatolik yuz berdi');
      }

      const data: PredictionResult = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
      {/* Form Section */}
      <div className="lg:col-span-7 bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-xs">
        <div className="flex items-center space-x-2 text-indigo-600 mb-2">
          <Calculator className="w-5 h-5" />
          <h2 className="text-lg font-bold text-slate-900">Mijoz Parametrlari Bo‘yicha Churn Kalkulyatori</h2>
        </div>
        <p className="text-xs text-slate-500 mb-6">
          Mijozning xizmat turi va shartnoma maʼlumotlarini kiriting, Machine Learning modeli uning ketish ehtimolini hisoblab beradi.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Mijoz ID</label>
              <input
                type="text"
                value={formData.customerID}
                onChange={(e) => setFormData({ ...formData, customerID: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Mijozlik Davri (Tenure): {formData.tenure} oy</label>
              <input
                type="range"
                min="0"
                max="72"
                value={formData.tenure}
                onChange={(e) => {
                  const val = Number(e.target.value);
                  setFormData({
                    ...formData,
                    tenure: val,
                    TotalCharges: Number((formData.MonthlyCharges * Math.max(1, val)).toFixed(1)),
                  });
                }}
                className="w-full accent-indigo-600 cursor-pointer mt-2"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Oylik To‘lov ($): {formData.MonthlyCharges}</label>
              <input
                type="number"
                step="0.5"
                min="18"
                max="150"
                value={formData.MonthlyCharges}
                onChange={(e) => {
                  const val = Number(e.target.value);
                  setFormData({
                    ...formData,
                    MonthlyCharges: val,
                    TotalCharges: Number((val * Math.max(1, formData.tenure)).toFixed(1)),
                  });
                }}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Shartnoma Turi</label>
              <select
                value={formData.Contract}
                onChange={(e) => setFormData({ ...formData, Contract: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              >
                <option value="Month-to-month">Month-to-month (Oylik)</option>
                <option value="One year">One year (1 yillik)</option>
                <option value="Two year">Two year (2 yillik)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Internet Xizmati</label>
              <select
                value={formData.InternetService}
                onChange={(e) => setFormData({ ...formData, InternetService: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              >
                <option value="Fiber optic">Fiber optic (Optik tola)</option>
                <option value="DSL">DSL</option>
                <option value="No">Internet xizmati yo‘q</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">To‘lov Usuli</label>
              <select
                value={formData.PaymentMethod}
                onChange={(e) => setFormData({ ...formData, PaymentMethod: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              >
                <option value="Electronic check">Electronic check (Elektron chek)</option>
                <option value="Mailed check">Mailed check (Pochta cheki)</option>
                <option value="Bank transfer (automatic)">Bank transfer (Avtomatik bank)</option>
                <option value="Credit card (automatic)">Credit card (Kredit karta)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Texnik Yordam (Tech Support)</label>
              <select
                value={formData.TechSupport}
                onChange={(e) => setFormData({ ...formData, TechSupport: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              >
                <option value="No">Yo‘q (No)</option>
                <option value="Yes">Bor (Yes)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Katta Yoshli Fuqaro (Senior)</label>
              <select
                value={formData.SeniorCitizen}
                onChange={(e) => setFormData({ ...formData, SeniorCitizen: Number(e.target.value) })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              >
                <option value={0}>Yo‘q (0)</option>
                <option value={1}>Ha (1)</option>
              </select>
            </div>
          </div>

          <div className="pt-4">
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-semibold shadow-md shadow-indigo-100 flex items-center justify-center space-x-2 transition-all cursor-pointer disabled:opacity-50"
            >
              {loading ? (
                <span>Model hisoblamoqda...</span>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  <span>Ketish Xavfini Hisoblash (Predict Churn)</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Result Section */}
      <div className="lg:col-span-5 space-y-6">
        {error && (
          <div className="p-4 bg-red-50 text-red-700 border border-red-200 rounded-xl text-sm">
            {error}
          </div>
        )}

        {result ? (
          <div className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-xs space-y-6">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Tahlil Natijasi</span>
                <h3 className="text-xl font-bold text-slate-900 mt-0.5">{result.customerID}</h3>
              </div>
              <span
                className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                  result.risk_level === 'High'
                    ? 'bg-rose-100 text-rose-700 border border-rose-200'
                    : result.risk_level === 'Medium'
                    ? 'bg-amber-100 text-amber-700 border border-amber-200'
                    : 'bg-emerald-100 text-emerald-700 border border-emerald-200'
                }`}
              >
                {result.risk_level} Risk
              </span>
            </div>

            {/* Probability Gauge Box */}
            <div
              className={`p-6 rounded-2xl text-center border ${
                result.risk_level === 'High'
                  ? 'bg-rose-50 border-rose-100 text-rose-900'
                  : result.risk_level === 'Medium'
                  ? 'bg-amber-50 border-amber-100 text-amber-900'
                  : 'bg-emerald-50 border-emerald-100 text-emerald-900'
              }`}
            >
              <p className="text-xs font-semibold uppercase tracking-wider">Ketish Ehtimoli (Churn Probability)</p>
              <h2 className="text-5xl font-black mt-2 tracking-tight">{(result.churn_probability * 100).toFixed(1)}%</h2>
              <p className="text-xs mt-2 font-medium">
                Klassifikatsiya qarori: **{result.churn_prediction === 'Yes' ? 'KETADI (Churn)' : 'QOLADI (Retain)'}**
              </p>
            </div>

            {/* Key Risk Factors */}
            <div>
              <h4 className="text-xs font-bold uppercase text-slate-700 tracking-wider mb-2 flex items-center">
                <ShieldAlert className="w-4 h-4 mr-1.5 text-rose-500" /> Aniqlangan Xavf Omili
              </h4>
              <ul className="space-y-1.5">
                {result.key_factors.map((factor, idx) => (
                  <li key={idx} className="text-xs text-slate-600 bg-slate-50 p-2 rounded-lg border border-slate-100">
                    • {factor}
                  </li>
                ))}
              </ul>
            </div>

            {/* Retention Recommendations */}
            <div>
              <h4 className="text-xs font-bold uppercase text-slate-700 tracking-wider mb-2 flex items-center">
                <CheckCircle2 className="w-4 h-4 mr-1.5 text-emerald-500" /> Tavsiya Etiladigan Harakatlar
              </h4>
              <ul className="space-y-1.5">
                {result.retention_recommendations.map((rec, idx) => (
                  <li key={idx} className="text-xs text-slate-700 bg-emerald-50/50 p-2.5 rounded-lg border border-emerald-100">
                    ✅ {rec}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ) : (
          <div className="bg-slate-50 border-2 border-dashed border-slate-200 rounded-2xl p-10 text-center flex flex-col items-center justify-center min-h-[350px]">
            <div className="p-4 bg-white rounded-full shadow-xs mb-3 text-slate-400">
              <Sparkles className="w-8 h-8" />
            </div>
            <h4 className="font-bold text-slate-700 text-base">Natijalar Bu Yerda Chiqadi</h4>
            <p className="text-xs text-slate-500 max-w-xs mt-1">
              Chap tarafdagi formani to‘ldiring va "Ketish Xavfini Hisoblash" tugmasini bosing.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
