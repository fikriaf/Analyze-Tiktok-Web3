# 📊 Panduan Visualisasi Advanced untuk Sentiment Analysis

## 🎨 Jenis Visualisasi Professional

File: `advanced_visualizations.py`

### 1. **Heatmap - Sentimen per Topik** 🔥
**Fungsi:** `create_sentiment_heatmap(df_clean)`

**Deskripsi:**
- Menunjukkan intensitas sentimen untuk setiap topik
- Warna hijau = positif, merah = negatif, kuning = netral
- Mudah melihat topik mana yang paling kontroversial

**Kegunaan:**
- ✅ Identifikasi topik dengan sentimen ekstrem
- ✅ Perbandingan antar topik
- ✅ Professional untuk publikasi akademik

**Output:** `advanced_heatmap_sentiment_topic.png`

---

### 2. **Sunburst Chart - Hierarki Topik & Sentimen** ☀️
**Fungsi:** `create_sunburst_chart(df_clean)`

**Deskripsi:**
- Visualisasi hierarki interaktif
- Lingkaran dalam = topik, lingkaran luar = sentimen
- Ukuran menunjukkan proporsi

**Kegunaan:**
- ✅ Melihat struktur data secara keseluruhan
- ✅ Interaktif (HTML) untuk presentasi
- ✅ Menarik secara visual

**Output:** 
- `advanced_sunburst_topic_sentiment.html` (interaktif)
- `advanced_sunburst_topic_sentiment.png` (static)

**Requirements:** `pip install plotly kaleido`

---

### 3. **Radar Chart - Profil Sentimen Multi-dimensi** 🎯
**Fungsi:** `create_radar_chart(df_clean)`

**Deskripsi:**
- Membandingkan profil sentimen antar topik
- Bentuk polygon menunjukkan karakteristik sentimen
- Mudah membandingkan 6 topik sekaligus

**Kegunaan:**
- ✅ Perbandingan visual yang jelas
- ✅ Identifikasi pola sentimen
- ✅ Cocok untuk presentasi

**Output:** `advanced_radar_sentiment_profile.png`

---

### 4. **Sankey Diagram - Flow Sentimen** 🌊
**Fungsi:** `create_sankey_diagram(df_clean)`

**Deskripsi:**
- Menunjukkan aliran dari topik ke sentimen
- Lebar aliran = jumlah data
- Interaktif dan mudah dipahami

**Kegunaan:**
- ✅ Visualisasi flow data
- ✅ Melihat distribusi sentimen per topik
- ✅ Sangat menarik untuk presentasi

**Output:** `advanced_sankey_topic_sentiment.html`

**Requirements:** `pip install plotly`

---

### 5. **Treemap - Proporsi Topik** 🗺️
**Fungsi:** `create_treemap(df_clean)`

**Deskripsi:**
- Kotak-kotak dengan ukuran proporsional
- Warna menunjukkan sentimen
- Hierarki topik → sentimen

**Kegunaan:**
- ✅ Melihat proporsi dengan cepat
- ✅ Space-efficient visualization
- ✅ Modern dan professional

**Output:** `advanced_treemap_topic_sentiment.html`

**Requirements:** `pip install plotly`

---

### 6. **Violin Plot - Distribusi Skor Sentimen** 🎻
**Fungsi:** `create_violin_plot(df_clean)`

**Deskripsi:**
- Menunjukkan distribusi skor sentimen per topik
- Bentuk "biola" = density distribution
- Garis tengah = median, titik = mean

**Kegunaan:**
- ✅ Analisis statistik mendalam
- ✅ Melihat outliers
- ✅ Membandingkan variabilitas antar topik

**Output:** `advanced_violin_sentiment_distribution.png`

---

### 7. **Network Graph - Co-occurrence Words** 🕸️
**Fungsi:** `create_network_graph(df_clean, top_n=20)`

**Deskripsi:**
- Node = kata kunci
- Edge = kata yang sering muncul bersamaan
- Ukuran node = frekuensi kata

**Kegunaan:**
- ✅ Melihat hubungan antar konsep
- ✅ Identifikasi cluster topik
- ✅ Analisis semantic network

**Output:** `advanced_network_cooccurrence.png`

**Requirements:** `pip install networkx`

---

### 8. **Infographic Summary - Publication Ready** 📰
**Fungsi:** `create_infographic_summary(df_clean)`

**Deskripsi:**
- Ringkasan lengkap dalam 1 halaman
- Kombinasi pie chart, bar chart, dan key insights
- Siap untuk publikasi atau presentasi

**Kegunaan:**
- ✅ Executive summary
- ✅ Poster presentasi
- ✅ Lampiran skripsi/paper

**Output:** `advanced_infographic_summary.png`

---

## 🚀 Cara Penggunaan

### Quick Start (Generate Semua)

```python
import pandas as pd
from advanced_visualizations import create_all_advanced_visualizations

# Load data
df = pd.read_csv('output/data/sentiment_results.csv')

# Generate semua visualisasi
create_all_advanced_visualizations(df)
```

### Individual Visualization

```python
from advanced_visualizations import (
    create_sentiment_heatmap,
    create_radar_chart,
    create_infographic_summary
)

# Load data
df = pd.read_csv('output/data/sentiment_results.csv')

# Generate heatmap saja
create_sentiment_heatmap(df)

# Generate radar chart saja
create_radar_chart(df)

# Generate infographic saja
create_infographic_summary(df)
```

---

## 📦 Dependencies

### Basic (Sudah Ada)
```bash
pip install pandas numpy matplotlib seaborn
```

### Advanced (Optional)
```bash
# Untuk Sunburst, Sankey, Treemap
pip install plotly kaleido

# Untuk Network Graph
pip install networkx
```

---

## 📁 Output Files

Semua file disimpan di: `output/graphs/`

### Static Images (PNG)
- `advanced_heatmap_sentiment_topic.png`
- `advanced_radar_sentiment_profile.png`
- `advanced_violin_sentiment_distribution.png`
- `advanced_network_cooccurrence.png`
- `advanced_infographic_summary.png`

### Interactive (HTML)
- `advanced_sunburst_topic_sentiment.html`
- `advanced_sankey_topic_sentiment.html`
- `advanced_treemap_topic_sentiment.html`

---

## 🎯 Rekomendasi Penggunaan

### Untuk Skripsi/Thesis:
1. ✅ **Heatmap** - Bab Hasil (menunjukkan distribusi)
2. ✅ **Violin Plot** - Bab Analisis (statistik mendalam)
3. ✅ **Infographic** - Lampiran atau Executive Summary

### Untuk Presentasi:
1. ✅ **Sunburst** - Opening (overview menarik)
2. ✅ **Sankey** - Flow analysis (mudah dipahami)
3. ✅ **Radar Chart** - Perbandingan topik

### Untuk Paper/Jurnal:
1. ✅ **Heatmap** - Figure 1 (main result)
2. ✅ **Violin Plot** - Figure 2 (statistical analysis)
3. ✅ **Network Graph** - Figure 3 (semantic analysis)

### Untuk Poster:
1. ✅ **Infographic** - All-in-one summary

---

## 🎨 Customization

### Mengubah Warna

```python
# Edit di script advanced_visualizations.py
colors = {
    'positif': '#2ecc71',  # Hijau
    'netral': '#95a5a6',   # Abu-abu
    'negatif': '#e74c3c'   # Merah
}

# Atau gunakan colormap lain
# 'viridis', 'plasma', 'inferno', 'magma', 'cividis'
# 'RdYlGn', 'RdBu', 'Spectral', 'coolwarm'
```

### Mengubah Ukuran

```python
# Untuk PNG
fig, ax = plt.subplots(figsize=(16, 10))  # width, height in inches

# Untuk HTML (Plotly)
fig.update_layout(width=1200, height=800)
```

### Mengubah DPI (Resolusi)

```python
# Untuk publikasi high-quality
plt.savefig('output.png', dpi=600)  # Very high quality

# Untuk web/presentasi
plt.savefig('output.png', dpi=150)  # Standard quality
```

---

## 💡 Tips Professional

### 1. Konsistensi Warna
Gunakan warna yang sama untuk sentimen di semua visualisasi:
- Hijau = Positif
- Abu-abu = Netral
- Merah = Negatif

### 2. Font Readable
Untuk publikasi, gunakan font size minimal:
- Title: 16-18pt
- Axis labels: 12-14pt
- Tick labels: 10-12pt

### 3. White Space
Jangan terlalu padat, beri ruang untuk breathe:
```python
plt.tight_layout(pad=2.0)
```

### 4. High Resolution
Untuk print/publikasi:
```python
plt.savefig('output.png', dpi=300, bbox_inches='tight')
```

### 5. Color Blind Friendly
Gunakan colormap yang ramah buta warna:
- ✅ 'viridis', 'plasma', 'cividis'
- ❌ 'jet', 'rainbow'

---

## 📊 Perbandingan dengan Visualisasi Basic

| Aspek | Basic (Bar/Pie) | Advanced |
|-------|----------------|----------|
| **Visual Appeal** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Information Density** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Interactivity** | ❌ | ✅ (HTML) |
| **Publication Ready** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Ease of Understanding** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Professional Look** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🔧 Troubleshooting

### Error: "No module named 'plotly'"
```bash
pip install plotly kaleido
```

### Error: "No module named 'networkx'"
```bash
pip install networkx
```

### Plotly image export tidak jalan
```bash
# Install kaleido untuk export static image
pip install kaleido

# Atau gunakan orca (alternatif)
conda install -c plotly plotly-orca
```

### Font terlalu kecil di output
```python
# Increase font scale
sns.set_context("paper", font_scale=1.5)
```

### Warna tidak muncul di heatmap
```python
# Pastikan data dalam format persentase
sentiment_topic = pd.crosstab(..., normalize='index') * 100
```

---

## ✅ Checklist untuk Publikasi

- [ ] Semua visualisasi dalam resolusi tinggi (300 dpi)
- [ ] Warna konsisten di semua grafik
- [ ] Font readable (minimal 10pt)
- [ ] Axis labels jelas dan deskriptif
- [ ] Title informatif
- [ ] Legend/caption lengkap
- [ ] White background untuk print
- [ ] File format sesuai (PNG untuk paper, HTML untuk presentasi)

---

## 📚 Referensi

**Matplotlib Gallery:**
https://matplotlib.org/stable/gallery/index.html

**Seaborn Gallery:**
https://seaborn.pydata.org/examples/index.html

**Plotly Gallery:**
https://plotly.com/python/

**Color Brewer (Color Schemes):**
https://colorbrewer2.org/

---

## 🎓 Untuk Skripsi/Thesis

### Cara Menulis Caption

**Contoh Caption Heatmap:**
```
Gambar 4.1: Heatmap Distribusi Sentimen per Topik Web3 di TikTok Indonesia.
Warna hijau menunjukkan sentimen positif, kuning netral, dan merah negatif.
Intensitas warna menunjukkan persentase sentimen pada masing-masing topik.
```

**Contoh Caption Radar Chart:**
```
Gambar 4.2: Radar Chart Profil Sentimen Multi-dimensi per Topik.
Setiap polygon mewakili satu topik dengan tiga dimensi sentimen
(positif, netral, negatif). Bentuk polygon menunjukkan karakteristik
sentimen dominan pada topik tersebut.
```

### Cara Interpretasi di Pembahasan

**Contoh Pembahasan Heatmap:**
```
Berdasarkan Gambar 4.1, terlihat bahwa topik "Blockchain & Crypto"
memiliki sentimen positif tertinggi (45.2%), menunjukkan bahwa
masyarakat Indonesia cenderung optimis terhadap teknologi blockchain.
Sebaliknya, topik "NFT & Metaverse" menunjukkan sentimen negatif
yang lebih tinggi (32.1%), mengindikasikan adanya skeptisisme
terhadap konsep NFT di kalangan pengguna TikTok Indonesia.
```

---

## 🚀 Next Level

Jika ingin lebih advanced lagi:

1. **Animated Visualizations** - Tren temporal dengan animasi
2. **3D Plots** - Visualisasi multi-dimensi
3. **Interactive Dashboard** - Plotly Dash atau Streamlit
4. **Geographic Maps** - Jika ada data lokasi
5. **Sentiment Timeline** - Line chart dengan annotations

File untuk advanced features ini bisa dibuat terpisah jika diperlukan!
