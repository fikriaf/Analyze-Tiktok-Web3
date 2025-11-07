# Analisis Sentimen TikTok: Persepsi Publik terhadap Isu Sosial Web3

Implementasi lengkap metodologi penelitian untuk menganalisis persepsi pengguna TikTok terhadap isu sosial di era Web3 menggunakan sentiment analysis dan visualisasi wordcloud.

## 📋 Deskripsi Proyek

Proyek ini mengimplementasikan analisis sentimen berbasis rule-based (lexicon-based) untuk memahami persepsi publik Indonesia terhadap isu-isu Web3 seperti AI ethics, blockchain, cryptocurrency, NFT, metaverse, sustainability, dan privacy di platform TikTok.

## 🎯 Tujuan

1. Mengumpulkan data komentar dan caption dari TikTok terkait isu sosial Web3
2. Melakukan analisis sentimen menggunakan metode rule-based
3. Mengidentifikasi tren topik dan kata dominan
4. Membuat visualisasi wordcloud untuk berbagai kategori
5. Menganalisis kesadaran masyarakat terhadap Web3

## 📊 Metodologi

### Tahapan Penelitian:

1. **Pengumpulan Data**
   - Scraping TikTok berdasarkan hashtag target
   - Target: #AIethics, #blockchain, #sustainability, #web3, #digitalfreedom, #cryptocurrency, #NFT, #metaverse, #privacy

2. **Pra-Pemrosesan Data**
   - Case folding
   - Tokenisasi
   - Stopword removal
   - Normalisasi slang TikTok
   - Filtering (emoji, URL, mention, hashtag)

3. **Analisis Sentimen (Rule-based)**
   - Lexicon-based sentiment analysis
   - Kamus kata positif dan negatif dengan bobot
   - Scoring: Σ(positif × bobot) - Σ(negatif × bobot)
   - Klasifikasi: Positif / Netral / Negatif

4. **Analisis Trending Topic**
   - Frequency analysis
   - TF-IDF manual calculation
   - Identifikasi kata kunci dominan

5. **Visualisasi Wordcloud**
   - Wordcloud keseluruhan
   - Wordcloud per sentimen (positif, netral, negatif)
   - Wordcloud per topik

6. **Analisis Kritis**
   - Kesadaran Web3
   - Polarisasi opini
   - Sentimen per topik
   - Tren temporal

## 🚀 Cara Menggunakan

### Prerequisites

```bash
pip install pandas numpy matplotlib seaborn wordcloud
```

Untuk scraping (pilih salah satu):
```bash
# Opsi 1: TikTokApi (unofficial)
pip install TikTokApi
playwright install

# Opsi 2: Gunakan RapidAPI atau Apify (perlu API key)
```

### Menjalankan Notebook

1. Buka Jupyter Notebook:
```bash
jupyter notebook tiktok_sentiment_analysis.ipynb
```

2. Jalankan sel secara berurutan dari atas ke bawah

3. **PENTING:** Modifikasi fungsi `scrape_tiktok_data()` dengan implementasi scraping yang sesuai dengan API yang Anda pilih

### Struktur Output

Semua hasil analisis akan disimpan di folder `output/`:

```
output/
├── data/
│   ├── raw_data.csv                    # Data mentah hasil scraping
│   ├── preprocessed_data.csv           # Data setelah preprocessing
│   ├── sentiment_results.csv           # Hasil analisis sentimen
│   ├── final_data_with_topics.csv      # Data final dengan kategori topik
│   ├── word_frequency.csv              # Frekuensi kata
│   ├── tfidf_scores.csv                # Skor TF-IDF
│   ├── web3_awareness.csv              # Analisis kesadaran Web3
│   ├── sentiment_by_topic.csv          # Sentimen per topik
│   ├── polarization_analysis.csv       # Analisis polarisasi
│   ├── positive_lexicon.json           # Kamus kata positif
│   └── negative_lexicon.json           # Kamus kata negatif
├── graphs/
│   ├── sentiment_distribution.png      # Distribusi sentimen
│   ├── top_words_comparison.png        # Perbandingan top words
│   ├── sentiment_by_topic.png          # Sentimen per topik
│   └── sentiment_trend.png             # Tren sentimen temporal
├── wordclouds/
│   ├── wordcloud_overall.png           # Wordcloud keseluruhan
│   ├── wordcloud_by_sentiment.png      # Wordcloud per sentimen
│   └── wordcloud_by_topic.png          # Wordcloud per topik
└── SUMMARY_REPORT.txt                  # Laporan ringkasan lengkap
```

## 📈 Fitur Utama

### 1. Sentiment Analysis Rule-based
- Tidak bergantung pada model AI besar
- Menggunakan kamus sentimen lokal (bahasa Indonesia)
- Disesuaikan dengan konteks TikTok dan Web3

### 2. Preprocessing Komprehensif
- Normalisasi slang TikTok (gak → tidak, banget → sangat, dll)
- Stopword removal bahasa Indonesia
- Filtering emoji, URL, mention

### 3. Visualisasi Lengkap
- Bar charts untuk distribusi sentimen
- Wordcloud dengan berbagai kategori
- Grafik tren temporal
- Stacked bar chart sentimen per topik

### 4. Analisis Mendalam
- Kesadaran Web3 (frekuensi mention istilah kunci)
- Polarisasi opini per topik
- TF-IDF untuk identifikasi kata penting
- Kategorisasi topik otomatis

## 📝 Catatan Implementasi

### Untuk Scraping Data Real:

**Opsi 1: TikTokApi (Unofficial)**
```python
from TikTokApi import TikTokApi

api = TikTokApi()
hashtag = api.hashtag(name='web3')
videos = hashtag.videos(count=100)
```

**Opsi 2: RapidAPI**
- Daftar di https://rapidapi.com
- Subscribe ke TikTok Scraper API
- Gunakan API key untuk request

**Opsi 3: Apify**
- Daftar di https://apify.com
- Gunakan TikTok Scraper actor
- Export hasil ke CSV/JSON

### Modifikasi yang Diperlukan:

1. Ganti fungsi `scrape_tiktok_data()` dengan implementasi API yang dipilih
2. Sesuaikan struktur data dengan response API
3. Tambahkan error handling dan rate limiting
4. Implementasikan data privacy (enkripsi username)

## 📚 Referensi

- Proposal lengkap: `tiktok_sentiment_proposal.md`
- TikTokApi Documentation: https://github.com/davidteather/TikTok-Api
- WordCloud Documentation: https://amueller.github.io/word_cloud/

## 🔬 Metodologi Penelitian

Proyek ini mengikuti metodologi penelitian kuantitatif deskriptif dengan pendekatan text mining dan sentiment analysis sesuai dengan proposal penelitian lengkap.

### Keunggulan Metode Rule-based:
- ✅ Transparan dan dapat dijelaskan
- ✅ Tidak memerlukan training data besar
- ✅ Dapat disesuaikan dengan konteks lokal
- ✅ Independen dari model AI besar
- ✅ Cocok untuk bahasa Indonesia informal (TikTok)

## 📊 Luaran Penelitian

1. **Dataset Isu Sosial TikTok** - Data terstruktur dengan label sentimen
2. **Kamus Sentimen TikTok** - Lexicon bahasa Indonesia untuk TikTok
3. **Grafik Persepsi Publik** - Visualisasi distribusi sentimen
4. **Wordcloud Isu Sosial** - Representasi visual kata dominan
5. **Tren Wacana** - Analisis perubahan sentimen temporal
6. **Peta Kesadaran Web3** - Insight tentang pemahaman masyarakat

## 👥 Kontributor

Proyek ini dibuat sebagai implementasi dari proposal penelitian:
**"Analisis Persepsi Pengguna terhadap Isu Sosial di TikTok Menggunakan Sentiment Analysis dan Visualisasi Wordcloud di Era Web3"**

## 📄 Lisensi

Data yang dikumpulkan harus mematuhi:
- Terms of Service TikTok
- Kebijakan privasi data
- GDPR dan regulasi Indonesia
- Anonimisasi data pengguna

## ⚠️ Disclaimer

- Notebook ini adalah template implementasi
- Scraping TikTok memerlukan API key atau setup khusus
- Pastikan mematuhi Terms of Service platform
- Data pengguna harus dianonimkan
- Hasil analisis untuk tujuan penelitian akademis

---

**Dibuat sesuai metodologi penelitian dalam proposal**

**Semua output disimpan otomatis ke folder `output/`**
