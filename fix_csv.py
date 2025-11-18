"""
Script untuk memperbaiki CSV yang rusak
Membaca file CSV yang rusak dan menyimpan ulang dengan format yang benar
"""

import pandas as pd
import csv
import re

def process_line(line, cleaned_data, line_num, skipped_lines):
    """Process single line and add to cleaned_data"""
    try:
        parts = line.split(',')
        
        if len(parts) < 6:
            skipped_lines.append(f"Line {line_num}: {line[:100]}... (too few parts: {len(parts)})")
            return False
        
        # Ambil field yang pasti (6 field pertama)
        video_id = parts[0].strip()
        username = parts[1].strip()
        caption = parts[2].strip()
        likes = parts[3].strip()
        hashtags = parts[4].strip()
        date = parts[5].strip()
        
        # Gabungkan sisa sebagai comment
        if len(parts) > 6:
            comment_parts = parts[6:]
            comment = ','.join(comment_parts)
        else:
            comment = ''
        
        # Bersihkan comment dari karakter rusak
        comment = comment.strip()
        # Hapus quote ganda di awal/akhir
        while comment.startswith('"') and comment.count('"') > 1:
            comment = comment[1:]
        while comment.endswith('"') and comment.count('"') > 1:
            comment = comment[:-1]
        
        # Bersihkan karakter rusak
        comment = comment.replace(';,', '')
        comment = comment.replace(',,,,,,', '')
        comment = re.sub(r';+', '', comment)  # Hapus semicolon
        comment = re.sub(r',{2,}', '', comment)  # Hapus multiple comma
        comment = comment.strip(',').strip()
        
        # Bersihkan field lain dari quote
        video_id = video_id.strip('"')
        username = username.strip('"')
        caption = caption.strip('"')
        likes = likes.strip('"')
        hashtags = hashtags.strip('"')
        date = date.strip('"')
        
        cleaned_data.append({
            'video_id': video_id,
            'username': username,
            'caption': caption,
            'likes': likes,
            'hashtags': hashtags,
            'date': date,
            'comment': comment
        })
        
        return True
        
    except Exception as e:
        skipped_lines.append(f"Line {line_num}: ERROR - {e}")
        return False

def fix_csv(input_file, output_file):
    """
    Perbaiki CSV yang rusak - ambil semua data
    """
    print(f"Membaca file: {input_file}")
    
    # Baca file mentah line by line
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    print(f"Total lines: {len(lines)}")
    
    # Data yang sudah dibersihkan
    cleaned_data = []
    skipped_lines = []  # Simpan line yang dibuang
    
    # Skip header yang rusak
    skipped = 0
    current_line_buffer = ""  # Buffer untuk multi-line
    
    for i, line in enumerate(lines[1:], start=2):  # Start from line 2
        try:
            # Hapus newline
            line = line.strip()
            
            if not line:
                continue
            
            # Jika line dimulai dengan quote, cek apakah ada video_id di dalamnya
            if line[0] == '"':
                # Coba hapus quote di awal dan cek lagi
                line_without_quote = line.lstrip('"')
                if line_without_quote and line_without_quote[0].isdigit():
                    # Ini data valid yang dimulai dengan quote
                    line = line_without_quote
                elif current_line_buffer:
                    # Ini continuation dari line sebelumnya
                    current_line_buffer += " " + line
                    continue
                else:
                    # Line yang tidak valid
                    skipped += 1
                    skipped_lines.append(f"Line {i}: {line[:100]}...")
                    continue
            
            # Jika ada buffer, process buffer dulu
            if current_line_buffer:
                # Process buffer
                if not process_line(current_line_buffer, cleaned_data, i-1, skipped_lines):
                    skipped += 1
                current_line_buffer = ""
            
            # Cek apakah line dimulai dengan angka (video_id)
            if not line[0].isdigit():
                skipped += 1
                skipped_lines.append(f"Line {i}: {line[:100]}...")
                continue
            
            # Split by comma
            parts = line.split(',')
            
            if len(parts) < 6:
                # Simpan ke buffer, mungkin multi-line
                current_line_buffer = line
                continue
            
            # Process line
            if not process_line(line, cleaned_data, i, skipped_lines):
                skipped += 1
            
        except Exception as e:
            skipped += 1
            skipped_lines.append(f"Line {i}: ERROR - {e}")
            continue
    
    # Process remaining buffer
    if current_line_buffer:
        if not process_line(current_line_buffer, cleaned_data, len(lines), skipped_lines):
            skipped += 1
    
    print(f"\nTotal data cleaned: {len(cleaned_data)}")
    print(f"Total skipped: {skipped}")
    
    # Save skipped lines
    if skipped_lines:
        skipped_file = output_file.replace('.csv', '_skipped.txt')
        with open(skipped_file, 'w', encoding='utf-8') as f:
            f.write(f"Total skipped lines: {len(skipped_lines)}\n")
            f.write("="*60 + "\n\n")
            for line in skipped_lines:
                f.write(line + '\n')
        print(f"Skipped lines saved to: {skipped_file}")
    
    # Buat DataFrame
    df = pd.DataFrame(cleaned_data)
    
    # Remove duplicates
    df_before = len(df)
    df = df.drop_duplicates()
    df_after = len(df)
    print(f"Removed {df_before - df_after} duplicates")
    
    # Save dengan format yang benar
    df.to_csv(output_file, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL, escapechar='\\')
    print(f"\n✓ Saved to: {output_file}")
    
    # Statistics
    print(f"\n{'='*60}")
    print("STATISTICS")
    print(f"{'='*60}")
    print(f"Total rows: {len(df)}")
    print(f"Unique videos: {df['video_id'].nunique()}")
    print(f"Unique users: {df['username'].nunique()}")
    print(f"Comments with text: {df['comment'].str.len().gt(0).sum()}")
    print(f"Empty comments: {df['comment'].str.len().eq(0).sum()}")
    print(f"{'='*60}")
    
    return df


if __name__ == "__main__":
    input_file = 'output/data/scraped_data.csv'
    output_file = 'output/data/scraped_data_fixed.csv'
    
    print("\n" + "="*60)
    print("CSV FIXER")
    print("="*60)
    
    try:
        df = fix_csv(input_file, output_file)
        
        print("\n✓ SUCCESS!")
        print(f"\nOriginal file: {input_file}")
        print(f"Fixed file: {output_file}")
        print("\nYou can now:")
        print("1. Check the fixed file")
        print("2. If OK, rename it to replace the original:")
        print(f"   mv {output_file} {input_file}")
        
    except Exception as e:
        print(f"\n✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to exit...")
