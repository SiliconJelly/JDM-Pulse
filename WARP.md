# JDM Pulse - Warp AI Rules & Development Guidelines

## Project Context
JDM Pulse is a B2B/B2C hybrid SaaS predictive analytics platform for Japanese Domestic Market (JDM) vehicle imports into Bangladesh. This project serves as a proof-of-concept for Chisel AI's domain-specific AI solutions targeting SMEs.

## Architecture Principles
1. **Hybrid Stack:** Laravel (PHP) frontend + Python ML backend
2. **Data-First:** Apache Parquet for analytics, Plotly.js for visualization
3. **Premium UX:** Apple-inspired design with GSAP animations
4. **Rapid Deployment:** Target Railway.app for 5-minute production deployment

## Technology Constraints
- **Dataset Limit:** < 75MB (Plotly Vibe-a-Thon requirement)
- **ML Model:** GradientBoostingRegressor (scikit-learn) with R² > 0.75
- **Response Time:** < 2 seconds for ML prediction + cost calculation
- **Browser Support:** Chrome/Firefox/Safari (latest 2 versions)

## File Structure Standards
```
JDM_Pulse/
├── ml/                      # Python ML engine
│   ├── engine.py           # Main prediction + calculation engine
│   ├── train_bid_predictor.py
│   ├── requirements.txt
│   └── __pycache__/
├── models/                  # Serialized ML models
│   ├── bid_predictor_model.joblib
│   ├── make_encoder.joblib
│   └── model_encoder.joblib
├── data/                    # Datasets
│   ├── jdm_pulse_dataset.parquet
│   └── bd_tax_rules.json
├── scripts/                 # Data acquisition scripts
│   ├── scrape_auction_data.py
│   └── convert_to_parquet.py
├── app/                     # Laravel application
│   └── Http/Controllers/
│       └── VehicleAnalyticsController.php
├── resources/views/         # Blade templates
│   └── dashboard.blade.php
├── public/js/              # Frontend JavaScript
│   └── dashboard.js
├── storage/app/            # JSON data files
│   └── featured_vehicles.json
└── routes/api.php          # API routes
```

## Development Workflow Rules

### Phase 1: Data Acquisition (Priority: CRITICAL)
- **ALWAYS** validate Parquet file size < 75MB before proceeding
- **ALWAYS** check for NULL values in critical fields: winning_bid_jpy, year, mileage_km, engine_cc
- Use dtype optimization: int16 for year, int32 for prices, category for make/model
- Include vehicles from 2015-2024 only (10-year window)
- Target 12K-15K records for ML training robustness

### Phase 2: ML Model Development (Priority: CRITICAL)
- **Success Criteria:** Test R² > 0.75 (non-negotiable)
- **Feature Engineering:** ALWAYS compute vehicle_age and mileage_per_year
- **Encoders:** Save LabelEncoders for make/model alongside model.joblib
- **Prediction Range:** Validate predictions are between ¥100K - ¥15M (sanity check)
- Test CLI interface with: `python ml/engine.py '{"make":"Toyota","model":"Land Cruiser","year":2020,"mileage_km":30000,"engine_cc":3500,"auction_grade":4.5}' 3500000`

### Phase 3: Laravel API Development (Priority: HIGH)
- **ALWAYS** use `Process::run()` for Python subprocess execution
- **Input Validation:** Required fields: make, model, year, mileage_km, engine_cc, auction_grade
- **Error Handling:** Return detailed error messages with HTTP 500 on Python execution failure
- **CSRF Protection:** Include CSRF token in all POST requests from frontend
- Path to Python engine: Use `base_path('ml/engine.py')` (absolute path)

### Phase 4: Frontend Development (Priority: HIGH)
- **Color Palette:** Use Tailwind colors (#3b82f6, #8b5cf6, #ec4899, etc.) for Plotly charts
- **GSAP Animations:** 
  - Number count-ups: 2 seconds duration
  - Section reveals: 0.8 seconds
  - Hover effects: 0.3 seconds
- **Plotly Config:** ALWAYS set `displayModeBar: false` for cleaner UI
- **Responsive:** Test on mobile (375px), tablet (768px), desktop (1920px)
- **Loading States:** Show "..." while fetching data (never leave UI blank)

### Phase 5: Testing (Priority: MEDIUM)
- **ML Model:** Verify predictions on 5 sample vehicles (diverse engine sizes)
- **API:** Use `curl` or Postman to test `/api/analyze-vehicle` independently
- **Frontend:** Test complete flow: vehicle selection → prediction → calculation → visualization
- **Edge Cases:** Test with invalid inputs (negative mileage, future year, etc.)

### Phase 6: Deployment (Priority: HIGH)
- **Platform:** Railway.app (primary), Vercel (backup)
- **Environment Variables:** APP_ENV=production, APP_DEBUG=false
- **Pre-deployment:** Test Python availability with `railway run python --version`
- **Post-deployment:** Test live URL within 5 minutes of deployment
- **Rollback Plan:** Keep local demo ready with ngrok if deployment fails

## Code Style Guidelines

### Python (ML Engine)
```python
# Always include type hints for public functions
def predict_winning_bid(self, vehicle_data: dict) -> int:
    """Predict winning bid in JPY"""
    
# Use descriptive variable names
vehicle_age = 2024 - vehicle_data['year']  # Good
va = 2024 - vehicle_data['year']           # Bad

# Always validate input data
if vehicle_age <= 0:
    raise ValueError("Vehicle year must be 2024 or earlier")
```

### PHP (Laravel Controller)
```php
// Always validate request data
$validated = $request->validate([
    'make' => 'required|string',
    'year' => 'required|integer|min:2010|max:2024',
]);

// Use meaningful variable names
$pythonPath = base_path('ml/engine.py');  // Good
$p = base_path('ml/engine.py');           // Bad

// Always handle process execution failures
if ($result->failed()) {
    return response()->json(['error' => 'Analysis engine failed'], 500);
}
```

### JavaScript (Frontend)
```javascript
// Use async/await for API calls
async function runPrediction() {
    try {
        const response = await fetch('/api/analyze-vehicle', {...});
        const result = await response.json();
        // Handle result
    } catch (error) {
        console.error('Prediction failed:', error);
    }
}

// Always animate number changes with GSAP
gsap.to(element, {
    textContent: newValue,
    duration: 2,
    ease: 'power2.out',
    snap: { textContent: 1 }
});
```

## Bangladesh-Specific Business Logic

### Tax Calculation Rules (Critical for Accuracy)
```python
# Engine size-based customs duty rates
if engine_cc <= 1500:
    customs_duty_rate = 1.25  # 125%
elif engine_cc <= 2000:
    customs_duty_rate = 1.50  # 150%
elif engine_cc <= 2500:
    customs_duty_rate = 2.50  # 250%
else:  # > 2500cc (luxury/sports)
    customs_duty_rate = 5.00  # 500%

# Age-based penalty (vehicles > 5 years old)
if vehicle_age > 5:
    customs_duty_rate += 0.50  # Additional 50%

# Multi-layer duty structure (ORDER MATTERS)
# 1. Customs Duty (on CIF)
# 2. Supplementary Duty (on CIF + Customs)
# 3. VAT 15% (on CIF + Customs + Supplementary)
# 4. Advance Tax, AIT, Regulatory Duty (on assessable values)
```

### Exchange Rate Management
- **Demo/MVP:** Hardcode JPY_TO_BDT = 0.72
- **Production:** Use live API (e.g., exchangerate-api.com)
- **Update Frequency:** Daily at midnight Bangladesh time (UTC+6)

## Performance Optimization Rules
1. **Model Loading:** Load ML model once at startup, cache in memory
2. **Parquet Queries:** Use row group size = 5000 for optimal analytics performance
3. **API Response:** Target < 2 seconds total (1s ML + 0.5s calculation + 0.5s network)
4. **Frontend Assets:** Use Cloudflare CDN for Plotly.js and GSAP (external CDN links)

## Security Rules
- **NEVER** expose Python script paths in client-side JavaScript
- **ALWAYS** validate user inputs on server-side (Laravel validation)
- **NEVER** execute user-provided code in Python engine
- **ALWAYS** use CSRF tokens for POST requests
- **NEVER** commit .env files or API keys to Git

## Chisel AI Integration Points (Future)
1. **Customer Support Chatbot:** Embed Chisel AI widget in dashboard (Month 3)
2. **Document Generation:** Use Chisel AI to auto-generate import paperwork (Month 4)
3. **Multilingual Support:** Bengali/English/Japanese translations (Month 6)
4. **B2B Cross-Sell:** Offer Chisel AI to JDM Pulse business customers (Month 9)

## Success Metrics Tracking
- **Tonight (Demo):** Complete user flow working end-to-end
- **Week 1:** 500+ email signups from beta launch
- **Month 1:** 50+ active users (3+ sessions each)
- **Month 6:** $5K MRR from subscriptions + transaction fees
- **Year 1:** $125K ARR (JDM Pulse + Chisel AI combined)

## Troubleshooting Guide

### Python Execution Fails in Laravel
**Symptom:** `Process::run()` returns error
**Fix:** 
1. Test Python path: `where python` (Windows) or `which python` (Linux)
2. Update controller to use full Python path: `$pythonPath = 'C:\\Python311\\python.exe';`
3. Fallback: Implement PHP-based calculation (skip ML prediction)

### ML Model Prediction Out of Range
**Symptom:** Predictions < ¥100K or > ¥15M
**Fix:**
1. Check feature engineering (vehicle_age, mileage_per_year)
2. Verify encoders match training data
3. Add prediction clipping: `prediction = np.clip(prediction, 100000, 15000000)`

### Parquet File > 75MB
**Symptom:** Dataset exceeds size limit
**Fix:**
1. Reduce records to 10K (sample randomly)
2. Remove outliers: `df = df[df['winning_bid_jpy'] < df['winning_bid_jpy'].quantile(0.95)]`
3. Use stronger compression: `compression='brotli'` instead of gzip

### Plotly Chart Not Rendering
**Symptom:** Blank chart area
**Fix:**
1. Check browser console for JavaScript errors
2. Verify data format: `console.log(currentAnalysis.cost_breakdown_bdt)`
3. Ensure Plotly.js CDN loaded: `<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>`

## Demo Presentation Tips
1. **Problem Statement (30s):** Show screenshot of opaque traditional importer pricing
2. **Live Demo (90s):** Select vehicle → See ML prediction → Calculate landed cost → Interactive Plotly chart
3. **Business Model (45s):** Explain SaaS tiers + transaction fees + Chisel AI connection
4. **Traction (15s):** "Built in 8 hours, ready for 500+ beta users, targeting $125K ARR Year 1"

## Critical Path for Tonight
```
4:00 PM - Data scraping started
5:30 PM - Parquet file validated (< 75MB)
7:00 PM - ML model trained (R² > 0.75)
8:30 PM - Laravel API working (tested with curl)
10:00 PM - Frontend integrated (complete user flow)
11:00 PM - Deployed to Railway (live URL tested)
11:30 PM - Demo rehearsed (3-minute script)
12:00 AM - SUBMISSION DEADLINE
```

## Emergency Contacts & Resources
- **Plotly Docs:** https://plotly.com/javascript/
- **GSAP Docs:** https://greensock.com/docs/
- **Railway Docs:** https://docs.railway.app/
- **Laravel Process:** https://laravel.com/docs/10.x/processes
- **Scikit-learn:** https://scikit-learn.org/stable/modules/ensemble.html#gradient-boosting

---

**Remember:** This is not just a hackathon project—it's the foundation of a real business. Build with production quality from day one. Every line of code should be clean, every design decision intentional, every metric tracked.

**Let's ship it! 🚀**
