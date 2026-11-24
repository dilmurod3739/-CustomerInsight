import { useEffect, useState } from 'react';
import { Users, UserMinus, UserCheck, DollarSign, AlertTriangle, TrendingUp, ArrowUpRight } from 'lucide-react';
import type { DatasetSummary } from '../types';

export const Dashboard: React.FC = () => {
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/v1/dataset/summary')
      .then((res) => {
        if (!res.ok) throw new Error('Statistika yuklanmadi');
        return res.json();
      })
      .then((data) => {
        setSummary(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error || !summary) {
    return (
      <div className="p-6 bg-red-50 text-red-700 rounded-xl border border-red-200">
        <h3 className="font-semibold text-lg">Xatolik yuz berdi</h3>
        <p>{error || 'Maʼlumotlarni yuklab bo‘lmadi. Backend server ishlayotganini tekshiring.'}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Banner Alert */}
      <div className="bg-gradient-to-r from-amber-500 to-orange-500 rounded-2xl p-6 text-white shadow-lg shadow-orange-100 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-6 h-6 text-amber-100" />
            <h2 className="text-xl font-bold">Churn Xavfi Bo‘yicha Muhim Xulosa</h2>
          </div>
          <p className="mt-1 text-amber-100 max-w-2xl text-sm">
            Dataset tahlili shuni ko‘rsatadiki, **Month-to-month** shartnomasidagi mijozlarning 42.7% qismi xizmatdan ketmoqda.
            Uzoq muddatli shartnomaga o‘tgan mijozlarda bu ko‘rsatkich atigi 2.8% gacha tushadi!
          </p>
        </div>
        <span className="bg-white/20 backdrop-blur-md px-4 py-2 rounded-xl text-sm font-semibold tracking-wide border border-white/20">
          Churn Rate: {summary.churn_rate}%
        </span>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold uppercase text-slate-500 tracking-wider">Jami Mijozlar</p>
            <h3 className="text-2xl font-bold text-slate-900 mt-1">{summary.total_customers.toLocaleString()}</h3>
            <span className="text-xs text-emerald-600 font-medium flex items-center mt-1">
              <TrendingUp className="w-3.5 h-3.5 mr-1" /> To‘liq Telco Dataset
            </span>
          </div>
          <div className="p-3 bg-blue-50 text-blue-600 rounded-xl">
            <Users className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold uppercase text-slate-500 tracking-wider">Faol Mijozlar</p>
            <h3 className="text-2xl font-bold text-slate-900 mt-1">{summary.active_customers.toLocaleString()}</h3>
            <span className="text-xs text-slate-500 mt-1 block">{(100 - summary.churn_rate).toFixed(1)}% umumiy bazadan</span>
          </div>
          <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl">
            <UserCheck className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold uppercase text-slate-500 tracking-wider">Xizmatdan Ketgan (Churn)</p>
            <h3 className="text-2xl font-bold text-rose-600 mt-1">{summary.churned_customers.toLocaleString()}</h3>
            <span className="text-xs text-rose-500 font-medium flex items-center mt-1">
              <ArrowUpRight className="w-3.5 h-3.5 mr-1" /> {summary.churn_rate}% yo‘qotish
            </span>
          </div>
          <div className="p-3 bg-rose-50 text-rose-600 rounded-xl">
            <UserMinus className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold uppercase text-slate-500 tracking-wider">O‘rtacha Oylik To‘lov</p>
            <h3 className="text-2xl font-bold text-slate-900 mt-1">${summary.avg_monthly_charges}</h3>
            <span className="text-xs text-slate-500 mt-1 block">O‘rtacha muddat: {summary.avg_tenure} oy</span>
          </div>
          <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl">
            <DollarSign className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Segment Distribution Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
          <h3 className="text-base font-bold text-slate-900 mb-1">Shartnoma Turi Kesimida Churn Xavfi</h3>
          <p className="text-xs text-slate-500 mb-6">Har bir shartnoma toifasida mijozlarning ketish foizi</p>
          <div className="space-y-4">
            {Object.entries(summary.churn_by_contract).map(([contract, rate]) => (
              <div key={contract}>
                <div className="flex justify-between text-sm mb-1.5 font-medium">
                  <span className="text-slate-700">{contract}</span>
                  <span className={rate > 30 ? 'text-rose-600 font-bold' : 'text-slate-700 font-bold'}>{rate}% churn</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
                  <div
                    className={`h-3 rounded-full transition-all duration-500 ${
                      rate > 30 ? 'bg-rose-500' : rate > 10 ? 'bg-amber-500' : 'bg-emerald-500'
                    }`}
                    style={{ width: `${rate}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
          <h3 className="text-base font-bold text-slate-900 mb-1">Internet Xizmati Kesimida Churn Xavfi</h3>
          <p className="text-xs text-slate-500 mb-6">Optik tola (Fiber Optic) mijozlarida narx va sifat muammolari sababli churn yuqori</p>
          <div className="space-y-4">
            {Object.entries(summary.churn_by_internet).map(([service, rate]) => (
              <div key={service}>
                <div className="flex justify-between text-sm mb-1.5 font-medium">
                  <span className="text-slate-700">{service}</span>
                  <span className={rate > 35 ? 'text-rose-600 font-bold' : 'text-slate-700 font-bold'}>{rate}% churn</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
                  <div
                    className={`h-3 rounded-full transition-all duration-500 ${
                      rate > 35 ? 'bg-rose-500' : rate > 15 ? 'bg-amber-500' : 'bg-emerald-500'
                    }`}
                    style={{ width: `${rate}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Payment methods & Seniors */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs md:col-span-2">
          <h3 className="text-base font-bold text-slate-900 mb-1">To‘lov Usullari Taqsimoti</h3>
          <p className="text-xs text-slate-500 mb-4">Elektron chek (Electronic check) orqali to‘lov qiluvchilar eng xavfli segment hisoblanadi</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {Object.entries(summary.payment_distribution).map(([method, count]) => {
              const pct = ((count / summary.total_customers) * 100).toFixed(1);
              return (
                <div key={method} className="p-3.5 bg-slate-50 rounded-xl border border-slate-100">
                  <div className="flex justify-between items-center text-xs font-semibold text-slate-600">
                    <span className="truncate pr-2">{method}</span>
                    <span className="text-indigo-600 font-bold">{pct}%</span>
                  </div>
                  <p className="text-base font-bold text-slate-900 mt-1">{count.toLocaleString()} ta</p>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-900 mb-1">Yosh Toifasi Taʼsiri</h3>
            <p className="text-xs text-slate-500 mb-4">Katta yoshli fuqarolar (Senior Citizen) guruhidagi xavf</p>
            <div className="space-y-4">
              <div className="p-4 bg-rose-50 border border-rose-100 rounded-xl">
                <span className="text-xs font-semibold text-rose-700 uppercase tracking-wider">Senior Citizen Churn</span>
                <p className="text-2xl font-bold text-rose-700 mt-1">{summary.churn_by_senior['1'] || 41.7}%</p>
                <p className="text-xs text-rose-600 mt-1">Oddiy mijozlarga qaraganda qariyb 2 barobar yuqori</p>
              </div>
              <div className="p-4 bg-emerald-50 border border-emerald-100 rounded-xl">
                <span className="text-xs font-semibold text-emerald-700 uppercase tracking-wider">Boshqa mijozlar</span>
                <p className="text-2xl font-bold text-emerald-700 mt-1">{summary.churn_by_senior['0'] || 23.6}%</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
