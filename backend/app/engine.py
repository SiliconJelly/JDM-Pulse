"""
Repurposed JDMPulseEngine for FastAPI service
Loads model and encoders from ../models (relative to this file)
"""

import os
import json
import pandas as pd
from typing import Optional, Dict

from . import schemas  # not strictly needed here, but kept for reference

import joblib

CURRENT_YEAR = 2024
MODEL_DIR = '../models'
JPY_TO_BDT = 0.72


class JDMPulseEngine:
    def __init__(self):
        model_dir = os.path.join(os.path.dirname(__file__), MODEL_DIR)
        self.model = joblib.load(os.path.join(model_dir, 'bid_predictor_model.joblib'))
        self.make_encoder = joblib.load(os.path.join(model_dir, 'make_encoder.joblib'))
        self.model_encoder = joblib.load(os.path.join(model_dir, 'model_encoder.joblib'))
        # Optional quantile models
        self.q20 = self._safe_load(os.path.join(model_dir, 'bid_predictor_q20.joblib'))
        self.q50 = self._safe_load(os.path.join(model_dir, 'bid_predictor_q50.joblib'))
        self.q80 = self._safe_load(os.path.join(model_dir, 'bid_predictor_q80.joblib'))

    def _safe_load(self, path: str):
        try:
            if os.path.exists(path):
                return joblib.load(path)
        except Exception:
            return None
        return None

    def _build_features(self, vehicle_data: dict) -> pd.DataFrame:
        vehicle_age = CURRENT_YEAR - int(vehicle_data['year'])
        if vehicle_age == 0:
            vehicle_age = 0.5
        mileage_per_year = vehicle_data['mileage_km'] / vehicle_age
        is_luxury_engine = 1 if vehicle_data['engine_cc'] >= 3000 else 0
        is_high_grade = 1 if float(vehicle_data['auction_grade']) >= 4.5 else 0

        try:
            make_encoded = self.make_encoder.transform([vehicle_data['make']])[0]
        except Exception:
            make_encoded = len(self.make_encoder.classes_) // 2
        try:
            model_encoded = self.model_encoder.transform([vehicle_data['model']])[0]
        except Exception:
            model_encoded = len(self.model_encoder.classes_) // 2

        return pd.DataFrame([{
            'vehicle_age': vehicle_age,
            'mileage_km': vehicle_data['mileage_km'],
            'engine_cc': vehicle_data['engine_cc'],
            'auction_grade': vehicle_data['auction_grade'],
            'make_encoded': make_encoded,
            'model_encoded': model_encoded,
            'mileage_per_year': mileage_per_year,
            'is_luxury_engine': is_luxury_engine,
            'is_high_grade': is_high_grade
        }])

    def predict_winning_bid(self, vehicle_data: dict) -> int:
        features = self._build_features(vehicle_data)
        prediction = self.model.predict(features)[0]
        prediction = max(500_000, min(prediction, 15_000_000))
        return int(prediction)

    def predict_quantiles(self, vehicle_data: dict) -> Dict[str, int]:
        """Return available quantiles (q20,q50,q80)."""
        features = self._build_features(vehicle_data)
        out: Dict[str, int] = {}
        if self.q20 is not None:
            out['q20'] = int(max(500_000, min(self.q20.predict(features)[0], 15_000_000)))
        if self.q50 is not None:
            out['q50'] = int(max(500_000, min(self.q50.predict(features)[0], 15_000_000)))
        if self.q80 is not None:
            out['q80'] = int(max(500_000, min(self.q80.predict(features)[0], 15_000_000)))
        return out

    def recommend_bid(self, vehicle_data: dict, target_win_prob: float = 0.7) -> int:
        q = self.predict_quantiles(vehicle_data)
        if not q:
            # Fallback to point estimate
            return self.predict_winning_bid(vehicle_data)
        p = max(0.2, min(0.8, target_win_prob))
        # Linear interpolation between known quantiles
        if p <= 0.5 and 'q20' in q and 'q50' in q:
            t = (p - 0.2) / (0.5 - 0.2)
            rec = q['q20'] + t * (q['q50'] - q['q20'])
        elif p > 0.5 and 'q50' in q and 'q80' in q:
            t = (p - 0.5) / (0.8 - 0.5)
            rec = q['q50'] + t * (q['q80'] - q['q50'])
        else:
            # If some quantiles missing, use whichever exists
            rec = q.get('q50') or q.get('q80') or q.get('q20') or self.predict_winning_bid(vehicle_data)
        rec = int(max(500_000, min(rec, 15_000_000)))
        return rec

    def calculate_landed_cost(self, winning_bid_jpy: int, vehicle_data: dict) -> dict:
        auction_fee_jpy = winning_bid_jpy * 0.05
        export_certificate_jpy = 15000
        freight_inspection_jpy = 25000
        shipping_to_bd_jpy = 150000

        total_japan_jpy = (
            winning_bid_jpy + auction_fee_jpy + export_certificate_jpy +
            freight_inspection_jpy + shipping_to_bd_jpy
        )

        cif_value_bdt = total_japan_jpy * JPY_TO_BDT

        engine_cc = vehicle_data['engine_cc']
        vehicle_age = CURRENT_YEAR - int(vehicle_data['year'])

        if engine_cc <= 1500:
            customs_duty_rate = 1.25
            supplementary_duty_rate = 0.20
        elif engine_cc <= 2000:
            customs_duty_rate = 1.50
            supplementary_duty_rate = 0.30
        elif engine_cc <= 2500:
            customs_duty_rate = 2.50
            supplementary_duty_rate = 0.35
        else:
            customs_duty_rate = 5.00
            supplementary_duty_rate = 0.45

        if vehicle_age > 5:
            customs_duty_rate += 0.50

        customs_duty = cif_value_bdt * customs_duty_rate
        assessable_value_1 = cif_value_bdt + customs_duty
        supplementary_duty = assessable_value_1 * supplementary_duty_rate
        assessable_value_2 = assessable_value_1 + supplementary_duty
        vat = assessable_value_2 * 0.15
        advance_tax = assessable_value_2 * 0.05
        ait = assessable_value_2 * 0.03
        regulatory_duty = cif_value_bdt * 0.04
        environmental_surcharge = cif_value_bdt * (0.02 if engine_cc > 2500 else 0.01)

        total_duties = (
            customs_duty + supplementary_duty + vat + advance_tax +
            ait + regulatory_duty + environmental_surcharge
        )

        clearing_agent_fee = 50000
        brta_registration = 85000
        documentation_fee = 15000
        total_local_costs = clearing_agent_fee + brta_registration + documentation_fee

        total_landed_cost_bdt = cif_value_bdt + total_duties + total_local_costs
        total_landed_cost_usd = total_landed_cost_bdt / 110

        return {
            'currency_conversion': {
                'jpy_to_bdt_rate': JPY_TO_BDT,
                'total_japan_cost_jpy': int(total_japan_jpy),
                'total_japan_cost_bdt': int(total_japan_jpy * JPY_TO_BDT)
            },
            'japan_costs_jpy': {
                'winning_bid': int(winning_bid_jpy),
                'auction_fee': int(auction_fee_jpy),
                'export_certificate': int(export_certificate_jpy),
                'freight_inspection': int(freight_inspection_jpy),
                'shipping': int(shipping_to_bd_jpy),
                'total': int(total_japan_jpy)
            },
            'bangladesh_duties_bdt': {
                'cif_value': int(cif_value_bdt),
                'customs_duty': int(customs_duty),
                'supplementary_duty': int(supplementary_duty),
                'vat': int(vat),
                'advance_tax': int(advance_tax),
                'ait': int(ait),
                'regulatory_duty': int(regulatory_duty),
                'environmental_surcharge': int(environmental_surcharge),
                'total_duties': int(total_duties)
            },
            'local_costs_bdt': {
                'clearing_agent_fee': int(clearing_agent_fee),
                'brta_registration': int(brta_registration),
                'documentation_fee': int(documentation_fee),
                'total': int(total_local_costs)
            },
            'total_landed_cost_bdt': int(total_landed_cost_bdt),
            'total_landed_cost_usd': int(total_landed_cost_usd),
            'duty_percentage': round((total_duties / cif_value_bdt) * 100, 1)
        }

    def predict_and_calculate(self, vehicle_data: dict, user_bid_jpy: Optional[int] = None) -> dict:
        predicted_bid_jpy = self.predict_winning_bid(vehicle_data)
        bid_to_use = user_bid_jpy if user_bid_jpy else predicted_bid_jpy
        result = self.calculate_landed_cost(bid_to_use, vehicle_data)
        result.update({
            'predicted_winning_bid_jpy': predicted_bid_jpy,
            'user_bid_jpy': user_bid_jpy,
            'bid_used_for_calculation': bid_to_use
        })
        return result
