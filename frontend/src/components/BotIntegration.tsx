import { useState } from 'react';
import { Bot, Send, KeyRound, MessageSquare } from 'lucide-react';

export const BotIntegration: React.FC = () => {
  const [code, setCode] = useState<string>('AGY-7489');
  const [copied, setCopied] = useState<boolean>(false);

  const generateCode = () => {
    const randomCode = 'CI-' + Math.floor(1000 + Math.random() * 9000);
    setCode(randomCode);
    setCopied(false);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(`/link ${code}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-gradient-to-tr from-blue-600 to-indigo-700 rounded-3xl p-8 text-white shadow-xl shadow-indigo-100 flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <span className="bg-white/20 text-white text-xs px-3 py-1 rounded-full font-bold uppercase tracking-wider backdrop-blur-xs">
            Aiogram 3 Integratsiyasi
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold mt-3">CustomerInsight Telegram Boti</h2>
          <p className="mt-2 text-indigo-100 text-sm max-w-xl">
            Telegram bot orqali tahlilchi va menejerlar mijozlar Churn xavfini istalgan joydan turib tekshirishlari
            va xavf 65% dan oshganda avtomatik ogohlantirish (Alert) olishlari mumkin.
          </p>
        </div>
        <div className="p-4 bg-white/10 rounded-2xl backdrop-blur-md border border-white/20 text-center">
          <Bot className="w-16 h-16 text-white mx-auto" />
          <span className="text-xs text-indigo-200 mt-2 block font-medium">@CustomerInsightAIBot</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Link Account Box */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 text-indigo-600 mb-2">
              <KeyRound className="w-5 h-5" />
              <h3 className="font-bold text-slate-900 text-base">Web Akkauntni Botga Ulash</h3>
            </div>
            <p className="text-xs text-slate-500 mb-4">
              Quyidagi bir martalik kod orqali Telegramdagi profilingizni web platforma bilan sinxronlashtiring:
            </p>

            <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-center mb-4">
              <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Sizning Ulanish Kodingiz</span>
              <p className="text-3xl font-mono font-black text-indigo-600 tracking-wider mt-1">{code}</p>
            </div>
          </div>

          <div className="space-y-2">
            <button
              onClick={copyToClipboard}
              className="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold flex items-center justify-center space-x-2 transition-all cursor-pointer"
            >
              <Send className="w-4 h-4" />
              <span>{copied ? 'Nusxa olindi!' : `"/link ${code}" buyrug‘idan nusxa olish`}</span>
            </button>
            <button
              onClick={generateCode}
              className="w-full py-2 px-4 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-semibold transition-all cursor-pointer"
            >
              Yangi kod yaratish
            </button>
          </div>
        </div>

        {/* Bot Commands Reference */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
          <div className="flex items-center space-x-2 text-indigo-600 mb-2">
            <MessageSquare className="w-5 h-5" />
            <h3 className="font-bold text-slate-900 text-base">Botning Asosiy Buyruqlari</h3>
          </div>
          <p className="text-xs text-slate-500 mb-4">Botga yuborish mumkin bo‘lgan buyruqlar ro‘yxati:</p>

          <div className="space-y-2.5 text-xs">
            <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-100 flex items-start space-x-2">
              <code className="bg-white px-2 py-0.5 rounded font-bold text-indigo-600 border border-slate-200">/start</code>
              <span className="text-slate-600">Botni ishga tushirish va asosiy menyuni ochish</span>
            </div>

            <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-100 flex items-start space-x-2">
              <code className="bg-white px-2 py-0.5 rounded font-bold text-indigo-600 border border-slate-200">/stats</code>
              <span className="text-slate-600">Umumiy mijozlar va Churn ko‘rsatkichlarini olish</span>
            </div>

            <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-100 flex items-start space-x-2">
              <code className="bg-white px-2 py-0.5 rounded font-bold text-indigo-600 border border-slate-200">/alerts</code>
              <span className="text-slate-600">Xavfi yuqori bo‘lgan mijozlar bo‘yicha tezkor signal</span>
            </div>

            <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-100 flex items-start space-x-2">
              <code className="bg-white px-2 py-0.5 rounded font-bold text-indigo-600 border border-slate-200">/metrics</code>
              <span className="text-slate-600">ML modelning Accuracy, Recall, ROC-AUC natijalarini ko‘rish</span>
            </div>

            <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-100 flex items-start space-x-2">
              <code className="bg-white px-2 py-0.5 rounded font-bold text-indigo-600 border border-slate-200">/link</code>
              <span className="text-slate-600">Web platformadagi tahlilchi profili bilan bog‘lash</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
