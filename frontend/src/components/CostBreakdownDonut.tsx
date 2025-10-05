"use client";

import dynamic from "next/dynamic";
import type { PredictResponse } from "@/lib/api";
import { useMemo } from "react";

const Plot = dynamic(async () => {
  const Plotly = await import("plotly.js-basic-dist-min");
  const createPlotlyComponent = (await import("react-plotly.js/factory")).default;
  return createPlotlyComponent(Plotly);
}, { ssr: false });

export default function CostBreakdownDonut({
  analysis,
  platformFeeBdt = 0,
}: {
  analysis: PredictResponse;
  platformFeeBdt?: number;
}) {
  const breakdown = analysis.bangladesh_duties_bdt;
  const local = analysis.local_costs_bdt;
  const values = useMemo(
    () => [
      breakdown.cif_value,
      breakdown.customs_duty,
      breakdown.supplementary_duty,
      breakdown.vat,
      breakdown.advance_tax,
      breakdown.ait,
      breakdown.regulatory_duty,
      breakdown.environmental_surcharge,
      local.clearing_agent_fee,
      local.brta_registration,
      platformFeeBdt,
    ],
    [analysis, platformFeeBdt]
  );

  const labels = [
    "CIF Value",
    "Customs Duty",
    "Supplementary Duty",
    "VAT (15%)",
    "Advance Tax",
    "AIT",
    "Regulatory Duty",
    "Environmental",
    "Clearing Agent",
    "BRTA Registration",
    "Platform Fee",
  ];

  const P: any = Plot as any;
  return (
    <div className="w-full">
      <P
        data={[
          {
            type: "pie",
            hole: 0.5,
            values,
            labels,
            textinfo: "label+percent",
            textposition: "outside",
            marker: {
              colors: [
                "#3b82f6",
                "#8b5cf6",
                "#ec4899",
                "#f59e0b",
                "#10b981",
                "#06b6d4",
                "#6366f1",
                "#84cc16",
                "#f97316",
                "#14b8a6",
              ],
            },
            hovertemplate:
              "<b>%{label}</b><br>৳%{value:,.0f}<br>%{percent}<extra></extra>",
          } as any,
        ]}
        layout={{
          paper_bgcolor: "rgba(0,0,0,0)",
          plot_bgcolor: "rgba(0,0,0,0)",
          font: { color: "#cbd5e1" },
          showlegend: false,
          margin: { t: 10, b: 10, l: 10, r: 10 },
          annotations: [
            {
              text: `৳${(analysis.total_landed_cost_bdt + (platformFeeBdt || 0)).toLocaleString()}`,
              showarrow: false,
              x: 0.5,
              y: 0.5,
              font: { size: 18, color: "#3b82f6" },
            },
          ],
        }}
        config={{ displayModeBar: false }}
        useResizeHandler
        style={{ width: "100%", height: 400 }}
      />
    </div>
  );
}
