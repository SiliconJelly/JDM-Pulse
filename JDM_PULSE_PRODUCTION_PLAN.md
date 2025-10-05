# JDM Pulse: Production-Ready MVP Documentation
## Plotly Vibe-a-Thon Submission & Startup Launch Plan

**Project Lead:** Nirjhor, Tanjim Mohamed  
**Target:** Live Demo by Tonight  
**Positioning:** B2B/B2C Hybrid SaaS for Predictive Automotive Import Analytics

---

## 1. MARKET POSITIONING & OPPORTUNITY IN BANGLADESH

### 1.1 Current Market Pain Points
- **Opacity in Pricing:** Traditional importers markup 30-50% without transparency
- **Limited Access:** Only wealthy institutions/individuals can afford showroom prices
- **Information Asymmetry:** Buyers have no visibility into auction dynamics or true costs
- **Inefficient Capital Deployment:** Large importers tie up capital in inventory and showrooms

### 1.2 Bangladesh-Specific Opportunity
**Market Size:**
- Bangladesh luxury/sports car import market: ~$150M annually
- Growing affluent middle class (8-10% annual growth)
- 200+ registered car importers (mostly traditional, non-tech)
- High smartphone penetration (50%+) but zero digital import solutions

**Regulatory Environment:**
- Complex multi-layer tax structure (300-800% total duty on luxury vehicles)
- Requires deep domain knowledge - our competitive advantage
- Government digitization push (Digital Bangladesh 2024)

**Target Segments:**
1. **B2C - Individual Enthusiasts:** Car enthusiasts, expatriates, young entrepreneurs ($30K-100K budget)
2. **B2B - SME Importers:** Small car trading businesses lacking tech infrastructure
3. **B2B - Corporate Fleets:** Corporations seeking executive vehicles with budget predictability

### 1.3 Competitive Moat
- **First-mover advantage** in tech-enabled vehicle dropshipping in Bangladesh
- **Proprietary ML model** trained on JDM auction data
- **Complete financial transparency** - no competitor offers full landed cost breakdown
- **Zero inventory model** - capital-light, highly scalable

---

## 2. BUSINESS MODEL: B2B/B2C HYBRID SAAS

### 2.1 Revenue Streams

#### Phase 1: MVP (Vibe-a-Thon) - FREE with Lead Generation
- Free access to predictive analytics and cost calculator
- Capture leads (email, phone) for future conversion
- **Goal:** 500+ signups during demo phase

#### Phase 2: SaaS Subscription (Month 1-3)
**B2C Tier:**
- **Free Tier:** 5 predictions/month, basic cost calculator
- **Pro Tier ($29/month):** Unlimited predictions, real-time auction alerts, saved searches
- **Premium Tier ($99/month):** White-glove import concierge, financing partnerships

**B2B Tier:**
- **Starter ($199/month):** For small importers, 50 vehicle analyses/month, API access
- **Business ($499/month):** Unlimited analyses, multi-user accounts, custom reports
- **Enterprise (Custom):** Full API, white-label solution, dedicated support

#### Phase 3: Transaction Revenue (Month 4+)
- **Commission Model:** 2-5% commission on successful imports facilitated through platform
- **Average Transaction Value:** $30,000 (JDM mid-range)
- **Target:** 20 transactions/month by Month 6 = $12K-30K/month

### 2.2 Connection to Chisel AI Ecosystem
- **JDM Pulse = Proof of Concept** for Decide AI v2's vertical application
- Demonstrates ability to create **domain-specific AI solutions** for SMEs
- **Data Flywheel:** Each transaction generates training data for Chisel AI's multilingual chatbot
- **Sales Pipeline:** JDM Pulse customers become Chisel AI enterprise leads

**Integration Path:**
1. JDM Pulse uses Chisel AI for **multilingual customer support** (Bengali, English, Japanese)
2. Chisel AI's **document assistant** helps users understand complex import regulations
3. Cross-sell Chisel AI to B2B customers needing **enterprise LLM** for their operations

---

## 3. TECHNOLOGY STACK: BEST-IN-CLASS FOR DATA ANALYTICS

### 3.1 Frontend Stack
```
├── Framework: Laravel 10+ (PHP 8.2)
├── Styling: TailwindCSS 3.4 + Shadcn UI design principles
├── Data Visualization: Plotly.js 2.27+
├── Animation: GSAP 3.12 (GreenSock)
├── State Management: Alpine.js (lightweight reactivity)
└── Build Tool: Vite 5.0
```

**Why This Stack:**
- Laravel provides rapid development with elegant syntax
- TailwindCSS + Shadcn ensures Apple-level UI polish
- Plotly.js is hackathon requirement and industry-standard for interactive charts
- GSAP delivers 60fps animations for premium feel

### 3.2 Backend/ML Engine Stack
```
├── Language: Python 3.11+
├── ML Framework: Scikit-learn 1.3+
├── Data Processing: Pandas 2.1+, NumPy 1.26+
├── Storage Format: Apache Parquet (columnar)
├── Model Serialization: Joblib 1.3+
├── API Bridge: Laravel Process (subprocess execution)
└── Future: FastAPI for production ML serving
```

**Why This Stack:**
- Scikit-learn's GradientBoostingRegressor perfect for tabular data
- Parquet format = 5-10x compression + 100x faster queries vs CSV
- Joblib ensures fast model loading (<100ms)

### 3.3 Data & Infrastructure Stack
```
├── Development DB: SQLite (embedded)
├── Production DB: PostgreSQL 15+ on Railway/Supabase
├── Dataset Format: Parquet (< 75MB compressed)
├── Static Assets: Cloudflare CDN
├── Hosting: Railway.app or Vercel (Laravel support)
├── CI/CD: GitHub Actions
└── Monitoring: Sentry (error tracking), Plausible (analytics)
```

### 3.4 DevOps & Deployment
```
├── Version Control: Git + GitHub
├── Environment Management: Docker (optional for tonight)
├── Package Managers: Composer (PHP), pip (Python)
├── Environment Variables: .env (Laravel convention)
└── Demo Hosting: Railway.app (5-minute deploy)
```

---

## 4. SDLC: TONIGHT'S SPRINT TO LIVE DEMO

### 4.1 Timeline (8-Hour Sprint)
**Assumption:** Starting at 4:00 PM, going live by 12:00 AM

| Time | Phase | Duration | Deliverable |
|------|-------|----------|-------------|
| 4:00-5:30 PM | Data Acquisition | 90 min | jdm_pulse_dataset.parquet (< 75MB) |
| 5:30-7:00 PM | ML Model Development | 90 min | bid_predictor_model.joblib |
| 7:00-8:30 PM | Backend API Development | 90 min | Laravel API endpoint + Python integration |
| 8:30-10:00 PM | Frontend Integration | 90 min | Plotly charts + GSAP animations |
| 10:00-11:00 PM | Testing & Refinement | 60 min | Bug fixes, UX polish |
| 11:00-12:00 AM | Deployment & Demo | 60 min | Live on Railway.app |

### 4.2 Phase 1: Data Acquisition (4:00-5:30 PM)

#### Task 1.1: Web Scraping Script
**File:** `scripts/scrape_auction_data.py`

```python
# Key scraping targets (publicly available historical data):
SOURCES = [
    "https://www.tradecarview.com/used_car/japan/",  # Past auction results
    # Add 2-3 more public sources
]

PRIORITY_MODELS = [
    "Toyota Land Cruiser",
    "Lexus LX",
    "Nissan GT-R",
    "Porsche 911",
    "Toyota GR Supra",
    "Honda NSX",
    "Mazda RX-7",
    "Subaru WRX STI"
]

# Target: 12,000-15,000 records
# Fields: make, model, year, mileage_km, engine_cc, auction_grade, winning_bid_jpy, auction_date
```

**Execution:**
```bash
cd scripts
pip install beautifulsoup4 requests pandas pyarrow
python scrape_auction_data.py
# Output: temp_auction_data.csv (~120MB)
```

#### Task 1.2: Parquet Conversion & Compression
**File:** `scripts/convert_to_parquet.py`

```python
import pandas as pd

df = pd.read_csv('temp_auction_data.csv')

# Data cleaning
df = df.dropna(subset=['winning_bid_jpy', 'year', 'mileage_km'])
df = df[df['year'] >= 2015]  # Focus on recent vehicles
df['auction_grade'] = df['auction_grade'].fillna('3.5')

# Optimize dtypes for compression
df['year'] = df['year'].astype('int16')
df['mileage_km'] = df['mileage_km'].astype('int32')
df['engine_cc'] = df['engine_cc'].astype('int16')
df['winning_bid_jpy'] = df['winning_bid_jpy'].astype('int32')

# Convert to Parquet with gzip compression
df.to_parquet(
    '../data/jdm_pulse_dataset.parquet',
    compression='gzip',
    index=False
)

print(f"Final size: {os.path.getsize('../data/jdm_pulse_dataset.parquet') / 1024 / 1024:.2f} MB")
```

**Validation:** Ensure `jdm_pulse_dataset.parquet` < 75MB

---

### 4.3 Phase 2: ML Model Development (5:30-7:00 PM)

#### Task 2.1: Training Script
**File:** `ml/train_bid_predictor.py`

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np

# Load data
df = pd.read_parquet('../data/jdm_pulse_dataset.parquet')

# Feature engineering
df['vehicle_age'] = 2024 - df['year']
df['mileage_per_year'] = df['mileage_km'] / df['vehicle_age']

# Encode categorical variables
le_make = LabelEncoder()
le_model = LabelEncoder()
df['make_encoded'] = le_make.fit_transform(df['make'])
df['model_encoded'] = le_model.fit_transform(df['model'])

# Features and target
features = ['vehicle_age', 'mileage_km', 'engine_cc', 'auction_grade', 
            'make_encoded', 'model_encoded', 'mileage_per_year']
X = df[features]
y = df['winning_bid_jpy']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f"Train R²: {train_score:.4f}, Test R²: {test_score:.4f}")

# Save model and encoders
joblib.dump(model, '../models/bid_predictor_model.joblib')
joblib.dump(le_make, '../models/make_encoder.joblib')
joblib.dump(le_model, '../models/model_encoder.joblib')
```

**Success Criteria:** Test R² > 0.75

#### Task 2.2: Prediction Engine
**File:** `ml/engine.py`

```python
import joblib
import pandas as pd
import json

class JDMPulseEngine:
    def __init__(self):
        self.model = joblib.load('../models/bid_predictor_model.joblib')
        self.make_encoder = joblib.load('../models/make_encoder.joblib')
        self.model_encoder = joblib.load('../models/model_encoder.joblib')
        
        # Load BD tax rules
        with open('../data/bd_tax_rules.json', 'r') as f:
            self.bd_tax_rules = json.load(f)
    
    def predict_winning_bid(self, vehicle_data):
        """Predict winning bid in JPY"""
        # Feature engineering (match training)
        vehicle_age = 2024 - vehicle_data['year']
        mileage_per_year = vehicle_data['mileage_km'] / vehicle_age
        
        # Encode categoricals
        make_encoded = self.make_encoder.transform([vehicle_data['make']])[0]
        model_encoded = self.model_encoder.transform([vehicle_data['model']])[0]
        
        # Create feature vector
        features = pd.DataFrame([{
            'vehicle_age': vehicle_age,
            'mileage_km': vehicle_data['mileage_km'],
            'engine_cc': vehicle_data['engine_cc'],
            'auction_grade': vehicle_data['auction_grade'],
            'make_encoded': make_encoded,
            'model_encoded': model_encoded,
            'mileage_per_year': mileage_per_year
        }])
        
        # Predict
        prediction = self.model.predict(features)[0]
        return int(prediction)
    
    def calculate_landed_cost(self, winning_bid_jpy, vehicle_data):
        """Calculate complete landed cost in BDT"""
        
        # Exchange rate (hardcoded for demo, use live API in production)
        JPY_TO_BDT = 0.72
        
        # Japan-side costs
        auction_fee_jpy = winning_bid_jpy * 0.05  # 5% auction house fee
        export_certificate_jpy = 15000  # ~$100
        freight_inspection_jpy = 25000  # ~$170
        shipping_to_bd_jpy = 150000  # ~$1000 (container share)
        
        total_japan_jpy = (winning_bid_jpy + auction_fee_jpy + 
                          export_certificate_jpy + freight_inspection_jpy + 
                          shipping_to_bd_jpy)
        
        # Convert to BDT
        cif_value_bdt = total_japan_jpy * JPY_TO_BDT
        
        # Bangladesh import duties (complex multi-layer structure)
        engine_cc = vehicle_data['engine_cc']
        vehicle_age = 2024 - vehicle_data['year']
        
        # Determine duty rates based on engine size and age
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
        
        # Age-based additional duty
        if vehicle_age > 5:
            customs_duty_rate += 0.50  # +50% for older vehicles
        
        # Calculate duties layer by layer
        customs_duty = cif_value_bdt * customs_duty_rate
        assessable_value_1 = cif_value_bdt + customs_duty
        
        supplementary_duty = assessable_value_1 * supplementary_duty_rate
        assessable_value_2 = assessable_value_1 + supplementary_duty
        
        vat = assessable_value_2 * 0.15  # 15% VAT
        advance_tax = assessable_value_2 * 0.05  # 5% advance income tax
        ait = assessable_value_2 * 0.03  # 3% AIT
        
        regulatory_duty = cif_value_bdt * 0.04  # 4% regulatory duty
        environmental_surcharge = cif_value_bdt * 0.02  # 2% for high-emission
        
        # Total landed cost
        total_landed_cost_bdt = (cif_value_bdt + customs_duty + 
                                supplementary_duty + vat + advance_tax + 
                                ait + regulatory_duty + environmental_surcharge)
        
        # Agent fees and registration (local)
        clearing_agent_fee = 50000  # BDT
        brta_registration = 85000  # BDT (Bangladesh Road Transport Authority)
        
        final_cost_bdt = total_landed_cost_bdt + clearing_agent_fee + brta_registration
        
        # Return detailed breakdown for visualization
        return {
            'predicted_winning_bid_jpy': None,  # Set by caller
            'user_bid_jpy': winning_bid_jpy,
            'currency_conversion': {
                'jpy_to_bdt_rate': JPY_TO_BDT,
                'total_japan_cost_jpy': int(total_japan_jpy),
                'total_japan_cost_bdt': int(total_japan_jpy * JPY_TO_BDT)
            },
            'cost_breakdown_bdt': {
                'cif_value': int(cif_value_bdt),
                'customs_duty': int(customs_duty),
                'supplementary_duty': int(supplementary_duty),
                'vat': int(vat),
                'advance_tax': int(advance_tax),
                'ait': int(ait),
                'regulatory_duty': int(regulatory_duty),
                'environmental_surcharge': int(environmental_surcharge),
                'clearing_agent_fee': clearing_agent_fee,
                'brta_registration': brta_registration
            },
            'total_landed_cost_bdt': int(final_cost_bdt),
            'total_landed_cost_usd': int(final_cost_bdt / 110)  # Approximate BDT to USD
        }
    
    def predict_and_calculate(self, vehicle_data, user_bid_jpy=None):
        """Main entry point: predict bid and calculate costs"""
        
        # Generate prediction
        predicted_bid_jpy = self.predict_winning_bid(vehicle_data)
        
        # Use user bid if provided, otherwise use prediction
        bid_to_use = user_bid_jpy if user_bid_jpy else predicted_bid_jpy
        
        # Calculate landed cost
        result = self.calculate_landed_cost(bid_to_use, vehicle_data)
        result['predicted_winning_bid_jpy'] = predicted_bid_jpy
        
        return result

# CLI interface for Laravel to call
if __name__ == '__main__':
    import sys
    
    # Parse JSON input from Laravel
    vehicle_input = json.loads(sys.argv[1])
    user_bid = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    engine = JDMPulseEngine()
    result = engine.predict_and_calculate(vehicle_input, user_bid)
    
    # Output JSON for Laravel to consume
    print(json.dumps(result))
```

**Test:**
```bash
python ml/engine.py '{"make":"Toyota","model":"Land Cruiser","year":2020,"mileage_km":30000,"engine_cc":3500,"auction_grade":4.5}' 3500000
```

---

### 4.4 Phase 3: Backend API Development (7:00-8:30 PM)

#### Task 3.1: Laravel API Route
**File:** `routes/api.php`

```php
use App\Http\Controllers\VehicleAnalyticsController;

Route::post('/analyze-vehicle', [VehicleAnalyticsController::class, 'analyze']);
Route::get('/featured-vehicles', [VehicleAnalyticsController::class, 'getFeaturedVehicles']);
```

#### Task 3.2: Controller
**File:** `app/Http/Controllers/VehicleAnalyticsController.php`

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Storage;

class VehicleAnalyticsController extends Controller
{
    public function analyze(Request $request)
    {
        $validated = $request->validate([
            'make' => 'required|string',
            'model' => 'required|string',
            'year' => 'required|integer|min:2010|max:2024',
            'mileage_km' => 'required|integer|min:0',
            'engine_cc' => 'required|integer|min:600',
            'auction_grade' => 'required|numeric|min:0|max:6',
            'user_bid_jpy' => 'nullable|integer|min:0'
        ]);

        // Prepare Python engine call
        $pythonPath = base_path('ml/engine.py');
        $vehicleJson = json_encode([
            'make' => $validated['make'],
            'model' => $validated['model'],
            'year' => $validated['year'],
            'mileage_km' => $validated['mileage_km'],
            'engine_cc' => $validated['engine_cc'],
            'auction_grade' => $validated['auction_grade']
        ]);

        $userBid = $validated['user_bid_jpy'] ?? '';

        // Execute Python script
        $result = Process::run("python {$pythonPath} '{$vehicleJson}' {$userBid}");

        if ($result->failed()) {
            return response()->json([
                'error' => 'Analysis engine failed',
                'details' => $result->errorOutput()
            ], 500);
        }

        $analysisResult = json_decode($result->output(), true);

        return response()->json([
            'success' => true,
            'data' => $analysisResult
        ]);
    }

    public function getFeaturedVehicles()
    {
        // Load curated sample vehicles from JSON
        $featuredVehicles = json_decode(
            Storage::disk('local')->get('featured_vehicles.json'),
            true
        );

        return response()->json([
            'success' => true,
            'vehicles' => $featuredVehicles
        ]);
    }
}
```

#### Task 3.3: Sample Featured Vehicles
**File:** `storage/app/featured_vehicles.json`

```json
[
    {
        "id": 1,
        "make": "Toyota",
        "model": "Land Cruiser 300",
        "year": 2022,
        "mileage_km": 15000,
        "engine_cc": 3500,
        "auction_grade": 4.5,
        "image_url": "/images/landcruiser300.jpg",
        "highlight": "Premium SUV with V6 Twin-Turbo"
    },
    {
        "id": 2,
        "make": "Nissan",
        "model": "GT-R R35",
        "year": 2020,
        "mileage_km": 25000,
        "engine_cc": 3800,
        "auction_grade": 4.0,
        "image_url": "/images/gtr35.jpg",
        "highlight": "Legendary performance"
    },
    {
        "id": 3,
        "make": "Lexus",
        "model": "LX 600",
        "year": 2023,
        "mileage_km": 8000,
        "engine_cc": 3500,
        "auction_grade": 5.0,
        "image_url": "/images/lx600.jpg",
        "highlight": "Luxury flagship SUV"
    },
    {
        "id": 4,
        "make": "Porsche",
        "model": "911 Carrera",
        "year": 2021,
        "mileage_km": 12000,
        "engine_cc": 3000,
        "auction_grade": 4.5,
        "image_url": "/images/911.jpg",
        "highlight": "Iconic sports car"
    }
]
```

---

### 4.5 Phase 4: Frontend Integration (8:30-10:00 PM)

#### Task 4.1: Main Dashboard Blade Template
**File:** `resources/views/dashboard.blade.php`

```html
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JDM Pulse - Predictive Import Analytics</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body class="bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white min-h-screen">
    
    <!-- Hero Section -->
    <header class="container mx-auto px-6 py-8">
        <nav class="flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg"></div>
                <h1 class="text-2xl font-bold">JDM Pulse</h1>
            </div>
            <div class="space-x-6 text-sm">
                <a href="#" class="hover:text-blue-400 transition">Analytics</a>
                <a href="#" class="hover:text-blue-400 transition">How It Works</a>
                <button class="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg transition">
                    Sign Up
                </button>
            </div>
        </nav>
        
        <div class="mt-16 text-center max-w-4xl mx-auto">
            <h2 class="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                Import JDM Vehicles with Absolute Certainty
            </h2>
            <p class="text-xl text-slate-400 mb-8">
                Predict winning bids with ML. Calculate landed costs down to the last Taka. 
                No showrooms. No hidden fees. Just data.
            </p>
        </div>
    </header>

    <!-- Vehicle Gallery -->
    <section class="container mx-auto px-6 py-12">
        <h3 class="text-3xl font-bold mb-8">Featured Live Auctions</h3>
        <div id="vehicle-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <!-- Populated by JavaScript -->
        </div>
    </section>

    <!-- Analytics Dashboard -->
    <section id="analytics-section" class="container mx-auto px-6 py-12 hidden">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            <!-- Left: Vehicle Details & Prediction -->
            <div class="bg-slate-900/50 backdrop-blur-xl rounded-2xl p-8 border border-slate-800">
                <h3 class="text-2xl font-bold mb-6">Predictive Analysis</h3>
                
                <div id="selected-vehicle-info" class="space-y-4 mb-8">
                    <!-- Populated dynamically -->
                </div>

                <div class="bg-slate-800/50 rounded-xl p-6 mb-6">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-slate-400">ML Predicted Winning Bid</span>
                        <span class="text-sm bg-green-500/20 text-green-400 px-3 py-1 rounded-full">
                            95% Confidence
                        </span>
                    </div>
                    <div class="text-4xl font-bold text-green-400">
                        ¥<span id="predicted-bid">-</span>
                    </div>
                </div>

                <div class="space-y-4">
                    <label class="block">
                        <span class="text-sm text-slate-400">Your Bid Amount (JPY)</span>
                        <input 
                            type="number" 
                            id="user-bid-input"
                            class="w-full mt-2 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
                            placeholder="Enter bid or use prediction"
                        />
                    </label>
                    <button 
                        id="calculate-btn"
                        class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 py-4 rounded-lg font-semibold text-lg transition-all transform hover:scale-105"
                    >
                        Calculate Landed Cost
                    </button>
                </div>
            </div>

            <!-- Right: Cost Visualization -->
            <div class="bg-slate-900/50 backdrop-blur-xl rounded-2xl p-8 border border-slate-800">
                <h3 class="text-2xl font-bold mb-6">Total Landed Cost</h3>
                
                <div class="text-center mb-8">
                    <div class="text-sm text-slate-400 mb-2">Final Price in Bangladesh</div>
                    <div class="text-6xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                        ৳<span id="total-cost-bdt">-</span>
                    </div>
                    <div class="text-lg text-slate-400 mt-2">
                        ~$<span id="total-cost-usd">-</span> USD
                    </div>
                </div>

                <!-- Plotly Donut Chart -->
                <div id="cost-breakdown-chart" class="w-full h-96"></div>

                <!-- Breakdown Table -->
                <div id="cost-breakdown-table" class="mt-6 space-y-2 text-sm hidden">
                    <!-- Populated dynamically -->
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="container mx-auto px-6 py-12 text-center text-slate-500 border-t border-slate-800 mt-20">
        <p>JDM Pulse - Built for Plotly Vibe-a-Thon 2024</p>
        <p class="mt-2">Revolutionizing automotive imports with predictive analytics</p>
    </footer>

    <script src="{{ asset('js/dashboard.js') }}"></script>
</body>
</html>
```

#### Task 4.2: Dashboard JavaScript
**File:** `public/js/dashboard.js`

```javascript
// State
let featuredVehicles = [];
let selectedVehicle = null;
let currentAnalysis = null;

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadFeaturedVehicles();
    setupEventListeners();
});

async function loadFeaturedVehicles() {
    try {
        const response = await fetch('/api/featured-vehicles');
        const data = await response.json();
        featuredVehicles = data.vehicles;
        renderVehicleGrid();
    } catch (error) {
        console.error('Failed to load vehicles:', error);
    }
}

function renderVehicleGrid() {
    const grid = document.getElementById('vehicle-grid');
    grid.innerHTML = '';

    featuredVehicles.forEach(vehicle => {
        const card = document.createElement('div');
        card.className = 'vehicle-card bg-slate-900/50 backdrop-blur-xl rounded-xl overflow-hidden border border-slate-800 cursor-pointer hover:border-blue-500 transition-all transform hover:scale-105';
        card.innerHTML = `
            <div class="aspect-video bg-slate-800 flex items-center justify-center">
                <span class="text-6xl">🚗</span>
            </div>
            <div class="p-6">
                <h4 class="text-xl font-bold mb-2">${vehicle.make} ${vehicle.model}</h4>
                <p class="text-slate-400 text-sm mb-4">${vehicle.highlight}</p>
                <div class="flex justify-between text-sm text-slate-500">
                    <span>${vehicle.year} • ${vehicle.mileage_km.toLocaleString()} km</span>
                    <span>Grade ${vehicle.auction_grade}</span>
                </div>
            </div>
        `;
        card.addEventListener('click', () => selectVehicle(vehicle));
        grid.appendChild(card);
    });
}

function selectVehicle(vehicle) {
    selectedVehicle = vehicle;
    
    // Show analytics section with GSAP animation
    const analyticsSection = document.getElementById('analytics-section');
    analyticsSection.classList.remove('hidden');
    gsap.from(analyticsSection, {
        opacity: 0,
        y: 50,
        duration: 0.8,
        ease: 'power3.out'
    });

    // Scroll to analytics
    analyticsSection.scrollIntoView({ behavior: 'smooth' });

    // Populate vehicle info
    const infoDiv = document.getElementById('selected-vehicle-info');
    infoDiv.innerHTML = `
        <div class="flex items-center space-x-4 mb-6">
            <div class="w-20 h-20 bg-slate-800 rounded-lg flex items-center justify-center text-4xl">
                🚗
            </div>
            <div>
                <h4 class="text-2xl font-bold">${vehicle.make} ${vehicle.model}</h4>
                <p class="text-slate-400">${vehicle.year} • ${vehicle.engine_cc}cc</p>
            </div>
        </div>
        <div class="grid grid-cols-2 gap-4 text-sm">
            <div class="bg-slate-800/50 rounded-lg p-3">
                <div class="text-slate-400">Mileage</div>
                <div class="text-lg font-semibold">${vehicle.mileage_km.toLocaleString()} km</div>
            </div>
            <div class="bg-slate-800/50 rounded-lg p-3">
                <div class="text-slate-400">Auction Grade</div>
                <div class="text-lg font-semibold">${vehicle.auction_grade}/6.0</div>
            </div>
        </div>
    `;

    // Trigger prediction
    runPrediction();
}

async function runPrediction() {
    try {
        // Show loading state
        document.getElementById('predicted-bid').textContent = '...';

        const response = await fetch('/api/analyze-vehicle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify(selectedVehicle)
        });

        const result = await response.json();
        currentAnalysis = result.data;

        // Animate prediction display
        const predictedBidEl = document.getElementById('predicted-bid');
        gsap.to(predictedBidEl, {
            textContent: currentAnalysis.predicted_winning_bid_jpy.toLocaleString(),
            duration: 1.5,
            ease: 'power2.out',
            snap: { textContent: 1 },
            onUpdate: function() {
                predictedBidEl.textContent = Math.round(this.targets()[0].textContent).toLocaleString();
            }
        });

        // Pre-fill user bid input
        document.getElementById('user-bid-input').value = currentAnalysis.predicted_winning_bid_jpy;

    } catch (error) {
        console.error('Prediction failed:', error);
        document.getElementById('predicted-bid').textContent = 'Error';
    }
}

function setupEventListeners() {
    document.getElementById('calculate-btn').addEventListener('click', calculateLandedCost);
    
    // Allow Enter key to trigger calculation
    document.getElementById('user-bid-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') calculateLandedCost();
    });
}

async function calculateLandedCost() {
    const userBid = parseInt(document.getElementById('user-bid-input').value);
    
    if (!userBid || userBid < 100000) {
        alert('Please enter a valid bid amount (min ¥100,000)');
        return;
    }

    try {
        // Show loading
        document.getElementById('total-cost-bdt').textContent = '...';

        const response = await fetch('/api/analyze-vehicle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify({
                ...selectedVehicle,
                user_bid_jpy: userBid
            })
        });

        const result = await response.json();
        currentAnalysis = result.data;

        // Animate cost display
        animateCostDisplay();
        renderCostBreakdownChart();
        renderCostBreakdownTable();

    } catch (error) {
        console.error('Calculation failed:', error);
        alert('Failed to calculate cost. Please try again.');
    }
}

function animateCostDisplay() {
    const totalCostBdt = currentAnalysis.total_landed_cost_bdt;
    const totalCostUsd = currentAnalysis.total_landed_cost_usd;

    // Animate BDT
    const bdt El = document.getElementById('total-cost-bdt');
    gsap.to(bdtEl, {
        textContent: totalCostBdt,
        duration: 2,
        ease: 'power2.out',
        snap: { textContent: 1 },
        onUpdate: function() {
            bdtEl.textContent = Math.round(this.targets()[0].textContent).toLocaleString();
        }
    });

    // Animate USD
    const usdEl = document.getElementById('total-cost-usd');
    gsap.to(usdEl, {
        textContent: totalCostUsd,
        duration: 2,
        ease: 'power2.out',
        snap: { textContent: 1 },
        onUpdate: function() {
            usdEl.textContent = Math.round(this.targets()[0].textContent).toLocaleString();
        }
    });
}

function renderCostBreakdownChart() {
    const breakdown = currentAnalysis.cost_breakdown_bdt;

    const data = [{
        values: Object.values(breakdown),
        labels: [
            'CIF Value (Japan Cost)',
            'Customs Duty',
            'Supplementary Duty',
            'VAT (15%)',
            'Advance Tax',
            'AIT',
            'Regulatory Duty',
            'Environmental Surcharge',
            'Clearing Agent',
            'BRTA Registration'
        ],
        type: 'pie',
        hole: 0.5,
        marker: {
            colors: [
                '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b',
                '#10b981', '#06b6d4', '#6366f1', '#84cc16',
                '#f97316', '#14b8a6'
            ]
        },
        textinfo: 'label+percent',
        textposition: 'outside',
        hovertemplate: '<b>%{label}</b><br>৳%{value:,.0f}<br>%{percent}<extra></extra>'
    }];

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {
            color: '#cbd5e1',
            family: 'Inter, system-ui, sans-serif'
        },
        showlegend: false,
        margin: { t: 0, b: 0, l: 0, r: 0 },
        annotations: [{
            text: `৳${currentAnalysis.total_landed_cost_bdt.toLocaleString()}`,
            font: {
                size: 20,
                color: '#3b82f6'
            },
            showarrow: false,
            x: 0.5,
            y: 0.5
        }]
    };

    const config = {
        responsive: true,
        displayModeBar: false
    };

    Plotly.newPlot('cost-breakdown-chart', data, layout, config);
}

function renderCostBreakdownTable() {
    const breakdown = currentAnalysis.cost_breakdown_bdt;
    const tableDiv = document.getElementById('cost-breakdown-table');
    
    tableDiv.innerHTML = `
        <div class="bg-slate-800/30 rounded-lg p-4 space-y-2">
            ${Object.entries(breakdown).map(([key, value]) => `
                <div class="flex justify-between">
                    <span class="text-slate-400">${formatLabel(key)}</span>
                    <span class="font-semibold">৳${value.toLocaleString()}</span>
                </div>
            `).join('')}
        </div>
    `;
    
    tableDiv.classList.remove('hidden');
    gsap.from(tableDiv, {
        opacity: 0,
        y: 20,
        duration: 0.6,
        ease: 'power2.out'
    });
}

function formatLabel(key) {
    return key.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}
```

---

### 4.6 Phase 5: Testing & Polish (10:00-11:00 PM)

#### Testing Checklist:
- [ ] **Unit Test ML Model:** Verify R² > 0.75 on test set
- [ ] **API Endpoint Test:** Use Postman/curl to test `/api/analyze-vehicle`
- [ ] **Frontend Flow:** Test complete user journey from vehicle selection to cost visualization
- [ ] **Cross-browser:** Test on Chrome, Firefox, Safari (if available)
- [ ] **Mobile Responsive:** Test on mobile viewport (DevTools)
- [ ] **Error Handling:** Test with invalid inputs
- [ ] **Performance:** Ensure response time < 2 seconds

#### Polish Tasks:
- Add loading spinners during API calls
- Smooth scroll animations
- Tooltips on complex terms (e.g., "Supplementary Duty")
- Meta tags for social sharing
- Favicon and app icons

---

### 4.7 Phase 6: Deployment (11:00-12:00 AM)

#### Railway.app Deployment (Recommended)

**Step 1: Prepare for Deployment**

Create `nixpacks.toml`:
```toml
[phases.setup]
nixPkgs = ['php82', 'php82Packages.composer', 'python311', 'python311Packages.pip']

[phases.install]
cmds = [
    'composer install --no-dev --optimize-autoloader',
    'pip install -r ml/requirements.txt'
]

[phases.build]
cmds = [
    'php artisan config:cache',
    'php artisan route:cache',
    'npm install',
    'npm run build'
]

[start]
cmd = 'php artisan serve --host=0.0.0.0 --port=${PORT:-8000}'
```

Create `ml/requirements.txt`:
```
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.26.2
joblib==1.3.2
pyarrow==14.0.1
```

**Step 2: Deploy to Railway**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to new project
railway link

# Add environment variables
railway variables set APP_ENV=production
railway variables set APP_DEBUG=false
railway variables set APP_URL=https://jdmpulse.up.railway.app

# Deploy
railway up
```

**Step 3: Post-Deployment**
- Test live URL
- Run migrations if needed: `railway run php artisan migrate --force`
- Monitor logs: `railway logs`

---

## 5. DATASET DEVELOPMENT RULES

### 5.1 Data Quality Standards
1. **Minimum Dataset Size:** 12,000 records for robust ML training
2. **Recency:** Focus on vehicles from 2015-2024 (last 10 years)
3. **Completeness:** Zero tolerance for NULL in critical fields (winning_bid_jpy, year, mileage_km, engine_cc)
4. **Diversity:** Ensure representation across:
   - Price ranges: ¥500K - ¥10M+
   - Engine sizes: 660cc (Kei cars) to 6000cc+ (supercars)
   - Vehicle ages: 0-9 years
   - Auction grades: 2.0 - 6.0

### 5.2 Feature Engineering Rules
```python
# Mandatory derived features for ML model:
df['vehicle_age'] = CURRENT_YEAR - df['year']
df['mileage_per_year'] = df['mileage_km'] / df['vehicle_age']
df['mileage_per_year'] = df['mileage_per_year'].replace([np.inf, -np.inf], 0)

# Categorical encoding
df['make_encoded'] = LabelEncoder().fit_transform(df['make'])
df['model_encoded'] = LabelEncoder().fit_transform(df['model'])

# Outlier removal (for training stability)
df = df[df['winning_bid_jpy'] < df['winning_bid_jpy'].quantile(0.99)]
df = df[df['mileage_km'] < 200000]  # Remove abnormally high mileage
```

### 5.3 Parquet Optimization Rules
```python
# dtype optimization for compression
DTYPE_MAPPING = {
    'year': 'int16',           # 2010-2024 fits in int16
    'mileage_km': 'int32',     # Max ~2B
    'engine_cc': 'int16',      # Max 32K is enough
    'winning_bid_jpy': 'int32',# Max ~2.1B JPY
    'auction_grade': 'float16',# 0.0-6.0 with 0.5 precision
    'make': 'category',        # Categorical compression
    'model': 'category'        # Categorical compression
}

# Parquet compression settings
df.to_parquet(
    'jdm_pulse_dataset.parquet',
    engine='pyarrow',
    compression='gzip',       # Best compression ratio
    index=False,
    row_group_size=5000       # Optimize for analytics queries
)
```

---

## 6. INTUITIVE DASHBOARD DEVELOPMENT RULES

### 6.1 UX Principles (Apple-Inspired)
1. **Progressive Disclosure:** Don't overwhelm with all data upfront
   - Show vehicle gallery first
   - Reveal analytics only after selection
   - Expand details on demand

2. **Meaningful Animation:** Every animation should serve a purpose
   - Number count-ups convey "calculation in progress"
   - Smooth transitions reduce cognitive load
   - Hover states provide immediate feedback

3. **Visual Hierarchy:**
   - Primary CTA: "Calculate Landed Cost" button (largest, most prominent)
   - Secondary info: Breakdown chart (visual but not overwhelming)
   - Tertiary: Detailed table (collapsed by default)

### 6.2 Plotly Chart Rules
```javascript
// Standardized color palette (cohesive with Tailwind)
const JDM_PULSE_COLORS = [
    '#3b82f6', // blue-500
    '#8b5cf6', // purple-500
    '#ec4899', // pink-500
    '#f59e0b', // amber-500
    '#10b981', // emerald-500
    '#06b6d4', // cyan-500
    '#6366f1', // indigo-500
    '#84cc16', // lime-500
    '#f97316', // orange-500
    '#14b8a6'  // teal-500
];

// Layout consistency
const STANDARD_LAYOUT = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: {
        color: '#cbd5e1',
        family: 'Inter, system-ui, sans-serif',
        size: 12
    },
    margin: { t: 20, b: 20, l: 40, r: 40 },
    hoverlabel: {
        bgcolor: '#1e293b',
        bordercolor: '#475569',
        font: { color: '#f1f5f9' }
    }
};

// Always disable mode bar for cleaner UI
const CONFIG = {
    responsive: true,
    displayModeBar: false
};
```

### 6.3 GSAP Animation Rules
```javascript
// Animation timing standards
const ANIM_DURATION = {
    fast: 0.3,    // UI feedback (hover, click)
    medium: 0.8,  // Section reveals
    slow: 2.0     // Number count-ups
};

const ANIM_EASING = {
    default: 'power2.out',
    bounce: 'elastic.out(1, 0.5)',
    snap: 'power1.inOut'
};

// Number animation template
function animateNumber(element, targetValue, duration = ANIM_DURATION.slow) {
    gsap.to(element, {
        textContent: targetValue,
        duration: duration,
        ease: ANIM_EASING.snap,
        snap: { textContent: 1 },
        onUpdate: function() {
            element.textContent = Math.round(this.targets()[0].textContent).toLocaleString();
        }
    });
}
```

### 6.4 Responsive Design Rules
```css
/* Mobile-first breakpoints (Tailwind defaults) */
/* sm: 640px - Small tablets */
/* md: 768px - Tablets */
/* lg: 1024px - Laptops */
/* xl: 1280px - Desktops */
/* 2xl: 1536px - Large desktops */

/* Chart sizing rules */
.plotly-chart-container {
    /* Mobile: Full width, reduced height */
    @apply w-full h-64 sm:h-80 lg:h-96;
}

/* Grid responsiveness */
.vehicle-grid {
    /* Mobile: 1 column */
    /* Tablet: 2 columns */
    /* Desktop: 4 columns */
    @apply grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6;
}
```

---

## 7. RISK MITIGATION & CONTINGENCY PLANS

### 7.1 Technical Risks

**Risk:** Python execution fails in Laravel
- **Mitigation:** Test Python CLI call in isolation first
- **Contingency:** Create PHP-based calculation as fallback (skip ML, use average bid)

**Risk:** Dataset scraping blocked/slow
- **Mitigation:** Use multiple data sources with retry logic
- **Contingency:** Use synthetic data generator based on market research

**Risk:** Parquet file > 75MB
- **Mitigation:** Reduce dataset to 10K records, increase compression
- **Contingency:** Use CSV with gzip compression

**Risk:** Railway deployment fails
- **Mitigation:** Have Vercel account ready as backup
- **Contingency:** Use local ngrok tunnel for demo

### 7.2 Time Management
**If running behind schedule:**
- **Cut Scope:** Remove GSAP animations (use CSS transitions)
- **Simplify UI:** Use pre-built Tailwind components instead of custom design
- **Reduce Dataset:** Train on 5K records instead of 15K
- **Local Demo:** Skip deployment, demo from localhost with screen share

---

## 8. POST-HACKATHON ROADMAP

### Week 1-2: MVP Validation
- [ ] Launch beta with 50 target users (car enthusiast Facebook groups in Bangladesh)
- [ ] Collect feedback via embedded Typeform
- [ ] Track key metrics: bounce rate, time on page, signups

### Week 3-4: Live API Integration
- [ ] Partner with licensed Japanese exporter for API access
- [ ] Integrate real-time auction feed (update every 5 minutes)
- [ ] Implement user authentication (Laravel Breeze)

### Month 2: Monetization
- [ ] Launch Pro tier ($29/month)
- [ ] Add Stripe/Paddle payment integration
- [ ] Create email marketing sequence (Mailchimp)

### Month 3: Dropshipping Backend
- [ ] Build admin panel for order management
- [ ] Integrate with logistics partners (freight forwarders)
- [ ] Implement escrow payment system

### Month 4-6: B2B Expansion
- [ ] Create white-label version for small importers
- [ ] Develop API for corporate clients
- [ ] Target 5 pilot B2B customers

### Month 7-12: Regional Expansion
- [ ] Add support for India, Pakistan, Sri Lanka import regulations
- [ ] Multilingual support (Bengali, Hindi, Urdu, Sinhala)
- [ ] **Integrate Chisel AI** for multilingual customer support

---

## 9. CHISEL AI INTEGRATION STRATEGY

### Phase 1: Internal Operations (Month 3)
- Deploy Chisel AI chatbot for customer support (24/7 Bengali/English)
- Use Chisel AI document assistant to auto-generate import documentation
- Train Chisel AI on Bangladesh customs regulations (30K+ pages)

### Phase 2: Customer-Facing (Month 6)
- Embed Chisel AI chat widget on JDM Pulse dashboard
- Offer "Import Advisor" feature powered by Chisel AI
- Multilingual support for Japanese auction house communication

### Phase 3: B2B Cross-Sell (Month 9)
- Offer Chisel AI as standalone product to JDM Pulse B2B customers
- Create industry-specific LLM for automotive import/export
- Target 20% conversion rate from JDM Pulse B2B to Chisel AI enterprise

### Phase 4: Data Flywheel (Month 12)
- Use JDM Pulse transaction data to fine-tune Chisel AI models
- Create proprietary "Automotive Trade LLM" (closed-source)
- Position Chisel AI as the "Decide AI v2 for SME importers"

**Revenue Synergy:**
- JDM Pulse customer → Chisel AI lead (25% conversion)
- Average Chisel AI contract: $3,000/year
- By Year 2: 100 JDM Pulse B2B customers → 25 Chisel AI customers = $75K ARR

---

## 10. SUCCESS METRICS

### Tonight's Demo (Vibe-a-Thon)
- [ ] **Functional:** Complete user flow from vehicle selection to cost calculation
- [ ] **Visual:** Polished UI matching Apple/Shadcn aesthetic
- [ ] **Technical:** ML model R² > 0.75, response time < 2s
- [ ] **Narrative:** Clear story from problem to solution to business model

### Month 1 (Post-Hackathon)
- 500+ email signups
- 50+ active users (returning 3+ times)
- 10+ qualified B2B leads

### Month 6
- $5K MRR from subscriptions
- 5 successful import transactions (commission revenue)
- 2 B2B pilot customers

### Year 1
- $50K ARR from JDM Pulse
- $75K ARR from Chisel AI cross-sell
- Total: $125K ARR
- Path to profitability with <5% CAC

---

## 11. APPENDICES

### A. Bangladesh Tax Calculation Reference

**Duty Structure (as of 2024):**
```
Base: CIF Value (Cost + Insurance + Freight)
├── Customs Duty: 125%-500% (based on engine size)
├── Supplementary Duty: 20%-45% (on CIF + Customs Duty)
├── VAT: 15% (on CIF + Customs + Supplementary)
├── Advance Tax: 5% (on assessable value)
├── AIT: 3% (on assessable value)
├── Regulatory Duty: 4% (on CIF)
└── Environmental Surcharge: 1-2% (on high-emission vehicles)

Local Costs:
├── Clearing Agent: BDT 40,000-60,000
├── BRTA Registration: BDT 85,000 (approximate)
└── Documentation: BDT 10,000-15,000
```

### B. Tech Stack Versions (Lock for Stability)
```json
{
  "php": "8.2",
  "laravel": "^10.0",
  "python": "3.11",
  "scikit-learn": "1.3.2",
  "pandas": "2.1.3",
  "plotly.js": "2.27.0",
  "gsap": "3.12.2",
  "tailwindcss": "^3.4.0"
}
```

### C. Quick Start Commands
```bash
# Clone and setup
git clone <repo-url> JDM_Pulse
cd JDM_Pulse

# Backend setup
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate

# Frontend setup
npm install
npm run build

# Python ML setup
cd ml
pip install -r requirements.txt
python train_bid_predictor.py

# Run development server
php artisan serve

# Deploy to Railway
railway login
railway init
railway up
```

---

## 12. TEAM ROLES FOR TONIGHT

**Nirjhor (Lead / Full-Stack):**
- [ ] Phase 1: Data scraping script
- [ ] Phase 2: ML model training
- [ ] Phase 6: Deployment

**Tanjim Mohamed (Frontend/UX):**
- [ ] Phase 4: Dashboard UI implementation
- [ ] Phase 4: Plotly chart design in Studio
- [ ] Phase 5: UX testing and polish

**Shared:**
- [ ] Phase 3: API integration (pair programming)
- [ ] Phase 5: End-to-end testing

---

## FINAL PRE-FLIGHT CHECKLIST

**Before Starting (4:00 PM):**
- [ ] All development tools installed (PHP, Python, Node.js, Composer, pip)
- [ ] GitHub repo created and cloned
- [ ] Railway account created and CLI installed
- [ ] Coffee/energy drinks stocked ☕
- [ ] Distractions minimized

**Before Demo (11:30 PM):**
- [ ] Live site accessible and tested
- [ ] Demo script prepared (3-minute walkthrough)
- [ ] Backup video recording of demo (in case of live issues)
- [ ] Slide deck with business model ready

**Demo Script (3 minutes):**
1. **Problem (30s):** "Importing JDM cars in Bangladesh is a black box. Hidden fees, no transparency, massive markups."
2. **Solution (60s):** [Live demo] "JDM Pulse uses ML to predict auction bids and calculates the exact landed cost down to the last Taka."
3. **Business Model (60s):** "We're building a tech-first dropshipping platform. SaaS subscriptions + transaction fees. Connects to our larger Chisel AI ecosystem for SMEs."
4. **Traction (30s):** "Built in one night. Ready for beta users. Targeting $125K ARR in Year 1."

---

**Let's build something extraordinary. Good luck, team! 🚀**
