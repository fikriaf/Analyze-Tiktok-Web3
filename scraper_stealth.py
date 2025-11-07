"""
TikTok Scraper with Stealth Mode & Cookie Support
Anti-detection scraper dengan login persistent

Usage:
    python scraper_stealth.py
"""

import pandas as pd
from datetime import datetime
import time
import re
import json
import os
from playwright.sync_api import sync_playwright

def create_stealth_context(browser):
    """Create browser context with stealth settings"""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale='id-ID',
        timezone_id='Asia/Jakarta'
    )
    
    # Anti-detection scripts
    context.add_init_script("""
        // Hide webdriver
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        
        // Fake plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        
        // Fake languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['id-ID', 'id', 'en-US', 'en']
        });
        
        // Fake chrome
        window.chrome = { runtime: {} };
        
        // Bypass debugger detection
        const noop = () => {};
        window.console.debug = noop;
        
        // Override debugger
        const originalDebugger = window.Function.prototype.constructor;
        window.Function.prototype.constructor = function(...args) {
            if (args.length > 0 && typeof args[args.length - 1] === 'string') {
                const code = args[args.length - 1];
                if (code.includes('debugger')) {
                    return noop;
                }
            }
            return originalDebugger.apply(this, args);
        };
        
        // Block debugger statements
        setInterval = new Proxy(setInterval, {
            apply(target, thisArg, args) {
                if (args[0] && args[0].toString().includes('debugger')) {
                    return noop;
                }
                return Reflect.apply(target, thisArg, args);
            }
        });
    """)
    
    return context


def scrape_with_stealth(input_file, comments_per_video=50):
    """
    Scrape TikTok dengan stealth mode dan cookie support
    """
    
    cookie_file = 'tiktok_cookies.json'
    
    # Read links
    print(f'Reading links from {input_file}...')
    if input_file.endswith('.csv'):
        links_df = pd.read_csv(input_file)
        links = links_df['link'].tolist()
    else:
        with open(input_file, 'r', encoding='utf-8') as f:
            links = [line.strip() for line in f if line.strip()]
    
    print(f'Found {len(links)} links\n')
    
    all_data = []
    
    with sync_playwright() as p:
        # Launch browser
        print('Launching browser...')
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials'
            ],
            devtools=False  # Disable devtools to avoid debugger
        )
        
        # Load or create context with cookies
        if os.path.exists(cookie_file):
            print(f'✓ Found cookies: {cookie_file}')
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            
            context = create_stealth_context(browser)
            context.add_cookies(cookies)
            page = context.new_page()
            
            # Test cookies
            page.goto('https://www.tiktok.com', timeout=60000)
            time.sleep(3)
            
            if page.query_selector('[data-e2e="profile-icon"]'):
                print('✓ Logged in with cookies!\n')
            else:
                print('✗ Cookies expired\n')
                os.remove(cookie_file)
                context.close()
                
                # Re-login
                context = create_stealth_context(browser)
                page = context.new_page()
                page.goto('https://www.tiktok.com', timeout=60000)
                
                print('='*60)
                print('LOGIN REQUIRED')
                print('='*60)
                input('Press ENTER after login... ')
                
                cookies = context.cookies()
                with open(cookie_file, 'w') as f:
                    json.dump(cookies, f)
                print(f'✓ Cookies saved!\n')
        else:
            print('No cookies found\n')
            context = create_stealth_context(browser)
            page = context.new_page()
            page.goto('https://www.tiktok.com', timeout=60000)
            
            print('='*60)
            print('LOGIN REQUIRED')
            print('='*60)
            input('Press ENTER after login... ')
            
            cookies = context.cookies()
            with open(cookie_file, 'w') as f:
                json.dump(cookies, f)
            print(f'✓ Cookies saved!\n')
        
        # Start scraping
        print('Starting scraping...\n')
        
        for idx, link in enumerate(links):
            print(f'[{idx+1}/{len(links)}] {link[:60]}...')
            
            try:
                # Human-like delay
                time.sleep(3 + (idx % 4))
                
                # Navigate
                page.goto(link, wait_until='domcontentloaded', timeout=60000)
                time.sleep(6)
                
                # Check for error
                if 'trouble' in page.content().lower():
                    print('  ⚠ Error page detected, waiting...')
                    time.sleep(15)
                    page.reload()
                    time.sleep(6)
                
                # Extract data
                video_id = re.search(r'/video/(\d+)', link).group(1) if re.search(r'/video/(\d+)', link) else ''
                username = re.search(r'@([^/]+)', link).group(1) if re.search(r'@([^/]+)', link) else ''
                
                # Caption
                caption = ''
                try:
                    caption_elem = page.query_selector('[data-e2e="browse-video-desc"]')
                    caption = caption_elem.inner_text() if caption_elem else ''
                    print(f'  Caption: {caption[:40]}...')
                except:
                    print(f'  Caption: (not found)')
                
                # Likes
                likes = 0
                try:
                    like_elem = page.query_selector('[data-e2e="like-count"]')
                    if like_elem:
                        likes_text = like_elem.inner_text()
                        likes = parse_count(likes_text)
                    print(f'  Likes: {likes}')
                except:
                    print(f'  Likes: 0')
                
                # Hashtags
                hashtags = ''
                try:
                    hashtag_elems = page.query_selector_all('a[href*="/tag/"]')
                    hashtags = ' '.join([elem.inner_text() for elem in hashtag_elems])
                    print(f'  Hashtags: {hashtags[:40]}...')
                except:
                    print(f'  Hashtags: (none)')
                
                video_data = {
                    'video_id': video_id,
                    'username': username,
                    'caption': caption,
                    'likes': likes,
                    'hashtags': hashtags,
                    'date': datetime.now()
                }
                
                # Comments
                try:
                    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    time.sleep(4)
                    
                    # Get all comments
                    comment_elems_l1 = page.query_selector_all('[data-e2e="comment-level-1"]')
                    comment_elems_l2 = page.query_selector_all('[data-e2e="comment-level-2"]')
                    all_comments = list(comment_elems_l1) + list(comment_elems_l2)
                    
                    comment_count = 0
                    for comment_elem in all_comments[:comments_per_video]:
                        try:
                            comment_text = comment_elem.inner_text().strip()
                            if comment_text:
                                comment_row = video_data.copy()
                                comment_row['comment'] = comment_text
                                all_data.append(comment_row)
                                comment_count += 1
                        except:
                            continue
                    
                    print(f'  Comments: {comment_count}')
                    
                    if comment_count == 0:
                        video_data['comment'] = ''
                        all_data.append(video_data)
                except Exception as e:
                    print(f'  Comments: Error - {e}')
                    video_data['comment'] = ''
                    all_data.append(video_data)
                
                print(f'  ✓ Success\n')
                
                # Human-like wait
                wait_time = 6 + (idx % 5)
                time.sleep(wait_time)
                
            except Exception as e:
                print(f'  ✗ Failed: {e}\n')
                time.sleep(5)
                continue
        
        browser.close()
    
    df = pd.DataFrame(all_data)
    return df


def parse_count(text):
    """Parse count like 1.2K"""
    text = text.strip().upper().replace(',', '')
    try:
        if 'K' in text:
            return int(float(text.replace('K', '')) * 1000)
        elif 'M' in text:
            return int(float(text.replace('M', '')) * 1000000)
        else:
            return int(re.sub(r'[^\d]', '', text))
    except:
        return 0


if __name__ == "__main__":
    input_file = 'tiktok_links.txt'
    
    print('\n' + '='*60)
    print('TikTok Scraper - Stealth Mode')
    print('='*60)
    
    df = scrape_with_stealth(input_file, comments_per_video=100)
    
    if df is not None and len(df) > 0:
        df.to_csv('output/data/scraped_data.csv', index=False)
        print(f'\n✓ SUCCESS!')
        print(f'✓ Total rows: {len(df)}')
        print(f'✓ Saved to: output/data/scraped_data.csv')
    else:
        print('\n✗ No data scraped')
    
    input('\nPress ENTER to exit...')
