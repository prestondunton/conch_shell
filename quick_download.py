import argparse
import os
from sanitize_filename import sanitize

import youtube_utils


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Download YouTube audio')
    
    # Add the required 'source' argument
    parser.add_argument('source', metavar='source', type=str, help='URL of the YouTube video')

    # Add the optional 'output_dir' argument
    parser.add_argument('output_dir', metavar='output_dir', type=str, help='Output directory')
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Create the temporary directory
    temp_dir = os.path.join(os.getcwd(), 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    try:
        if args.source.startswith('https://open.spotify.com/'):

            import spotify_utils

            print(f'Querying Spotify for song name and artist')
            song_name, artist = spotify_utils.get_song_name_and_artist(args.source)
            title = f'{song_name} - {artist}' 
            download_youtube_url = youtube_utils.get_top_search_video_url(title)

        elif args.source.startswith('https://www.youtube.com/'):
            print(f'Querying YouTube for video name')
            download_youtube_url = args.source
            title = youtube_utils.get_video_title(args.source)

        else:
            raise ValueError(f'Did not recognize source {args.source} as Spotify or YouTube')


        # Call the download_youtube_audio function
        filename = sanitize(f'{title}.wav')
        print(f'Downloading {filename}')
        youtube_utils.download_youtube_audio(download_youtube_url, filename, args.output_dir, temp_dir)

    finally:
        # Remove the temporary directory
        os.rmdir(temp_dir)

if __name__ == '__main__':
    main()
