import os
import argparse
from pytube import YouTube

def download_audio(url, output_dir):
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()

        # Set a temporary directory for the downloaded MP4 file
        temp_dir = os.path.join(output_dir, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        temp_path = audio.download(output_path=temp_dir)
        new_file_path = os.path.join(temp_dir, f'{yt.title}.mp4')
        os.rename(temp_path, new_file_path)

        # Convert the MP4 file to WAV using ffmpeg
        new_wav_path = os.path.join(output_dir, f'{yt.title}.wav')
        os.system(f'ffmpeg -i "{new_file_path}" -acodec pcm_s16le -ar 44100 "{new_wav_path}" -y')

        # Clean up the temporary directory and file
        os.remove(new_file_path)
        os.rmdir(temp_dir)

        print(f'Successfully downloaded: {yt.title}.wav')
    except Exception as e:
        print(f'Error downloading audio from {url}: {str(e)}')

def main():
    parser = argparse.ArgumentParser(description='Download audio from YouTube videos as WAV files.')
    parser.add_argument('-i', '--input', default='input.txt', help='Input file containing YouTube URLs (default: input.txt)')
    parser.add_argument('-o', '--output', default='output', help='Output directory to save the WAV files (default: output)')

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    with open(args.input, 'r') as file:
        urls = file.read().splitlines()

    for url in urls:
        download_audio(url, args.output)

    print('Download complete!')

if __name__ == '__main__':
    main()
