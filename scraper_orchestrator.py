"""
TikTok Scraper Orchestrator
Mencoba semua metode scraping secara berurutan sampai berhasil

Usage:
    python scraper_orchestrator.py

Metode yang akan dicoba:
1. TikTokApi (unofficial) - Gratis, butuh playwright
2. RapidAPI - Butuh API key, ada free tier
3. Apify - Butuh API token, ada free tier
4. Manual Links - Input batch link dari file CSV/TXT
"""

import pandas as pd
import os
from datetime import datetime

# Import all scraper methods
try:
    from scraper_method_1_tiktokapi import scrape_with_tiktokapi
    METHOD_1_AVAILABLE = True
except Exception as e:
    METHOD_1_AVAILABLE = False
    print(f"⚠ Method 1 (TikTokApi) not available: {e}")

try:
    from scraper_method_2_rapidapi import scrape_with_rapidapi
    METHOD_2_AVAILABLE = True
except Exception as e:
    METHOD_2_AVAILABLE = False
    print(f"⚠ Method 2 (RapidAPI) not available: {e}")

try:
    from scraper_method_3_apify import scrape_with_apify
    METHOD_3_AVAILABLE = True
except Exception as e:
    METHOD_3_AVAILABLE = False
    print(f"⚠ Method 3 (Apify) not available: {e}")

try:
    from scraper_method_4_manual import scrape_with_manual_links
    METHOD_4_AVAILABLE = True
except Exception as e:
    METHOD_4_AVAILABLE = False
    print(f"⚠ Method 4 (Manual) not available: {e}")


class TikTokScraperOrchestrator:
    """
    Orchestrator untuk mencoba berbagai metode scraping
    """
    
    def __init__(self, hashtags=None, manual_input_file=None, 
                 videos_per_hashtag=100, comments_per_video=50):
        """
        Initialize orchestrator
        
        Parameters:
        - hashtags: list of strings (untuk method 1-3)
        - manual_input_file: str, path ke file CSV/TXT (untuk method 4)
        - videos_per_hashtag: int
        - comments_per_video: int
        """
        self.hashtags = hashtags or []
        self.manual_input_file = manual_input_file
        self.videos_per_hashtag = videos_per_hashtag
        self.comments_per_video = comments_per_video
        self.df_result = None
        self.successful_method = None
    
    def scrape(self):
        """
        Mencoba semua metode scraping sampai berhasil
        
        Returns:
        - DataFrame hasil scraping
        """
        
        print("="*70)
        print("TikTok Scraper Orchestrator")
        print("="*70)
        print(f"Target hashtags: {self.hashtags}")
        print(f"Manual input file: {self.manual_input_file}")
        print(f"Videos per hashtag: {self.videos_per_hashtag}")
        print(f"Comments per video: {self.comments_per_video}")
        print("="*70)
        
        methods = [
            (1, "TikTokApi", METHOD_1_AVAILABLE, self._try_method_1),
            (2, "RapidAPI", METHOD_2_AVAILABLE, self._try_method_2),
            (3, "Apify", METHOD_3_AVAILABLE, self._try_method_3),
            (4, "Manual Links", METHOD_4_AVAILABLE, self._try_method_4),
        ]
        
        for method_num, method_name, available, method_func in methods:
            if not available:
                print(f"\n[Method {method_num}] {method_name} - SKIPPED (not available)")
                continue
            
            print(f"\n{'='*70}")
            print(f"Trying Method {method_num}: {method_name}")
            print(f"{'='*70}")
            
            try:
                df = method_func()
                
                if df is not None and len(df) > 0:
                    self.df_result = df
                    self.successful_method = f"Method {method_num}: {method_name}"
                    
                    print(f"\n{'='*70}")
                    print(f"✓ SUCCESS with {method_name}!")
                    print(f"✓ Total data scraped: {len(df)} rows")
                    print(f"{'='*70}")
                    
                    return df
                else:
                    print(f"\n✗ Method {method_num} returned no data")
                    
            except Exception as e:
                print(f"\n✗ Method {method_num} failed: {e}")
                continue
        
        # If all methods failed
        print(f"\n{'='*70}")
        print("✗ ALL METHODS FAILED")
        print("Please check:")
        print("  1. Internet connection")
        print("  2. API keys/tokens are set correctly")
        print("  3. Required packages are installed")
        print("  4. Manual input file exists (for method 4)")
        print(f"{'='*70}")
        
        return None
    
    def _try_method_1(self):
        """Try TikTokApi method"""
        if not self.hashtags:
            print("  ⚠ No hashtags provided, skipping")
            return None
        
        return scrape_with_tiktokapi(
            self.hashtags, 
            self.videos_per_hashtag, 
            self.comments_per_video
        )
    
    def _try_method_2(self):
        """Try RapidAPI method"""
        if not self.hashtags:
            print("  ⚠ No hashtags provided, skipping")
            return None
        
        return scrape_with_rapidapi(
            self.hashtags, 
            self.videos_per_hashtag, 
            self.comments_per_video
        )
    
    def _try_method_3(self):
        """Try Apify method"""
        if not self.hashtags:
            print("  ⚠ No hashtags provided, skipping")
            return None
        
        return scrape_with_apify(
            self.hashtags, 
            self.videos_per_hashtag, 
            self.comments_per_video
        )
    
    def _try_method_4(self):
        """Try Manual Links method"""
        if not self.manual_input_file:
            print("  ⚠ No manual input file provided, skipping")
            return None
        
        if not os.path.exists(self.manual_input_file):
            print(f"  ⚠ File not found: {self.manual_input_file}")
            return None
        
        return scrape_with_manual_links(
            self.manual_input_file, 
            self.comments_per_video
        )
    
    def save_results(self, output_file='output/data/raw_data.csv'):
        """
        Save scraping results to CSV
        
        Parameters:
        - output_file: str, path to output file
        """
        if self.df_result is None:
            print("✗ No data to save")
            return False
        
        # Create output directory if not exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save to CSV
        self.df_result.to_csv(output_file, index=False)
        
        print(f"\n{'='*70}")
        print(f"✓ Data saved to: {output_file}")
        print(f"✓ Total rows: {len(self.df_result)}")
        print(f"✓ Successful method: {self.successful_method}")
        print(f"{'='*70}")
        
        # Show preview
        print("\nData Preview:")
        print(self.df_result.head())
        
        return True


def main():
    """
    Main function untuk menjalankan orchestrator
    """
    
    # Configuration
    HASHTAGS = [
        'AIethics', 'blockchain', 'sustainability', 'web3',
        'digitalfreedom', 'cryptocurrency', 'NFT', 'metaverse', 'privacy'
    ]
    
    MANUAL_INPUT_FILE = 'tiktok_links.csv'  # Untuk method 4
    VIDEOS_PER_HASHTAG = 100
    COMMENTS_PER_VIDEO = 50
    OUTPUT_FILE = 'output/data/raw_data.csv'
    
    # Create orchestrator
    orchestrator = TikTokScraperOrchestrator(
        hashtags=HASHTAGS,
        manual_input_file=MANUAL_INPUT_FILE,
        videos_per_hashtag=VIDEOS_PER_HASHTAG,
        comments_per_video=COMMENTS_PER_VIDEO
    )
    
    # Try scraping
    df = orchestrator.scrape()
    
    # Save results if successful
    if df is not None:
        orchestrator.save_results(OUTPUT_FILE)
        return True
    else:
        print("\n✗ Scraping failed with all methods")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
