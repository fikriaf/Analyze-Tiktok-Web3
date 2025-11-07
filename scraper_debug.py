"""
TikTok Scraper - DEBUG MODE
Untuk debugging dan melihat struktur HTML yang sebenarnya

Usage:
    python scraper_debug.py
"""

import time
import re
from playwright.sync_api import sync_playwright

def debug_search_page(search_url):
    """
    Debug mode - lihat struktur HTML dan screenshot
    """
    
    print("="*70)
    print("TikTok Scraper - DEBUG MODE")
    print("="*70)
    print(f"URL: {search_url}")
    print("="*70)
    
    with sync_playwright() as p:
        print("\n[1] Opening browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        print("[2] Loading page...")
        page.goto(search_url, timeout=60000)
        time.sleep(5)
        
        print("[3] Scrolling...")
        for i in range(5):
            page.evaluate('window.scrollBy(0, window.innerHeight)')
            time.sleep(2)
        
        print("\n[4] Taking screenshot...")
        page.screenshot(path='debug_screenshot.png', full_page=True)
        print("    ✓ Screenshot saved: debug_screenshot.png")
        
        print("\n[5] Analyzing first video container...")
        
        # Try different selectors
        selectors = [
            'div[data-e2e="search_video-item"]',
            'div[class*="video-feed-item"]',
            'div[class*="DivItemContainer"]',
            'a[href*="/video/"]'
        ]
        
        container = None
        for selector in selectors:
            containers = page.query_selector_all(selector)
            if containers:
                print(f"    ✓ Found {len(containers)} items with selector: {selector}")
                container = containers[0]
                break
        
        if not container:
            print("    ✗ No container found!")
            browser.close()
            return
        
        print("\n[6] Extracting HTML from first container...")
        html = container.inner_html()
        
        # Save HTML to file
        with open('debug_container.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("    ✓ HTML saved: debug_container.html")
        
        print("\n[7] Looking for numbers in container...")
        
        # Find all strong tags
        strong_elems = container.query_selector_all('strong')
        print(f"    Found {len(strong_elems)} <strong> tags:")
        
        for idx, elem in enumerate(strong_elems):
            text = elem.inner_text().strip()
            data_e2e = elem.get_attribute('data-e2e')
            class_name = elem.get_attribute('class')
            
            print(f"\n    Strong #{idx+1}:")
            print(f"      Text: {text}")
            print(f"      data-e2e: {data_e2e}")
            print(f"      class: {class_name}")
            
            # Get parent context
            try:
                parent_html = elem.evaluate('el => el.parentElement.outerHTML')
                # Show first 200 chars
                print(f"      Parent: {parent_html[:200]}...")
            except:
                pass
        
        print("\n[8] Looking for all numbers in HTML...")
        numbers = re.findall(r'>(\d+\.?\d*[KMB]?)<', html)
        print(f"    Found numbers: {numbers[:20]}")  # Show first 20
        
        print("\n[9] Looking for data-e2e attributes...")
        data_e2e_attrs = re.findall(r'data-e2e="([^"]+)"', html)
        unique_attrs = list(set(data_e2e_attrs))
        print(f"    Found {len(unique_attrs)} unique data-e2e attributes:")
        for attr in sorted(unique_attrs):
            print(f"      - {attr}")
        
        print("\n[10] Looking for like/heart related elements...")
        # Search for heart icon or like text
        if 'heart' in html.lower():
            print("    ✓ Found 'heart' in HTML")
        if 'like' in html.lower():
            print("    ✓ Found 'like' in HTML")
        if 'digg' in html.lower():
            print("    ✓ Found 'digg' in HTML (TikTok's internal name for likes)")
        
        # Look for SVG heart icon
        svg_elems = container.query_selector_all('svg')
        print(f"\n    Found {len(svg_elems)} SVG elements")
        for idx, svg in enumerate(svg_elems[:3]):  # Check first 3
            svg_html = svg.evaluate('el => el.outerHTML')
            if 'heart' in svg_html.lower() or 'like' in svg_html.lower():
                print(f"      SVG #{idx+1} might be like icon")
                # Get next sibling (might be the count)
                try:
                    next_elem = svg.evaluate('el => el.nextElementSibling')
                    if next_elem:
                        next_text = next_elem.inner_text()
                        print(f"        Next element text: {next_text}")
                except:
                    pass
        
        print("\n" + "="*70)
        print("DEBUG COMPLETE")
        print("="*70)
        print("\nCheck these files:")
        print("  - debug_screenshot.png (visual)")
        print("  - debug_container.html (HTML structure)")
        print("\nAnalyze the output above to find the correct selector for likes")
        print("="*70)
        
        input("\nPress Enter to close browser...")
        browser.close()


def main():
    """Main function"""
    
    default_url = "https://www.tiktok.com/search/video?q=web3%20blockchain%20crypto%20Indonesia"
    
    print("\n" + "="*70)
    print("TikTok Scraper - DEBUG MODE")
    print("="*70)
    print(f"\nDefault: {default_url}")
    
    user_url = input("\nEnter search URL (or press Enter for default): ").strip()
    search_url = user_url if user_url else default_url
    
    debug_search_page(search_url)


if __name__ == "__main__":
    main()
