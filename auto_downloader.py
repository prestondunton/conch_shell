import argparse
from tqdm import tqdm
import os
from sanitize_filename import sanitize

import spotify_utils
import youtube_utils


DOWNLOAD_SPOTIFY_PLAYLIST_LINK = 'https://open.spotify.com/playlist/6MOfGpQPUtLx1L1CnXen3X?si=15f08920c8dd4ebc'
DEFAULT_OUTPUT_DIR = './auto_downloads'


def search_and_downlod(search_query, output_dir, temp_dir):
    try:
        url = youtube_utils.get_top_search_video_url(search_query)
    except Exception as e:
        print(f'\tError searching YouTube for query {search_query}: {str(e)}')

    try:
        filename = sanitize(f'{search_query}.wav')
        print(f'\nDownloading {filename}')
        youtube_utils.download_youtube_audio(url, filename, output_dir, temp_dir)
        print(f'\tSuccessfully downloaded: {filename}')
    except Exception as e:
        print(f'\tError downloading audio from {url}: {str(e)}')



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