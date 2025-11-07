"""
TikTok Search Scraper - FINAL VERSION
Scrape video links dari halaman pencarian berdasarkan likes

Usage:
    python scraper_final.py
"""

import time
import re
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright

def parse_number(text):
    """Parse number from text like '832', '1.2K', '3.5M'"""
    if not text:
        return 0
    
    text = str(text).strip().upper().replace(',', '').replace(' ', '')
    
    try:
        if 'K' in text:
            num = text.replace('K', '')
            return int(float(num) * 1000)
        elif 'M' in text:
            num = text.replace('M', '')
            return int(float(num) * 1000000)
        elif 'B' in text:
            num = text.replace('B', '')
            return int(float(num) * 1000000000)
        else:
            # Plain number
            num = re.sub(r'[^\d]', '', text)
            return int(num) if num else 0
    except Exception as e:
        print(f"      ⚠ Parse error for '{text}': {e}")
        return 0


def scrape_tiktok_search(search_url, min_likes=1000, scroll_times=15):
    """
    Scrape video links dari TikTok search page
    HANYA ambil link video, TIDAK ambil komentar
    Filter berdasarkan title/caption yang mengandung kata Web3
    """
    
    # Daftar kata kunci Web3 (case insensitive)
    web3_keywords = [
        'web3', 'web 3', 'blockchain', 'crypto', 'cryptocurrency', 'kripto',
        'bitcoin', 'ethereum', 'nft', 'metaverse', 'defi', 'dapp',
        'smart contract', 'token', 'coin', 'mining', 'wallet',
        'decentralized', 'desentralisasi', 'terdesentralisasi',
        'binance', 'coinbase', 'opensea', 'metamask',
        'altcoin', 'stablecoin', 'dao', 'dex', 'cefi',
        'hodl', 'bull', 'bear', 'pump', 'dump',
        'airdrop', 'whitelist', 'mint', 'gas fee',
        'layer 2', 'polygon', 'solana', 'cardano',
        'trading', 'investasi crypto', 'investasi kripto'
    ]
    
    print("="*70)
    print("TikTok Search Scraper - FINAL")
    print("="*70)
    print(f"URL: {search_url}")
    print(f"Min likes: {min_likes}")
    print(f"Scroll times: {scroll_times}")
    print("="*70)
    
    links_data = []
    seen_links = set()
    
    with sync_playwright() as p:
        print("\n[1] Opening browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        print("[2] Loading page...")
        page.goto(search_url, timeout=60000)
        time.sleep(5)
        
        print("[3] Ready to auto scroll")
        print("    Browser is open. Press ENTER to start auto scrolling...")
        input("    > ")
        
        print("    Auto scrolling...")
        for i in range(scroll_times):
            page.evaluate('window.scrollBy(0, window.innerHeight)')
            time.sleep(2)
            print(f"    Scroll {i+1}/{scroll_times}", end='\r')
        
        print(f"\n\n[4] Extracting video data...")
        
        # Get all video containers
        containers = page.query_selector_all('div[data-e2e="search_video-item"]')
        
        if not containers:
            print("    Trying alternative selector...")
            containers = page.query_selector_all('a[href*="/video/"]')
        
        # Get all titles from page
        all_titles = page.query_selector_all('span[data-e2e="new-desc-span"]')
        titles_text = [t.inner_text().strip() for t in all_titles]
        
        print(f"    Found {len(containers)} video containers")
        print(f"    Found {len(titles_text)} titles\n")
        
        for idx, container in enumerate(containers):
            try:
                print(f"[{idx+1}/{len(containers)}] Processing video...")
                
                # Get link
                link = None
                if container.get_attribute('href'):
                    link = container.get_attribute('href')
                else:
                    link_elem = container.query_selector('a[href*="/video/"]')
                    if link_elem:
                        link = link_elem.get_attribute('href')
                
                if not link:
                    print("  ✗ No link found\n")
                    continue
                
                # Make full URL
                if not link.startswith('http'):
                    link = 'https://www.tiktok.com' + link
                
                # Skip duplicates
                if link in seen_links:
                    print(f"  ⊘ Duplicate\n")
                    continue
                
                seen_links.add(link)
                print(f"  Link: {link[:65]}...")
                
                # Get title from pre-fetched titles list
                title = ''
                if idx < len(titles_text):
                    title = titles_text[idx]
                    print(f"  Title: {title[:60]}...")
                else:
                    print(f"  Title: (not found - index out of range)")
                
                # WAJIB: Check if title contains Web3 keywords
                if not title:
                    print(f"  ✗ SKIPPED (no title found)\n")
                    continue
                
                title_lower = title.lower()
                has_keyword = any(keyword.lower() in title_lower for keyword in web3_keywords)
                
                if not has_keyword:
                    print(f"  ✗ SKIPPED (no Web3 keywords in title)\n")
                    continue
                
                print(f"  ✓ Contains Web3 keywords")
                
                # Get likes - data-e2e="video-views" is actually LIKES in search page
                likes = 0
                like_elem = container.query_selector('strong[data-e2e="video-views"]')
                
                if like_elem:
                    like_text = like_elem.inner_text().strip()
                    likes = parse_number(like_text)
                    print(f"  Likes: {likes} (raw: '{like_text}')")
                else:
                    print(f"  ⚠ No likes element found")
                
                # Check if meets criteria
                if likes >= min_likes:
                    links_data.append({
                        'link': link,
                        'likes': likes,
                        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    print(f"  ✓ ADDED (likes: {likes} >= {min_likes})\n")
                else:
                    print(f"  ✗ SKIPPED (likes: {likes} < {min_likes})\n")
                
            except Exception as e:
                print(f"  ✗ Error: {e}\n")
                continue
        
        browser.close()
    
    print("="*70)
    print("SCRAPING COMPLETED")
    print("="*70)
    print(f"Total videos checked: {len(containers)}")
    print(f"Videos with >={min_likes} likes: {len(links_data)}")
    print("="*70)
    
    if links_data:
        df = pd.DataFrame(links_data)
        return df
    else:
        return None


def save_results(df):
    """Save results to CSV and TXT"""
    
    if df is None or len(df) == 0:
        print("\n✗ No data to save")
        return False
    
    # Sort by likes
    df = df.sort_values('likes', ascending=False)
    
    # Save CSV
    df.to_csv('tiktok_links.csv', index=False)
    print(f"\n✓ Saved to: tiktok_links.csv")
    
    # Save TXT
    with open('tiktok_links.txt', 'w', encoding='utf-8') as f:
        for link in df['link']:
            f.write(link + '\n')
    print(f"✓ Saved to: tiktok_links.txt")
    
    # Statistics
    print(f"\n{'='*70}")
    print("STATISTICS")
    print(f"{'='*70}")
    print(f"Total videos: {len(df)}")
    print(f"Average likes: {df['likes'].mean():.0f}")
    print(f"Max likes: {df['likes'].max()}")
    print(f"Min likes: {df['likes'].min()}")
    
    print(f"\n{'='*70}")
    print("TOP 10 VIDEOS BY LIKES")
    print(f"{'='*70}")
    for idx, row in df.head(10).iterrows():
        print(f"{row['likes']:>8,} likes - {row['link']}")
    print(f"{'='*70}")
    
    return True


def main():
    """Main function"""
    
    print("\n" + "="*70)
    print("TikTok Search Scraper - AUTO RUN")
    print("="*70)
    
    # List of search URLs
    search_urls = [
        "https://www.tiktok.com/search/video?q=web3%20blockchain%20crypto%20Indonesia",
        "https://www.tiktok.com/search/video?q=cryptocurrency%20Indonesia",
        "https://www.tiktok.com/search/video?q=NFT%20Indonesia",
        "https://www.tiktok.com/search/video?q=blockchain%20Indonesia",
        "https://www.tiktok.com/search/video?q=kripto%20Indonesia"
    ]
    
    # Configuration
    min_likes = 1000
    scroll_times = 15
    
    print(f"\nSearch URLs:")
    for idx, url in enumerate(search_urls, 1):
        print(f"  {idx}. {url}")
    
    print(f"\nConfiguration:")
    print(f"  Min likes: {min_likes}")
    print(f"  Manual scroll: YES")
    print("="*70)
    
    all_results = []
    
    for idx, search_url in enumerate(search_urls, 1):
        print(f"\n\n{'='*70}")
        print(f"PROCESSING URL {idx}/{len(search_urls)}")
        print(f"{'='*70}")
        
        # Start scraping
        df = scrape_tiktok_search(search_url, min_likes, scroll_times)
        
        if df is not None and len(df) > 0:
            all_results.append(df)
            print(f"\n✓ Got {len(df)} videos from URL {idx}")
        else:
            print(f"\n✗ No data from URL {idx}")
        
        # Wait between URLs
        if idx < len(search_urls):
            print("\nWaiting 3 seconds before next URL...")
            time.sleep(3)
    
    # Combine all results
    if all_results:
        df_combined = pd.concat(all_results, ignore_index=True)
        df_combined = df_combined.drop_duplicates(subset=['link'], keep='first')
        df_combined = df_combined.sort_values('likes', ascending=False)
        
        print(f"\n\n{'='*70}")
        print("ALL URLS COMPLETED")
        print(f"{'='*70}")
        print(f"Total unique videos: {len(df_combined)}")
        
        return df_combined
    else:
        return None



if __name__ == "__main__":
    df = main()
    
    if df is not None:
        save_results(df)
        print("\n✓ SUCCESS!")
    else:
        print("\n✗ FAILED")
    
    input("\nPress Enter to exit...")
    exit(0 if df is not None else 1)
