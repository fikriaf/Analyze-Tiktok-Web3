#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Advanced Visualizations untuk Sentiment Analysis TikTok
Visualisasi professional dan menarik untuk publikasi akademik

Jenis visualisasi:
1. Heatmap - Sentimen per Topik
2. Sunburst Chart - Hierarki Topik & Sentimen
3. Radar Chart - Profil Sentimen Multi-dimensi
4. Sankey Diagram - Flow Sentimen
5. Treemap - Proporsi Topik
6. Violin Plot - Distribusi Skor Sentimen
7. Network Graph - Co-occurrence Words
8. Timeline Animation - Tren Temporal
9. Dashboard Interaktif - Plotly
10. Infographic Style - Publication Ready
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style untuk publikasi
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.2)
sns.set_palette("husl")


# ============================================================================
# 1. HEATMAP - Sentimen per Topik (Professional)
# ============================================================================

def create_sentiment_heatmap(df_clean):
    """
    Heatmap yang menunjukkan intensitas sentimen per topik
    """
    print('\n--- Creating Sentiment Heatmap ---')
    
    # Create crosstab
    sentiment_topic = pd.crosstab(
        df_clean['topic_category'], 
        df_clean['sentiment_label'], 
        normalize='index'
    ) * 100
    
    # Reorder columns
    col_order = ['positif', 'netral', 'negatif']
    sentiment_topic = sentiment_topic[[c for c in col_order if c in sentiment_topic.columns]]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create heatmap with custom colormap
    sns.heatmap(
        sentiment_topic, 
        annot=True, 
        fmt='.1f',
        cmap='RdYlGn',
        center=33.33,  # Center at neutral
        cbar_kws={'label': 'Persentase (%)'},
        linewidths=0.5,
        linecolor='white',
        ax=ax
    )
    
    ax.set_title('Heatmap Distribusi Sentimen per Topik Web3', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Sentimen', fontsize=13, fontweight='bold')
    ax.set_ylabel('Topik', fontsize=13, fontweight='bold')
    
    # Rotate labels
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    
    plt.tight_layout()
    plt.savefig('output/graphs/advanced_heatmap_sentiment_topic.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print('✓ Heatmap saved: output/graphs/advanced_heatmap_sentiment_topic.png')


# ============================================================================
# 2. SUNBURST CHART - Hierarki Topik & Sentimen
# ============================================================================

def create_sunburst_chart(df_clean):
    """
    Sunburst chart untuk menunjukkan hierarki topik dan sentimen
    Requires: plotly
    """
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        
        print('\n--- Creating Sunburst Chart ---')
        
        # Prepare data
        topic_sentiment = df_clean.groupby(['topic_category', 'sentiment_label']).size().reset_index(name='count')
        
        # Create sunburst
        fig = px.sunburst(
            topic_sentiment,
            path=['topic_category', 'sentiment_label'],
            values='count',
            color='sentiment_label',
            color_discrete_map={
                'positif': '#2ecc71',
                'netral': '#95a5a6',
                'negatif': '#e74c3c'
            },
            title='Hierarki Topik dan Sentimen Web3 di TikTok Indonesia'
        )
        
        fig.update_layout(
            font=dict(size=14),
            title_font_size=18,
            width=900,
            height=900
        )
        
        fig.write_html('output/graphs/advanced_sunburst_topic_sentiment.html')
        fig.write_image('output/graphs/advanced_sunburst_topic_sentiment.png', 
                       width=900, height=900, scale=2)
        
        print('✓ Sunburst saved: output/graphs/advanced_sunburst_topic_sentiment.html')
        print('✓ Sunburst saved: output/graphs/advanced_sunburst_topic_sentiment.png')
        
    except ImportError:
        print('⚠ Plotly not installed. Run: pip install plotly kaleido')
    except Exception as e:
        print(f'⚠ Error creating sunburst: {e}')


# ============================================================================
# 3. RADAR CHART - Profil Sentimen Multi-dimensi
# ============================================================================

def create_radar_chart(df_clean):
    """
    Radar chart untuk membandingkan profil sentimen antar topik
    """
    print('\n--- Creating Radar Chart ---')
    
    # Calculate sentiment percentages per topic
    topics = df_clean['topic_category'].unique()[:6]  # Top 6 topics
    
    categories = ['Positif', 'Netral', 'Negatif']
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(topics)))
    
    for idx, topic in enumerate(topics):
        topic_data = df_clean[df_clean['topic_category'] == topic]
        
        values = []
        for sentiment in ['positif', 'netral', 'negatif']:
            pct = (topic_data['sentiment_label'] == sentiment).sum() / len(topic_data) * 100
            values.append(pct)
        
        values += values[:1]  # Complete the circle
        
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


# ============================================================================
# 4. SANKEY DIAGRAM - Flow Sentimen
# ============================================================================

def create_sankey_diagram(df_clean):
    """
    Sankey diagram untuk menunjukkan flow dari topik ke sentimen
    """
    try:
        import plotly.graph_objects as go
        
        print('\n--- Creating Sankey Diagram ---')
        
        # Prepare data
        topic_sentiment = df_clean.groupby(['topic_category', 'sentiment_label']).size().reset_index(name='value')
        
        # Create node labels
        topics = df_clean['topic_category'].unique().tolist()
        sentiments = ['Positif', 'Netral', 'Negatif']
        all_nodes = topics + sentiments
        
        # Create links
        source = []
        target = []
        value = []
        
        for _, row in topic_sentiment.iterrows():
            source.append(all_nodes.index(row['topic_category']))
            target.append(all_nodes.index(row['sentiment_label'].capitalize()))
            value.append(row['value'])
        
        # Create Sankey
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color='black', width=0.5),
                label=all_nodes,
                color=['#3498db'] * len(topics) + ['#2ecc71', '#95a5a6', '#e74c3c']
            ),
            link=dict(
                source=source,
                target=target,
                value=value,
                color='rgba(0,0,0,0.2)'
            )
        )])
        
        fig.update_layout(
            title_text='Flow Topik ke Sentimen (Sankey Diagram)',
            font_size=14,
            width=1200,
            height=800
        )
        
        fig.write_html('output/graphs/advanced_sankey_topic_sentiment.html')
        
        print('✓ Sankey saved: output/graphs/advanced_sankey_topic_sentiment.html')
        
    except ImportError:
        print('⚠ Plotly not installed. Run: pip install plotly')
    except Exception as e:
        print(f'⚠ Error creating sankey: {e}')


# ============================================================================
# 5. TREEMAP - Proporsi Topik
# ============================================================================

def create_treemap(df_clean):
    """
    Treemap untuk menunjukkan proporsi topik dan sentimen
    """
    try:
        import plotly.express as px
        
        print('\n--- Creating Treemap ---')
        
        # Prepare data
        topic_sentiment = df_clean.groupby(['topic_category', 'sentiment_label']).size().reset_index(name='count')
        
        fig = px.treemap(
            topic_sentiment,
            path=['topic_category', 'sentiment_label'],
            values='count',
            color='sentiment_label',
            color_discrete_map={
                'positif': '#2ecc71',
                'netral': '#95a5a6',
                'negatif': '#e74c3c'
            },
            title='Treemap Proporsi Topik dan Sentimen Web3'
        )
        
        fig.update_layout(
            font=dict(size=14),
            title_font_size=18,
            width=1200,
            height=800
        )
        
        fig.write_html('output/graphs/advanced_treemap_topic_sentiment.html')
        
        print('✓ Treemap saved: output/graphs/advanced_treemap_topic_sentiment.html')
        
    except ImportError:
        print('⚠ Plotly not installed. Run: pip install plotly')
    except Exception as e:
        print(f'⚠ Error creating treemap: {e}')


# ============================================================================
# 6. VIOLIN PLOT - Distribusi Skor Sentimen
# ============================================================================

def create_violin_plot(df_clean):
    """
    Violin plot untuk menunjukkan distribusi skor sentimen per topik
    """
    print('\n--- Creating Violin Plot ---')
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Create violin plot
    parts = ax.violinplot(
        [df_clean[df_clean['topic_category'] == topic]['sentiment_score'].values 
         for topic in df_clean['topic_category'].unique()],
        positions=range(len(df_clean['topic_category'].unique())),
        showmeans=True,
        showmedians=True,
        widths=0.7
    )
    
    # Customize colors
    colors = plt.cm.Set3(np.linspace(0, 1, len(df_clean['topic_category'].unique())))
    for idx, pc in enumerate(parts['bodies']):
        pc.set_facecolor(colors[idx])
        pc.set_alpha(0.7)
    
    # Add horizontal line at y=0
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


# ============================================================================
# 7. NETWORK GRAPH - Co-occurrence Words
# ============================================================================

def create_network_graph(df_clean, top_n=20):
    """
    Network graph untuk menunjukkan co-occurrence kata-kata penting
    """
    try:
        import networkx as nx
        from itertools import combinations
        
        print('\n--- Creating Network Graph ---')
        
        # Get top words
        all_words = ' '.join(df_clean['processed_text']).split()
        word_freq = Counter(all_words)
        top_words = [word for word, _ in word_freq.most_common(top_n)]
        
        # Calculate co-occurrence
        cooccurrence = Counter()
        for text in df_clean['processed_text']:
            words = [w for w in text.split() if w in top_words]
            for pair in combinations(set(words), 2):
                cooccurrence[tuple(sorted(pair))] += 1
        
        # Create graph
        G = nx.Graph()
        
        # Add nodes
        for word in top_words:
            G.add_node(word, size=word_freq[word])
        
        # Add edges (only strong connections)
        threshold = np.percentile(list(cooccurrence.values()), 75)
        for (word1, word2), weight in cooccurrence.items():
            if weight >= threshold:
                G.add_edge(word1, word2, weight=weight)
        
        # Draw
        fig, ax = plt.subplots(figsize=(16, 16))
        
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Node sizes based on frequency
        node_sizes = [G.nodes[node]['size'] * 10 for node in G.nodes()]
        
        # Draw network
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                              node_color='lightblue', alpha=0.7, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.5, ax=ax)
        
        ax.set_title('Network Graph: Co-occurrence Kata Kunci Web3', 
                    fontsize=18, fontweight='bold', pad=20)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig('output/graphs/advanced_network_cooccurrence.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        
        print('✓ Network graph saved: output/graphs/advanced_network_cooccurrence.png')
        
    except ImportError:
        print('⚠ NetworkX not installed. Run: pip install networkx')
    except Exception as e:
        print(f'⚠ Error creating network graph: {e}')


# ============================================================================
# 8. INFOGRAPHIC STYLE - Publication Ready
# ============================================================================

def create_infographic_summary(df_clean):
    """
    Infographic style summary untuk publikasi
    """
    print('\n--- Creating Infographic Summary ---')
    
    fig = plt.figure(figsize=(16, 20))
    gs = fig.add_gridspec(5, 2, hspace=0.4, wspace=0.3)
    
    # Color scheme
    colors = {'positif': '#2ecc71', 'netral': '#95a5a6', 'negatif': '#e74c3c'}
    
    # 1. Title
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.text(0.5, 0.5, 'ANALISIS SENTIMEN WEB3 DI TIKTOK INDONESIA', 
                 ha='center', va='center', fontsize=28, fontweight='bold')
    ax_title.text(0.5, 0.2, f'Total Data: {len(df_clean):,} Comment | {df_clean["video_id"].nunique()} Video', 
                 ha='center', va='center', fontsize=16, color='gray')
    ax_title.axis('off')
    
    # 2. Sentiment Distribution (Pie)
    ax1 = fig.add_subplot(gs[1, 0])
    sentiment_counts = df_clean['sentiment_label'].value_counts()
    ax1.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
           colors=[colors[l] for l in sentiment_counts.index], startangle=90,
           textprops={'fontsize': 12, 'fontweight': 'bold'})
    ax1.set_title('Distribusi Sentimen', fontsize=14, fontweight='bold', pad=10)
    
    # 3. Top Topics (Horizontal Bar)
    ax2 = fig.add_subplot(gs[1, 1])
    top_topics = df_clean['topic_category'].value_counts().head(5)
    ax2.barh(range(len(top_topics)), top_topics.values, color='steelblue')
    ax2.set_yticks(range(len(top_topics)))
    ax2.set_yticklabels(top_topics.index, fontsize=10)
    ax2.set_xlabel('Jumlah', fontsize=11)
    ax2.set_title('Top 5 Topik Terpopuler', fontsize=14, fontweight='bold', pad=10)
    ax2.invert_yaxis()
    
    # 4. Sentiment by Topic (Stacked Bar)
    ax3 = fig.add_subplot(gs[2, :])
    sentiment_topic = pd.crosstab(df_clean['topic_category'], df_clean['sentiment_label'], normalize='index') * 100
    sentiment_topic = sentiment_topic[[c for c in ['positif', 'netral', 'negatif'] if c in sentiment_topic.columns]]
    sentiment_topic.plot(kind='barh', stacked=True, ax=ax3, 
                        color=[colors[c] for c in sentiment_topic.columns],
                        legend=True)
    ax3.set_xlabel('Persentase (%)', fontsize=11)
    ax3.set_title('Sentimen per Topik', fontsize=14, fontweight='bold', pad=10)
    ax3.legend(title='Sentimen', loc='lower right')
    
    # 5. Top Keywords
    ax4 = fig.add_subplot(gs[3, :])
    all_words = ' '.join(df_clean['processed_text']).split()
    word_freq = Counter(all_words)
    top_20 = pd.DataFrame(word_freq.most_common(20), columns=['word', 'freq'])
    ax4.barh(range(len(top_20)), top_20['freq'], color='coral')
    ax4.set_yticks(range(len(top_20)))
    ax4.set_yticklabels(top_20['word'], fontsize=9)
    ax4.set_xlabel('Frekuensi', fontsize=11)
    ax4.set_title('Top 20 Kata Paling Sering Muncul', fontsize=14, fontweight='bold', pad=10)
    ax4.invert_yaxis()
    
    # 6. Key Insights
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
    
    plt.suptitle('', fontsize=1)  # Remove default title
    plt.savefig('output/graphs/advanced_infographic_summary.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print('✓ Infographic saved: output/graphs/advanced_infographic_summary.png')


# ============================================================================
# DATA PREPARATION
# ============================================================================

def prepare_data(df_clean):
    """
    Prepare data: tambahkan topic_category jika belum ada
    """
    print('\n--- Preparing Data ---')
    
    # Check required columns
    required_cols = ['processed_text', 'sentiment_label', 'sentiment_score']
    missing_cols = [col for col in required_cols if col not in df_clean.columns]
    
    if missing_cols:
        print(f'❌ Error: Missing required columns: {missing_cols}')
        print('   Please run tiktok_sentiment_analysis.py first!')
        return None
    
    # Add topic_category if not exists
    if 'topic_category' not in df_clean.columns:
        print('⚠ Column "topic_category" not found. Creating from hashtags...')
        
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
        
        if 'hashtags' in df_clean.columns:
            df_clean['topic_category'] = df_clean['hashtags'].apply(categorize_topic)
        else:
            # If no hashtags column, categorize based on processed_text
            print('⚠ Column "hashtags" not found. Categorizing based on text content...')
            
            def categorize_from_text(text):
                if pd.isna(text):
                    return 'Web3 General'
                text_lower = str(text).lower()
                if any(word in text_lower for word in ['ai', 'artificial', 'intelligence', 'kecerdasan']):
                    return 'AI Ethics'
                elif any(word in text_lower for word in ['blockchain', 'crypto', 'bitcoin', 'ethereum']):
                    return 'Blockchain & Crypto'
                elif any(word in text_lower for word in ['nft', 'metaverse', 'virtual']):
                    return 'NFT & Metaverse'
                elif any(word in text_lower for word in ['privacy', 'privasi', 'security', 'keamanan']):
                    return 'Privacy & Security'
                else:
                    return 'Web3 General'
            
            df_clean['topic_category'] = df_clean['processed_text'].apply(categorize_from_text)
        
        print(f'✓ Topic categories created')
        print(f'  Distribution: {df_clean["topic_category"].value_counts().to_dict()}')
    
    print('✓ Data preparation complete')
    return df_clean


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def create_all_advanced_visualizations(df_clean):
    """
    Generate semua visualisasi advanced
    """
    print('\n' + '='*80)
    print('GENERATING ADVANCED VISUALIZATIONS')
    print('='*80)
    
    # Prepare data first
    df_clean = prepare_data(df_clean)
    if df_clean is None:
        return
    
    # 1. Heatmap
    create_sentiment_heatmap(df_clean)
    
    # 2. Sunburst (requires plotly)
    create_sunburst_chart(df_clean)
    
    # 3. Radar Chart
    create_radar_chart(df_clean)
    
    # 4. Sankey (requires plotly)
    create_sankey_diagram(df_clean)
    
    # 5. Treemap (requires plotly)
    create_treemap(df_clean)
    
    # 6. Violin Plot
    create_violin_plot(df_clean)
    
    # 7. Network Graph (requires networkx)
    create_network_graph(df_clean)
    
    # 8. Infographic
    create_infographic_summary(df_clean)
    
    print('\n' + '='*80)
    print('✅ ALL ADVANCED VISUALIZATIONS COMPLETED!')
    print('='*80)
    print('\nFiles saved in: output/graphs/')
    print('- advanced_heatmap_sentiment_topic.png')
    print('- advanced_sunburst_topic_sentiment.html')
    print('- advanced_radar_sentiment_profile.png')
    print('- advanced_sankey_topic_sentiment.html')
    print('- advanced_treemap_topic_sentiment.html')
    print('- advanced_violin_sentiment_distribution.png')
    print('- advanced_network_cooccurrence.png')
    print('- advanced_infographic_summary.png')


if __name__ == "__main__":
    print("Advanced Visualizations Script")
    print("="*80)
    print("\nUsage:")
    print("1. Load your data: df = pd.read_csv('output/data/sentiment_results.csv')")
    print("2. Run: create_all_advanced_visualizations(df)")
    print("\nOr run individual functions:")
    print("- create_sentiment_heatmap(df)")
    print("- create_radar_chart(df)")
    print("- create_infographic_summary(df)")
    print("="*80)
    
    # Auto-run if data exists
    import os
    if os.path.exists('output/data/sentiment_results.csv'):
        print("\n✓ Found sentiment_results.csv, generating visualizations...")
        df = pd.read_csv('output/data/sentiment_results.csv', encoding='utf-8')
        create_all_advanced_visualizations(df)
    elif os.path.exists('output/data/final_data_with_topics.csv'):
        print("\n✓ Found final_data_with_topics.csv, generating visualizations...")
        df = pd.read_csv('output/data/final_data_with_topics.csv', encoding='utf-8')
        create_all_advanced_visualizations(df)
    else:
        print("\n⚠ No data file found. Please run tiktok_sentiment_analysis.py first!")
        print("   Expected files:")
        print("   - output/data/sentiment_results.csv")
        print("   - output/data/final_data_with_topics.csv")
    df = pd.read_csv('output/data/sentiment_results.csv')
    create_all_advanced_visualizations(df)