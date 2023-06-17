from pytube import Search, YouTube
import os
import sys
import subprocess
from contextlib import contextmanager


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


def download_youtube_audio(url, filename, output_dir, temp_dir):

    if url is None:
        raise ValueError('Expected a url, got None')

    if filename is None:
        raise ValueError('Expected a filename, got None')

    if output_dir is None:
        raise ValueError('Expected an output_dir, got None')

    if temp_dir is None:
        raise ValueError('Expected a temp_dir, got None')

    mp4_path = os.path.join(temp_dir, filename.replace('.wav', '.mp4'))

    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()

        # Download as MP4
        temp_path = audio.download(output_path=temp_dir)
        os.rename(temp_path, mp4_path)

        # Convert the MP4 file to WAV using ffmpeg
        wav_path = os.path.join(output_dir, filename)
        subprocess.run(f'ffmpeg -i "{mp4_path}" -acodec pcm_s16le -ar 44100 "{wav_path}" -y', capture_output=True)

    finally:
        if os.path.exists(mp4_path):
            os.remove(mp4_path)


def get_video_title(url):
    try:
        # Create a YouTube object for the given URL
        yt = YouTube(url)

        # Retrieve the video title
        video_title = yt.title
        return video_title

    except Exception as e:
        raise RuntimeError(f"An error occurred getting the video title for YouTube url {url}: {str(e)}")