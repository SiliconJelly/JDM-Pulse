"""
JDM Pulse - CSV to Parquet Converter
Converts temporary CSV data to optimized Parquet format for ML training
Target: < 75MB final file size with gzip compression
"""

import pandas as pd
import numpy as np
import os
import sys

# File paths
CSV_FILE = 'temp_auction_data.csv'
PARQUET_FILE = 'jdm_pulse_dataset.parquet'
MAX_FILE_SIZE_MB = 75

def optimize_datatypes(df):
    """
    Optimize DataFrame column datatypes for maximum compression
    """
    print("Optimizing data types for compression...")
    
    # Integer optimizations
    df['year'] = df['year'].astype('int16')           # 2015-2024 fits in int16
    df['mileage_km'] = df['mileage_km'].astype('int32')  # Max ~2.1B
    df['engine_cc'] = df['engine_cc'].astype('int16')    # Max 32K
    df['winning_bid_jpy'] = df['winning_bid_jpy'].astype('int32')  # Max ~2.1B
    
    # Float optimizations
    df['auction_grade'] = df['auction_grade'].astype('float16')  # 0.0-6.0
    
    # Categorical compressions (huge space savings)
    df['make'] = df['make'].astype('category')
    df['model'] = df['model'].astype('category')
    
    # Date optimization
    df['auction_date'] = pd.to_datetime(df['auction_date'])
    
    print("✓ Data types optimized")
    return df


def clean_data(df):
    """
    Perform final data cleaning before Parquet conversion
    """
    print("\nCleaning data...")
    
    initial_count = len(df)
    
    # Remove any remaining nulls
    df = df.dropna()
    
    # Remove outliers for training stability
    # Remove top 1% of bids (potential data errors)
    df = df[df['winning_bid_jpy'] < df['winning_bid_jpy'].quantile(0.99)]
    
    # Remove abnormally high mileage
    df = df[df['mileage_km'] < 200000]
    
    # Ensure data quality
    df = df[
        (df['year'] >= 2015) & 
        (df['year'] <= 2024) &
        (df['mileage_km'] > 0) &
        (df['engine_cc'] >= 600) &
        (df['auction_grade'] >= 0) &
        (df['auction_grade'] <= 6.0) &
        (df['winning_bid_jpy'] >= 100000)
    ]
    
    removed_count = initial_count - len(df)
    print(f"✓ Removed {removed_count} outlier/invalid records")
    print(f"✓ Final dataset: {len(df)} records")
    
    return df


def convert_to_parquet():
    """
    Main conversion function
    """
    print("=" * 60)
    print("JDM PULSE - CSV to Parquet Conversion")
    print("=" * 60)
    print(f"Target file size: < {MAX_FILE_SIZE_MB}MB")
    print()
    
    # Locate CSV file
    csv_path = os.path.join(os.path.dirname(__file__), '..', CSV_FILE)
    
    if not os.path.exists(csv_path):
        print(f"❌ ERROR: CSV file not found at {csv_path}")
        print("\nPlease run scrape_auction_data.py first!")
        sys.exit(1)
    
    # Load CSV
    print(f"Loading {CSV_FILE}...")
    df = pd.read_csv(csv_path)
    print(f"✓ Loaded {len(df)} records")
    
    # Clean data
    df = clean_data(df)
    
    # Optimize data types
    df = optimize_datatypes(df)
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Convert to Parquet with optimal compression
    parquet_path = os.path.join(data_dir, PARQUET_FILE)
    
    print("\n" + "=" * 60)
    print("CONVERTING TO PARQUET")
    print("=" * 60)
    
    df.to_parquet(
        parquet_path,
        engine='pyarrow',
        compression='gzip',  # Best compression ratio
        index=False,
        row_group_size=5000  # Optimize for analytics queries
    )
    
    # Verify file size
    file_size_mb = os.path.getsize(parquet_path) / 1024 / 1024
    
    print(f"\n✓ Parquet file created: {PARQUET_FILE}")
    print(f"  Location: {parquet_path}")
    print(f"  File size: {file_size_mb:.2f} MB")
    
    if file_size_mb > MAX_FILE_SIZE_MB:
        print(f"\n⚠ WARNING: File size exceeds {MAX_FILE_SIZE_MB}MB limit!")
        print(f"  Current size: {file_size_mb:.2f}MB")
        print(f"  Excess: {file_size_mb - MAX_FILE_SIZE_MB:.2f}MB")
        print("\nConsider:")
        print("  1. Reducing dataset size")
        print("  2. Removing more outliers")
        print("  3. Using stronger compression")
        return False
    else:
        print(f"✓ File size within {MAX_FILE_SIZE_MB}MB limit")
    
    # Print final statistics
    print("\n" + "=" * 60)
    print("DATASET STATISTICS")
    print("=" * 60)
    
    print(f"\nRecords: {len(df):,}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Compression Ratio: {(os.path.getsize(csv_path) / os.path.getsize(parquet_path)):.2f}x")
    
    print(f"\nYear Range: {df['year'].min()} - {df['year'].max()}")
    print(f"Mileage Range: {df['mileage_km'].min():,} - {df['mileage_km'].max():,} km")
    print(f"Bid Range: ¥{df['winning_bid_jpy'].min():,} - ¥{df['winning_bid_jpy'].max():,}")
    print(f"Engine Size Range: {df['engine_cc'].min()} - {df['engine_cc'].max()} cc")
    
    print(f"\nMake Distribution:")
    print(df['make'].value_counts())
    
    print(f"\nAuction Grade Distribution:")
    print(df['auction_grade'].value_counts().sort_index())
    
    # Memory usage comparison
    print(f"\nMemory Usage:")
    print(f"  CSV (in memory): {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    print(f"  Parquet (on disk): {file_size_mb:.2f} MB")
    
    print("\n" + "=" * 60)
    print("✓ SUCCESS! Dataset ready for ML training")
    print("=" * 60)
    
    print("\nNext steps:")
    print("1. Create directory: mkdir ml")
    print("2. Create directory: mkdir models")
    print("3. Create training script: ml\\train_bid_predictor.py")
    print("4. Run training: python ml\\train_bid_predictor.py")
    
    return True


if __name__ == '__main__':
    try:
        success = convert_to_parquet()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
