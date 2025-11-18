#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script helper untuk menjalankan advanced visualizations dengan error handling
"""

import pandas as pd
import os
import sys

print("="*80)
print("ADVANCED VISUALIZATIONS - SAFE RUN")
print("="*80)

# Check if data exists
data_files = [
    'output/data/final_data_with_topics.csv',
    'output/data/sentiment_results.csv',
    'output/data/preprocessed_data.csv'
]

df = None
data_file = None

for file in data_files:
    if os.path.exists(file):
        print(f"\n✓ Found: {file}")
        try:
            df = pd.read_csv(file, encoding='utf-8')
            data_file = file
            print(f"  Loaded {len(df)} rows")
            break
        except Exception as e:
            print(f"  ❌ Error loading: {e}")
            continue

if df is None:
    print("\n❌ ERROR: No data file found!")
    print("\nPlease run one of these first:")
    print("1. python tiktok_sentiment_analysis.py")
    print("2. Make sure output/data/ folder exists with CSV files")
    sys.exit(1)

# Check columns
print(f"\n📊 Data Info:")
print(f"  Rows: {len(df)}")
print(f"  Columns: {list(df.columns)}")

required_cols = ['processed_text', 'sentiment_label', 'sentiment_score']
missing = [col for col in required_cols if col not in df.columns]

if missing:
    print(f"\n❌ ERROR: Missing required columns: {missing}")
    print("\nYour data must have these columns:")
    print("  - processed_text")
    print("  - sentiment_label")
    print("  - sentiment_score")
    print("\nPlease run tiktok_sentiment_analysis.py first!")
    sys.exit(1)

print("\n✓ All required columns present")

# Import and run visualizations
try:
    from advanced_visualizations import create_all_advanced_visualizations
    
    print("\n" + "="*80)
    print("STARTING VISUALIZATION GENERATION")
    print("="*80)
    
    create_all_advanced_visualizations(df)
    
    print("\n" + "="*80)
    print("✅ SUCCESS! All visualizations generated")
    print("="*80)
    print("\nCheck output/graphs/ folder for results:")
    print("  - advanced_heatmap_sentiment_topic.png")
    print("  - advanced_radar_sentiment_profile.png")
    print("  - advanced_violin_sentiment_distribution.png")
    print("  - advanced_network_cooccurrence.png")
    print("  - advanced_infographic_summary.png")
    print("  - advanced_sunburst_topic_sentiment.html (if plotly installed)")
    print("  - advanced_sankey_topic_sentiment.html (if plotly installed)")
    print("  - advanced_treemap_topic_sentiment.html (if plotly installed)")
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nMake sure you have installed:")
    print("  pip install pandas numpy matplotlib seaborn")
    print("\nOptional (for interactive visualizations):")
    print("  pip install plotly kaleido networkx")
    
except Exception as e:
    print(f"\n❌ Error during visualization: {e}")
    print("\nTroubleshooting:")
    print("1. Check if output/graphs/ folder exists")
    print("2. Make sure you have write permissions")
    print("3. Try running individual visualizations")
    import traceback
    traceback.print_exc()
