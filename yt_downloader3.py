import os
import argparse
from pytube import YouTube
from tqdm import tqdm
import subprocess

def download_audio(url, output_dir, downloaded_files):
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()

        title = escape_title(f'{yt.title}.wav')
        print(f'\nDownloading {title}')

        if title in downloaded_files:
            print(f'\t{title} has already been downloaded. Skipping...')
            return

        # Set a temporary directory for the downloaded MP4 file
        temp_dir = os.path.join(output_dir, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        temp_path = audio.download(output_path=temp_dir)
        new_file_path = os.path.join(temp_dir, title.replace('.wav', '.mp4'))
        os.rename(temp_path, new_file_path)

        # Convert the MP4 file to WAV using ffmpeg
        new_wav_path = os.path.join(output_dir, title)
        subprocess.run(f'ffmpeg -i "{new_file_path}" -acodec pcm_s16le -ar 44100 "{new_wav_path}" -y', capture_output=True)


        # Clean up the temporary directory and file
        os.remove(new_file_path)
        os.rmdir(temp_dir)

        print(f'\tSuccessfully downloaded: {title}')

        # Add the downloaded file name to the set
        downloaded_files.add(title)
    except Exception as e:
        print(f'\tError downloading audio from {url}: {str(e)}')


def escape_title(path):
    return path.replace('|', '_').replace(' ', '_').replace('(', '_').replace(')', '').replace(':', '_')


def main():
    parser = argparse.ArgumentParser(description='Download audio from YouTube videos as WAV files and extract BPM')
    parser.add_argument('-i', '--input', default='input.txt', help='Input file containing YouTube URLs (default: input.txt)')
    parser.add_argument('-o', '--output', default='output', help='Output directory to save the WAV files (default: output)')

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    with open(args.input, 'r') as file:
        urls = file.read().splitlines()

    downloaded_files = set()

    # Check the existing files in the output directory
    for file in os.listdir(args.output):
        if file.endswith('.wav'):
            downloaded_files.add(file)

    for url in tqdm(urls):
        download_audio(url, args.output, downloaded_files)

    print('Download complete!')

if __name__ == '__main__':
    main()
