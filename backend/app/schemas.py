from pydantic import BaseModel, Field, conint, confloat
from typing import Optional, Dict, Any

class VehicleInput(BaseModel):
    make: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., min_length=1, max_length=100)
    year: conint(ge=2015, le=2024)
    mileage_km: conint(ge=0, le=500_000)
    engine_cc: conint(ge=600, le=8_000)
    auction_grade: confloat(ge=0, le=6)
    user_bid_jpy: Optional[conint(ge=100_000, le=20_000_000)] = None
    target_win_prob: Optional[confloat(ge=0.5, le=0.9)] = None

class HealthResponse(BaseModel):
    status: str
    is_model_loaded: bool

class PredictResponse(BaseModel):
    predicted_winning_bid_jpy: int
    user_bid_jpy: Optional[int]
    bid_used_for_calculation: int
    currency_conversion: Dict[str, Any]
    japan_costs_jpy: Dict[str, int]
    bangladesh_duties_bdt: Dict[str, int]
    local_costs_bdt: Dict[str, int]
    total_landed_cost_bdt: int
    total_landed_cost_usd: int
    duty_percentage: float
    # Added fields
    q20_jpy: Optional[int] = None
    q50_jpy: Optional[int] = None
    q80_jpy: Optional[int] = None
    recommended_bid_jpy: Optional[int] = None
    platform_fee_bdt: Optional[int] = None
    total_incl_platform_bdt: Optional[int] = None
