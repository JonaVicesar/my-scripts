#!/usr/bin/env python3
import yt_dlp
import argparse
import sys


def loader(d):

    if d['status'] == 'downloading':
        downloaded = d['downloaded_bytes']
        total = d['total_bytes']
        speed = d['_speed_str']
        
        if total > 0:
            percentage = (downloaded / total) * 100
            filled = int(percentage / 5) # divide by 5 because we want a 20 '#' bar: 100/5=20

            bar = '#' * filled + '_' * (20 - filled)  # 20 - filled to pad with '_' what's left
            
            print(f'\r[{bar}] {percentage:.1f}% | {speed}', end='')
            sys.stdout.flush()
    
    elif d['status'] == 'finished':
        print('\nDownload finished!')


def download_audio(url, quality='192'):
    print(f"Starting download for: {url}")
    options = {
        'format': 'bestaudio/best',
        'progress_hooks': [loader],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,  # avoid downloading entire playlists by accident
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        print("\nDownload completed successfully!")
    except Exception as e:
        print(f"\nError during download: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Downloads audio from a YouTube video and converts it to MP3.")
    parser.add_argument("url", help="Full URL of the YouTube video.")
    parser.add_argument("-c", "--quality", default="192", help="Audio quality in kbps (e.g: 128, 192, 320). Default: 192.")
    args = parser.parse_args()
    download_audio(args.url, args.quality)

if __name__ == "__main__":
    main()