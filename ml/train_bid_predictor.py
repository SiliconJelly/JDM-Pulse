"""
JDM Pulse - ML Model Training Script
Trains a GradientBoostingRegressor to predict Japanese auction winning bids
Target: R² > 0.75 on test set
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import sys

# Constants
CURRENT_YEAR = 2024
DATA_PATH = '../data/jdm_pulse_dataset.parquet'
MODEL_DIR = '../models'
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Model hyperparameters (optimized for tabular data)
MODEL_PARAMS = {
    'n_estimators': 200,
    'learning_rate': 0.1,
    'max_depth': 5,
    'min_samples_split': 10,
    'min_samples_leaf': 4,
    'subsample': 0.8,
    'random_state': RANDOM_STATE,
    'verbose': 1
}


def load_dataset():
    """Load the Parquet dataset"""
    print("=" * 60)
    print("LOADING DATASET")
    print("=" * 60)
    
    data_path = os.path.join(os.path.dirname(__file__), DATA_PATH)
    
    if not os.path.exists(data_path):
        print(f"❌ ERROR: Dataset not found at {data_path}")
        print("\nPlease run the data acquisition scripts first:")
        print("1. python scripts\\scrape_auction_data.py")
        print("2. python scripts\\convert_to_parquet.py")
        sys.exit(1)
    
    print(f"Loading: {data_path}")
    df = pd.read_parquet(data_path)
    
    print(f"✓ Loaded {len(df):,} records")
    print(f"✓ Columns: {list(df.columns)}")
    
    return df


def feature_engineering(df):
    """
    Create derived features for better prediction accuracy
    """
    print("\n" + "=" * 60)
    print("FEATURE ENGINEERING")
    print("=" * 60)
    
    df = df.copy()
    
    # Derived features
    print("Creating derived features...")
    
    # 1. Vehicle age (critical predictor)
    df['vehicle_age'] = CURRENT_YEAR - df['year']
    
    # 2. Mileage per year (wear indicator)
    df['mileage_per_year'] = df['mileage_km'] / df['vehicle_age']
    # Handle edge case: brand new cars
    df['mileage_per_year'] = df['mileage_per_year'].replace([np.inf, -np.inf], 0)
    
    # 3. Engine size categories (luxury vs economy)
    df['is_luxury_engine'] = (df['engine_cc'] >= 3000).astype(int)
    
    # 4. High grade indicator
    df['is_high_grade'] = (df['auction_grade'] >= 4.5).astype(int)
    
    # 5. Price per CC (value density indicator)
    df['price_per_cc'] = df['winning_bid_jpy'] / df['engine_cc']
    
    print(f"✓ Created 5 derived features")
    print(f"✓ Total features available: {len(df.columns)}")
    
    return df


def encode_categoricals(df):
    """
    Encode categorical variables (make, model)
    """
    print("\n" + "=" * 60)
    print("ENCODING CATEGORICAL VARIABLES")
    print("=" * 60)
    
    # Initialize encoders
    le_make = LabelEncoder()
    le_model = LabelEncoder()
    
    # Encode make and model
    df['make_encoded'] = le_make.fit_transform(df['make'])
    df['model_encoded'] = le_model.fit_transform(df['model'])
    
    print(f"✓ Encoded 'make': {len(le_make.classes_)} unique values")
    print(f"  Classes: {', '.join(le_make.classes_)}")
    
    print(f"✓ Encoded 'model': {len(le_model.classes_)} unique values")
    
    # Save encoders for prediction
    model_dir = os.path.join(os.path.dirname(__file__), MODEL_DIR)
    os.makedirs(model_dir, exist_ok=True)
    
    joblib.dump(le_make, os.path.join(model_dir, 'make_encoder.joblib'))
    joblib.dump(le_model, os.path.join(model_dir, 'model_encoder.joblib'))
    
    print(f"✓ Saved encoders to {model_dir}")
    
    return df, le_make, le_model


def prepare_features(df):
    """
    Prepare feature matrix X and target vector y
    """
    print("\n" + "=" * 60)
    print("PREPARING FEATURES")
    print("=" * 60)
    
    # Define features for model training
    feature_columns = [
        'vehicle_age',
        'mileage_km',
        'engine_cc',
        'auction_grade',
        'make_encoded',
        'model_encoded',
        'mileage_per_year',
        'is_luxury_engine',
        'is_high_grade'
    ]
    
    # Target variable
    target = 'winning_bid_jpy'
    
    X = df[feature_columns]
    y = df[target]
    
    print(f"✓ Features: {len(feature_columns)}")
    print(f"  {', '.join(feature_columns)}")
    print(f"✓ Target: {target}")
    print(f"✓ Dataset shape: {X.shape}")
    
    return X, y, feature_columns


def train_model(X_train, y_train):
    """
    Train GradientBoostingRegressor model
    """
    print("\n" + "=" * 60)
    print("TRAINING MODEL")
    print("=" * 60)
    
    print("Model: GradientBoostingRegressor (point estimate)")
    print(f"Parameters: {MODEL_PARAMS}")
    print()
    
    model = GradientBoostingRegressor(**MODEL_PARAMS)
    
    print("Training in progress...")
    model.fit(X_train, y_train)
    
    print("✓ Training complete!")
    
    return model


def train_quantile_model(X_train, y_train, alpha: float):
    """
    Train a Quantile GradientBoostingRegressor for the given alpha.
    """
    print("\n" + "=" * 60)
    print(f"TRAINING QUANTILE MODEL (alpha={alpha})")
    print("=" * 60)
    params = MODEL_PARAMS.copy()
    params.update({
        'loss': 'quantile',
        'alpha': alpha,
        'verbose': 0,
    })
    q_model = GradientBoostingRegressor(**params)
    q_model.fit(X_train, y_train)
    print(f"✓ Quantile model (alpha={alpha}) trained")
    return q_model


def evaluate_model(model, X_train, y_train, X_test, y_test):
    """
    Evaluate model performance on train and test sets
    """
    print("\n" + "=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)
    
    # Training set predictions
    train_pred = model.predict(X_train)
    train_r2 = r2_score(y_train, train_pred)
    train_mae = mean_absolute_error(y_train, train_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    
    # Test set predictions
    test_pred = model.predict(X_test)
    test_r2 = r2_score(y_test, test_pred)
    test_mae = mean_absolute_error(y_test, test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    
    print("\n📊 TRAINING SET PERFORMANCE:")
    print(f"  R² Score:  {train_r2:.4f}")
    print(f"  MAE:       ¥{train_mae:,.0f}")
    print(f"  RMSE:      ¥{train_rmse:,.0f}")
    
    print("\n📊 TEST SET PERFORMANCE:")
    print(f"  R² Score:  {test_r2:.4f}")
    print(f"  MAE:       ¥{test_mae:,.0f}")
    print(f"  RMSE:      ¥{test_rmse:,.0f}")
    
    # Success criteria
    print("\n" + "=" * 60)
    if test_r2 >= 0.75:
        print("✓ SUCCESS! Model meets R² > 0.75 requirement")
    else:
        print(f"⚠ WARNING: Model R² ({test_r2:.4f}) below 0.75 target")
        print("  Consider:")
        print("  - Adding more features")
        print("  - Tuning hyperparameters")
        print("  - Collecting more data")
    print("=" * 60)
    
    # Feature importance
    print("\n📈 TOP 5 FEATURE IMPORTANCE:")
    feature_names = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else [f"feature_{i}" for i in range(len(model.feature_importances_))]
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in importance_df.head(5).iterrows():
        print(f"  {row['feature']:<20} {row['importance']:.4f}")
    
    return {
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse
    }


def save_model(model):
    """
    Save trained model to disk
    """
    print("\n" + "=" * 60)
    print("SAVING MODEL")
    print("=" * 60)
    
    model_dir = os.path.join(os.path.dirname(__file__), MODEL_DIR)
    model_path = os.path.join(model_dir, 'bid_predictor_model.joblib')
    
    joblib.dump(model, model_path)
    
    file_size_mb = os.path.getsize(model_path) / 1024 / 1024
    print(f"✓ Model saved to: {model_path}")
    print(f"  File size: {file_size_mb:.2f} MB")


def save_quantile_models(models: dict):
    model_dir = os.path.join(os.path.dirname(__file__), MODEL_DIR)
    os.makedirs(model_dir, exist_ok=True)
    for name, m in models.items():
        path = os.path.join(model_dir, f"bid_predictor_{name}.joblib")
        joblib.dump(m, path)
        size_mb = os.path.getsize(path) / 1024 / 1024
        print(f"✓ Quantile model saved: {path} ({size_mb:.2f} MB)")


def test_sample_predictions(model, X_test, y_test, feature_columns):
    """
    Test model on sample vehicles
    """
    print("\n" + "=" * 60)
    print("SAMPLE PREDICTIONS")
    print("=" * 60)
    
    # Get 5 random samples
    sample_indices = np.random.choice(len(X_test), size=min(5, len(X_test)), replace=False)
    
    for i, idx in enumerate(sample_indices, 1):
        actual = y_test.iloc[idx]
        predicted = model.predict(X_test.iloc[[idx]])[0]
        error_pct = abs(predicted - actual) / actual * 100
        
        print(f"\nSample {i}:")
        print(f"  Actual:    ¥{actual:,.0f}")
        print(f"  Predicted: ¥{predicted:,.0f}")
        print(f"  Error:     {error_pct:.1f}%")


def main():
    """
    Main training pipeline
    """
    print("=" * 60)
    print("JDM PULSE - ML MODEL TRAINING")
    print("=" * 60)
    print(f"Target: R² > 0.75")
    print(f"Algorithm: GradientBoostingRegressor")
    print()
    
    # Step 1: Load dataset
    df = load_dataset()
    
    # Step 2: Feature engineering
    df = feature_engineering(df)
    
    # Step 3: Encode categoricals
    df, le_make, le_model = encode_categoricals(df)
    
    # Step 4: Prepare features
    X, y, feature_columns = prepare_features(df)
    
    # Step 5: Split data
    print("\n" + "=" * 60)
    print("SPLITTING DATA")
    print("=" * 60)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=TEST_SIZE, 
        random_state=RANDOM_STATE
    )
    
    print(f"✓ Training set: {len(X_train):,} records ({(1-TEST_SIZE)*100:.0f}%)")
    print(f"✓ Test set:     {len(X_test):,} records ({TEST_SIZE*100:.0f}%)")
    
    # Step 6: Train point-estimate model
    model = train_model(X_train, y_train)

    # Step 6b: Train quantile models (q20, q50, q80)
    q20_model = train_quantile_model(X_train, y_train, alpha=0.20)
    q50_model = train_quantile_model(X_train, y_train, alpha=0.50)
    q80_model = train_quantile_model(X_train, y_train, alpha=0.80)

    # Step 7: Evaluate model
    metrics = evaluate_model(model, X_train, y_train, X_test, y_test)
    
    # Step 8: Save models
    save_model(model)
    save_quantile_models({
        'q20': q20_model,
        'q50': q50_model,
        'q80': q80_model,
    })
    
    # Step 9: Test sample predictions
    test_sample_predictions(model, X_test, y_test, feature_columns)
    
    # Final summary
    print("\n" + "=" * 60)
    print("✓ TRAINING COMPLETE!")
    print("=" * 60)
    
    print("\nModel artifacts created:")
    print("  ✓ models/bid_predictor_model.joblib")
    print("  ✓ models/make_encoder.joblib")
    print("  ✓ models/model_encoder.joblib")
    
    print("\nNext steps:")
    print("  1. Create ml/engine.py (prediction engine)")
    print("  2. Test engine with sample vehicle")
    print("  3. Proceed to Phase 3: Laravel API integration")
    
    return metrics['test_r2'] >= 0.75


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
