export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8001";

export type VehicleInput = {
  make: string;
  model: string;
  year: number;
  mileage_km: number;
  engine_cc: number;
  auction_grade: number;
  user_bid_jpy?: number | null;
};

export type PredictResponse = {
  predicted_winning_bid_jpy: number;
  user_bid_jpy: number | null;
  bid_used_for_calculation: number;
  currency_conversion: { jpy_to_bdt_rate: number; [k: string]: any };
  japan_costs_jpy: Record<string, number>;
  bangladesh_duties_bdt: Record<string, number>;
  local_costs_bdt: Record<string, number>;
  total_landed_cost_bdt: number;
  total_landed_cost_usd: number;
  duty_percentage: number;
  // Optional fields (after backend update)
  q20_jpy?: number;
  q50_jpy?: number;
  q80_jpy?: number;
  recommended_bid_jpy?: number;
  platform_fee_bdt?: number;
  total_incl_platform_bdt?: number;
};

export async function analyzeVehicle(input: VehicleInput, targetWinProb?: number): Promise<PredictResponse> {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...input, ...(targetWinProb ? { target_win_prob: targetWinProb } : {}) }),
    cache: "no-store",
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return (await res.json()) as PredictResponse;
}
