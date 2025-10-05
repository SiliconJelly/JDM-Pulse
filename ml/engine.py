"""
JDM Pulse - Prediction Engine
Combines ML bid prediction with Bangladesh tax/cost calculations
Called by Laravel backend via CLI
"""

import joblib
import pandas as pd
import numpy as np
import json
import os
import sys

# Constants
CURRENT_YEAR = 2024
JPY_TO_BDT = 0.72  # Exchange rate (hardcoded for MVP, use live API in production)
MODEL_DIR = '../models'


class JDMPulseEngine:
    def __init__(self):
        """Initialize the prediction engine by loading models and encoders"""
        model_dir = os.path.join(os.path.dirname(__file__), MODEL_DIR)
        
        # Load ML model
        self.model = joblib.load(os.path.join(model_dir, 'bid_predictor_model.joblib'))
        
        # Load encoders
        self.make_encoder = joblib.load(os.path.join(model_dir, 'make_encoder.joblib'))
        self.model_encoder = joblib.load(os.path.join(model_dir, 'model_encoder.joblib'))
        
        print("✓ Engine initialized successfully", file=sys.stderr)
    
    def predict_winning_bid(self, vehicle_data):
        """
        Predict winning bid in JPY using ML model
        
        Args:
            vehicle_data: dict with keys: make, model, year, mileage_km, engine_cc, auction_grade
        
        Returns:
            int: Predicted winning bid in JPY
        """
        # Feature engineering (must match training exactly)
        vehicle_age = CURRENT_YEAR - vehicle_data['year']
        
        # Handle brand new cars
        if vehicle_age == 0:
            vehicle_age = 0.5  # Half year old
        
        mileage_per_year = vehicle_data['mileage_km'] / vehicle_age
        
        # Binary features
        is_luxury_engine = 1 if vehicle_data['engine_cc'] >= 3000 else 0
        is_high_grade = 1 if vehicle_data['auction_grade'] >= 4.5 else 0
        
        # Encode categoricals
        try:
            make_encoded = self.make_encoder.transform([vehicle_data['make']])[0]
        except ValueError:
            # Unknown make, use most common (Toyota = 7)
            make_encoded = 7
            print(f"⚠ Unknown make '{vehicle_data['make']}', using default", file=sys.stderr)
        
        try:
            model_encoded = self.model_encoder.transform([vehicle_data['model']])[0]
        except ValueError:
            # Unknown model, use average
            model_encoded = len(self.model_encoder.classes_) // 2
            print(f"⚠ Unknown model '{vehicle_data['model']}', using default", file=sys.stderr)
        
        # Create feature vector (must match training order)
        features = pd.DataFrame([{
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
        
        # Predict
        prediction = self.model.predict(features)[0]
        
        # Clamp to reasonable range
        prediction = max(500000, min(prediction, 15000000))
        
        return int(prediction)
    
    def calculate_landed_cost(self, winning_bid_jpy, vehicle_data):
        """
        Calculate complete landed cost in Bangladesh (BDT)
        
        Args:
            winning_bid_jpy: Winning bid amount in JPY
            vehicle_data: dict with vehicle details
        
        Returns:
            dict: Complete cost breakdown
        """
        
        # =====================================================
        # JAPAN-SIDE COSTS (in JPY)
        # =====================================================
        
        auction_fee_jpy = winning_bid_jpy * 0.05  # 5% auction house fee
        export_certificate_jpy = 15000  # ~$100 export documentation
        freight_inspection_jpy = 25000  # ~$170 pre-shipment inspection
        shipping_to_bd_jpy = 150000  # ~$1000 container share to Bangladesh
        
        total_japan_jpy = (
            winning_bid_jpy + 
            auction_fee_jpy + 
            export_certificate_jpy + 
            freight_inspection_jpy + 
            shipping_to_bd_jpy
        )
        
        # Convert to BDT (CIF value)
        cif_value_bdt = total_japan_jpy * JPY_TO_BDT
        
        # =====================================================
        # BANGLADESH IMPORT DUTIES
        # =====================================================
        
        engine_cc = vehicle_data['engine_cc']
        vehicle_age = CURRENT_YEAR - vehicle_data['year']
        
        # Determine customs duty rate based on engine size
        if engine_cc <= 1500:
            customs_duty_rate = 1.25  # 125%
            supplementary_duty_rate = 0.20  # 20%
        elif engine_cc <= 2000:
            customs_duty_rate = 1.50  # 150%
            supplementary_duty_rate = 0.30  # 30%
        elif engine_cc <= 2500:
            customs_duty_rate = 2.50  # 250%
            supplementary_duty_rate = 0.35  # 35%
        else:  # > 2500cc (luxury/sports)
            customs_duty_rate = 5.00  # 500%
            supplementary_duty_rate = 0.45  # 45%
        
        # Age-based penalty (older vehicles taxed more)
        if vehicle_age > 5:
            customs_duty_rate += 0.50  # Additional 50% for older vehicles
        
        # Multi-layer tax calculation (ORDER MATTERS!)
        # Layer 1: Customs Duty (on CIF)
        customs_duty = cif_value_bdt * customs_duty_rate
        assessable_value_1 = cif_value_bdt + customs_duty
        
        # Layer 2: Supplementary Duty (on CIF + Customs)
        supplementary_duty = assessable_value_1 * supplementary_duty_rate
        assessable_value_2 = assessable_value_1 + supplementary_duty
        
        # Layer 3: VAT (on total assessable value)
        vat = assessable_value_2 * 0.15  # 15% VAT
        
        # Layer 4: Additional taxes
        advance_tax = assessable_value_2 * 0.05  # 5% advance income tax
        ait = assessable_value_2 * 0.03  # 3% AIT (Advance Income Tax)
        
        # Layer 5: Regulatory duties
        regulatory_duty = cif_value_bdt * 0.04  # 4% regulatory duty
        
        # Environmental surcharge (for high-emission vehicles)
        if engine_cc > 2500:
            environmental_surcharge = cif_value_bdt * 0.02  # 2%
        else:
            environmental_surcharge = cif_value_bdt * 0.01  # 1%
        
        # Total import duties
        total_duties = (
            customs_duty + 
            supplementary_duty + 
            vat + 
            advance_tax + 
            ait + 
            regulatory_duty + 
            environmental_surcharge
        )
        
        # =====================================================
        # LOCAL BANGLADESH COSTS
        # =====================================================
        
        clearing_agent_fee = 50000  # BDT - customs clearance agent
        brta_registration = 85000  # BDT - Bangladesh Road Transport Authority registration
        documentation_fee = 15000  # BDT - miscellaneous paperwork
        
        total_local_costs = (
            clearing_agent_fee + 
            brta_registration + 
            documentation_fee
        )
        
        # =====================================================
        # FINAL LANDED COST
        # =====================================================
        
        total_landed_cost_bdt = cif_value_bdt + total_duties + total_local_costs
        total_landed_cost_usd = total_landed_cost_bdt / 110  # Approximate BDT to USD
        
        # =====================================================
        # RETURN DETAILED BREAKDOWN
        # =====================================================
        
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
    
    def predict_and_calculate(self, vehicle_data, user_bid_jpy=None):
        """
        Main entry point: predict bid and calculate complete landed cost
        
        Args:
            vehicle_data: dict with vehicle details
            user_bid_jpy: optional user-specified bid (if None, uses ML prediction)
        
        Returns:
            dict: Complete analysis result
        """
        
        # Generate ML prediction
        predicted_bid_jpy = self.predict_winning_bid(vehicle_data)
        
        # Use user bid if provided, otherwise use prediction
        bid_to_use = user_bid_jpy if user_bid_jpy else predicted_bid_jpy
        
        # Calculate landed cost
        cost_breakdown = self.calculate_landed_cost(bid_to_use, vehicle_data)
        
        # Compile result
        result = {
            'predicted_winning_bid_jpy': predicted_bid_jpy,
            'user_bid_jpy': user_bid_jpy,
            'bid_used_for_calculation': bid_to_use,
            **cost_breakdown
        }
        
        return result


# =====================================================
# CLI INTERFACE FOR LARAVEL
# =====================================================

def main():
    """
    CLI interface for Laravel to call via Process::run()
    
    Usage:
        python engine.py '{"make":"Toyota","model":"Land Cruiser",...]' [user_bid_jpy]
    """
    
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': 'Missing vehicle data',
            'usage': 'python engine.py \'{"make":"Toyota",...}\' [user_bid]'
        }))
        sys.exit(1)
    
    try:
        # Parse vehicle data from JSON
        vehicle_input = json.loads(sys.argv[1])
        
        # Optional user bid
        user_bid = None
        if len(sys.argv) > 2 and sys.argv[2]:
            user_bid = int(sys.argv[2])
        
        # Initialize engine
        engine = JDMPulseEngine()
        
        # Run prediction and calculation
        result = engine.predict_and_calculate(vehicle_input, user_bid)
        
        # Output JSON for Laravel to consume
        print(json.dumps(result, indent=2))
        
    except json.JSONDecodeError as e:
        print(json.dumps({
            'error': 'Invalid JSON input',
            'details': str(e)
        }))
        sys.exit(1)
    
    except Exception as e:
        print(json.dumps({
            'error': 'Engine execution failed',
            'details': str(e)
        }), file=sys.stdout)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
