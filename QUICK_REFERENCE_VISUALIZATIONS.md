# 📊 Quick Reference: Visualisasi untuk Sentiment Analysis

## 🎯 Pilih Visualisasi Berdasarkan Tujuan

### Ingin Menunjukkan DISTRIBUSI?
```python
✅ Heatmap          - Distribusi sentimen per topik
✅ Violin Plot      - Distribusi skor sentimen
✅ Treemap          - Proporsi topik dan sentimen
```

### Ingin Menunjukkan PERBANDINGAN?
```python
✅ Radar Chart      - Perbandingan profil sentimen antar topik
✅ Heatmap          - Perbandingan intensitas sentimen
✅ Bar Chart        - Perbandingan jumlah (basic)
```

### Ingin Menunjukkan HUBUNGAN?
```python
✅ Network Graph    - Hubungan antar kata kunci
✅ Sankey Diagram   - Flow dari topik ke sentimen
✅ Sunburst Chart   - Hierarki topik-sentimen
```

### Ingin Menunjukkan OVERVIEW?
```python
✅ Infographic      - Ringkasan lengkap 1 halaman
✅ Sunburst Chart   - Overview hierarki
✅ Dashboard        - Multiple charts interaktif
```

---

## 🚀 One-Liner Commands

```python
import pandas as pd
from advanced_visualizations import *

df = pd.read_csv('output/data/sentiment_results.csv')

# Generate SEMUA visualisasi
create_all_advanced_visualizations(df)

# Atau pilih satu:
create_sentiment_heatmap(df)           # Heatmap
create_radar_chart(df)                 # Radar
create_violin_plot(df)                 # Violin
create_network_graph(df)               # Network
create_infographic_summary(df)         # Infographic
create_sunburst_chart(df)              # Sunburst (needs plotly)
create_sankey_diagram(df)              # Sankey (needs plotly)
create_treemap(df)                     # Treemap (needs plotly)
```

---

## 📦 Install Dependencies

```bash
# Basic (wajib)
pip install pandas numpy matplotlib seaborn

# Advanced (optional, untuk visualisasi interaktif)
pip install plotly kaleido networkx
```

---

## 📁 Output Files Cheat Sheet

| Visualisasi | File Output | Format | Interaktif? |
|-------------|-------------|--------|-------------|
| Heatmap | `advanced_heatmap_sentiment_topic.png` | PNG | ❌ |
| Radar | `advanced_radar_sentiment_profile.png` | PNG | ❌ |
| Violin | `advanced_violin_sentiment_distribution.png` | PNG | ❌ |
| Network | `advanced_network_cooccurrence.png` | PNG | ❌ |
| Infographic | `advanced_infographic_summary.png` | PNG | ❌ |
| Sunburst | `advanced_sunburst_topic_sentiment.html` | HTML | ✅ |
| Sankey | `advanced_sankey_topic_sentiment.html` | HTML | ✅ |
| Treemap | `advanced_treemap_topic_sentiment.html` | HTML | ✅ |

---

## 🎨 Customization Cheat Sheet

### Ubah Warna
```python
colors = {'positif': '#2ecc71', 'netral': '#95a5a6', 'negatif': '#e74c3c'}
```

### Ubah Ukuran
```python
fig, ax = plt.subplots(figsize=(16, 10))  # width, height
```

### Ubah Resolusi
```python
plt.savefig('output.png', dpi=300)  # 300 untuk publikasi
```

### Ubah Font Size
```python
sns.set_context("paper", font_scale=1.5)
```

---

## 💡 Best Practices

### ✅ DO
- Gunakan warna konsisten (hijau=positif, merah=negatif)
- Resolusi minimal 300 dpi untuk publikasi
- Font minimal 10pt untuk readability
- White background untuk print
- Tambahkan title dan labels yang jelas

### ❌ DON'T
- Jangan gunakan terlalu banyak warna
- Jangan font terlalu kecil (<8pt)
- Jangan 3D chart (sulit dibaca)
- Jangan colormap 'jet' atau 'rainbow' (not colorblind-friendly)
- Jangan terlalu banyak informasi dalam 1 chart

---

## 🎓 Untuk Publikasi Akademik

### Skripsi/Thesis
```
Bab 4 (Hasil):
- Heatmap (distribusi utama)
- Violin Plot (analisis statistik)

Bab 5 (Pembahasan):
- Radar Chart (perbandingan)
- Network Graph (analisis semantic)

Lampiran:
- Infographic (executive summary)
```

### Paper/Jurnal
```
Figure 1: Heatmap (main result)
Figure 2: Violin Plot (statistical analysis)
Figure 3: Network Graph (optional, jika ada space)
```

### Presentasi
```
Slide 1: Infographic (overview)
Slide 2: Sunburst (interaktif, menarik)
Slide 3: Sankey (flow analysis)
Slide 4: Radar (perbandingan)
```

---

## 🔧 Troubleshooting Quick Fix

| Error | Solution |
|-------|----------|
| `No module named 'plotly'` | `pip install plotly kaleido` |
| `No module named 'networkx'` | `pip install networkx` |
| Font terlalu kecil | `sns.set_context("paper", font_scale=1.5)` |
| Warna tidak muncul | Pastikan data dalam format persentase |
| Image export gagal (plotly) | `pip install kaleido` |

---

## 📊 Comparison Matrix

| Visualisasi | Complexity | Visual Appeal | Info Density | Best For |
|-------------|-----------|---------------|--------------|----------|
| Heatmap | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Publikasi |
| Radar | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Presentasi |
| Violin | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Analisis Statistik |
| Network | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Semantic Analysis |
| Infographic | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Executive Summary |
| Sunburst | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Presentasi Interaktif |
| Sankey | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Flow Analysis |
| Treemap | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Proporsi |

---

## 🎯 Rekomendasi Cepat

**Untuk Skripsi:** Heatmap + Violin + Infographic

**Untuk Paper:** Heatmap + Violin

**Untuk Presentasi:** Sunburst + Sankey + Radar

**Untuk Poster:** Infographic

**Untuk Website:** Semua HTML (interaktif)

---

## 📞 Need Help?

Baca dokumentasi lengkap: `PANDUAN_VISUALISASI_ADVANCED.md`
