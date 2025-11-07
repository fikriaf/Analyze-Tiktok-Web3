"""
METODE 4: Manual Input - Batch Link TikTok
Input manual dari file CSV/TXT berisi link TikTok, lalu scrape menggunakan Playwright

Installation:
pip install playwright pandas
playwright install

Input Format (CSV):
link
https://www.tiktok.com/@username/video/1234567890
https://www.tiktok.com/@username/video/0987654321

atau TXT (satu link per baris)
"""

import pandas as pd
from datetime import datetime
import time
import re
import json
import os

def scrape_with_manual_links(input_file, comments_per_video=50):
    """
    Scrape data dari TikTok menggunakan batch link manual
    
    Parameters:
    - input_file: str, path ke file CSV atau TXT berisi link TikTok
    - comments_per_video: int, jumlah komentar per video
    
    Returns:
    - DataFrame dengan kolom: video_id, username, caption, comment, likes, hashtags, date
    """
    
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise ImportError("Playwright not installed. Run: pip install playwright && playwright install")
    
    # Read input file
    print(f'[Method 4] Reading links from {input_file}...')
    
    if input_file.endswith('.csv'):
        links_df = pd.read_csv(input_file)
        links = links_df['link'].tolist()
    elif input_file.endswith('.txt'):
        with open(input_file, 'r', encoding='utf-8') as f:
            links = [line.strip() for line in f if line.strip()]
    else:
        raise ValueError("Input file must be CSV or TXT")
    
    print(f'  Found {len(links)} links')
    
    all_data = []
    
    cookie_file = 'tiktok_cookies.json'
    
    with sync_playwright() as p:
        # Launch browser with stealth mode
        print('  Launching browser...')
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security'
            ]
        )
        
        # Check if cookies exist
        if os.path.exists(cookie_file):
            print(f'\n  ✓ Found saved cookies: {cookie_file}')
            print('  Loading cookies...')
            
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            context.add_cookies(cookies)
            page = context.new_page()
            
            # Test if cookies still valid
            page.goto('https://www.tiktok.com', timeout=60000)
            time.sleep(3)
            
            # Check if logged in
            if page.query_selector('[data-e2e="profile-icon"]'):
                print('  ✓ Cookies valid, already logged in!\n')
            else:
                print('  ✗ Cookies expired, need to login again\n')
                os.remove(cookie_file)
                # Reload without cookies
                context.close()
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                page = context.new_page()
                page.goto('https://www.tiktok.com', timeout=60000)
                
                print('\n  ========================================')
                print('  MANUAL LOGIN REQUIRED')
                print('  ========================================')
                print('  1. LOGIN manually with your account')
                print('  2. After login, press ENTER to save cookies')
                print('  ========================================\n')
                
                input('  Press ENTER after you logged in... ')
                
                # Save cookies
                cookies = context.cookies()
                with open(cookie_file, 'w') as f:
                    json.dump(cookies, f)
                print(f'\n  ✓ Cookies saved to: {cookie_file}')
                print('  Next time you run, no need to login!\n')
        else:
            print('\n  No saved cookies found')
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            # Go to TikTok for login
            print('\n  ========================================')
            print('  MANUAL LOGIN REQUIRED')
            print('  ========================================')
            print('  1. Browser will open TikTok')
            print('  2. LOGIN manually with your account')
            print('  3. After login, press ENTER to save cookies')
            print('  ========================================\n')
            
            page.goto('https://www.tiktok.com', timeout=60000)
            input('  Press ENTER after you logged in... ')
            
            # Save cookies
            cookies = context.cookies()
            with open(cookie_file, 'w') as f:
                json.dump(cookies, f)
            print(f'\n  ✓ Cookies saved to: {cookie_file}')
            print('  Next time you run, no need to login!\n')
        
        print('  Starting scraping...\n')
        
        for idx, link in enumerate(links):
            print(f'\n[{idx+1}/{len(links)}] Scraping: {link[:60]}...')
            
            try:
                # Navigate to video with better error handling
                try:
                    # Random delay before navigation (human-like)
                    time.sleep(2 + (idx % 3))
                    
                    page.goto(link, wait_until='domcontentloaded', timeout=45000)
                    
                    # Wait and check if page loaded correctly
                    time.sleep(5)
                    
                    # Check for error page
                    page_content = page.content()
                    if 'trouble' in page_content.lower() or 'error' in page_content.lower():
                        print(f'  ⚠ Page shows error/trouble message')
                        print(f'  Waiting 10 seconds and retry...')
                        time.sleep(10)
                        page.reload()
                        time.sleep(5)
                    
                except Exception as nav_error:
                    print(f'  ⚠ Navigation warning: {nav_error}')
                    print(f'  Trying to continue anyway...')
                    time.sleep(3)
                
                # Extract video ID from URL
                video_id_match = re.search(r'/video/(\d+)', link)
                video_id = video_id_match.group(1) if video_id_match else ''
                
                # Extract username from URL
                username_match = re.search(r'@([^/]+)', link)
                username = username_match.group(1) if username_match else ''
                
                # Extract caption
                try:
                    caption_elem = page.query_selector('[data-e2e="browse-video-desc"]')
                    caption = caption_elem.inner_text() if caption_elem else ''
                    print(f'  Caption: {caption[:50]}...' if caption else '  Caption: (empty)')
                except Exception as e:
                    caption = ''
                    print(f'  Caption: Error - {e}')
                
                # Extract likes
                try:
                    likes_elem = page.query_selector('[data-e2e="like-count"]')
                    likes_text = likes_elem.inner_text() if likes_elem else '0'
                    # Convert K, M to numbers
                    likes = parse_count(likes_text)
                    print(f'  Likes: {likes} (raw: {likes_text})')
                except Exception as e:
                    likes = 0
                    print(f'  Likes: Error - {e}')
                
                # Extract hashtags
                try:
                    hashtag_elems = page.query_selector_all('a[href*="/tag/"]')
                    hashtags = ' '.join([elem.inner_text() for elem in hashtag_elems])
                    print(f'  Hashtags: {hashtags[:50]}...' if hashtags else '  Hashtags: (none)')
                except Exception as e:
                    hashtags = ''
                    print(f'  Hashtags: Error - {e}')
                
                # Extract date (if available)
                try:
                    date_elem = page.query_selector('[data-e2e="browser-nickname"] + span')
                    date_text = date_elem.inner_text() if date_elem else ''
                    date = parse_date(date_text)
                except:
                    date = datetime.now()
                
                video_data = {
                    'video_id': video_id,
                    'username': username,
                    'caption': caption,
                    'likes': likes,
                    'hashtags': hashtags,
                    'date': date
                }
                
                # Scroll to load comments
                try:
                    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    time.sleep(3)
                    
                    # Click "View more replies" buttons if any
                    try:
                        view_more_buttons = page.query_selector_all('button:has-text("View more replies")')
                        for btn in view_more_buttons[:5]:  # Click first 5
                            try:
                                btn.click()
                                time.sleep(1)
                            except:
                                pass
                    except:
                        pass
                    
                    # Extract ALL comments (level 1 and level 2)
                    # Method 1: Get by data-e2e
                    comment_elems_level1 = page.query_selector_all('[data-e2e="comment-level-1"]')
                    comment_elems_level2 = page.query_selector_all('[data-e2e="comment-level-2"]')
                    
                    all_comment_elems = list(comment_elems_level1) + list(comment_elems_level2)
                    
                    # Method 2: If not found, try by class
                    if not all_comment_elems:
                        all_comment_elems = page.query_selector_all('p[class*="CommentText"]')
                    
                    print(f'  Found {len(all_comment_elems)} comment elements')
                    
                    comment_count = 0
                    for comment_elem in all_comment_elems[:comments_per_video]:
                        try:
                            # Get text from span inside p
                            comment_text = comment_elem.inner_text().strip()
                            
                            if comment_text and len(comment_text) > 0:
                                comment_row = video_data.copy()
                                comment_row['comment'] = comment_text
                                all_data.append(comment_row)
                                comment_count += 1
                        except Exception as e:
                            continue
                    
                    print(f'  Comments: {comment_count} extracted')
                    
                    # If no comments, add video data only
                    if comment_count == 0:
                        video_data['comment'] = ''
                        all_data.append(video_data)
                        print(f'  No comments found, added video data only')
                        
                except Exception as e:
                    # If can't get comments, add video data only
                    print(f'  Comments: Error - {e}')
                    video_data['comment'] = ''
                    all_data.append(video_data)
                
                print(f'  ✓ Video scraped successfully')
                
                # Rate limiting - random wait (human-like)
                wait_time = 5 + (idx % 5)  # 5-9 seconds
                print(f'  Waiting {wait_time} seconds before next video...')
                time.sleep(wait_time)
                
            except Exception as e:
                print(f'  ✗ FAILED: {e}')
                print(f'  Waiting 3 seconds before next video...')
                time.sleep(3)
                continue
        
        browser.close()
    
    print(f'\n  ✓ Scraped {len(links)} videos')
    
    df = pd.DataFrame(all_data)
    
    if len(df) == 0:
        raise Exception("No data scraped with manual method")
    
    print(f'\n[Method 4] ✓ Total data scraped: {len(df)} rows')
    return df


def parse_count(text):
    """Convert text like '1.2K' or '3.5M' to number"""
    text = text.strip().upper()
    if 'K' in text:
        return int(float(text.replace('K', '')) * 1000)
    elif 'M' in text:
        return int(float(text.replace('M', '')) * 1000000)
    else:
        try:
            return int(text)
        except:
            return 0


def parse_date(text):
    """Parse date text to datetime"""
    # Simple implementation - adjust based on actual format
    try:
        # Handle formats like "2024-01-15" or "15-01-2024"
        return pd.to_datetime(text)
    except:
        return datetime.now()


def create_sample_input_file(filename='tiktok_links.csv'):
    """Create sample input file"""
    sample_data = {
        'link': [
            'https://www.tiktok.com/@example/video/1234567890',
            'https://www.tiktok.com/@example/video/0987654321',
        ]
    }
    df = pd.DataFrame(sample_data)
    df.to_csv(filename, index=False)
    print(f'Sample file created: {filename}')
    print('Edit this file and add your TikTok video links')


if __name__ == "__main__":
    # Create sample input file
    # create_sample_input_file()
    
    # Test scraping
    df = scrape_with_manual_links('tiktok_links.csv', comments_per_video=20)
    print(df.head())
