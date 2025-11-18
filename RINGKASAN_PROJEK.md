# Ringkasan Projek Penelitian

## Tema Penelitian

**Sentimen dan Persepsi Publik Indonesia di TikTok pada Era Web3**

---

## Judul Projek

**Analisis Persepsi Pengguna Indonesia terhadap Isu Sosial di TikTok Menggunakan Sentiment Analysis dan Visualisasi Wordcloud di Era Web3**

---

## Penjelasan Projek

### Latar Belakang

Penelitian ini berangkat dari kebutuhan untuk memahami bagaimana masyarakat Indonesia merespons dan memahami konsep-konsep Web3 yang masih relatif baru. TikTok, dengan lebih dari 109 juta pengguna aktif di Indonesia, telah menjadi platform utama untuk diskusi teknologi dan isu sosial. Namun, opini yang terbentuk seringkali bersifat emosional, tidak terstruktur, dan sulit dipetakan secara sistematis.

### Tujuan

Projek ini bertujuan untuk menganalisis persepsi dan sentimen publik Indonesia terhadap isu sosial era Web3 melalui data TikTok menggunakan pendekatan rule-based sentiment analysis dan visualisasi data. Secara khusus, penelitian ini akan:

- Mengumpulkan data komentar dan caption dari TikTok terkait isu sosial Web3
- Melakukan analisis sentimen berbasis kamus kata positif-negatif yang disesuaikan dengan bahasa Indonesia informal
- Mengidentifikasi tren topik dan kata dominan menggunakan visualisasi wordcloud
- Menyusun peta persepsi publik terhadap isu sosial digital
- Menganalisis tingkat kesadaran masyarakat Indonesia terhadap konsep Web3

### Metode

Penelitian ini menggunakan pendekatan kuantitatif deskriptif dengan metode text mining dan sentiment analysis. Proses penelitian dibagi menjadi enam tahapan utama:

1. **Pengumpulan Data**: Scraping TikTok menggunakan Selenium + Firefox dengan metode dua tahap
2. **Pra-Pemrosesan Data**: Case folding, tokenisasi, stopword removal, normalisasi, dan filtering
3. **Analisis Sentimen**: Rule-based sentiment analysis menggunakan kamus sentimen lokal
4. **Analisis Topik**: Frequency analysis dan TF-IDF untuk identifikasi kata kunci dominan
5. **Visualisasi**: Pembuatan wordcloud dan grafik distribusi sentimen
6. **Analisis Kritis**: Interpretasi mendalam tentang kesadaran Web3 dan polarisasi opini

### Keunggulan

Penelitian ini memiliki beberapa keunggulan dibandingkan pendekatan konvensional:

- **Transparan**: Menggunakan metode rule-based yang dapat dijelaskan, bukan black-box AI
- **Konteks Lokal**: Disesuaikan dengan bahasa Indonesia informal dan slang TikTok
- **Independen**: Tidak bergantung pada model AI besar atau API berbayar
- **Komprehensif**: Mencakup analisis sentimen, topik, dan visualisasi dalam satu framework
- **Praktis**: Menghasilkan insight yang actionable untuk stakeholder

---

## Sumber Data dan API

### Platform Sumber Data

**TikTok Indonesia** dipilih sebagai sumber data utama dengan pertimbangan:

- Platform media sosial dengan pertumbuhan tercepat di Indonesia (109+ juta pengguna aktif)
- Demografi pengguna mayoritas berusia 16-35 tahun (target audience Web3)
- Format konten video pendek yang mendorong diskusi spontan dan autentik
- Algoritma powerful yang menangkap tren dan sentimen publik secara real-time

### Metode Pengumpulan Data

Penelitian ini menggunakan **web scraping dengan Selenium + Firefox** sebagai metode pengumpulan data. Metode ini dipilih karena:

- Tidak memerlukan API key atau subscription berbayar
- Memberikan full control terhadap proses scraping
- Firefox lebih susah dideteksi sebagai bot dibandingkan Chrome
- Dapat handle berbagai layout TikTok (normal comment dan side comment)
- Geckodriver dapat di-download otomatis

### Tool Scraping

Penelitian ini mengembangkan dua tool scraping utama:

**1. scraper_link_video_tt.py**
- Fungsi: Mengumpulkan link video dari halaman pencarian TikTok
- Input: URL pencarian dengan query Web3-related
- Filter: Keyword Web3 di title/caption + minimum 1000 likes
- Output: `tiktok_links.txt` dan `tiktok_links.csv`

**2. scraper_firefox.py**
- Fungsi: Mengekstrak detail video dan semua komentar
- Input: File `tiktok_links.txt`
- Fitur: Auto-detect comment mode, smart scrolling, expand replies, auto-save
- Output: `scraped_data.csv` dengan struktur lengkap

### URL Pencarian yang Digunakan

| No | Query Pencarian | URL |
|----|----------------|-----|
| 1 | Web3 Blockchain Crypto Indonesia | `https://www.tiktok.com/search/video?q=web3%20blockchain%20crypto%20Indonesia` |
| 2 | Cryptocurrency Indonesia | `https://www.tiktok.com/search/video?q=cryptocurrency%20Indonesia` |
| 3 | NFT Indonesia | `https://www.tiktok.com/search/video?q=NFT%20Indonesia` |
| 4 | Blockchain Indonesia | `https://www.tiktok.com/search/video?q=blockchain%20Indonesia` |
| 5 | Kripto Indonesia | `https://www.tiktok.com/search/video?q=kripto%20Indonesia` |

### Struktur Data yang Dikumpulkan

| Field | Deskripsi |
|-------|-----------|
| `video_id` | ID unik video |
| `username` | Username creator (dapat dienkripsi) |
| `caption` | Teks caption video |
| `comment` | Teks komentar pengguna |
| `likes` | Jumlah likes pada video |
| `hashtags` | Daftar hashtag yang digunakan |
| `date` | Tanggal scraping |

### Alternatif Sumber Data

Meskipun menggunakan web scraping sebagai metode utama, terdapat beberapa alternatif yang dapat dipertimbangkan:

- **TikTok Official API**: Akses resmi namun memerlukan approval dan rate limiting ketat
- **RapidAPI TikTok Scraper**: API third-party berbayar dengan fitur lengkap
- **Apify TikTok Scraper**: Platform scraping as a service dengan model pay-per-use
- **Pre-collected Datasets**: Dataset publik dari Kaggle atau academic repositories (jika tersedia)

---

## Visualisasi Wordcloud

### Konsep Wordcloud

Wordcloud (atau word map) adalah representasi visual dari data teks di mana ukuran setiap kata menunjukkan frekuensi atau kepentingannya dalam teks. Kata yang lebih sering muncul ditampilkan lebih besar dan lebih mencolok. Dalam penelitian ini, wordcloud digunakan untuk mengidentifikasi cepat tema dominan dan buzzwords dalam diskusi Web3 di TikTok Indonesia.

**[IMAGE: Contoh wordcloud umum untuk referensi visual]**

### Jenis Wordcloud yang Dibuat

Penelitian ini menghasilkan beberapa jenis wordcloud untuk perspektif analisis yang berbeda:

#### 1. Wordcloud Keseluruhan
- Menampilkan semua kata dominan dari seluruh dataset
- Menunjukkan buzzwords umum dalam diskusi Web3
- Ukuran kata proporsional dengan frekuensi kemunculan
- Warna: Gradasi viridis untuk variasi visual

#### 2. Wordcloud Per Sentimen

**Wordcloud Positif**
- Kata-kata dari komentar bersentimen positif
- Colormap: Greens (gradasi hijau)
- Menunjukkan aspek Web3 yang diterima positif oleh publik

**Wordcloud Negatif**
- Kata-kata dari komentar bersentimen negatif
- Colormap: Reds (gradasi merah)
- Menunjukkan kekhawatiran dan kritik terhadap Web3

**Wordcloud Netral**
- Kata-kata dari komentar bersentimen netral
- Colormap: Greys (gradasi abu-abu)
- Menunjukkan diskusi informatif tanpa bias sentimen

#### 3. Wordcloud Per Topik

Wordcloud dibuat untuk setiap kategori isu sosial Web3:

- **AI Ethics Wordcloud**: Kata dominan dalam diskusi etika AI
- **Blockchain Wordcloud**: Kata dominan dalam diskusi blockchain dan crypto
- **Sustainability Wordcloud**: Kata dominan dalam diskusi keberlanjutan
- **Digital Freedom Wordcloud**: Kata dominan dalam diskusi kebebasan digital
- **Privacy Wordcloud**: Kata dominan dalam diskusi privasi data
- **NFT & Metaverse Wordcloud**: Kata dominan dalam diskusi NFT dan metaverse

### Spesifikasi Teknis Wordcloud

Semua wordcloud dibuat dengan spesifikasi standar untuk konsistensi:

- **Resolusi**: 1600 x 800 pixels minimum
- **Format**: PNG dengan transparansi
- **DPI**: 300 untuk kualitas publikasi
- **Max words**: 100-150 kata per wordcloud
- **Font**: Sans-serif untuk keterbacaan optimal
- **Background**: White untuk kontras maksimal

### Interpretasi Wordcloud

Wordcloud memberikan insight visual yang mudah dipahami:

- **Ukuran kata**: Kata besar = frekuensi tinggi = topik penting
- **Posisi kata**: Tengah biasanya kata paling dominan, pinggir kata dengan frekuensi lebih rendah
- **Warna**: Dalam wordcloud sentimen, warna menunjukkan polaritas (hijau=positif, merah=negatif)
- **Clustering visual**: Kata-kata yang sering muncul bersama cenderung berdekatan

### Output Wordcloud

Semua wordcloud disimpan dalam folder `output/wordclouds/` dengan naming convention yang jelas:

- `wordcloud_overall.png` - Wordcloud keseluruhan
- `wordcloud_positive.png` - Wordcloud sentimen positif
- `wordcloud_negative.png` - Wordcloud sentimen negatif
- `wordcloud_neutral.png` - Wordcloud sentimen netral
- `wordcloud_ai_ethics.png` - Wordcloud topik AI Ethics
- `wordcloud_blockchain.png` - Wordcloud topik Blockchain
- `wordcloud_sustainability.png` - Wordcloud topik Sustainability
- `wordcloud_digital_freedom.png` - Wordcloud topik Digital Freedom
- `wordcloud_privacy.png` - Wordcloud topik Privacy
- `wordcloud_nft_metaverse.png` - Wordcloud topik NFT & Metaverse

Setiap wordcloud disertai dengan file CSV yang berisi top 20 kata dengan frekuensi kemunculannya untuk analisis kuantitatif lebih lanjut.

### Manfaat Wordcloud dalam Penelitian

Wordcloud memberikan beberapa manfaat penting dalam penelitian ini:

- **Identifikasi Cepat**: Menangkap tema dominan dalam hitungan detik
- **Komunikasi Efektif**: Lebih mudah dipahami audiens non-teknis dibanding tabel angka
- **Validasi Analisis**: Memvalidasi hasil analisis kuantitatif secara visual
- **Eksplorasi Data**: Menemukan pola yang tidak terduga dalam diskusi
- **Presentasi Menarik**: Visual yang compelling untuk publikasi dan presentasi

