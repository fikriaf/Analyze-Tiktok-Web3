#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script untuk menjalankan Improved Sentiment Analysis
Mengatasi masalah "terlalu banyak netral"
"""

import pandas as pd
import os
import sys

print("="*80)
print("IMPROVED SENTIMENT ANALYSIS")
print("Mengatasi masalah 'terlalu banyak netral'")
print("="*80)

# Step 1: Check if basic sentiment analysis has been run
print("\n[Step 1] Checking for existing sentiment results...")

data_files = [
    'output/data/sentiment_results.csv',
    'output/data/final_data_with_topics.csv',
    'output/data/preprocessed_data.csv'
]

df_clean = None
data_file = None

for file in data_files:
    if os.path.exists(file):
        print(f"  ✓ Found: {file}")
        try:
            df_clean = pd.read_csv(file, encoding='utf-8')
            data_file = file
            print(f"    Loaded {len(df_clean)} rows")
            break
        except Exception as e:
            print(f"    ❌ Error loading: {e}")
            continue

if df_clean is None:
    print("\n❌ ERROR: No sentiment results found!")
    print("\nPlease run basic sentiment analysis first:")
    print("  python tiktok_sentiment_analysis.py")
    sys.exit(1)

# Step 2: Check required columns
print("\n[Step 2] Checking data columns...")

required_cols = ['processed_text', 'sentiment_label', 'sentiment_score']
missing = [col for col in required_cols if col not in df_clean.columns]

if missing:
    print(f"  ❌ Missing columns: {missing}")
    print("\n  Please run tiktok_sentiment_analysis.py first!")
    sys.exit(1)

print(f"  ✓ All required columns present")
print(f"  ✓ Data shape: {df_clean.shape}")

# Step 3: Show current distribution
print("\n[Step 3] Current Sentiment Distribution (OLD METHOD):")
old_dist = df_clean['sentiment_label'].value_counts()
for label, count in old_dist.items():
    pct = count / len(df_clean) * 100
    print(f"  {label.capitalize()}: {count} ({pct:.1f}%)")

neutral_pct = old_dist.get('netral', 0) / len(df_clean) * 100
if neutral_pct > 60:
    print(f"\n  ⚠ WARNING: Netral terlalu tinggi ({neutral_pct:.1f}%)")
    print(f"     Improved method akan mengurangi netral!")
elif neutral_pct > 40:
    print(f"\n  ℹ INFO: Netral cukup tinggi ({neutral_pct:.1f}%)")
    print(f"     Improved method bisa membantu")
else:
    print(f"\n  ✓ Netral dalam batas wajar ({neutral_pct:.1f}%)")

# Step 4: Import improved functions
print("\n[Step 4] Loading improved sentiment analysis...")

try:
    from tiktok_sentiment_analysis_improved import (
        compare_methods, 
        analyze_samples,
        calculate_sentiment_improved
    )
    print("  ✓ Improved functions loaded")
except ImportError as e:
    print(f"  ❌ Error importing: {e}")
    print("\n  Make sure tiktok_sentiment_analysis_improved.py exists!")
    sys.exit(1)

# Step 5: Run improved analysis
print("\n[Step 5] Running improved sentiment analysis...")
print("  This may take a few moments...")

try:
    df_improved = compare_methods(df_clean)
    print("\n  ✓ Improved analysis complete!")
    
except Exception as e:
    print(f"\n  ❌ Error during analysis: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 6: Show sample changes
print("\n[Step 6] Analyzing changes...")

try:
    analyze_samples(df_improved, n=10)
except Exception as e:
    print(f"  ⚠ Could not analyze samples: {e}")

# Step 7: Summary
print("\n" + "="*80)
print("✅ IMPROVED SENTIMENT ANALYSIS COMPLETED!")
print("="*80)

print("\n📊 RESULTS:")
print(f"  Total data: {len(df_improved)} rows")
print(f"  Data saved: output/data/sentiment_results_improved.csv")
print(f"  Graph saved: output/graphs/sentiment_comparison_old_vs_improved.png")

print("\n📈 IMPROVEMENT:")
new_dist = df_improved['sentiment_label_improved'].value_counts()
new_neutral_pct = new_dist.get('netral', 0) / len(df_improved) * 100
reduction = neutral_pct - new_neutral_pct

if reduction > 0:
    print(f"  ✓ Netral berkurang: {reduction:.1f}%")
    print(f"    (dari {neutral_pct:.1f}% → {new_neutral_pct:.1f}%)")
else:
    print(f"  ℹ Netral tidak berubah signifikan")

print("\n💡 NEXT STEPS:")
print("  1. Review hasil di: output/data/sentiment_results_improved.csv")
print("  2. Lihat grafik perbandingan di: output/graphs/")
print("  3. Gunakan kolom 'sentiment_label_improved' untuk analisis selanjutnya")
print("  4. Generate visualisasi: python run_visualizations.py")

print("\n" + "="*80)
