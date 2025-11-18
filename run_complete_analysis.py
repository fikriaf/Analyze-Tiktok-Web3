#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete Analysis Pipeline
Menjalankan semua tahap analisis dari awal sampai akhir
"""

import os
import sys

print("="*80)
print("COMPLETE SENTIMENT ANALYSIS PIPELINE")
print("="*80)
print("\nPipeline:")
print("1. Load & Preprocess Data")
print("2. Basic Sentiment Analysis")
print("3. Improved Sentiment Analysis (fix netral)")
print("4. Advanced Visualizations")
print("="*80)

# Check if data exists
if not os.path.exists('output/data/scraped_data_fixed.csv') and \
   not os.path.exists('output/data/scraped_data.csv'):
    print("\n❌ ERROR: No scraped data found!")
    print("\nPlease run scraper first:")
    print("  1. python scraper_link_video_tt.py")
    print("  2. python scraper_firefox.py")
    sys.exit(1)

# ============================================================================
# STEP 1: Basic Sentiment Analysis
# ============================================================================

print("\n" + "="*80)
print("STEP 1: BASIC SENTIMENT ANALYSIS")
print("="*80)

if os.path.exists('output/data/sentiment_results.csv'):
    print("\n✓ Sentiment results already exist")
    print("  Skipping basic analysis...")
    print("  (Delete output/data/sentiment_results.csv to re-run)")
else:
    print("\n⚠ Running basic sentiment analysis...")
    print("  This will take a few minutes...")
    
    try:
        # Import and run basic analysis
        import tiktok_sentiment_analysis
        print("\n✓ Basic sentiment analysis completed!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTry running manually:")
        print("  python tiktok_sentiment_analysis.py")
        sys.exit(1)

# ============================================================================
# STEP 2: Improved Sentiment Analysis
# ============================================================================

print("\n" + "="*80)
print("STEP 2: IMPROVED SENTIMENT ANALYSIS")
print("="*80)

if os.path.exists('output/data/sentiment_results_improved.csv'):
    print("\n✓ Improved results already exist")
    print("  Skipping improved analysis...")
    print("  (Delete output/data/sentiment_results_improved.csv to re-run)")
else:
    print("\n⚠ Running improved sentiment analysis...")
    
    try:
        import pandas as pd
        from tiktok_sentiment_analysis_improved import compare_methods
        
        df = pd.read_csv('output/data/sentiment_results.csv', encoding='utf-8')
        df_improved = compare_methods(df)
        
        print("\n✓ Improved sentiment analysis completed!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTry running manually:")
        print("  python run_improved_sentiment.py")
        # Don't exit, continue to visualizations

# ============================================================================
# STEP 3: Advanced Visualizations
# ============================================================================

print("\n" + "="*80)
print("STEP 3: ADVANCED VISUALIZATIONS")
print("="*80)

print("\n⚠ Generating advanced visualizations...")

try:
    import pandas as pd
    from advanced_visualizations import create_all_advanced_visualizations
    
    # Use improved results if available, otherwise use basic
    if os.path.exists('output/data/sentiment_results_improved.csv'):
        df = pd.read_csv('output/data/sentiment_results_improved.csv', encoding='utf-8')
        print("  Using improved sentiment results")
        # Use improved columns
        if 'sentiment_label_improved' in df.columns:
            df['sentiment_label'] = df['sentiment_label_improved']
            df['sentiment_score'] = df['sentiment_score_improved']
    else:
        df = pd.read_csv('output/data/sentiment_results.csv', encoding='utf-8')
        print("  Using basic sentiment results")
    
    create_all_advanced_visualizations(df)
    
    print("\n✓ Advanced visualizations completed!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTry running manually:")
    print("  python run_visualizations.py")
    import traceback
    traceback.print_exc()

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "="*80)
print("✅ COMPLETE ANALYSIS FINISHED!")
print("="*80)

print("\n📁 OUTPUT FILES:")

print("\n1. Data Files (output/data/):")
files = [
    'preprocessed_data.csv',
    'sentiment_results.csv',
    'sentiment_results_improved.csv',
    'final_data_with_topics.csv',
    'word_frequency.csv',
    'tfidf_scores.csv',
    'web3_keyword_mentions.csv',
    'summary_report.json'
]
for f in files:
    path = f'output/data/{f}'
    if os.path.exists(path):
        size = os.path.getsize(path) / 1024  # KB
        print(f"  ✓ {f} ({size:.1f} KB)")

print("\n2. Visualizations (output/graphs/):")
graphs = [
    'sentiment_distribution.png',
    'sentiment_comparison_old_vs_improved.png',
    'top_words_comparison.png',
    'web3_keyword_mentions.png',
    'sentiment_by_topic.png',
    'advanced_heatmap_sentiment_topic.png',
    'advanced_radar_sentiment_profile.png',
    'advanced_violin_sentiment_distribution.png',
    'advanced_network_cooccurrence.png',
    'advanced_infographic_summary.png'
]
for g in graphs:
    path = f'output/graphs/{g}'
    if os.path.exists(path):
        print(f"  ✓ {g}")

print("\n3. Wordclouds (output/wordclouds/):")
wcs = [
    'wordcloud_overall.png',
    'wordcloud_by_sentiment.png',
    'wordcloud_by_topic.png'
]
for w in wcs:
    path = f'output/wordclouds/{w}'
    if os.path.exists(path):
        print(f"  ✓ {w}")

print("\n💡 RECOMMENDATIONS:")
print("  1. Review sentiment_results_improved.csv for final results")
print("  2. Use advanced visualizations for publication")
print("  3. Check summary_report.json for key metrics")
print("  4. Wordclouds are great for presentations")

print("\n📊 NEXT STEPS:")
print("  - Open Jupyter Notebook for interactive analysis")
print("  - Review visualizations in output/graphs/")
print("  - Write your findings in thesis/paper")
print("  - Present results using infographic and interactive charts")

print("\n" + "="*80)
print("Thank you for using this sentiment analysis pipeline!")
print("="*80)
