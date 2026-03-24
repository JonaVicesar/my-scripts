#!/usr/bin/env python3
import yt_dlp
import argparse
import sys
import re #regex

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

def filter_message(msg):
    #ignore normal download messages
    if any(x in msg for x in [
        '[download]',
        'Download finished',
        '[youtube] Downloading webpage',
        '[youtube] Downloading android vr player',
        '[youtube] Downloading player',
        'No supported JavaScript runtime',
        'YouTube extraction without a JS runtime',
        '[info] Downloading 1 format',
        '[ExtractAudio]',
    ]):
        return
    
    #if it's a regional or blocked by country error, show a message
    if 'not made this video available' in msg:
        match = re.search(r'\[youtube\] ([a-zA-Z0-9_-]+):', msg)
        if match:
            video_id = match.group(1) #get video id
            print(f"\nSkipping the video: ({video_id})")
        return
    
    # show other messages
    if msg and not msg.strip().startswith('[youtube]'):
        print(msg)


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
        'skip_unavailable_fragments': True, #skip videos that are not available in a country
        'quiet': False,
        'no_warnings': True,
        'ignoreerrors': True,#skip errors and continue with the next video
    }
    
    #class to filter yt-dlp output
    class FilterMessage:
        def debug(self, msg):
            filter_message(msg)
        def info(self, msg):
            filter_message(msg)
        def warning(self, msg):
            filter_message(msg)
        def error(self, msg):
            filter_message(msg)
    
    options['logger'] = FilterMessage()
    
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    
    print("\nDownload completed!")

def main():
    parser = argparse.ArgumentParser(description="Downloads audio from a YouTube video and converts it to MP3.")
    parser.add_argument("url", help="Full URL of the YouTube video.")
    parser.add_argument("-c", "--quality", default="192", help="Audio quality in kbps (e.g: 128, 192, 320). Default: 192.")
    args = parser.parse_args()
    download_audio(args.url, args.quality)

if __name__ == "__main__":
    main()