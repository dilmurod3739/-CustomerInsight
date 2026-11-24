import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Dashboard } from './components/Dashboard';
import { PredictCalculator } from './components/PredictCalculator';
import { ModelMetricsView } from './components/ModelMetricsView';
import { DataTable } from './components/DataTable';
import { BotIntegration } from './components/BotIntegration';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'predict' && <PredictCalculator />}
        {activeTab === 'metrics' && <ModelMetricsView />}
        {activeTab === 'dataset' && <DataTable />}
        {activeTab === 'bot' && <BotIntegration />}
      </main>

      <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
        <p>CustomerInsight — 4-amaliy loyiha: Mijozlar xatti-harakatini tahlil qilish va Churn Prediction platformasi</p>
        <p className="mt-1 text-slate-400">FastAPI • Scikit-learn • React • TypeScript • Tailwind CSS • Aiogram 3</p>
      </footer>
    </div>
  );
}

export default App;
