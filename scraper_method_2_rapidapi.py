"""
METODE 2: RapidAPI TikTok Scraper
Menggunakan RapidAPI untuk scraping

Installation:
pip install requests

Setup:
1. Daftar di https://rapidapi.com
2. Subscribe ke TikTok Scraper API
3. Copy API Key
4. Set environment variable: RAPIDAPI_KEY=your_api_key
   atau edit langsung di kode
"""

import pandas as pd
import requests
import time
import os
from datetime import datetime

def scrape_with_rapidapi(hashtags, videos_per_hashtag=100, comments_per_video=50):
    """
    Scrape data dari TikTok menggunakan RapidAPI
    
    Parameters:
    - hashtags: list of strings
    - videos_per_hashtag: int, jumlah video per hashtag
    - comments_per_video: int, jumlah komentar per video
    
    Returns:
    - DataFrame dengan kolom: video_id, username, caption, comment, likes, hashtags, date
    """
    
    # Get API key from environment or set directly
    api_key = os.getenv('RAPIDAPI_KEY', 'YOUR_RAPIDAPI_KEY_HERE')
    
    if api_key == 'YOUR_RAPIDAPI_KEY_HERE':
        raise ValueError("Please set RAPIDAPI_KEY environment variable or edit the code")
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
    }
    
    all_data = []
    
    for hashtag in hashtags:
        print(f'[Method 2] Scraping #{hashtag}...')
        
        try:
            # Search videos by hashtag
            search_url = "https://tiktok-scraper7.p.rapidapi.com/challenge/posts"
            search_params = {
                "challenge_name": hashtag,
                "count": str(videos_per_hashtag)
            }
            
            response = requests.get(search_url, headers=headers, params=search_params)
            
            if response.status_code != 200:
                print(f'  ✗ Error: API returned status {response.status_code}')
                continue
            
            data = response.json()
            videos = data.get('data', {}).get('videos', [])
            
            print(f'  Found {len(videos)} videos')
            
            for idx, video in enumerate(videos):
                print(f'  Processing video {idx+1}/{len(videos)}', end='\r')
                
                video_data = {
                    'video_id': video.get('video_id', ''),
                    'username': video.get('author', {}).get('unique_id', ''),
                    'caption': video.get('desc', ''),
                    'likes': video.get('statistics', {}).get('digg_count', 0),
                    'hashtags': f'#{hashtag}',
                    'date': datetime.fromtimestamp(video.get('create_time', 0))
                }
                
                # Get comments for this video
                video_id = video.get('video_id', '')
                if video_id:
                    try:
                        comment_url = "https://tiktok-scraper7.p.rapidapi.com/video/comments"
                        comment_params = {
                            "video_id": video_id,
                            "count": str(comments_per_video)
                        }
                        
                        comment_response = requests.get(comment_url, headers=headers, params=comment_params)
                        
                        if comment_response.status_code == 200:
                            comment_data_json = comment_response.json()
                            comments = comment_data_json.get('data', {}).get('comments', [])
                            
                            for comment in comments:
                                comment_row = video_data.copy()
                                comment_row['comment'] = comment.get('text', '')
                                all_data.append(comment_row)
                        
                        # Rate limiting
                        time.sleep(0.5)
                        
                    except Exception as e:
                        print(f'\n  Warning: Could not get comments for video {video_id}: {e}')
                
                # If no comments, add video data only
                if not any(d['video_id'] == video_id for d in all_data):
                    video_data['comment'] = ''
                    all_data.append(video_data)
                
                # Rate limiting
                time.sleep(0.3)
            
            print(f'\n  ✓ Scraped {len(videos)} videos from #{hashtag}')
            
        except Exception as e:
            print(f'  ✗ Error scraping #{hashtag}: {e}')
            continue
    
    df = pd.DataFrame(all_data)
    
    if len(df) == 0:
        raise Exception("No data scraped with RapidAPI method")
    
    print(f'\n[Method 2] ✓ Total data scraped: {len(df)} rows')
    return df


if __name__ == "__main__":
    # Test
    hashtags = ['web3', 'blockchain']
    df = scrape_with_rapidapi(hashtags, videos_per_hashtag=10, comments_per_video=20)
    print(df.head())
