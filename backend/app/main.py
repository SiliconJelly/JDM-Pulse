from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import VehicleInput, PredictResponse, HealthResponse
from .engine import JDMPulseEngine, JPY_TO_BDT

app = FastAPI(title="JDM Pulse API", version="1.0.0")

# CORS - allow local Next.js during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"  # loosened for MVP dev; tighten in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance (loaded once)
engine: JDMPulseEngine | None = None

@app.on_event("startup")
def load_engine():
    global engine
    engine = JDMPulseEngine()

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", is_model_loaded=engine is not None)

@app.post("/predict", response_model=PredictResponse)
async def predict(vehicle: VehicleInput):
    assert engine is not None, "Engine not initialized"

    # Extract inputs
    v = vehicle.model_dump()
    user_bid = v.pop("user_bid_jpy", None)
    target_prob = v.pop("target_win_prob", None)

    # Quantiles and recommendation
    quantiles = engine.predict_quantiles(v)
    recommended = engine.recommend_bid(v, target_win_prob=target_prob or 0.7)

    # Decide bid used
    bid_to_use = user_bid if user_bid is not None else recommended

    # Compute breakdown using chosen bid
    breakdown = engine.calculate_landed_cost(bid_to_use, v)

    # Platform fee (2% of bid, converted to BDT using model rate)
    jpy_to_bdt = breakdown["currency_conversion"]["jpy_to_bdt_rate"]
    platform_fee_bdt = int(bid_to_use * jpy_to_bdt * 0.02)
    total_incl_platform_bdt = breakdown["total_landed_cost_bdt"] + platform_fee_bdt

    response = {
        **breakdown,
        "predicted_winning_bid_jpy": engine.predict_winning_bid(v),
        "user_bid_jpy": user_bid,
        "bid_used_for_calculation": bid_to_use,
        "q20_jpy": quantiles.get("q20"),
        "q50_jpy": quantiles.get("q50"),
        "q80_jpy": quantiles.get("q80"),
        "recommended_bid_jpy": recommended,
        "platform_fee_bdt": platform_fee_bdt,
        "total_incl_platform_bdt": total_incl_platform_bdt,
    }

    return PredictResponse(**response)
