from pytube import Search, YouTube
import os
import argparse
from tqdm import tqdm
import subprocess
from sanitize_filename import sanitize
from contextlib import contextmanager
import sys


import spotify_utils


DOWNLOAD_SPOTIFY_PLAYLIST_LINK = 'https://open.spotify.com/playlist/6MOfGpQPUtLx1L1CnXen3X?si=15f08920c8dd4ebc'
DEFAULT_OUTPUT_DIR = './auto_downloads'


@contextmanager
def suppress_stderr():
    with open(os.devnull, "w") as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:  
            yield
        finally:
            sys.stderr = old_stderr


def get_top_search_video_url(search_query):
    # Surpress stderr because YouTube Reels cause noisey searching in pytube, which isn't patched yet
    with suppress_stderr():
        search_results = Search(search_query).results

        if search_results and len(search_results) > 0:
            top_result = search_results[0]
            video_url = f"https://www.youtube.com/watch?v={top_result.video_id}"
            return video_url
        else:
            print(f'Found no search results for query "{search_query}"')
            return None


def download_audio(url, filename, output_dir, temp_dir):

    mp4_path = os.path.join(temp_dir, filename.replace('.wav', '.mp4'))

    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()

        print(f'\nDownloading {filename}')

        # Download as MP4
        temp_path = audio.download(output_path=temp_dir)
        os.rename(temp_path, mp4_path)

        # Convert the MP4 file to WAV using ffmpeg
        wav_path = os.path.join(output_dir, filename)
        subprocess.run(f'ffmpeg -i "{mp4_path}" -acodec pcm_s16le -ar 44100 "{wav_path}" -y', capture_output=True)

        print(f'\tSuccessfully downloaded: {filename}')

    except Exception as e:
        print(f'\tError downloading audio from {url}: {str(e)}')

    finally:
        if os.path.exists(mp4_path):
            os.remove(mp4_path)


def search_and_downlod(search_query, output_dir, temp_dir):
    url = get_top_search_video_url(search_query)
    download_audio(url, sanitize(f'{search_query}.wav'), output_dir, temp_dir)


def main():
    parser = argparse.ArgumentParser(description='Download audio from YouTube videos as WAV files')
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT_DIR, help='Output directory to save the WAV files (default: output)')
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Set a temporary directory for the downloaded MP4 files
    temp_dir = os.path.join(args.output, 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    try:
        print(f'Getting tracks for Spotify platlist {DOWNLOAD_SPOTIFY_PLAYLIST_LINK}')
        tracks = spotify_utils.get_playlist_tracks(DOWNLOAD_SPOTIFY_PLAYLIST_LINK)
        print(f'Discovered {len(tracks)} tracks\n')

        # Check the existing files in the output directory so we don't waste time redownloading songs already downloaded
        pre_downloaded_files = {file for file in os.listdir(args.output) if file.endswith('.wav')}
        print(f'There are {len(pre_downloaded_files)} pre-downloaded files\n')

        search_queries = [f"{track['Track Name']} - {track['Artist']}" for track in tracks]
        search_queries = [query for query in search_queries if sanitize(f'{query}.wav') not in pre_downloaded_files]

        print(f'{len(search_queries)} appear to be new (not downloaded):')
        for query in search_queries:
            print(f'\t{query}')
        print('')

        print('Searching and downloading these songs')
        for query in tqdm(search_queries):
            search_and_downlod(query, args.output, temp_dir)
        print('')

        print('Download complete!')

    finally:
        os.rmdir(temp_dir)



if __name__ == '__main__':
    main()