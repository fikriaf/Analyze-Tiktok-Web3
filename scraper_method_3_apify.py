"""
METODE 3: Apify TikTok Scraper
Menggunakan Apify Actor untuk scraping

Installation:
pip install apify-client

Setup:
1. Daftar di https://apify.com
2. Get API Token dari dashboard
3. Set environment variable: APIFY_TOKEN=your_token
   atau edit langsung di kode
"""

import pandas as pd
import os
from datetime import datetime
import time

def scrape_with_apify(hashtags, videos_per_hashtag=100, comments_per_video=50):
    """
    Scrape data dari TikTok menggunakan Apify
    
    Parameters:
    - hashtags: list of strings
    - videos_per_hashtag: int, jumlah video per hashtag
    - comments_per_video: int, jumlah komentar per video
    
    Returns:
    - DataFrame dengan kolom: video_id, username, caption, comment, likes, hashtags, date
    """
    
    try:
        from apify_client import ApifyClient
    except ImportError:
        raise ImportError("Apify client not installed. Run: pip install apify-client")
    
    # Get API token from environment or set directly
    api_token = os.getenv('APIFY_TOKEN', 'YOUR_APIFY_TOKEN_HERE')
    
    if api_token == 'YOUR_APIFY_TOKEN_HERE':
        raise ValueError("Please set APIFY_TOKEN environment variable or edit the code")
    
    client = ApifyClient(api_token)
    all_data = []
    
    for hashtag in hashtags:
        print(f'[Method 3] Scraping #{hashtag}...')
        
        try:
            # Prepare Actor input
            run_input = {
                "hashtags": [hashtag],
                "resultsPerPage": videos_per_hashtag,
                "shouldDownloadVideos": False,
                "shouldDownloadCovers": False,
                "shouldDownloadSubtitles": False,
                "shouldDownloadSlideshowImages": False
            }
            
            # Run the Actor and wait for it to finish
            print(f'  Starting Apify actor...')
            run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
            
            # Fetch results from the run's dataset
            print(f'  Fetching results...')
            items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
            
            print(f'  Found {len(items)} videos')
            
            for idx, item in enumerate(items):
                print(f'  Processing video {idx+1}/{len(items)}', end='\r')
                
                video_data = {
                    'video_id': item.get('id', ''),
                    'username': item.get('authorMeta', {}).get('name', ''),
                    'caption': item.get('text', ''),
                    'likes': item.get('diggCount', 0),
                    'hashtags': ' '.join([f"#{tag.get('name', '')}" for tag in item.get('hashtags', [])]),
                    'date': datetime.fromtimestamp(item.get('createTime', 0))
                }
                
                # Get comments if available
                comments = item.get('comments', [])
                
                if comments:
                    for comment in comments[:comments_per_video]:
                        comment_row = video_data.copy()
                        comment_row['comment'] = comment.get('text', '')
                        all_data.append(comment_row)
                else:
                    # If no comments, add video data only
                    video_data['comment'] = ''
                    all_data.append(video_data)
            
            print(f'\n  ✓ Scraped {len(items)} videos from #{hashtag}')
            
        except Exception as e:
            print(f'  ✗ Error scraping #{hashtag}: {e}')
            continue
    
    df = pd.DataFrame(all_data)
    
    if len(df) == 0:
        raise Exception("No data scraped with Apify method")
    
    print(f'\n[Method 3] ✓ Total data scraped: {len(df)} rows')
    return df


if __name__ == "__main__":
    # Test
    hashtags = ['web3', 'blockchain']
    df = scrape_with_apify(hashtags, videos_per_hashtag=10, comments_per_video=20)
    print(df.head())
