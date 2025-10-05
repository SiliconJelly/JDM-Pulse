"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useState, useRef } from "react";
import type { PredictResponse, VehicleInput } from "@/lib/api";
import { analyzeVehicle } from "@/lib/api";
import CostBreakdownDonut from "@/components/CostBreakdownDonut";

const FEATURED: VehicleInput[] = [
  {
    make: "Toyota",
    model: "Land Cruiser 300",
    year: 2022,
    mileage_km: 15000,
    engine_cc: 3500,
    auction_grade: 4.5,
  },
  {
    make: "Nissan",
    model: "GT-R R35",
    year: 2020,
    mileage_km: 25000,
    engine_cc: 3800,
    auction_grade: 4.0,
  },
  {
    make: "Lexus",
    model: "LX 600",
    year: 2023,
    mileage_km: 8000,
    engine_cc: 3500,
    auction_grade: 5.0,
  },
  {
    make: "Porsche",
    model: "911 Carrera",
    year: 2021,
    mileage_km: 12000,
    engine_cc: 3000,
    auction_grade: 4.5,
  },
];

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-slate-800/50 rounded-lg p-3">
      <div className="text-slate-400 text-sm">{label}</div>
      <div className="text-lg font-semibold">{value}</div>
    </div>
  );
}

export default function AnalyticsPanel() {
  const [selected, setSelected] = useState<VehicleInput | null>(null);
  const [analysis, setAnalysis] = useState<PredictResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [userBid, setUserBid] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [winProb, setWinProb] = useState<number>(0.7);
  const [recommendedBid, setRecommendedBid] = useState<number | null>(null);
  const debounceRef = useRef<number | null>(null);

  function heuristicRecommended(predict: number, wp: number) {
    // Until backend returns quantiles, scale ±10% from predicted between 50% and 90%
    const t = (Math.min(0.9, Math.max(0.5, wp)) - 0.5) / 0.4; // 0..1
    const scale = 0.9 + 0.2 * t; // 0.9..1.1
    return Math.round(predict * scale);
  }

  async function runAnalysis(v: VehicleInput, customBid?: number, target?: number) {
    setLoading(true);
    setError(null);
    try {
      const res = await analyzeVehicle({ ...v, user_bid_jpy: customBid ?? null }, target ?? winProb);
      setAnalysis(res);
      const basePred = res.recommended_bid_jpy ?? res.predicted_winning_bid_jpy;
      const rb = res.q50_jpy && res.q80_jpy && res.q20_jpy ? basePred : heuristicRecommended(basePred, target ?? winProb);
      setRecommendedBid(rb);
      if (!customBid) {
        setUserBid(String(res.predicted_winning_bid_jpy));
      }
    } catch (e: any) {
      setError(e.message || "Failed to analyze vehicle");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      {/* Featured Grid */}
      <div>
        <h3 className="text-2xl font-bold mb-4">Featured Live Auctions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {FEATURED.map((v, idx) => (
            <motion.button
              key={idx}
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => {
                setSelected(v);
                setAnalysis(null);
                runAnalysis(v, undefined, winProb);
              }}
              className="text-left bg-slate-900/50 border border-slate-800 rounded-xl overflow-hidden"
            >
              <div className="aspect-video bg-slate-800 flex items-center justify-center text-5xl">
                🚗
              </div>
              <div className="p-4">
                <div className="font-semibold">{v.make + " " + v.model}</div>
                <div className="text-slate-400 text-sm">
                  {v.year} • {v.engine_cc}cc
                </div>
              </div>
            </motion.button>
          ))}
        </div>
      </div>

      {/* Analytics Section */}
      <AnimatePresence>
        {selected && (
          <motion.section
            key="analytics"
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 24 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="grid grid-cols-1 lg:grid-cols-2 gap-6"
          >
            {/* Left: Prediction + Controls */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
              <h4 className="text-xl font-semibold mb-4">Predictive Analysis</h4>

              <div className="flex items-center gap-4 mb-6">
                <div className="w-16 h-16 rounded-lg bg-slate-800 flex items-center justify-center text-3xl">
                  🚗
                </div>
                <div>
                  <div className="text-lg font-semibold">
                    {selected.make} {selected.model}
                  </div>
                  <div className="text-slate-400 text-sm">
                    {selected.year} • {selected.engine_cc}cc
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 rounded-xl p-5 mb-5">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-slate-400 text-sm">ML Predicted Winning Bid</span>
                  <span className="text-xs bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full">
                    Fast inference
                  </span>
                </div>
                <div className="text-3xl font-bold text-green-400">
                  {analysis ? `¥${analysis.predicted_winning_bid_jpy.toLocaleString()}` : loading ? "..." : "-"}
                </div>
              </div>

              <div className="bg-slate-800/50 rounded-xl p-5 mb-5">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400 text-sm">Target Win Probability</span>
                  <span className="text-xs text-slate-400">{Math.round(winProb * 100)}%</span>
                </div>
                <input
                  type="range"
                  min={50}
                  max={90}
                  step={5}
                  value={Math.round(winProb * 100)}
                  onChange={(e) => {
                    const v = Number(e.target.value) / 100;
                    setWinProb(v);
                    // Debounce an API call to recompute recommended bid and breakdown from backend
                    if (debounceRef.current) window.clearTimeout(debounceRef.current);
                    debounceRef.current = window.setTimeout(() => {
                      if (selected) {
                        runAnalysis(selected, undefined, v);
                      }
                    }, 300);
                  }}
                  className="w-full accent-blue-500"
                />
                <div className="mt-3 text-slate-400 text-sm">Recommended Bid</div>
                <div className="text-3xl font-bold">
                  {recommendedBid ? `¥${recommendedBid.toLocaleString()}` : "-"}
                </div>
                <div className="mt-2">
                  <button
                    disabled={!selected || loading || !recommendedBid}
                    onClick={() => {
                      if (selected && recommendedBid) runAnalysis(selected, recommendedBid, winProb);
                    }}
                    className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded-lg font-semibold disabled:opacity-50"
                  >
                    Use Recommended Bid
                  </button>
                </div>
              </div>

              <div className="space-y-3">
                <label className="block">
                  <span className="text-sm text-slate-400">Your Bid (JPY)</span>
                  <input
                    type="number"
                    className="w-full mt-1 bg-slate-800 border border-slate-700 rounded-lg px-3 py-2"
                    value={userBid}
                    onChange={(e) => setUserBid(e.target.value)}
                    placeholder="Enter bid or use prediction"
                  />
                </label>
                <button
                  disabled={!selected || loading}
              onClick={() => {
                    const bid = Number(userBid);
                    if (!isFinite(bid) || bid < 100000) return;
                    runAnalysis(selected, bid, winProb);
                  }}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 py-3 rounded-lg font-semibold disabled:opacity-50"
                >
                  {loading ? "Calculating..." : "Calculate Landed Cost"}
                </button>
                {error && <div className="text-red-400 text-sm">{error}</div>}
              </div>
            </div>

            {/* Right: Cost Visualization */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
              <h4 className="text-xl font-semibold mb-4">Total Landed Cost</h4>

              <div className="text-center mb-4">
                <div className="text-sm text-slate-400 mb-1">Final Price (incl. platform)</div>
                <div className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                  {(() => {
                    if (!analysis) return loading ? "..." : "-";
                    const totalIncl = analysis.total_incl_platform_bdt ?? (analysis.total_landed_cost_bdt + (analysis.platform_fee_bdt || 0));
                    return `৳${totalIncl.toLocaleString()}`;
                  })()}
                </div>
                <div className="text-slate-400 text-sm">
                  Base landed: ৳{analysis ? analysis.total_landed_cost_bdt.toLocaleString() : "-"} • Platform: ৳{analysis?.platform_fee_bdt?.toLocaleString() ?? "n/a"}
                </div>
              </div>

              {analysis && (
                <CostBreakdownDonut analysis={analysis} platformFeeBdt={analysis.platform_fee_bdt || 0} />
              )}

              {analysis && (
                <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
                  <Stat label="Customs Duty" value={`৳${analysis.bangladesh_duties_bdt.customs_duty.toLocaleString()}`} />
                  <Stat label="VAT" value={`৳${analysis.bangladesh_duties_bdt.vat.toLocaleString()}`} />
                  <Stat label="Advance Tax" value={`৳${analysis.bangladesh_duties_bdt.advance_tax.toLocaleString()}`} />
                  <Stat label="AIT" value={`৳${analysis.bangladesh_duties_bdt.ait.toLocaleString()}`} />
                </div>
              )}
            </div>
          </motion.section>
        )}
      </AnimatePresence>
    </div>
  );
}
