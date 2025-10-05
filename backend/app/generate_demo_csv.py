"""
Generate an enriched CSV for Plotly Studio demo.
- Samples N vehicles from the dataset
- Uses JDMPulseEngine to predict winning bid and compute full landed cost breakdown
- Adds a demo platform fee and total including platform fee

Output: ../../demo/plotly_studio_demo.csv (relative to this file)
"""

import os
import sys
import argparse
import pandas as pd

# Ensure relative imports work when executing directly
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app.engine import JDMPulseEngine, JPY_TO_BDT  # type: ignore


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=500, help="Number of rows to sample")
    parser.add_argument("--platform_rate", type=float, default=0.02, help="Platform fee rate (of winning bid JPY)")
    parser.add_argument("--out", type=str, default=os.path.join(PROJECT_ROOT, 'demo', 'plotly_studio_demo.csv'))
    args = parser.parse_args()

    # Load dataset
    dataset_path = os.path.join(PROJECT_ROOT, 'data', 'jdm_pulse_dataset.parquet')
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at {dataset_path}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_parquet(dataset_path)

    if len(df) == 0:
        print("❌ Dataset is empty", file=sys.stderr)
        sys.exit(1)

    n = min(args.n, len(df))
    sample = df.sample(n=n, random_state=42).reset_index(drop=True)

    # Init engine (loads model once)
    engine = JDMPulseEngine()

    records = []
    for _, row in sample.iterrows():
        vehicle = {
            'make': row['make'],
            'model': row['model'],
            'year': int(row['year']),
            'mileage_km': int(row['mileage_km']),
            'engine_cc': int(row['engine_cc']),
            'auction_grade': float(row['auction_grade']),
        }

        # Predict quantiles and recommended bid at 70% win probability
        predicted = engine.predict_winning_bid(vehicle)
        quantiles = engine.predict_quantiles(vehicle)
        recommended = engine.recommend_bid(vehicle, target_win_prob=0.7)
        # Compute breakdown using recommended bid (proxy strategy)
        breakdown = engine.calculate_landed_cost(recommended, vehicle)

        # Platform fee (demo policy): % of winning bid (JPY) converted to BDT
        platform_fee_bdt = int(recommended * JPY_TO_BDT * args.platform_rate)
        total_incl_platform_bdt = breakdown['total_landed_cost_bdt'] + platform_fee_bdt

        # Flatten into a single record
        rec = {
            # Raw features
            'make': vehicle['make'],
            'model': vehicle['model'],
            'year': vehicle['year'],
            'mileage_km': vehicle['mileage_km'],
            'engine_cc': vehicle['engine_cc'],
            'auction_grade': vehicle['auction_grade'],
            'auction_date': row.get('auction_date', None),
            # Predictions
            'predicted_winning_bid_jpy': predicted,
            'q20_jpy': quantiles.get('q20'),
            'q50_jpy': quantiles.get('q50'),
            'q80_jpy': quantiles.get('q80'),
            'recommended_bid_jpy': recommended,
            # Currency conversion/Japan costs
            'jpy_to_bdt_rate': breakdown['currency_conversion']['jpy_to_bdt_rate'],
            'total_japan_cost_jpy': breakdown['currency_conversion']['total_japan_cost_jpy'],
            'total_japan_cost_bdt': breakdown['currency_conversion']['total_japan_cost_bdt'],
            # Duties breakdown (BDT)
            'cif_value_bdt': breakdown['bangladesh_duties_bdt']['cif_value'],
            'customs_duty_bdt': breakdown['bangladesh_duties_bdt']['customs_duty'],
            'supplementary_duty_bdt': breakdown['bangladesh_duties_bdt']['supplementary_duty'],
            'vat_bdt': breakdown['bangladesh_duties_bdt']['vat'],
            'advance_tax_bdt': breakdown['bangladesh_duties_bdt']['advance_tax'],
            'ait_bdt': breakdown['bangladesh_duties_bdt']['ait'],
            'regulatory_duty_bdt': breakdown['bangladesh_duties_bdt']['regulatory_duty'],
            'environmental_surcharge_bdt': breakdown['bangladesh_duties_bdt']['environmental_surcharge'],
            'total_duties_bdt': breakdown['bangladesh_duties_bdt']['total_duties'],
            # Local costs (BDT)
            'clearing_agent_fee_bdt': breakdown['local_costs_bdt']['clearing_agent_fee'],
            'brta_registration_bdt': breakdown['local_costs_bdt']['brta_registration'],
            'documentation_fee_bdt': breakdown['local_costs_bdt']['documentation_fee'],
            'total_local_costs_bdt': breakdown['local_costs_bdt']['total'],
            # Totals
            'total_landed_cost_bdt': breakdown['total_landed_cost_bdt'],
            'total_landed_cost_usd': breakdown['total_landed_cost_usd'],
            # Platform fee (demo) and total including platform
            'platform_fee_bdt': platform_fee_bdt,
            'total_incl_platform_bdt': total_incl_platform_bdt,
        }
        records.append(rec)

    out_dir = os.path.dirname(args.out)
    os.makedirs(out_dir, exist_ok=True)
    out_path = args.out

    pd.DataFrame(records).to_csv(out_path, index=False)
    print(f"✓ Demo CSV written: {out_path}")


if __name__ == "__main__":
    main()
