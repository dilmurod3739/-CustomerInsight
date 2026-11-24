import { useEffect, useState } from 'react';
import { Table2, Search, ChevronLeft, ChevronRight, CheckCircle2, XCircle } from 'lucide-react';

export const DataTable: React.FC = () => {
  const [data, setData] = useState<any[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [offset, setOffset] = useState<number>(0);
  const [limit] = useState<number>(15);
  const [filterChurn, setFilterChurn] = useState<string>('');
  const [search, setSearch] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  const fetchData = () => {
    setLoading(true);
    let url = `/api/v1/dataset/sample?limit=${limit}&offset=${offset}`;
    if (filterChurn) {
      url += `&churn=${filterChurn}`;
    }
    fetch(url)
      .then((res) => res.json())
      .then((resData) => {
        setData(resData.data || []);
        setTotal(resData.total || 0);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
  }, [offset, filterChurn]);

  const filteredData = search
    ? data.filter((row) => String(row.customerID).toLowerCase().includes(search.toLowerCase()))
    : data;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
      {/* Table Header Controls */}
      <div className="p-5 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center">
            <Table2 className="w-5 h-5 mr-2 text-indigo-600" /> Mijozlar Dataseti (Telco Churn)
          </h2>
          <p className="text-xs text-slate-500">Jami yozuvlar soni: {total.toLocaleString()} ta</p>
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto">
          {/* Search box */}
          <div className="relative flex-1 sm:w-48">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="CustomerID qidirish..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs w-full focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          {/* Filter */}
          <select
            value={filterChurn}
            onChange={(e) => {
              setFilterChurn(e.target.value);
              setOffset(0);
            }}
            className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs font-medium text-slate-700 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          >
            <option value="">Barchasi (Hammasi)</option>
            <option value="Yes">Ketganlar (Churn: Yes)</option>
            <option value="No">Qolganlar (Churn: No)</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50 text-slate-500 font-semibold border-b border-slate-200 uppercase tracking-wider">
            <tr>
              <th className="py-3 px-4">Customer ID</th>
              <th className="py-3 px-4">Jinsi / Yosh</th>
              <th className="py-3 px-4">Muddat (Tenure)</th>
              <th className="py-3 px-4">Shartnoma</th>
              <th className="py-3 px-4">Internet</th>
              <th className="py-3 px-4">Oylik To‘lov</th>
              <th className="py-3 px-4">Jami To‘lov</th>
              <th className="py-3 px-4 text-center">Churn Holati</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading ? (
              <tr>
                <td colSpan={8} className="py-12 text-center text-slate-400">
                  Yuklanmoqda...
                </td>
              </tr>
            ) : filteredData.length === 0 ? (
              <tr>
                <td colSpan={8} className="py-12 text-center text-slate-400">
                  Mos yozuvlar topilmadi
                </td>
              </tr>
            ) : (
              filteredData.map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-50 transition-colors">
                  <td className="py-3 px-4 font-mono font-medium text-slate-800">{row.customerID}</td>
                  <td className="py-3 px-4 text-slate-600">
                    {row.gender}, {row.SeniorCitizen === 1 ? 'Senior' : 'Adult'}
                  </td>
                  <td className="py-3 px-4 font-medium text-slate-700">{row.tenure} oy</td>
                  <td className="py-3 px-4 text-slate-600">{row.Contract}</td>
                  <td className="py-3 px-4 text-slate-600">{row.InternetService}</td>
                  <td className="py-3 px-4 font-semibold text-slate-900">${row.MonthlyCharges}</td>
                  <td className="py-3 px-4 text-slate-600">${row.TotalCharges}</td>
                  <td className="py-3 px-4 text-center">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                        row.Churn === 'Yes'
                          ? 'bg-rose-100 text-rose-700'
                          : 'bg-emerald-100 text-emerald-700'
                      }`}
                    >
                      {row.Churn === 'Yes' ? (
                        <>
                          <XCircle className="w-3 h-3 mr-1" /> Ketgan
                        </>
                      ) : (
                        <>
                          <CheckCircle2 className="w-3 h-3 mr-1" /> Faol
                        </>
                      )}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div className="p-4 border-t border-slate-200 flex justify-between items-center text-xs text-slate-500">
        <span>
          Ko‘rsatilmoqda: {offset + 1} – {Math.min(offset + limit, total)} (Jami: {total})
        </span>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setOffset(Math.max(0, offset - limit))}
            disabled={offset === 0 || loading}
            className="p-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 disabled:opacity-40 cursor-pointer"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="font-semibold text-slate-700 px-2">
            {Math.floor(offset / limit) + 1} / {Math.ceil(total / limit) || 1}
          </span>
          <button
            onClick={() => setOffset(offset + limit)}
            disabled={offset + limit >= total || loading}
            className="p-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 disabled:opacity-40 cursor-pointer"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
