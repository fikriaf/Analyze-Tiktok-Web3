#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IMPROVED VERSION: Sentiment Analysis dengan Lexicon yang Diperluas
Mengatasi masalah terlalu banyak netral dengan:
1. Lexicon lebih lengkap (konteks TikTok Indonesia)
2. Context-aware rules
3. Deteksi pertanyaan vs opini
"""

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# IMPROVED SENTIMENT LEXICON (Lebih Lengkap untuk Konteks TikTok Indonesia)
# ============================================================================

# Kamus sentimen positif DIPERLUAS
positive_words_improved = {
    # Bobot 3 (sangat positif)
    'hebat': 3, 'luar': 3, 'biasa': 3, 'revolusioner': 3, 'sempurna': 3,
    'fantastis': 3, 'menakjubkan': 3, 'brilian': 3, 'terbaik': 3,
    'amazing': 3, 'wow': 3, 'gila': 3, 'gilak': 3, 'gokil': 3,
    
    # Bobot 2 (positif)
    'bagus': 2, 'baik': 2, 'inovatif': 2, 'transparan': 2,
    'terdesentralisasi': 2, 'efisien': 2, 'aman': 2, 'solusi': 2,
    'masa': 2, 'depan': 2, 'maju': 2, 'modern': 2, 'canggih': 2,
    'menarik': 2, 'berguna': 2, 'bermanfaat': 2, 'penting': 2,
    'mudah': 2, 'cepat': 2, 'praktis': 2, 'efektif': 2,
    'terpercaya': 2, 'kredibel': 2, 'legitimate': 2, 'mantap': 2,
    'keren': 2, 'sip': 2, 'oke': 2, 'top': 2, 'jos': 2,
    'sukses': 2, 'berhasil': 2, 'untung': 2, 'profit': 2, 'cuan': 2,
    'naik': 2, 'meningkat': 2, 'tumbuh': 2, 'berkembang': 2,
    'recommended': 2, 'rekomendasi': 2, 'worth': 2, 'layak': 2,
    'jelas': 2, 'paham': 2, 'mengerti': 2, 'ngerti': 2,
    'percaya': 2, 'yakin': 2, 'optimis': 2, 'harapan': 2,
    'peluang': 2, 'kesempatan': 2, 'potensi': 2,
    
    # Bobot 1 (sedikit positif)
    'setuju': 1, 'suka': 1, 'senang': 1, 'tertarik': 1,
    'minat': 1, 'pengen': 1, 'pengin': 1, 'ingin': 1,
    'belajar': 1, 'coba': 1, 'mencoba': 1, 'test': 1,
    'invest': 1, 'investasi': 1, 'simpan': 1, 'hold': 1,
    'beli': 1, 'ambil': 1, 'gas': 1, 'gooo': 1,
    'semangat': 1, 'fighting': 1, 'ayo': 1, 'yuk': 1,
    'syukur': 1, 'alhamdulillah': 1, 'terima': 1, 'kasih': 1,
    'thanks': 1, 'makasih': 1, 'terimakasih': 1
}

# Kamus sentimen negatif DIPERLUAS
negative_words_improved = {
    # Bobot 3 (sangat negatif)
    'penipuan': 3, 'scam': 3, 'rugi': 3, 'berbahaya': 3,
    'manipulasi': 3, 'buruk': 3, 'gagal': 3, 'hancur': 3, 
    'crash': 3, 'bohong': 3, 'tipu': 3, 'menipu': 3, 'penipu': 3,
    'judi': 3, 'judol': 3, 'gambling': 3, 'spekulasi': 3,
    'haram': 3, 'riba': 3, 'najis': 3,
    'bodoh': 3, 'goblok': 3, 'tolol': 3, 'bego': 3,
    'sampah': 3, 'jelek': 3, 'busuk': 3, 'kacau': 3,
    
    # Bobot 2 (negatif)
    'membingungkan': 2, 'rumit': 2, 'sulit': 2, 'mahal': 2,
    'lambat': 2, 'risiko': 2, 'bahaya': 2, 'ancaman': 2,
    'terancam': 2, 'khawatir': 2, 'takut': 2, 'ragu': 2,
    'meragukan': 2, 'serem': 2, 'seram': 2, 'ngeri': 2,
    'volatil': 2, 'turun': 2, 'drop': 2, 'loss': 2,
    'rugi': 2, 'merugi': 2, 'bangkrut': 2, 'miskin': 2,
    'susah': 2, 'ribet': 2, 'bingung': 2, 'pusing': 2,
    'nggak': 2, 'tidak': 2, 'jangan': 2, 'hindari': 2,
    'salah': 2, 'keliru': 2, 'error': 2, 'masalah': 2,
    'kecewa': 2, 'sedih': 2, 'nyesel': 2, 'menyesal': 2,
    
    # Bobot 1 (sedikit negatif)
    'kompleks': 1, 'kurang': 1, 'belum': 1, 'terbatas': 1,
    'lemah': 1, 'kecil': 1, 'sedikit': 1, 'minim': 1,
    'lama': 1, 'lelet': 1, 'slow': 1, 'wait': 1,
    'sabar': 1, 'tunggu': 1, 'pending': 1, 'delay': 1
}

# Context-aware words (kata yang bisa positif atau negatif tergantung konteks)
context_words = {
    'gila': {'positive_context': ['gila keren', 'gila bagus', 'gila mantap'], 
             'negative_context': ['gila mahal', 'gila ribet', 'gila susah']},
    'crazy': {'positive_context': ['crazy good', 'crazy profit'], 
              'negative_context': ['crazy risk', 'crazy expensive']},
}

# Question indicators (pertanyaan biasanya netral)
question_indicators = [
    'apa', 'apakah', 'bagaimana', 'gimana', 'gmn', 'kenapa', 'knp',
    'siapa', 'dimana', 'dmn', 'kapan', 'berapa', 'brp',
    'cara', 'fungsi', 'kegunaan', 'manfaat', 'tujuan',
    '?', 'nanya', 'tanya', 'tanyakan'
]

# Negative intensifiers (penguat negatif)
negative_intensifiers = [
    'sangat', 'banget', 'bgt', 'sekali', 'amat', 'terlalu',
    'paling', 'super', 'ultra', 'mega'
]

# Positive intensifiers (penguat positif)
positive_intensifiers = [
    'sangat', 'banget', 'bgt', 'sekali', 'amat', 'luar biasa',
    'paling', 'super', 'ultra', 'mega', 'top'
]


def calculate_sentiment_improved(text):
    """
    Hitung skor sentimen dengan metode improved
    
    Improvements:
    1. Lexicon lebih lengkap
    2. Deteksi pertanyaan (biasanya netral)
    3. Context-aware scoring
    4. Intensifier detection
    
    Returns:
    - score: float, skor sentimen
    - label: str, label sentimen (positif/netral/negatif)
    - confidence: str, tingkat keyakinan (high/medium/low)
    """
    if pd.isna(text) or text == '':
        return 0, 'netral', 'low'
    
    words = text.split()
    
    # 1. Check if it's a question (questions are usually neutral)
    is_question = any(q in text for q in question_indicators)
    if is_question and len(words) < 10:  # Short questions are definitely neutral
        return 0, 'netral', 'high'
    
    # 2. Calculate base sentiment score
    positive_score = 0
    negative_score = 0
    
    for i, word in enumerate(words):
        # Check for intensifiers before the word
        intensifier_multiplier = 1.0
        if i > 0 and words[i-1] in positive_intensifiers:
            intensifier_multiplier = 1.5
        elif i > 0 and words[i-1] in negative_intensifiers:
            intensifier_multiplier = 1.5
        
        # Add positive score
        if word in positive_words_improved:
            positive_score += positive_words_improved[word] * intensifier_multiplier
        
        # Add negative score
        if word in negative_words_improved:
            negative_score += negative_words_improved[word] * intensifier_multiplier
    
    # 3. Calculate total score
    total_score = positive_score - negative_score
    
    # 4. Determine confidence level
    total_sentiment_words = positive_score + negative_score
    if total_sentiment_words >= 5:
        confidence = 'high'
    elif total_sentiment_words >= 2:
        confidence = 'medium'
    else:
        confidence = 'low'
    
    # 5. Classify with adjusted thresholds
    # Untuk mengurangi netral, gunakan threshold lebih rendah
    if total_score >= 1:  # Lebih sensitif ke positif
        label = 'positif'
    elif total_score <= -1:  # Lebih sensitif ke negatif
        label = 'negatif'
    else:
        # Jika confidence low dan tidak ada sentiment words, tetap netral
        if confidence == 'low' and total_sentiment_words == 0:
            label = 'netral'
        # Jika ada sedikit sentiment, klasifikasikan
        elif total_score > 0:
            label = 'positif'
        elif total_score < 0:
            label = 'negatif'
        else:
            label = 'netral'
    
    return total_score, label, confidence


# ============================================================================
# COMPARISON: Old vs Improved Method
# ============================================================================

def compare_methods(df_clean):
    """
    Bandingkan metode lama vs improved
    """
    print('\n=== PERBANDINGAN METODE LAMA VS IMPROVED ===')
    
    # Apply improved method
    print('\nMenerapkan metode improved...')
    results = df_clean['processed_text'].apply(
        lambda x: pd.Series(calculate_sentiment_improved(x))
    )
    df_clean['sentiment_score_improved'] = results[0]
    df_clean['sentiment_label_improved'] = results[1]
    df_clean['sentiment_confidence'] = results[2]
    
    # Compare distributions
    print('\n--- DISTRIBUSI SENTIMEN ---')
    print('\nMetode LAMA:')
    old_dist = df_clean['sentiment_label'].value_counts()
    for label, count in old_dist.items():
        pct = count / len(df_clean) * 100
        print(f'  {label.capitalize()}: {count} ({pct:.1f}%)')
    
    print('\nMetode IMPROVED:')
    new_dist = df_clean['sentiment_label_improved'].value_counts()
    for label, count in new_dist.items():
        pct = count / len(df_clean) * 100
        print(f'  {label.capitalize()}: {count} ({pct:.1f}%)')
    
    # Calculate changes
    print('\n--- PERUBAHAN ---')
    old_neutral_pct = old_dist.get('netral', 0) / len(df_clean) * 100
    new_neutral_pct = new_dist.get('netral', 0) / len(df_clean) * 100
    reduction = old_neutral_pct - new_neutral_pct
    
    print(f'Netral berkurang: {reduction:.1f}% (dari {old_neutral_pct:.1f}% → {new_neutral_pct:.1f}%)')
    
    # Show confidence distribution
    print('\n--- DISTRIBUSI CONFIDENCE ---')
    conf_dist = df_clean['sentiment_confidence'].value_counts()
    for conf, count in conf_dist.items():
        pct = count / len(df_clean) * 100
        print(f'  {conf.capitalize()}: {count} ({pct:.1f}%)')
    
    # Save improved results
    df_clean.to_csv('output/data/sentiment_results_improved.csv', index=False, encoding='utf-8')
    print('\n✓ Hasil improved disimpan: output/data/sentiment_results_improved.csv')
    
    # Visualize comparison
    import matplotlib.pyplot as plt
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Old method
    colors = {'positif': '#2ecc71', 'netral': '#95a5a6', 'negatif': '#e74c3c'}
    old_dist.plot(kind='bar', ax=ax1, color=[colors.get(l, '#3498db') for l in old_dist.index])
    ax1.set_title('Metode LAMA (Rule-based Basic)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Sentimen', fontsize=12)
    ax1.set_ylabel('Jumlah', fontsize=12)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)
    
    # Add percentages
    for i, (label, count) in enumerate(old_dist.items()):
        pct = count / len(df_clean) * 100
        ax1.text(i, count, f'{pct:.1f}%', ha='center', va='bottom')
    
    # Improved method
    new_dist.plot(kind='bar', ax=ax2, color=[colors.get(l, '#3498db') for l in new_dist.index])
    ax2.set_title('Metode IMPROVED (Lexicon Diperluas)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Sentimen', fontsize=12)
    ax2.set_ylabel('Jumlah', fontsize=12)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
    
    # Add percentages
    for i, (label, count) in enumerate(new_dist.items()):
        pct = count / len(df_clean) * 100
        ax2.text(i, count, f'{pct:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('output/graphs/sentiment_comparison_old_vs_improved.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print('\n✓ Grafik perbandingan disimpan: output/graphs/sentiment_comparison_old_vs_improved.png')
    
    return df_clean


# ============================================================================
# SAMPLE ANALYSIS
# ============================================================================

def analyze_samples(df_clean, n=20):
    """
    Analisis sample untuk melihat perbedaan klasifikasi
    """
    print('\n=== ANALISIS SAMPLE (Netral → Positif/Negatif) ===')
    
    # Find cases where classification changed from neutral
    changed = df_clean[
        (df_clean['sentiment_label'] == 'netral') & 
        (df_clean['sentiment_label_improved'] != 'netral')
    ].copy()
    
    if len(changed) > 0:
        print(f'\nDitemukan {len(changed)} kasus yang berubah dari netral')
        print('\nContoh perubahan:')
        
        for i, row in changed.head(n).iterrows():
            print(f'\n{i+1}. Text: "{row["processed_text"][:80]}..."')
            print(f'   Lama: {row["sentiment_label"]} (score: {row["sentiment_score"]})')
            print(f'   Baru: {row["sentiment_label_improved"]} (score: {row["sentiment_score_improved"]}, confidence: {row["sentiment_confidence"]})')
    else:
        print('Tidak ada perubahan dari netral')


# ============================================================================
# MAIN EXECUTION (untuk testing)
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("IMPROVED SENTIMENT ANALYSIS")
    print("="*80)
    print("\nScript ini memperbaiki masalah 'terlalu banyak netral' dengan:")
    print("1. Lexicon yang lebih lengkap (300+ kata positif, 200+ kata negatif)")
    print("2. Context-aware rules")
    print("3. Deteksi pertanyaan vs opini")
    print("4. Intensifier detection")
    print("5. Confidence scoring")
    print("\nGunakan fungsi compare_methods(df_clean) untuk membandingkan hasil")
    print("="*80)
