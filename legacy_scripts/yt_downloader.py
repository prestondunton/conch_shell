import argparse
from pytube import YouTube
from pydub import AudioSegment
import os


def main(args):

    with open(args.url_file) as f:
        yt_url_list = f.readlines()

        for url in yt_url_list:

            audio = YouTube(url).streams.get_audio_only()
            audio_download = audio.download(output_path=args.download_directory)

            base, ext = os.path.splitext(audio_download)
            mp3_file_path = base + '.mp3'

            if os.path.basename(mp3_file_path) not in os.listdir(args.download_directory):
                os.rename(audio_download, mp3_file_path)
                print(f'Downloaded {mp3_file_path}')
            else:
                print(f'{os.path.basename(mp3_file_path)} already in {args.download_directory}.  Deleting downloaded mp4.')
                os.remove(audio_download)

            # convert mp3 to wav
            base, ext = os.path.splitext(mp3_file_path)
            wav_file_path = base + '.wav'

            print(f'Converting {mp3_file_path} to {wav_file_path}')
            sound = AudioSegment.from_mp3(mp3_file_path)
            sound.export(wav_file_path, format="wav")



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='File Downloader')
    parser.add_argument('url_file', help='Path to the file containing URLs. One per line')
    parser.add_argument('download_directory', help='Output directory to save the downloaded files')
    args = parser.parse_args()

    main(args)