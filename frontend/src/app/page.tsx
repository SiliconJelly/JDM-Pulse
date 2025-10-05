import AnalyticsPanel from "@/components/AnalyticsPanel";

export default function Home() {
  return (
    <main className="container mx-auto px-6 py-10">
      <header className="mb-10">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg" />
            <h1 className="text-2xl font-bold">JDM Pulse</h1>
          </div>
          <div className="text-sm text-slate-400">v1 • Fast, ML-first</div>
        </div>
        <div className="mt-10 max-w-3xl">
          <h2 className="text-4xl font-bold mb-3 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Import JDM Vehicles with Confidence
          </h2>
          <p className="text-slate-400">
            Predict winning bids with ML. Calculate landed costs down to the last Taka. No hidden fees—just data.
          </p>
        </div>
      </header>

      <AnalyticsPanel />

      <footer className="text-center text-slate-500 mt-16 border-t border-slate-800 pt-6">
        Built for speed • Plotly + Framer Motion • Python FastAPI backend
      </footer>
    </main>
  );
}
