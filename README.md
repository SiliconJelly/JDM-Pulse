# JDM Pulse

Predictive import analytics for JDM vehicles with a premium, fast UX.

- Frontend: Next.js 14 (TypeScript, Tailwind v4, Framer Motion, Plotly)
- Backend: FastAPI (Python), model warm-loaded for sub-100ms inference after warm-up
- ML: Gradient Boosting with engineered features + quantile models for proxy bidding
- Demo: Plotly Studio CSV in `demo/plotly_studio_demo.csv`

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ (recommended 20/22)

### Backend (FastAPI)
```powershell
# Install
pip install -r backend/requirements.txt -r backend/requirements-dev.txt

# Run (dev)
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001 --reload

# Test
pytest backend/tests -q
```

### Frontend (Next.js)
```powershell
# Install
npm --prefix frontend ci

# Dev
npm --prefix frontend run dev

# Build
npm --prefix frontend run build
```

### Environment
- Frontend uses `frontend/.env.local`
```
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8001
```

## Data & Model
- Synthetic CSV: `temp_auction_data.csv`
- Parquet dataset: `data/jdm_pulse_dataset.parquet`
- Trained models: `models/*.joblib` (git-ignored)
- Enriched demo CSV for Plotly Studio: `demo/plotly_studio_demo.csv`

## Proxy Bidding (v1)
- Quantile models: q20, q50, q80
- Recommended bid computed for a target win probability (default 70%)
- Platform fee: demo 2% of bid (converted to BDT) returned by backend

## CI/CD
- GitHub Actions:
  - Backend CI: lint import + pytest
  - Frontend CI: npm ci + lint + build
- Dependabot: weekly updates for npm and pip

## Contributing & Security
- See CONTRIBUTING.md for dev workflow and PR expectations
- See SECURITY.md to report vulnerabilities
- Code of Conduct: CODE_OF_CONDUCT.md

## License
MIT License (see LICENSE). If you prefer a different license, open an issue.

> **🎯 Mission:** Build and deploy a production-ready MVP by midnight for Plotly Vibe-a-Thon  
> **🚀 Status:** Ready to start 8-hour sprint  
> **👥 Team:** Nirjhor (Lead/Full-Stack), Tanjim Mohamed (Frontend/UX)

## What We're Building

JDM Pulse is a B2B/B2C hybrid SaaS platform that uses machine learning to predict Japanese auction bids and calculate exact landed costs for importing JDM vehicles into Bangladesh. We're solving a $150M market's complete lack of price transparency.

**Key Innovation:** ML-powered bid prediction + real-time landed cost calculator with interactive Plotly visualizations.

## Tonight's Goal (8-Hour Sprint)

| Time | Milestone | Status |
|------|-----------|--------|
| 4:00-5:30 PM | Data acquisition & Parquet creation | ⏳ |
| 5:30-7:00 PM | ML model training (R² > 0.75) | ⏳ |
| 7:00-8:30 PM | Laravel API + Python integration | ⏳ |
| 8:30-10:00 PM | Frontend with Plotly + GSAP | ⏳ |
| 10:00-11:00 PM | Testing & polish | ⏳ |
| 11:00-12:00 AM | Deploy to Railway + demo prep | ⏳ |

## Quick Start (Before You Begin)

### Prerequisites Check
```powershell
# Verify all tools are installed (Run in PowerShell)
php --version        # Need PHP 8.2+
python --version     # Need Python 3.11+
composer --version   # Need Composer 2.x
node --version       # Need Node.js 18+
npm --version        # Need npm 9+
```

**If any are missing:**
- PHP 8.2: https://windows.php.net/download/
- Python 3.11: https://www.python.org/downloads/
- Composer: https://getcomposer.org/download/
- Node.js: https://nodejs.org/en/download/

### Initial Setup (5 minutes)
```powershell
# 1. Create project structure
New-Item -ItemType Directory -Force -Path ml, models, data, scripts, storage\app, public\js

# 2. Create Python virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install Python dependencies
pip install beautifulsoup4 requests pandas pyarrow scikit-learn joblib numpy

# 4. Initialize Laravel (if not already set up)
# If you have existing Laravel app, skip this
# composer create-project laravel/laravel . "10.*"
# OR use your existing Laravel installation

# 5. Install frontend dependencies
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init

# 6. Create .env file (if starting fresh)
# Copy from .env.example and set APP_KEY
```

## Phase-by-Phase Execution Guide

### Phase 1: Data Acquisition (4:00-5:30 PM) ⚠️ CRITICAL

**Objective:** Create `jdm_pulse_dataset.parquet` < 75MB with 12K+ vehicle records

#### Step 1.1: Create Web Scraping Script
```powershell
# Create the scraper
New-Item -ItemType File -Path scripts\scrape_auction_data.py
```

**Implementation hints:**
- Target: TradeCarView, Goo-net Exchange (publicly available sold vehicles)
- Focus on: Toyota, Nissan, Lexus, Porsche (high-value models)
- Required fields: make, model, year, mileage_km, engine_cc, auction_grade, winning_bid_jpy
- Use `requests` + `BeautifulSoup4` for scraping
- Implement retry logic (3 attempts per page)
- Save to `temp_auction_data.csv`

#### Step 1.2: Convert to Parquet
```powershell
# Create converter script
New-Item -ItemType File -Path scripts\convert_to_parquet.py

# Run conversion
python scripts\convert_to_parquet.py

# Verify size (MUST be < 75MB)
(Get-Item data\jdm_pulse_dataset.parquet).length / 1MB
```

**✅ Phase 1 Success Criteria:**
- [ ] Parquet file exists at `data/jdm_pulse_dataset.parquet`
- [ ] File size < 75MB
- [ ] Contains 12,000+ records
- [ ] No NULL values in critical fields

---

### Phase 2: ML Model Training (5:30-7:00 PM) ⚠️ CRITICAL

**Objective:** Train GradientBoostingRegressor with R² > 0.75

#### Step 2.1: Create Training Script
```powershell
# Create training script
New-Item -ItemType File -Path ml\train_bid_predictor.py

# Run training
python ml\train_bid_predictor.py
```

**Expected output:**
```
Loading dataset: 14,523 records
Feature engineering complete
Training model...
Train R²: 0.8234, Test R²: 0.7856
Model saved to ../models/bid_predictor_model.joblib
```

#### Step 2.2: Create Prediction Engine
```powershell
# Create engine
New-Item -ItemType File -Path ml\engine.py

# Test engine
python ml\engine.py '{\"make\":\"Toyota\",\"model\":\"Land Cruiser\",\"year\":2020,\"mileage_km\":30000,\"engine_cc\":3500,\"auction_grade\":4.5}' 3500000
```

**Expected output:**
```json
{
  "predicted_winning_bid_jpy": 3450000,
  "user_bid_jpy": 3500000,
  "total_landed_cost_bdt": 18500000,
  "cost_breakdown_bdt": {...}
}
```

**✅ Phase 2 Success Criteria:**
- [ ] Model trained with Test R² > 0.75
- [ ] Three files created: `bid_predictor_model.joblib`, `make_encoder.joblib`, `model_encoder.joblib`
- [ ] `engine.py` returns valid JSON when called via CLI
- [ ] Predictions are within ¥100K - ¥15M range

---

### Phase 3: Laravel API (7:00-8:30 PM) 🔥 HIGH PRIORITY

**Objective:** Create API endpoint that bridges Laravel → Python engine

#### Step 3.1: Create Controller
```powershell
# Generate controller
php artisan make:controller VehicleAnalyticsController
```

**Edit:** `app/Http/Controllers/VehicleAnalyticsController.php` (see full code in production plan)

#### Step 3.2: Add Routes
**Edit:** `routes/api.php`
```php
Route::post('/analyze-vehicle', [VehicleAnalyticsController::class, 'analyze']);
Route::get('/featured-vehicles', [VehicleAnalyticsController::class, 'getFeaturedVehicles']);
```

#### Step 3.3: Create Featured Vehicles JSON
**Create:** `storage/app/featured_vehicles.json` (see full JSON in production plan)

#### Step 3.4: Test API
```powershell
# Start Laravel dev server (in one terminal)
php artisan serve

# Test API (in another terminal)
curl -X POST http://localhost:8000/api/analyze-vehicle `
  -H "Content-Type: application/json" `
  -d '{\"make\":\"Toyota\",\"model\":\"Land Cruiser 300\",\"year\":2022,\"mileage_km\":15000,\"engine_cc\":3500,\"auction_grade\":4.5}'
```

**✅ Phase 3 Success Criteria:**
- [ ] `/api/analyze-vehicle` returns valid JSON
- [ ] Response time < 3 seconds
- [ ] Python execution works from Laravel
- [ ] Error handling returns HTTP 500 with details

---

### Phase 4: Frontend Integration (8:30-10:00 PM) 🔥 HIGH PRIORITY

**Objective:** Build Apple-inspired dashboard with Plotly visualizations

#### Step 4.1: Create Dashboard Blade Template
**Create:** `resources/views/dashboard.blade.php` (see full HTML in production plan)

#### Step 4.2: Configure Tailwind
**Edit:** `tailwind.config.js`
```javascript
module.exports = {
  content: [
    "./resources/**/*.blade.php",
    "./resources/**/*.js",
    "./public/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Edit:** `resources/css/app.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

#### Step 4.3: Create Dashboard JavaScript
**Create:** `public/js/dashboard.js` (see full code in production plan)

#### Step 4.4: Add CDN Links
Ensure these are in your Blade template:
```html
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
```

#### Step 4.5: Build Assets
```powershell
# Build Tailwind CSS
npm run build

# Or for development with watch
npm run dev
```

**✅ Phase 4 Success Criteria:**
- [ ] Vehicle cards display correctly
- [ ] Clicking vehicle shows analytics section with smooth animation
- [ ] ML prediction displays with number count-up animation
- [ ] Plotly donut chart renders with correct data
- [ ] Responsive on mobile (375px), tablet (768px), desktop (1920px)

---

### Phase 5: Testing & Polish (10:00-11:00 PM)

**Testing Checklist:**
```powershell
# 1. ML Model Unit Test
python ml\train_bid_predictor.py  # Verify R² > 0.75

# 2. API Test
# Test 5 different vehicles with diverse engine sizes

# 3. Frontend Test
# Open http://localhost:8000 in browser
# Test complete flow: select vehicle → prediction → calculate → visualize

# 4. Mobile Responsive Test
# Open DevTools, test on iPhone SE (375px), iPad (768px), Desktop (1920px)

# 5. Error Handling Test
# Try invalid inputs (negative mileage, future year, etc.)
```

**Polish Tasks:**
- [ ] Add loading spinners (replace "..." with animated spinner)
- [ ] Add tooltips on "Supplementary Duty", "AIT", etc.
- [ ] Test all GSAP animations (smooth 60fps)
- [ ] Add favicon and meta tags
- [ ] Spell-check all UI text

**✅ Phase 5 Success Criteria:**
- [ ] No JavaScript console errors
- [ ] All animations smooth (60fps)
- [ ] Mobile experience polished
- [ ] Edge cases handled gracefully

---

### Phase 6: Deployment (11:00-12:00 AM) 🚀 CRITICAL

**Objective:** Deploy live to Railway.app with public URL

#### Step 6.1: Prepare for Deployment
```powershell
# Create Railway config
New-Item -ItemType File -Path nixpacks.toml

# Create Python requirements
New-Item -ItemType File -Path ml\requirements.txt

# Initialize Git (if not already)
git init
git add .
git commit -m "Initial commit - JDM Pulse MVP"
```

#### Step 6.2: Deploy to Railway
```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Set environment variables
railway variables set APP_ENV=production
railway variables set APP_DEBUG=false
railway variables set APP_KEY=base64:YOUR_KEY_HERE

# Deploy!
railway up
```

#### Step 6.3: Post-Deployment Verification
```powershell
# Get your live URL
railway status

# Test live URL
curl https://your-app.up.railway.app/api/featured-vehicles
```

**✅ Phase 6 Success Criteria:**
- [ ] Live URL accessible
- [ ] Complete user flow works on production
- [ ] Response time < 3 seconds
- [ ] No 500 errors in Railway logs

---

## Emergency Fallback Plans

### If Data Scraping Fails
**Plan B:** Use synthetic data generator
```python
import pandas as pd
import numpy as np

# Generate synthetic dataset
np.random.seed(42)
n_records = 12000
df = pd.DataFrame({
    'make': np.random.choice(['Toyota', 'Nissan', 'Lexus', 'Porsche'], n_records),
    'model': np.random.choice(['Land Cruiser', 'GT-R', 'LX', '911'], n_records),
    'year': np.random.randint(2015, 2025, n_records),
    'mileage_km': np.random.randint(5000, 150000, n_records),
    'engine_cc': np.random.choice([1500, 2000, 2500, 3500], n_records),
    'auction_grade': np.random.uniform(3.0, 5.0, n_records).round(1),
    'winning_bid_jpy': np.random.randint(500000, 10000000, n_records)
})
df.to_parquet('data/jdm_pulse_dataset.parquet', compression='gzip')
```

### If Python Execution Fails in Laravel
**Plan B:** Implement PHP calculation (no ML prediction)
```php
// Use average bid based on engine size
$avgBid = match(true) {
    $engineCc <= 1500 => 1500000,
    $engineCc <= 2000 => 2500000,
    $engineCc <= 2500 => 4000000,
    default => 6000000
};
```

### If Railway Deployment Fails
**Plan B:** Use ngrok for local demo
```powershell
# Download ngrok: https://ngrok.com/download
ngrok http 8000
# Use ngrok URL for demo
```

---

## Demo Script (3 Minutes)

### Slide 1: Problem (30 seconds)
> "Importing JDM cars in Bangladesh is a $150M black box. Traditional importers markup 30-50% without any transparency. Buyers have zero visibility into auction dynamics or true landed costs."

**Visual:** Show screenshot of opaque traditional pricing

### Slide 2: Solution - Live Demo (90 seconds)
> "JDM Pulse uses machine learning to predict auction bids and calculates exact landed costs down to the last Taka."

**Live Demo Flow:**
1. Open dashboard → Show 4 featured vehicles
2. Click "Toyota Land Cruiser 300"
3. **ML Prediction appears:** "Our model predicts winning bid: ¥3,450,000 with 95% confidence"
4. User enters bid: ¥3,500,000
5. Click "Calculate Landed Cost"
6. **Animation:** Numbers count up, Plotly donut chart renders
7. **Result:** "Total landed cost in Bangladesh: ৳18,500,000 (~$168,000 USD)"
8. Expand breakdown table → Show transparent cost structure

### Slide 3: Business Model (45 seconds)
> "We're building a tech-first dropshipping platform for vehicles."

**Revenue Streams:**
- SaaS Subscriptions: $29-99/month (B2C), $199-499/month (B2B)
- Transaction Fees: 2-5% commission on facilitated imports
- Target: 20 transactions/month by Month 6 = $12K-30K/month

**Chisel AI Connection:**
- JDM Pulse is proof-of-concept for Chisel AI's vertical AI solutions
- 25% conversion from JDM Pulse B2B to Chisel AI enterprise
- Combined ARR target: $125K Year 1

### Slide 4: Traction (15 seconds)
> "Built in 8 hours. Production-ready with R² > 0.75 ML accuracy. Ready to onboard 500+ beta users from Bangladesh car enthusiast communities. We're not just building a hackathon project—we're building a business."

---

## Tech Stack Summary

**Frontend:**
- Laravel 10 (PHP 8.2)
- TailwindCSS 3.4 (Apple-inspired design)
- Plotly.js 2.27 (data visualization)
- GSAP 3.12 (animations)

**Backend:**
- Python 3.11
- scikit-learn 1.3 (ML)
- pandas 2.1 (data processing)
- Apache Parquet (columnar storage)

**Infrastructure:**
- Railway.app (hosting)
- PostgreSQL (production DB)
- Cloudflare CDN (static assets)

---

## Critical Success Factors

1. **Dataset Quality:** 12K+ clean records, < 75MB
2. **ML Performance:** R² > 0.75 (non-negotiable)
3. **UX Polish:** Apple-level design with smooth animations
4. **Business Story:** Clear path from problem → solution → revenue
5. **Live Demo:** Flawless execution in 3 minutes

---

## Resources & Links

- **Production Plan:** `JDM_PULSE_PRODUCTION_PLAN.md` (complete SDLC guide)
- **Project Rules:** `WARP.md` (development guidelines)
- **Plotly Docs:** https://plotly.com/javascript/
- **GSAP Docs:** https://greensock.com/docs/
- **Railway Docs:** https://docs.railway.app/
- **scikit-learn:** https://scikit-learn.org/stable/

---

## Team Roles

**Nirjhor (Lead / Full-Stack):**
- Phases 1-2: Data acquisition + ML model
- Phase 3: API integration
- Phase 6: Deployment

**Tanjim Mohamed (Frontend / UX):**
- Phase 4: Dashboard UI + Plotly charts
- Phase 5: UX testing + polish
- Demo preparation

**Shared:**
- Phase 3: API integration (pair programming)
- Phase 5: End-to-end testing

---

## Final Pre-Flight Checklist

**Right Now (Before 4:00 PM):**
- [ ] All tools installed and verified
- [ ] Project structure created
- [ ] Python virtual environment activated
- [ ] Dependencies installed
- [ ] GitHub repo created
- [ ] Railway account created
- [ ] Energy drinks stocked ☕
- [ ] Focus mode activated 🔇

**Before Demo (11:30 PM):**
- [ ] Live site working
- [ ] Demo script rehearsed
- [ ] Backup video recorded
- [ ] Slide deck ready

---

## Let's Go! 🚀

**Current Time:** Check your clock  
**Deadline:** 12:00 AM (Midnight)  
**Hours Available:** Calculate remaining time  

**First Action:** Start with Phase 1 - Data Acquisition  
**Command:** `python scripts/scrape_auction_data.py`

Remember: This isn't just a hackathon project. This is the foundation of a real business that will disrupt a $150M market in Bangladesh and prove the viability of Chisel AI's vertical SaaS model.

**Build fast. Build smart. Ship it.**

---

*"The best way to predict the future is to invent it." - Alan Kay*

**Now go make it happen! 💪**
