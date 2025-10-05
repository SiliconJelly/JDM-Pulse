"""
Test script for JDM Pulse prediction engine
"""

from engine import JDMPulseEngine
import json

# Test vehicle data
test_vehicles = [
    {
        "name": "Toyota Land Cruiser 300 (2022, Low Mileage)",
        "data": {
            "make": "Toyota",
            "model": "Land Cruiser 300",
            "year": 2022,
            "mileage_km": 15000,
            "engine_cc": 3500,
            "auction_grade": 4.5
        },
        "user_bid": None
    },
    {
        "name": "Nissan GT-R R35 (2020, Medium Mileage)",
        "data": {
            "make": "Nissan",
            "model": "GT-R R35",
            "year": 2020,
            "mileage_km": 25000,
            "engine_cc": 3800,
            "auction_grade": 4.0
        },
        "user_bid": 3500000
    },
    {
        "name": "Lexus LX 600 (2023, Excellent Condition)",
        "data": {
            "make": "Lexus",
            "model": "LX 600",
            "year": 2023,
            "mileage_km": 8000,
            "engine_cc": 3500,
            "auction_grade": 5.0
        },
        "user_bid": None
    }
]

def format_currency(amount):
    """Format currency with thousand separators"""
    return f"{amount:,}"

def print_result(vehicle_name, result):
    """Pretty print the result"""
    print("\n" + "=" * 80)
    print(f"🚗 {vehicle_name}")
    print("=" * 80)
    
    # Prediction
    print(f"\n📊 ML PREDICTION:")
    print(f"  Predicted Winning Bid: ¥{format_currency(result['predicted_winning_bid_jpy'])}")
    
    if result['user_bid_jpy']:
        print(f"  User Specified Bid:    ¥{format_currency(result['user_bid_jpy'])}")
        print(f"  Using:                 ¥{format_currency(result['bid_used_for_calculation'])}")
    
    # Japan costs
    print(f"\n💴 JAPAN COSTS:")
    japan = result['japan_costs_jpy']
    print(f"  Winning Bid:           ¥{format_currency(japan['winning_bid'])}")
    print(f"  Auction Fee (5%):      ¥{format_currency(japan['auction_fee'])}")
    print(f"  Export Certificate:    ¥{format_currency(japan['export_certificate'])}")
    print(f"  Freight Inspection:    ¥{format_currency(japan['freight_inspection'])}")
    print(f"  Shipping to BD:        ¥{format_currency(japan['shipping'])}")
    print(f"  " + "-" * 60)
    print(f"  Total Japan Costs:     ¥{format_currency(japan['total'])}")
    
    # Currency conversion
    conv = result['currency_conversion']
    print(f"\n💱 CURRENCY CONVERSION:")
    print(f"  Exchange Rate:         ¥1 = ৳{conv['jpy_to_bdt_rate']}")
    print(f"  Japan Costs in BDT:    ৳{format_currency(conv['total_japan_cost_bdt'])}")
    
    # Bangladesh duties
    print(f"\n🇧🇩 BANGLADESH IMPORT DUTIES:")
    bd = result['bangladesh_duties_bdt']
    print(f"  CIF Value:             ৳{format_currency(bd['cif_value'])}")
    print(f"  Customs Duty:          ৳{format_currency(bd['customs_duty'])}")
    print(f"  Supplementary Duty:    ৳{format_currency(bd['supplementary_duty'])}")
    print(f"  VAT (15%):             ৳{format_currency(bd['vat'])}")
    print(f"  Advance Tax:           ৳{format_currency(bd['advance_tax'])}")
    print(f"  AIT:                   ৳{format_currency(bd['ait'])}")
    print(f"  Regulatory Duty:       ৳{format_currency(bd['regulatory_duty'])}")
    print(f"  Environmental:         ৳{format_currency(bd['environmental_surcharge'])}")
    print(f"  " + "-" * 60)
    print(f"  Total Duties:          ৳{format_currency(bd['total_duties'])}")
    print(f"  (Duty Rate: {result['duty_percentage']}% of CIF)")
    
    # Local costs
    print(f"\n🏪 LOCAL BANGLADESH COSTS:")
    local = result['local_costs_bdt']
    print(f"  Clearing Agent:        ৳{format_currency(local['clearing_agent_fee'])}")
    print(f"  BRTA Registration:     ৳{format_currency(local['brta_registration'])}")
    print(f"  Documentation:         ৳{format_currency(local['documentation_fee'])}")
    print(f"  " + "-" * 60)
    print(f"  Total Local Costs:     ৳{format_currency(local['total'])}")
    
    # Final total
    print(f"\n" + "=" * 80)
    print(f"✅ TOTAL LANDED COST IN BANGLADESH")
    print(f"=" * 80)
    print(f"  ৳{format_currency(result['total_landed_cost_bdt'])} BDT")
    print(f"  ~${format_currency(result['total_landed_cost_usd'])} USD")
    print(f"=" * 80)


def main():
    print("=" * 80)
    print("JDM PULSE - PREDICTION ENGINE TEST")
    print("=" * 80)
    
    # Initialize engine
    print("\nInitializing prediction engine...")
    engine = JDMPulseEngine()
    print("✓ Engine ready\n")
    
    # Test each vehicle
    for test in test_vehicles:
        try:
            result = engine.predict_and_calculate(
                test['data'], 
                test['user_bid']
            )
            print_result(test['name'], result)
        except Exception as e:
            print(f"\n❌ Error testing {test['name']}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("✓ ALL TESTS COMPLETE")
    print("=" * 80)
    print("\nEngine is ready for Laravel integration!")


if __name__ == '__main__':
    main()
