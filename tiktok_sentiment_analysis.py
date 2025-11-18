#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analisis Sentimen TikTok: Persepsi Publik terhadap Isu Sosial Web3

Script ini mengimplementasikan metodologi penelitian sesuai dengan METODOLOGI_PENELITIAN.md

Tahapan:
1. Setup dan Import Libraries
2. Load Data (dari hasil scraping)
3. Pra-Pemrosesan Data
4. Analisis Sentimen (Rule-based)
5. Analisis Trending Topic
6. Visualisasi Wordcloud
7. Analisis Kritis dan Kesimpulan

Note: Data scraping dilakukan terpisah menggunakan scraper_link_video_tt.py dan scraper_firefox.py
Semua output akan disimpan ke folder output/
"""

# ============================================================================
# TAHAP 1: Setup dan Import Libraries
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
import json
import os
from datetime import datetime
from collections import Counter
import math
import warnings
warnings.filterwarnings('ignore')

# Setup matplotlib untuk visualisasi
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

# Buat folder output jika belum ada
os.makedirs('output', exist_ok=True)
os.makedirs('output/wordclouds', exist_ok=True)
os.makedirs('output/graphs', exist_ok=True)
os.makedirs('output/data', exist_ok=True)

print('✓ Setup selesai')
print('✓ Folder output dibuat')


# ============================================================================
# TAHAP 2: Load Data dari Hasil Scraping
# ============================================================================

# Load data dari hasil scraping
# Coba load dari scraped_data_fixed.csv terlebih dahulu, jika tidak ada gunakan scraped_data.csv
try:
    df_raw = pd.read_csv('output/data/scraped_data_fixed.csv', encoding='utf-8')
    print('✓ Data loaded dari: output/data/scraped_data_fixed.csv')
except FileNotFoundError:
    try:
        df_raw = pd.read_csv('output/data/scraped_data.csv', encoding='utf-8')
        print('✓ Data loaded dari: output/data/scraped_data.csv')
    except FileNotFoundError:
        print('❌ Error: File data tidak ditemukan!')
        print('   Pastikan sudah menjalankan scraper_firefox.py terlebih dahulu')
        raise

print(f'\nJumlah data: {len(df_raw)} baris')
print(f'Kolom: {list(df_raw.columns)}')
print('\nPreview data:')
print(df_raw.head())

# Informasi dataset
print('\n=== INFORMASI DATASET ===')
print(f'Total baris: {len(df_raw)}')
print(f'Total video unik: {df_raw["video_id"].nunique()}')
print(f'Total comment: {df_raw["comment"].notna().sum()}')
print(f'\nMissing values:')
print(df_raw.isnull().sum())


# ============================================================================
# TAHAP 3: Pra-Pemrosesan Data
# ============================================================================

print('\n=== TAHAP 3: PRA-PEMROSESAN DATA ===')
print('Sesuai metodologi penelitian (BAB II, Tahap 2.2.2):')
print('1. Case Folding')
print('2. Tokenisasi')
print('3. Stopword Removal')
print('4. Normalisasi (slang → formal)')
print('5. Filtering (emoji, URL, mention, hashtag)')

# Load stopwords dari sources/stopwords-id.json
with open('sources/stopwords-id.json', 'r', encoding='utf-8') as f:
    stopwords_id = json.load(f)

print(f'\n✓ Stopwords loaded: {len(stopwords_id)} kata')
print(f'  Contoh: {stopwords_id[:10]}')

# Load slang dictionary dari sources/slang_indo.csv
slang_df = pd.read_csv('sources/slang_indo.csv', header=None, names=['slang', 'formal'])
slang_dict = dict(zip(slang_df['slang'], slang_df['formal']))

print(f'\n✓ Slang dictionary loaded: {len(slang_dict)} kata')
print(f'  Contoh mapping:')
for i, (slang, formal) in enumerate(list(slang_dict.items())[:10]):
    print(f'    {slang} → {formal}')


def preprocess_text(text):
    """
    Preprocessing teks sesuai metodologi penelitian
    
    Langkah:
    1. Case folding
    2. Filtering (URL, mention, hashtag, emoji)
    3. Hapus tanda baca dan angka
    4. Tokenisasi
    5. Normalisasi slang
    6. Stopword removal
    
    Returns:
    - str: teks yang sudah diproses
    """
    if pd.isna(text) or text == '':
        return ''
    
    # 1. Case folding
    text = text.lower()
    
    # 2. Hapus URL
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # 3. Hapus mention (@username)
    text = re.sub(r'@\w+', '', text)
    
    # 4. Hapus hashtag (sudah disimpan terpisah di kolom hashtags)
    text = re.sub(r'#\w+', '', text)
    
    # 5. Hapus emoji dan emoticon
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    
    # 6. Hapus tanda baca
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # 7. Hapus angka
    text = re.sub(r'\d+', '', text)
    
    # 8. Hapus spasi berlebihan
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 9. Tokenisasi
    tokens = text.split()
    
    # 10. Normalisasi slang
    tokens = [slang_dict.get(word, word) for word in tokens]
    
    # 11. Stopword removal dan filter kata pendek
    tokens = [word for word in tokens if word not in stopwords_id and len(word) > 2]
    
    return ' '.join(tokens)


print('\n✓ Fungsi preprocessing siap')

# Apply preprocessing ke caption dan comment
print('\nMemproses caption...')
df_raw['processed_caption'] = df_raw['caption'].apply(preprocess_text)

print('Memproses comment...')
df_raw['processed_comment'] = df_raw['comment'].apply(preprocess_text)

# Gabungkan caption dan comment untuk analisis
df_raw['processed_text'] = df_raw['processed_caption'] + ' ' + df_raw['processed_comment']
df_raw['processed_text'] = df_raw['processed_text'].str.strip()

# Remove empty rows (baris yang teksnya kosong setelah preprocessing)
df_clean = df_raw[df_raw['processed_text'] != ''].copy()

# Save preprocessed data
df_clean.to_csv('output/data/preprocessed_data.csv', index=False, encoding='utf-8')

print(f'\n✓ Preprocessing selesai')
print(f'✓ Data bersih: {len(df_clean)} baris (dari {len(df_raw)} baris)')
print(f'✓ Data disimpan: output/data/preprocessed_data.csv')
print('\nContoh hasil preprocessing:')
print(df_clean[['caption', 'comment', 'processed_text']].head(10))


# ============================================================================
# TAHAP 4: Analisis Sentimen (Rule-based)
# ============================================================================

print('\n=== TAHAP 4: ANALISIS SENTIMEN (RULE-BASED) ===')
print('Metode: Lexicon-based Sentiment Analysis')
print('Algoritma: Skor Sentimen = Σ(kata positif × bobot) - Σ(kata negatif × bobot)')
print('Klasifikasi: Skor > 0 → Positif, Skor = 0 → Netral, Skor < 0 → Negatif')

# Kamus sentimen positif dengan bobot (disesuaikan dengan konteks Web3 dan TikTok Indonesia)
positive_words = {
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

# Kamus sentimen negatif dengan bobot (disesuaikan dengan konteks Web3 dan TikTok Indonesia)
negative_words = {
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

# Save lexicons untuk dokumentasi
with open('output/data/positive_lexicon.json', 'w', encoding='utf-8') as f:
    json.dump(positive_words, f, indent=2, ensure_ascii=False)

with open('output/data/negative_lexicon.json', 'w', encoding='utf-8') as f:
    json.dump(negative_words, f, indent=2, ensure_ascii=False)

print(f'\n✓ Kamus sentimen dibuat dan disimpan')
print(f'  - Kata positif: {len(positive_words)} kata')
print(f'  - Kata negatif: {len(negative_words)} kata')


# Question indicators (pertanyaan biasanya netral)
question_indicators = [
    'apa', 'apakah', 'bagaimana', 'gimana', 'gmn', 'kenapa', 'knp',
    'siapa', 'dimana', 'dmn', 'kapan', 'berapa', 'brp',
    'cara', 'fungsi', 'kegunaan', 'manfaat', 'tujuan'
]

def calculate_sentiment(text):
    """
    Hitung skor sentimen berdasarkan lexicon dengan context-aware rules
    
    Returns:
    - score: float, skor sentimen
    - label: str, label sentimen (positif/netral/negatif)
    """
    if pd.isna(text) or text == '':
        return 0, 'netral'
    
    words = text.split()
    
    # Check if it's a short question (questions are usually neutral)
    is_question = any(q in text for q in question_indicators)
    if is_question and len(words) < 10:
        return 0, 'netral'
    
    # Hitung skor positif
    positive_score = 0
    negative_score = 0
    
    for i, word in enumerate(words):
        # Check for intensifiers before the word
        intensifier_multiplier = 1.0
        if i > 0 and words[i-1] in ['sangat', 'banget', 'bgt', 'sekali', 'amat', 'terlalu', 'paling', 'super']:
            intensifier_multiplier = 1.5
        
        # Add positive score
        if word in positive_words:
            positive_score += positive_words[word] * intensifier_multiplier
        
        # Add negative score
        if word in negative_words:
            negative_score += negative_words[word] * intensifier_multiplier
    
    # Total skor
    total_score = positive_score - negative_score
    
    # Klasifikasi dengan threshold yang lebih sensitif
    if total_score >= 1:  # Lebih sensitif ke positif
        label = 'positif'
    elif total_score <= -1:  # Lebih sensitif ke negatif
        label = 'negatif'
    else:
        label = 'netral'
    
    return total_score, label


# Apply sentiment analysis
print('\nMelakukan analisis sentimen...')
df_clean[['sentiment_score', 'sentiment_label']] = df_clean['processed_text'].apply(
    lambda x: pd.Series(calculate_sentiment(x))
)

# Save results
df_clean.to_csv('output/data/sentiment_results.csv', index=False, encoding='utf-8')

print('\n✓ Analisis sentimen selesai')
print(f'✓ Hasil disimpan: output/data/sentiment_results.csv')
print('\n=== DISTRIBUSI SENTIMEN ===')
sentiment_dist = df_clean['sentiment_label'].value_counts()
for label, count in sentiment_dist.items():
    pct = count / len(df_clean) * 100
    print(f'{label.capitalize()}: {count} ({pct:.1f}%)')

print('\n=== STATISTIK SKOR SENTIMEN ===')
print(df_clean['sentiment_score'].describe())

# Visualisasi: Bar Chart - Distribusi Sentimen
fig, ax = plt.subplots(figsize=(10, 6))
sentiment_counts = df_clean['sentiment_label'].value_counts()
colors = {'positif': '#2ecc71', 'netral': '#95a5a6', 'negatif': '#e74c3c'}
bars = ax.bar(sentiment_counts.index, sentiment_counts.values, 
              color=[colors.get(label, '#3498db') for label in sentiment_counts.index])

ax.set_xlabel('Sentimen', fontsize=12)
ax.set_ylabel('Jumlah', fontsize=12)
ax.set_title('Distribusi Sentimen Publik terhadap Isu Web3 di TikTok Indonesia', 
             fontsize=14, fontweight='bold')

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}\n({height/len(df_clean)*100:.1f}%)',
            ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('output/graphs/sentiment_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

print('\n✓ Grafik distribusi sentimen disimpan: output/graphs/sentiment_distribution.png')


# ============================================================================
# TAHAP 5: Analisis Trending Topic
# ============================================================================

print('\n=== TAHAP 5: ANALISIS TRENDING TOPIC ===')
print('Metode:')
print('1. Frequency Analysis')
print('2. TF-IDF Manual')
print('3. Identifikasi Tren Temporal')

# 1. Frequency Analysis
print('\n--- Frequency Analysis ---')
all_words = ' '.join(df_clean['processed_text']).split()
word_freq = Counter(all_words)
top_50_words = word_freq.most_common(50)

# Save frequency data
freq_df = pd.DataFrame(top_50_words, columns=['word', 'frequency'])
freq_df.to_csv('output/data/word_frequency.csv', index=False, encoding='utf-8')

print(f'✓ Analisis frekuensi selesai')
print(f'✓ Top 50 kata disimpan: output/data/word_frequency.csv')
print('\nTop 20 Kata Paling Sering Muncul:')
print(freq_df.head(20))


# 2. TF-IDF Manual Implementation
print('\n--- TF-IDF Manual Implementation ---')

def calculate_tf(text):
    """Calculate Term Frequency"""
    words = text.split()
    word_count = Counter(words)
    total_words = len(words)
    tf = {word: count/total_words for word, count in word_count.items()}
    return tf

def calculate_idf(documents):
    """Calculate Inverse Document Frequency"""
    N = len(documents)
    idf = {}
    
    # Get all unique words
    all_words = set()
    for doc in documents:
        all_words.update(doc.split())
    
    # Calculate IDF for each word
    for word in all_words:
        doc_count = sum(1 for doc in documents if word in doc.split())
        idf[word] = math.log(N / doc_count) if doc_count > 0 else 0
    
    return idf

def calculate_tfidf(documents):
    """Calculate TF-IDF scores"""
    idf = calculate_idf(documents)
    tfidf_scores = []
    
    for doc in documents:
        tf = calculate_tf(doc)
        tfidf = {word: tf_score * idf.get(word, 0) for word, tf_score in tf.items()}
        tfidf_scores.append(tfidf)
    
    return tfidf_scores, idf

# Calculate TF-IDF
print('Menghitung TF-IDF...')
documents = df_clean['processed_text'].tolist()
tfidf_scores, idf_scores = calculate_tfidf(documents)

# Get top TF-IDF words across all documents
all_tfidf = {}
for tfidf in tfidf_scores:
    for word, score in tfidf.items():
        all_tfidf[word] = all_tfidf.get(word, 0) + score

top_tfidf = sorted(all_tfidf.items(), key=lambda x: x[1], reverse=True)[:50]
tfidf_df = pd.DataFrame(top_tfidf, columns=['word', 'tfidf_score'])
tfidf_df.to_csv('output/data/tfidf_scores.csv', index=False, encoding='utf-8')

print('✓ TF-IDF selesai')
print(f'✓ Hasil disimpan: output/data/tfidf_scores.csv')
print('\nTop 20 Kata Berdasarkan TF-IDF:')
print(tfidf_df.head(20))


# 3. Visualisasi Top Words
print('\n--- Visualisasi Top Words ---')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Frequency bar chart
top_20_freq = freq_df.head(20)
ax1.barh(top_20_freq['word'], top_20_freq['frequency'], color='steelblue')
ax1.set_xlabel('Frekuensi', fontsize=11)
ax1.set_title('Top 20 Kata (Frequency)', fontsize=13, fontweight='bold')
ax1.invert_yaxis()

# TF-IDF bar chart
top_20_tfidf = tfidf_df.head(20)
ax2.barh(top_20_tfidf['word'], top_20_tfidf['tfidf_score'], color='coral')
ax2.set_xlabel('TF-IDF Score', fontsize=11)
ax2.set_title('Top 20 Kata (TF-IDF)', fontsize=13, fontweight='bold')
ax2.invert_yaxis()

plt.tight_layout()
plt.savefig('output/graphs/top_words_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

print('✓ Grafik top words disimpan: output/graphs/top_words_comparison.png')


# ============================================================================
# TAHAP 6: Visualisasi Wordcloud
# ============================================================================

print('\n=== TAHAP 6: VISUALISASI WORDCLOUD ===')
print('Jenis Wordcloud:')
print('1. Wordcloud Keseluruhan')
print('2. Wordcloud Per Sentimen (Positif, Negatif, Netral)')
print('3. Wordcloud Per Topik')

# 1. Wordcloud Keseluruhan
print('\n--- Wordcloud Keseluruhan ---')
all_text = ' '.join(df_clean['processed_text'])

wordcloud_all = WordCloud(
    width=1600,
    height=800,
    background_color='white',
    colormap='viridis',
    max_words=100,
    relative_scaling=0.5,
    min_font_size=10
).generate(all_text)

plt.figure(figsize=(20, 10))
plt.imshow(wordcloud_all, interpolation='bilinear')
plt.axis('off')
plt.title('Wordcloud Keseluruhan - Isu Web3 di TikTok Indonesia', 
          fontsize=20, fontweight='bold', pad=20)
plt.savefig('output/wordclouds/wordcloud_overall.png', dpi=300, bbox_inches='tight')
plt.show()

print('✓ Wordcloud keseluruhan disimpan: output/wordclouds/wordcloud_overall.png')


# 2. Wordcloud Per Sentimen
print('\n--- Wordcloud Per Sentimen ---')
fig, axes = plt.subplots(1, 3, figsize=(24, 8))

sentiments = [
    ('positif', 'Greens', axes[0]),
    ('netral', 'Greys', axes[1]),
    ('negatif', 'Reds', axes[2])
]

for sentiment, colormap, ax in sentiments:
    text_data = ' '.join(df_clean[df_clean['sentiment_label'] == sentiment]['processed_text'])
    
    if text_data.strip():  # Only create if there's data
        wc = WordCloud(
            width=1200,
            height=800,
            background_color='white',
            colormap=colormap,
            max_words=80,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(text_data)
        
        ax.imshow(wc, interpolation='bilinear')
    
    ax.axis('off')
    ax.set_title(f'Sentimen {sentiment.upper()}', fontsize=16, fontweight='bold')

plt.tight_layout()
plt.savefig('output/wordclouds/wordcloud_by_sentiment.png', dpi=300, bbox_inches='tight')
plt.show()

print('✓ Wordcloud per sentimen disimpan: output/wordclouds/wordcloud_by_sentiment.png')


# 3. Wordcloud Per Topik
print('\n--- Wordcloud Per Topik ---')

# Kategorisasi topik berdasarkan hashtag
def categorize_topic(hashtags):
    if pd.isna(hashtags):
        return 'Web3 General'
    hashtags_lower = str(hashtags).lower()
    if 'ai' in hashtags_lower or 'ethics' in hashtags_lower:
        return 'AI Ethics'
    elif 'blockchain' in hashtags_lower or 'crypto' in hashtags_lower:
        return 'Blockchain & Crypto'
    elif 'sustainability' in hashtags_lower or 'green' in hashtags_lower:
        return 'Sustainability'
    elif 'nft' in hashtags_lower or 'metaverse' in hashtags_lower:
        return 'NFT & Metaverse'
    elif 'privacy' in hashtags_lower or 'security' in hashtags_lower:
        return 'Privacy & Security'
    else:
        return 'Web3 General'

df_clean['topic_category'] = df_clean['hashtags'].apply(categorize_topic)

# Save categorized data
df_clean.to_csv('output/data/final_data_with_topics.csv', index=False, encoding='utf-8')

print('✓ Kategorisasi topik selesai')
print('\nDistribusi Topik:')
print(df_clean['topic_category'].value_counts())

# Create wordcloud for each topic
topics = df_clean['topic_category'].unique()
n_topics = len(topics)
cols = 3
rows = (n_topics + cols - 1) // cols

fig, axes = plt.subplots(rows, cols, figsize=(20, 6*rows))
axes = axes.flatten() if n_topics > 1 else [axes]

for idx, topic in enumerate(topics):
    text_data = ' '.join(df_clean[df_clean['topic_category'] == topic]['processed_text'])
    
    if text_data.strip():
        wc = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            colormap='plasma',
            max_words=60,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(text_data)
        
        axes[idx].imshow(wc, interpolation='bilinear')
    
    axes[idx].axis('off')
    axes[idx].set_title(topic, fontsize=14, fontweight='bold')

# Hide unused subplots
for idx in range(n_topics, len(axes)):
    axes[idx].axis('off')

plt.tight_layout()
plt.savefig('output/wordclouds/wordcloud_by_topic.png', dpi=300, bbox_inches='tight')
plt.show()

print('✓ Wordcloud per topik disimpan: output/wordclouds/wordcloud_by_topic.png')


# ============================================================================
# TAHAP 7: Analisis Kritis
# ============================================================================

print('\n=== TAHAP 7: ANALISIS KRITIS ===')
print('Fokus Analisis:')
print('1. Kesadaran Web3')
print('2. Polarisasi Opini')
print('3. Sentimen Per Topik')
print('4. Tren Temporal')

# 1. Analisis Kesadaran Web3
print('\n--- Analisis Kesadaran Web3 ---')
web3_keywords = ['web3', 'blockchain', 'crypto', 'cryptocurrency', 'decentralized', 
                 'terdesentralisasi', 'nft', 'metaverse', 'defi', 'smart', 'contract',
                 'token', 'bitcoin', 'ethereum']

# Hitung frekuensi mention
keyword_mentions = {}
for keyword in web3_keywords:
    count = sum(1 for text in df_clean['processed_text'] if keyword in text.split())
    if count > 0:
        keyword_mentions[keyword] = count

keyword_df = pd.DataFrame(list(keyword_mentions.items()), columns=['keyword', 'mentions'])
keyword_df = keyword_df.sort_values('mentions', ascending=False)
keyword_df.to_csv('output/data/web3_keyword_mentions.csv', index=False, encoding='utf-8')

print('✓ Analisis kesadaran Web3 selesai')
print('\nTop 10 Keyword Web3:')
print(keyword_df.head(10))

# Visualisasi keyword mentions
plt.figure(figsize=(12, 6))
plt.bar(keyword_df['keyword'][:15], keyword_df['mentions'][:15], color='#3498db')
plt.xlabel('Keyword', fontsize=12)
plt.ylabel('Jumlah Mention', fontsize=12)
plt.title('Frekuensi Mention Keyword Web3 di TikTok Indonesia', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('output/graphs/web3_keyword_mentions.png', dpi=300, bbox_inches='tight')
plt.show()

print('✓ Grafik keyword mentions disimpan: output/graphs/web3_keyword_mentions.png')


# 2. Polarisasi Opini
print('\n--- Polarisasi Opini ---')
polarization_score = (sentiment_dist.get('positif', 0) + sentiment_dist.get('negatif', 0)) / len(df_clean) * 100
neutral_pct = sentiment_dist.get('netral', 0) / len(df_clean) * 100

print(f'Polarisasi: {polarization_score:.1f}% (positif + negatif)')
print(f'Netral: {neutral_pct:.1f}%')

if polarization_score > 60:
    print('→ Opini publik TERPOLARISASI (banyak pendapat ekstrem)')
elif neutral_pct > 50:
    print('→ Opini publik NETRAL (mayoritas tidak berpendapat ekstrem)')
else:
    print('→ Opini publik SEIMBANG')


# 3. Sentimen Per Topik
print('\n--- Sentimen Per Topik ---')
sentiment_by_topic = pd.crosstab(df_clean['topic_category'], df_clean['sentiment_label'], normalize='index') * 100
sentiment_by_topic = sentiment_by_topic.round(1)
sentiment_by_topic.to_csv('output/data/sentiment_by_topic.csv', encoding='utf-8')

print('✓ Sentimen per topik:')
print(sentiment_by_topic)

# Visualisasi sentimen per topik
sentiment_by_topic.plot(kind='bar', stacked=False, figsize=(12, 6), 
                        color=['#2ecc71', '#e74c3c', '#95a5a6'])
plt.xlabel('Topik', fontsize=12)
plt.ylabel('Persentase (%)', fontsize=12)
plt.title('Distribusi Sentimen Per Topik Web3', fontsize=14, fontweight='bold')
plt.legend(title='Sentimen', labels=['Negatif', 'Netral', 'Positif'])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('output/graphs/sentiment_by_topic.png', dpi=300, bbox_inches='tight')
plt.show()

print('✓ Grafik sentimen per topik disimpan: output/graphs/sentiment_by_topic.png')


# 4. Summary Report
print('\n=== SUMMARY REPORT ===')
summary = {
    'total_data': len(df_clean),
    'total_videos': df_clean['video_id'].nunique(),
    'sentiment_distribution': sentiment_dist.to_dict(),
    'top_5_words': freq_df.head(5)['word'].tolist(),
    'top_5_topics': df_clean['topic_category'].value_counts().head(5).to_dict(),
    'polarization_score': round(polarization_score, 2),
    'neutral_percentage': round(neutral_pct, 2)
}

with open('output/data/summary_report.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print('✓ Summary report disimpan: output/data/summary_report.json')
print('\n--- RINGKASAN HASIL ANALISIS ---')
print(f'Total Data: {summary["total_data"]} comment')
print(f'Total Video: {summary["total_videos"]} video')
print(f'\nDistribusi Sentimen:')
for label, count in summary['sentiment_distribution'].items():
    pct = count / summary['total_data'] * 100
    print(f'  {label.capitalize()}: {count} ({pct:.1f}%)')
print(f'\nTop 5 Kata: {", ".join(summary["top_5_words"])}')
print(f'Polarisasi Opini: {summary["polarization_score"]}%')

print('\n' + '='*80)
print('✓ ANALISIS SELESAI!')
print('✓ Semua hasil tersimpan di folder output/')
print('='*80)


# ============================================================================
# TAHAP TAMBAHAN: Analisis Tren Temporal (sesuai proposal)
# ============================================================================

print('\n=== ANALISIS TREN TEMPORAL ===')

# Cek apakah ada kolom date
if 'date' in df_clean.columns:
    # Convert date column to datetime
    df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
    
    # Filter data yang memiliki tanggal valid
    df_temporal = df_clean[df_clean['date'].notna()].copy()
    
    if len(df_temporal) > 0:
        # Group by week
        df_temporal['week'] = df_temporal['date'].dt.to_period('W')
        
        # 1. Sentiment trend over time
        print('\n--- Tren Sentimen per Minggu ---')
        sentiment_by_week = df_temporal.groupby(['week', 'sentiment_label']).size().unstack(fill_value=0)
        sentiment_by_week_pct = sentiment_by_week.div(sentiment_by_week.sum(axis=1), axis=0) * 100
        
        # Plot sentiment trend
        plt.figure(figsize=(14, 6))
        sentiment_by_week_pct.plot(kind='line', marker='o', linewidth=2)
        plt.xlabel('Minggu', fontsize=12)
        plt.ylabel('Persentase (%)', fontsize=12)
        plt.title('Tren Sentimen dari Waktu ke Waktu', fontsize=14, fontweight='bold')
        plt.legend(title='Sentimen', labels=['Negatif', 'Netral', 'Positif'])
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('output/graphs/sentiment_trend_temporal.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print('✓ Grafik tren sentimen disimpan: output/graphs/sentiment_trend_temporal.png')
        
        # 2. Keyword frequency over time
        print('\n--- Tren Keyword Web3 per Minggu ---')
        
        # Track top keywords over time
        top_keywords = ['web3', 'blockchain', 'crypto', 'nft', 'metaverse']
        keyword_trend = {}
        
        for keyword in top_keywords:
            keyword_trend[keyword] = []
            for week in df_temporal['week'].unique():
                week_data = df_temporal[df_temporal['week'] == week]
                count = sum(1 for text in week_data['processed_text'] if keyword in text.split())
                keyword_trend[keyword].append(count)
        
        # Plot keyword trend
        plt.figure(figsize=(14, 6))
        weeks = sorted(df_temporal['week'].unique())
        for keyword in top_keywords:
            plt.plot(range(len(weeks)), keyword_trend[keyword], marker='o', label=keyword, linewidth=2)
        
        plt.xlabel('Minggu', fontsize=12)
        plt.ylabel('Jumlah Mention', fontsize=12)
        plt.title('Tren Mention Keyword Web3 dari Waktu ke Waktu', fontsize=14, fontweight='bold')
        plt.legend(title='Keyword')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('output/graphs/keyword_trend_temporal.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print('✓ Grafik tren keyword disimpan: output/graphs/keyword_trend_temporal.png')
        
        # 3. Emerging topics detection
        print('\n--- Deteksi Emerging Topics ---')
        
        # Compare first half vs second half
        weeks_sorted = sorted(df_temporal['week'].unique())
        mid_point = len(weeks_sorted) // 2
        
        first_half = df_temporal[df_temporal['week'].isin(weeks_sorted[:mid_point])]
        second_half = df_temporal[df_temporal['week'].isin(weeks_sorted[mid_point:])]
        
        # Get word frequency for each period
        words_first = Counter(' '.join(first_half['processed_text']).split())
        words_second = Counter(' '.join(second_half['processed_text']).split())
        
        # Find emerging words (higher frequency in second half)
        emerging = {}
        for word, count2 in words_second.most_common(100):
            count1 = words_first.get(word, 0)
            if count1 > 0:
                growth = (count2 - count1) / count1 * 100
                if growth > 50:  # At least 50% growth
                    emerging[word] = {
                        'first_half': count1,
                        'second_half': count2,
                        'growth_pct': round(growth, 1)
                    }
        
        # Sort by growth
        emerging_sorted = sorted(emerging.items(), key=lambda x: x[1]['growth_pct'], reverse=True)[:20]
        
        if emerging_sorted:
            print('\nTop 10 Emerging Topics (pertumbuhan tertinggi):')
            for i, (word, stats) in enumerate(emerging_sorted[:10], 1):
                print(f'{i}. {word}: {stats["first_half"]} → {stats["second_half"]} (+{stats["growth_pct"]}%)')
            
            # Save to CSV
            emerging_df = pd.DataFrame([
                {'word': word, **stats} for word, stats in emerging_sorted
            ])
            emerging_df.to_csv('output/data/emerging_topics.csv', index=False, encoding='utf-8')
            print('\n✓ Emerging topics disimpan: output/data/emerging_topics.csv')
        else:
            print('Tidak ada emerging topics yang signifikan terdeteksi')
        
    else:
        print('⚠ Tidak ada data dengan tanggal valid untuk analisis temporal')
else:
    print('⚠ Kolom "date" tidak ditemukan dalam dataset')
    print('  Analisis temporal dilewati')


# ============================================================================
# FINAL SUMMARY & RECOMMENDATIONS
# ============================================================================

print('\n' + '='*80)
print('=== FINAL SUMMARY & RECOMMENDATIONS ===')
print('='*80)

print('\n📊 HASIL ANALISIS:')
print(f'1. Total Data Dianalisis: {len(df_clean)} comment dari {df_clean["video_id"].nunique()} video')
print(f'2. Distribusi Sentimen:')
for label in ['positif', 'netral', 'negatif']:
    count = sentiment_dist.get(label, 0)
    pct = count / len(df_clean) * 100
    print(f'   - {label.capitalize()}: {count} ({pct:.1f}%)')

print(f'\n3. Top 5 Kata Paling Sering: {", ".join(freq_df.head(5)["word"].tolist())}')
print(f'4. Polarisasi Opini: {polarization_score:.1f}%')

if polarization_score > 60:
    print('   → Opini publik TERPOLARISASI (banyak pendapat ekstrem)')
elif neutral_pct > 50:
    print('   → Opini publik NETRAL (mayoritas tidak berpendapat ekstrem)')
else:
    print('   → Opini publik SEIMBANG')

print(f'\n5. Topik Paling Banyak Dibahas:')
top_topics = df_clean['topic_category'].value_counts().head(3)
for topic, count in top_topics.items():
    pct = count / len(df_clean) * 100
    print(f'   - {topic}: {count} ({pct:.1f}%)')

print(f'\n6. Kesadaran Web3:')
web3_mention_rate = (keyword_df['mentions'].sum() / len(df_clean)) * 100
print(f'   - Tingkat mention keyword Web3: {web3_mention_rate:.1f}%')
if web3_mention_rate > 50:
    print('   → Kesadaran TINGGI')
elif web3_mention_rate > 20:
    print('   → Kesadaran SEDANG')
else:
    print('   → Kesadaran RENDAH')

print('\n📁 OUTPUT FILES:')
print('Data:')
print('  - output/data/preprocessed_data.csv')
print('  - output/data/sentiment_results.csv')
print('  - output/data/final_data_with_topics.csv')
print('  - output/data/word_frequency.csv')
print('  - output/data/tfidf_scores.csv')
print('  - output/data/web3_keyword_mentions.csv')
print('  - output/data/sentiment_by_topic.csv')
print('  - output/data/summary_report.json')
if 'date' in df_clean.columns and len(df_temporal) > 0:
    print('  - output/data/emerging_topics.csv')

print('\nGrafik:')
print('  - output/graphs/sentiment_distribution.png')
print('  - output/graphs/top_words_comparison.png')
print('  - output/graphs/web3_keyword_mentions.png')
print('  - output/graphs/sentiment_by_topic.png')
if 'date' in df_clean.columns and len(df_temporal) > 0:
    print('  - output/graphs/sentiment_trend_temporal.png')
    print('  - output/graphs/keyword_trend_temporal.png')

print('\nWordcloud:')
print('  - output/wordclouds/wordcloud_overall.png')
print('  - output/wordclouds/wordcloud_by_sentiment.png')
print('  - output/wordclouds/wordcloud_by_topic.png')

print('\nLexicon:')
print('  - output/data/positive_lexicon.json')
print('  - output/data/negative_lexicon.json')

print('\n💡 REKOMENDASI:')
print('1. Gunakan hasil analisis ini untuk memahami persepsi publik Indonesia terhadap Web3')
print('2. Perhatikan topik dengan sentimen negatif tinggi untuk edukasi lebih lanjut')
print('3. Manfaatkan emerging topics untuk mengidentifikasi tren baru')
print('4. Kamus sentimen dapat digunakan untuk penelitian lanjutan')
print('5. Dataset dapat menjadi benchmark untuk metode sentiment analysis lain')

print('\n' + '='*80)
print('✅ ANALISIS SELESAI!')
print('✅ Semua hasil tersimpan di folder output/')
print('✅ Script sesuai dengan METODOLOGI_PENELITIAN.md dan tiktok_sentiment_proposal.md')
print('='*80)



# ============================================================================
# CATATAN PENTING: Mengatasi Masalah "Terlalu Banyak Netral"
# ============================================================================

print('\n' + '='*80)
print('📝 CATATAN: Jika hasil menunjukkan terlalu banyak NETRAL')
print('='*80)
print('''
PENYEBAB:
1. Komentar TikTok sering pendek dan informatif (contoh: "harga btc", "cara beli")
2. Banyak pertanyaan yang memang netral (contoh: "bitcoin itu apa?")
3. Lexicon basic belum mencakup semua kata slang TikTok Indonesia

SOLUSI (TIDAK PERLU MODEL BESAR!):
✅ Gunakan script improved: tiktok_sentiment_analysis_improved.py
   - Lexicon diperluas 3x lipat (300+ positif, 200+ negatif)
   - Context-aware rules
   - Deteksi pertanyaan vs opini
   - Intensifier detection (sangat, banget, dll)
   - Confidence scoring

CARA PAKAI:
1. Import improved version:
   from tiktok_sentiment_analysis_improved import compare_methods
   
2. Jalankan comparison:
   df_improved = compare_methods(df_clean)
   
3. Hasil akan menunjukkan:
   - Perbandingan distribusi lama vs baru
   - Pengurangan % netral
   - Visualisasi side-by-side

ALTERNATIF LAIN (jika masih kurang):
1. Manual review: Tambahkan kata-kata spesifik ke lexicon
2. Bigram/Trigram: Deteksi frasa (contoh: "sangat bagus", "tidak suka")
3. Emoji sentiment: Tambahkan scoring untuk emoji
4. Hybrid: Kombinasi rule-based + simple ML (Naive Bayes)

CATATAN: Rule-based sudah cukup untuk penelitian akademik!
Model besar (BERT, GPT) overkill untuk kasus ini dan tidak transparan.
''')
print('='*80)


# ============================================================================
# TAHAP 8: Advanced Visualizations (Professional)
# ============================================================================

print('\n=== TAHAP 8: ADVANCED VISUALIZATIONS ===')
print('Generating professional visualizations for publication...')

# 1. Heatmap - Sentimen per Topik
print('\n--- Creating Heatmap ---')
try:
    sentiment_topic = pd.crosstab(
        df_clean['topic_category'], 
        df_clean['sentiment_label'], 
        normalize='index'
    ) * 100
    
    col_order = ['positif', 'netral', 'negatif']
    sentiment_topic = sentiment_topic[[c for c in col_order if c in sentiment_topic.columns]]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(
        sentiment_topic, 
        annot=True, 
        fmt='.1f',
        cmap='RdYlGn',
        center=33.33,
        cbar_kws={'label': 'Persentase (%)'},
        linewidths=0.5,
        linecolor='white',
        ax=ax
    )
    
    ax.set_title('Heatmap Distribusi Sentimen per Topik Web3', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Sentimen', fontsize=13, fontweight='bold')
    ax.set_ylabel('Topik', fontsize=13, fontweight='bold')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    
    plt.tight_layout()
    plt.savefig('output/graphs/advanced_heatmap_sentiment_topic.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print('✓ Heatmap saved: output/graphs/advanced_heatmap_sentiment_topic.png')
except Exception as e:
    print(f'⚠ Error creating heatmap: {e}')


# 2. Radar Chart - Profil Sentimen
print('\n--- Creating Radar Chart ---')
try:
    topics = df_clean['topic_category'].unique()[:6]
    categories = ['Positif', 'Netral', 'Negatif']
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(topics)))
    
    for idx, topic in enumerate(topics):
        topic_data = df_clean[df_clean['topic_category'] == topic]
        
        values = []
        for sentiment in ['positif', 'netral', 'negatif']:
            pct = (topic_data['sentiment_label'] == sentiment).sum() / len(topic_data) * 100
            values.append(pct)
        
        values += values[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2, label=topic, color=colors[idx])
        ax.fill(angles, values, alpha=0.15, color=colors[idx])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=12)
    ax.set_ylim(0, 100)
    ax.set_title('Profil Sentimen per Topik Web3\n(Radar Chart)', 
                 size=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('output/graphs/advanced_radar_sentiment_profile.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print('✓ Radar chart saved: output/graphs/advanced_radar_sentiment_profile.png')
except Exception as e:
    print(f'⚠ Error creating radar chart: {e}')


# 3. Violin Plot - Distribusi Skor
print('\n--- Creating Violin Plot ---')
try:
    fig, ax = plt.subplots(figsize=(14, 8))
    
    parts = ax.violinplot(
        [df_clean[df_clean['topic_category'] == topic]['sentiment_score'].values 
         for topic in df_clean['topic_category'].unique()],
        positions=range(len(df_clean['topic_category'].unique())),
        showmeans=True,
        showmedians=True,
        widths=0.7
    )
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(df_clean['topic_category'].unique())))
    for idx, pc in enumerate(parts['bodies']):
        pc.set_facecolor(colors[idx])
        pc.set_alpha(0.7)
    
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Netral (0)')
    
    ax.set_xticks(range(len(df_clean['topic_category'].unique())))
    ax.set_xticklabels(df_clean['topic_category'].unique(), rotation=45, ha='right')
    ax.set_ylabel('Skor Sentimen', fontsize=13, fontweight='bold')
    ax.set_title('Distribusi Skor Sentimen per Topik (Violin Plot)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/graphs/advanced_violin_sentiment_distribution.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print('✓ Violin plot saved: output/graphs/advanced_violin_sentiment_distribution.png')
except Exception as e:
    print(f'⚠ Error creating violin plot: {e}')


# 4. Infographic Summary
print('\n--- Creating Infographic Summary ---')
try:
    fig = plt.figure(figsize=(16, 20))
    gs = fig.add_gridspec(5, 2, hspace=0.4, wspace=0.3)
    
    colors_map = {'positif': '#2ecc71', 'netral': '#95a5a6', 'negatif': '#e74c3c'}
    
    # Title
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.text(0.5, 0.5, 'ANALISIS SENTIMEN WEB3 DI TIKTOK INDONESIA', 
                 ha='center', va='center', fontsize=28, fontweight='bold')
    ax_title.text(0.5, 0.2, f'Total Data: {len(df_clean):,} Comment | {df_clean["video_id"].nunique()} Video', 
                 ha='center', va='center', fontsize=16, color='gray')
    ax_title.axis('off')
    
    # Sentiment Distribution (Pie)
    ax1 = fig.add_subplot(gs[1, 0])
    sentiment_counts = df_clean['sentiment_label'].value_counts()
    ax1.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
           colors=[colors_map[l] for l in sentiment_counts.index], startangle=90,
           textprops={'fontsize': 12, 'fontweight': 'bold'})
    ax1.set_title('Distribusi Sentimen', fontsize=14, fontweight='bold', pad=10)
    
    # Top Topics (Horizontal Bar)
    ax2 = fig.add_subplot(gs[1, 1])
    top_topics = df_clean['topic_category'].value_counts().head(5)
    ax2.barh(range(len(top_topics)), top_topics.values, color='steelblue')
    ax2.set_yticks(range(len(top_topics)))
    ax2.set_yticklabels(top_topics.index, fontsize=10)
    ax2.set_xlabel('Jumlah', fontsize=11)
    ax2.set_title('Top 5 Topik Terpopuler', fontsize=14, fontweight='bold', pad=10)
    ax2.invert_yaxis()
    
    # Sentiment by Topic (Stacked Bar)
    ax3 = fig.add_subplot(gs[2, :])
    sentiment_topic_plot = pd.crosstab(df_clean['topic_category'], df_clean['sentiment_label'], normalize='index') * 100
    sentiment_topic_plot = sentiment_topic_plot[[c for c in ['positif', 'netral', 'negatif'] if c in sentiment_topic_plot.columns]]
    sentiment_topic_plot.plot(kind='barh', stacked=True, ax=ax3, 
                        color=[colors_map[c] for c in sentiment_topic_plot.columns],
                        legend=True)
    ax3.set_xlabel('Persentase (%)', fontsize=11)
    ax3.set_title('Sentimen per Topik', fontsize=14, fontweight='bold', pad=10)
    ax3.legend(title='Sentimen', loc='lower right')
    
    # Top Keywords
    ax4 = fig.add_subplot(gs[3, :])
    all_words = ' '.join(df_clean['processed_text']).split()
    word_freq_plot = Counter(all_words)
    top_20 = pd.DataFrame(word_freq_plot.most_common(20), columns=['word', 'freq'])
    ax4.barh(range(len(top_20)), top_20['freq'], color='coral')
    ax4.set_yticks(range(len(top_20)))
    ax4.set_yticklabels(top_20['word'], fontsize=9)
    ax4.set_xlabel('Frekuensi', fontsize=11)
    ax4.set_title('Top 20 Kata Paling Sering Muncul', fontsize=14, fontweight='bold', pad=10)
    ax4.invert_yaxis()
    
    # Key Insights
    ax5 = fig.add_subplot(gs[4, :])
    insights = f"""
    KEY INSIGHTS:
    
    • Sentimen Dominan: {sentiment_counts.index[0].upper()} ({sentiment_counts.values[0]/len(df_clean)*100:.1f}%)
    • Topik Terpopuler: {top_topics.index[0]}
    • Total Kata Unik: {len(set(all_words)):,}
    • Rata-rata Panjang Comment: {df_clean['processed_text'].str.split().str.len().mean():.1f} kata
    • Polarisasi Opini: {(sentiment_counts.get('positif', 0) + sentiment_counts.get('negatif', 0))/len(df_clean)*100:.1f}%
    """
    ax5.text(0.1, 0.5, insights, fontsize=13, verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    ax5.axis('off')
    
    plt.suptitle('', fontsize=1)
    plt.savefig('output/graphs/advanced_infographic_summary.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print('✓ Infographic saved: output/graphs/advanced_infographic_summary.png')
except Exception as e:
    print(f'⚠ Error creating infographic: {e}')

print('\n✓ Advanced visualizations completed!')
