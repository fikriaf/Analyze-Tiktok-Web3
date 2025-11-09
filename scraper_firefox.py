"""
TikTok Scraper using Selenium with Firefox
Firefox lebih susah dideteksi daripada Chrome

Installation:
pip install selenium webdriver-manager

Usage:
    python scraper_firefox.py
"""

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
import json
import os
from datetime import datetime

def scrape_with_firefox(input_file):
    """
    Scrape TikTok menggunakan Selenium + Firefox (No Login Required)
    """
    
    # Read links
    print(f'Reading links from {input_file}...')
    if input_file.endswith('.csv'):
        links_df = pd.read_csv(input_file)
        links = links_df['link'].tolist()
    else:
        with open(input_file, 'r', encoding='utf-8') as f:
            links = [line.strip() for line in f if line.strip()]
    
    print(f'Found {len(links)} links\n')
    
    # Load existing data if file exists
    all_data = []
    output_file = 'output/data/scraped_data.csv'
    if os.path.exists(output_file):
        try:
            existing_df = pd.read_csv(output_file)
            all_data = existing_df.to_dict('records')
            print(f'Loaded {len(all_data)} existing rows from {output_file}\n')
        except:
            print(f'Could not load existing file, starting fresh\n')
    
    # Setup Firefox options
    options = Options()
    # options.add_argument('--headless')  # Uncomment untuk background mode
    
    # Set preferences untuk anti-detection
    options.set_preference('dom.webdriver.enabled', False)
    options.set_preference('useAutomationExtension', False)
    options.set_preference('general.useragent.override', 
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0')
    options.set_preference('intl.accept_languages', 'id-ID, id, en-US, en')
    
    # Create driver with auto-download geckodriver
    print('Launching Firefox...')
    print('(Auto-downloading geckodriver if needed...)')
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    
    try:
        # Start scraping directly (no login needed)
        print('Starting scraping...\n')
        
        for idx, link in enumerate(links):
            print(f'\n[{idx+1}/{len(links)}] {link[:60]}...')
            
            try:
                # Human-like delay
                time.sleep(4 + (idx % 5))
                
                # Navigate
                driver.get(link)
                time.sleep(7)
                
                # ASK USER: Normal or Side Comment? (AFTER loading video)
                while True:
                    mode_input = input('  Comment mode? (0=Normal, 1=Side Comment): ').strip()
                    if mode_input in ['0', '1']:
                        comment_mode = int(mode_input)
                        break
                    else:
                        print('  ⚠ Invalid input! Enter 0 or 1')
                
                print(f'  Mode: {"SIDE COMMENT" if comment_mode == 1 else "NORMAL"}')
                
                # Check for error
                page_source = driver.page_source.lower()
                if 'trouble' in page_source or 'error' in page_source:
                    print('  ⚠ Error page detected, waiting 3s...')
                    time.sleep(3)
                    driver.refresh()
                    time.sleep(7)
                
                # Extract video ID and username
                video_id = re.search(r'/video/(\d+)', link).group(1) if re.search(r'/video/(\d+)', link) else ''
                username = re.search(r'@([^/]+)', link).group(1) if re.search(r'@([^/]+)', link) else ''
                
                # Caption - WAIT for element
                caption = ''
                try:
                    caption_elem = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="browse-video-desc"]'))
                    )
                    caption = caption_elem.text
                    print(f'  Caption: {caption[:40]}...')
                except:
                    try:
                        # Fallback selector
                        caption_elem = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[data-e2e="browse-video-desc"]'))
                        )
                        caption = caption_elem.text
                        print(f'  Caption: {caption[:40]}...')
                    except:
                        print(f'  Caption: (not found)')
                
                # Likes - WAIT for element
                likes = 0
                try:
                    like_elem = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="like-count"]'))
                    )
                    likes_text = like_elem.text
                    likes = parse_count(likes_text)
                    print(f'  Likes: {likes}')
                except:
                    try:
                        # Fallback
                        like_elem = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'strong[data-e2e="like-count"]'))
                        )
                        likes_text = like_elem.text
                        likes = parse_count(likes_text)
                        print(f'  Likes: {likes}')
                    except:
                        print(f'  Likes: 0')
                
                # Hashtags - WAIT for elements
                hashtags = ''
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/tag/"]'))
                    )
                    hashtag_elems = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/tag/"]')
                    hashtags = ' '.join([elem.text for elem in hashtag_elems if elem.text])
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
                
                # Scroll to comments - FORCE LOAD
                try:
                    print(f'  Loading comments...')
                    
                    # SIDE COMMENT MODE: Click icon to open sidebar
                    if comment_mode == 1:
                        try:
                            comment_icon = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="comment-icon"]'))
                            )
                            driver.execute_script("arguments[0].click();", comment_icon)
                            print(f'    ✓ Clicked comment icon (sidebar)')
                            time.sleep(5)  # Wait lebih lama untuk sidebar load
                        except:
                            print(f'    ⚠ Comment icon not found')
                    
                    # Scroll dulu untuk trigger comment section load (NORMAL MODE)
                    if comment_mode == 0:
                        print(f'  Initial scroll to load comments...')
                        for i in range(3):
                            driver.execute_script("window.scrollBy(0, 800)")
                            time.sleep(2)
                    
                    # GET TOTAL COMMENT COUNT (based on mode)
                    total_comments = 0
                    
                    try:
                        if comment_mode == 1:
                            # SIDE COMMENT: Wait untuk DivCommentCountContainer
                            print(f'  Detecting comment count in sidebar...')
                            
                            # Wait sampai container muncul
                            count_container = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="DivCommentCountContainer"]'))
                            )
                            
                            # Ambil span di dalam container
                            count_span = count_container.find_element(By.CSS_SELECTOR, 'span[class*="TUXText"]')
                            count_text = count_span.text
                            
                            if 'komentar' in count_text.lower() or 'comment' in count_text.lower():
                                total_comments = parse_count(count_text.split()[0])
                                print(f'  Total comments: {total_comments}')
                            else:
                                print(f'  Total comments: (text not found in span)')
                        
                        else:
                            # NORMAL COMMENT: Use p.PCommentTitle
                            print(f'  Detecting comment count in page...')
                            
                            # Wait untuk ada p element dulu
                            WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.TAG_NAME, 'p'))
                            )
                            
                            # Cari semua p element yang ada text "komentar"
                            all_p = driver.find_elements(By.TAG_NAME, 'p')
                            print(f'  Found {len(all_p)} p elements, searching for comment count...')
                            
                            for p in all_p:
                                try:
                                    p_text = p.text
                                    p_class = p.get_attribute('class')
                                    
                                    if 'komentar' in p_text.lower() or 'comment' in p_text.lower():
                                        # Check if it's the title (has PCommentTitle or e1avzmag1)
                                        if 'PCommentTitle' in p_class or 'e1avzmag1' in p_class:
                                            total_comments = parse_count(p_text.split()[0])
                                            print(f'  Total comments: {total_comments} (found in class: {p_class[:50]}...)')
                                            break
                                except:
                                    continue
                        
                        
                        if total_comments == 0:
                            print(f'  Total comments: (unknown)')
                    except Exception as e:
                        print(f'  Total comments: (error - {e})')
                    
                    # SCROLL based on mode
                    if comment_mode == 1:
                        # SIDE COMMENT: Scroll di dalam sidebar
                        print(f'  Scrolling comment sidebar...')
                        
                        # Find comment sidebar container
                        comment_container = None
                        try:
                            # Try multiple selectors for comment container
                            selectors = [
                                'div[class*="DivCommentMain"]',  # Comment main container
                                'div[class*="DivTabContainer"]',
                                'div[class*="DivCommentListContainer"]',
                                '[data-e2e="comment-list-container"]'
                            ]
                            
                            for selector in selectors:
                                try:
                                    comment_container = driver.find_element(By.CSS_SELECTOR, selector)
                                    print(f'    ✓ Found comment container: {selector}')
                                    break
                                except:
                                    continue
                        except:
                            pass
                        
                        # Scroll inside comment sidebar with smart stop
                        if comment_container:
                            print(f'    ✓ Starting sidebar scroll...')
                            scroll_count = 0
                            no_change_count = 0
                            prev_comment_count = 0
                            
                            while True:
                                # Smooth scroll: scroll bertahap 500px per step
                                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 500", comment_container)
                                time.sleep(1)  # Beri waktu comment load
                                scroll_count += 1
                                
                                # Count current comments
                                current_comment_count = len(driver.find_elements(By.CSS_SELECTOR, '[data-e2e="comment-level-1"]'))
                                current_comment_count += len(driver.find_elements(By.CSS_SELECTOR, '[data-e2e="comment-level-2"]'))
                                
                                print(f'    Scroll {scroll_count} | Comments: {current_comment_count}/{total_comments}', end='\r')
                                
                                # Check if no new comments loaded
                                if current_comment_count == prev_comment_count:
                                    no_change_count += 1
                                else:
                                    no_change_count = 0
                                
                                prev_comment_count = current_comment_count
                                
                                # Stop conditions - lebih toleran
                                if no_change_count >= 30:  # Dari 5 ke 10 scroll
                                    print(f'\n    ✓ Reached bottom (no new comments after 10 scrolls)')
                                    break
                                
                                if total_comments > 0 and current_comment_count >= total_comments * 0.95:
                                    print(f'\n    ✓ Reached 95% of total comments')
                                    break
                                
                                if scroll_count >= 200:  # Safety limit lebih tinggi
                                    print(f'\n    ⚠ Max scroll limit reached')
                                    break
                        else:
                            print(f'    ⚠ Comment container not found!')
                    else:
                        # NORMAL: Scroll halaman utama with smart stop
                        print(f'  Scrolling main page...')
                        scroll_count = 0
                        no_change_count = 0
                        prev_comment_count = 0
                        
                        while True:
                            # Smooth scroll: scroll bertahap, bukan langsung ke bawah
                            current_scroll = driver.execute_script("return window.pageYOffset")
                            
                            # Scroll 800px per step (smooth)
                            driver.execute_script("window.scrollBy(0, 800)")
                            time.sleep(4)  # Lebih lama: beri waktu comment load
                            scroll_count += 1
                            
                            # Count current comments
                            current_comment_count = len(driver.find_elements(By.CSS_SELECTOR, '[data-e2e="comment-level-1"]'))
                            current_comment_count += len(driver.find_elements(By.CSS_SELECTOR, '[data-e2e="comment-level-2"]'))
                            
                            print(f'    Scroll {scroll_count} | Comments: {current_comment_count}/{total_comments}', end='\r')
                            
                            # Check if no new comments loaded
                            if current_comment_count == prev_comment_count:
                                no_change_count += 1
                            else:
                                no_change_count = 0
                            
                            prev_comment_count = current_comment_count
                            
                            # Stop conditions - lebih toleran
                            if no_change_count >= 10:  # Dari 5 ke 10 scroll
                                print(f'\n    ✓ Reached bottom (no new comments after 10 scrolls)')
                                break
                            
                            if total_comments > 0 and current_comment_count >= total_comments * 0.95:
                                print(f'\n    ✓ Reached 95% of total comments')
                                break
                            
                            if scroll_count >= 200:  # Safety limit lebih tinggi
                                print(f'\n    ⚠ Max scroll limit reached')
                                break
                    
                    print(f'\n  Expanding replies...')
                    
                    # Find all reply/more buttons (sama untuk kedua mode)
                    try:
                        # Find all reply buttons: "Lihat X balasan" dan "Lihat X lainnya"
                        reply_selectors = [
                            "//span[contains(text(), 'Lihat') and (contains(text(), 'balasan') or contains(text(), 'lainnya'))]",
                            "//span[contains(text(), 'View') and (contains(text(), 'repl') or contains(text(), 'more'))]"
                        ]
                        
                        reply_btns = []
                        for selector in reply_selectors:
                            try:
                                reply_btns = driver.find_elements(By.XPATH, selector)
                                if reply_btns:
                                    break
                            except:
                                continue
                        
                        if reply_btns:
                            print(f'    Found {len(reply_btns)} reply/more buttons')
                            
                            for btn_idx, btn in enumerate(reply_btns):
                                try:
                                    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                                    time.sleep(1)
                                    driver.execute_script("arguments[0].click();", btn)
                                    time.sleep(2)
                                    print(f'    Clicked button {btn_idx+1}', end='\r')
                                except:
                                    pass
                            print()
                        else:
                            print(f'    No reply/more buttons found')
                    except Exception as e:
                        print(f'    Error expanding replies: {e}')
                    
                    # Final scroll
                    print(f'\n  Final loading...')
                    for i in range(3):
                        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                        time.sleep(1)
                    
                    # Wait for comments to load
                    print(f'  Waiting for comments...')
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="comment-level-1"]'))
                        )
                        print(f'  Comments loaded!')
                    except:
                        print(f'  Timeout waiting for comments')
                    
                    # Get all comments (level 1 and 2)
                    comment_elems = []
                    try:
                        comment_elems += driver.find_elements(By.CSS_SELECTOR, '[data-e2e="comment-level-1"]')
                    except:
                        pass
                    
                    try:
                        comment_elems += driver.find_elements(By.CSS_SELECTOR, '[data-e2e="comment-level-2"]')
                    except:
                        pass
                    
                    # Fallback: find by class
                    if not comment_elems:
                        try:
                            comment_elems = driver.find_elements(By.CSS_SELECTOR, 'p[class*="CommentText"]')
                        except:
                            pass
                    
                    # Another fallback: find by tag
                    if not comment_elems:
                        try:
                            comment_elems = driver.find_elements(By.TAG_NAME, 'p')
                            # Filter only comments
                            comment_elems = [elem for elem in comment_elems if 'comment' in elem.get_attribute('class').lower()]
                        except:
                            pass
                    
                    comment_count = 0
                    seen_comments = set()  # Avoid duplicates
                    
                    # AMBIL SEMUA COMMENTS - NO LIMIT
                    print(f'  Extracting {len(comment_elems)} comment elements...')
                    for comment_elem in comment_elems:
                        try:
                            comment_text = ''
                            
                            # Try to find nested span with TUXText
                            try:
                                text_span = comment_elem.find_element(By.CSS_SELECTOR, 'span[class*="TUXText"]')
                                comment_text = text_span.text.strip()
                            except:
                                pass
                            
                            # If empty, try direct text
                            if not comment_text:
                                comment_text = comment_elem.text.strip()
                            
                            # If empty, try textContent
                            if not comment_text:
                                comment_text = driver.execute_script("return arguments[0].textContent;", comment_elem).strip()
                            
                            # Validate and add
                            if comment_text and len(comment_text) > 1:
                                # Avoid duplicates
                                if comment_text not in seen_comments:
                                    seen_comments.add(comment_text)
                                    comment_row = video_data.copy()
                                    comment_row['comment'] = comment_text
                                    all_data.append(comment_row)
                                    comment_count += 1
                        except Exception as e:
                            continue
                    
                    print(f'  Comments: {comment_count} (unique from {len(comment_elems)} elements)')
                    
                    if comment_count == 0:
                        video_data['comment'] = ''
                        all_data.append(video_data)
                        
                except Exception as e:
                    print(f'  Comments: Error - {e}')
                    video_data['comment'] = ''
                    all_data.append(video_data)
                
                print(f'  ✓ Success\n')
                
                # SAVE AFTER EACH VIDEO
                if len(all_data) > 0:
                    os.makedirs('output/data', exist_ok=True)
                    temp_df = pd.DataFrame(all_data)
                    temp_df.to_csv('output/data/scraped_data.csv', index=False)
                    print(f'  💾 Saved {len(all_data)} rows to output/data/scraped_data.csv\n')
                
                # Human-like wait
                wait_time = 7 + (idx % 6)
                time.sleep(wait_time)
                
            except Exception as e:
                print(f'  ✗ Failed: {e}\n')
                time.sleep(5)
                continue
        
    finally:
        print('\nClosing Firefox...')
        driver.quit()
    
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
    print('TikTok Scraper - Firefox')
    print('='*60)
    
    df = scrape_with_firefox(input_file)
    
    if df is not None and len(df) > 0:
        os.makedirs('output/data', exist_ok=True)
        df.to_csv('output/data/scraped_data.csv', index=False)
        print(f'\n✓ SUCCESS!')
        print(f'✓ Total rows: {len(df)}')
        print(f'✓ Saved to: output/data/scraped_data.csv')
    else:
        print('\n✗ No data scraped')
    
    input('\nPress ENTER to exit...')
