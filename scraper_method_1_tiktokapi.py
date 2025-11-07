"""
METODE 1: TikTokApi (Unofficial)
Menggunakan library TikTokApi untuk scraping

Installation:
pip install TikTokApi
playwright install
"""

import pandas as pd
from datetime import datetime
import asyncio

def scrape_with_tiktokapi(hashtags, videos_per_hashtag=100, comments_per_video=50):
    """
    Scrape data dari TikTok menggunakan TikTokApi
    
    Parameters:
    - hashtags: list of strings
    - videos_per_hashtag: int, jumlah video per hashtag
    - comments_per_video: int, jumlah komentar per video
    
    Returns:
    - DataFrame dengan kolom: video_id, username, caption, comment, likes, hashtags, date
    """
    
    try:
        from TikTokApi import TikTokApi
    except ImportError:
        raise ImportError("TikTokApi not installed. Run: pip install TikTokApi && playwright install")
    
    async def scrape_async():
        all_data = []
        
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[None], num_sessions=1, sleep_after=3)
            
            for hashtag in hashtags:
                print(f'[Method 1] Scraping #{hashtag}...')
                
                try:
                    tag = api.hashtag(name=hashtag)
                    video_count = 0
                    
                    async for video in tag.videos(count=videos_per_hashtag):
                        try:
                            video_count += 1
                            print(f'  Video {video_count}/{videos_per_hashtag}', end='\r')
                            
                            video_info = video.as_dict
                            
                            video_data = {
                                'video_id': video_info.get('id', ''),
                                'username': video_info.get('author', {}).get('uniqueId', ''),
                                'caption': video_info.get('desc', ''),
                                'likes': video_info.get('stats', {}).get('diggCount', 0),
                                'hashtags': ' '.join([f"#{tag['title']}" for tag in video_info.get('challenges', [])]),
                                'date': datetime.fromtimestamp(video_info.get('createTime', 0))
                            }
                            
                            # Get comments
                            comment_count = 0
                            async for comment in video.comments(count=comments_per_video):
                                try:
                                    comment_data = video_data.copy()
                                    comment_info = comment.as_dict
                                    comment_data['comment'] = comment_info.get('text', '')
                                    all_data.append(comment_data)
                                    comment_count += 1
                                except Exception as e:
                                    continue
                            
                            # If no comments, add video data only
                            if comment_count == 0:
                                video_data['comment'] = ''
                                all_data.append(video_data)
                                
                        except Exception as e:
                            print(f'\n  Error processing video: {e}')
                            continue
                    
                    print(f'\n  ✓ Scraped {video_count} videos from #{hashtag}')
                    
                except Exception as e:
                    print(f'  ✗ Error scraping #{hashtag}: {e}')
                    continue
        
        return pd.DataFrame(all_data)
    
    # Run async function
    df = asyncio.run(scrape_async())
    
    if len(df) == 0:
        raise Exception("No data scraped with TikTokApi method")
    
    print(f'\n[Method 1] ✓ Total data scraped: {len(df)} rows')
    return df


if __name__ == "__main__":
    # Test
    hashtags = ['web3', 'blockchain']
    df = scrape_with_tiktokapi(hashtags, videos_per_hashtag=10, comments_per_video=20)
    print(df.head())
