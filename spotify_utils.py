import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime

import music_theory


# Set up Spotify API credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_song_name_and_artist(link):
    # Extract the track ID from the shareable link
    track_id = link.split('/')[-1].split('?')[0]

    # Retrieve track information
    track = sp.track(track_id)
    song_name = track['name']
    artist_name = track['artists'][0]['name']

    return song_name, artist_name



def get_playlist_tracks(playlist_url):
    # Get playlist ID from the playlist URL
    playlist_id = playlist_url.split("/")[-1].split("?")[0]

    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    tracks = [track["track"] for track in tracks]

    # Process each track in the playlist
    data = []
    for track in tracks:

        # Extract desired information for each track
        track_name = track["name"]
        artist = track["artists"][0]["name"]
        track_id = track["id"]

        # Get audio features for the track
        audio_features = sp.audio_features([track_id])[0]
        key = audio_features["key"]
        bpm = audio_features["tempo"]

        # Convert key to Camelot wheel representation
        pitch_class = key % 12
        mode = audio_features["mode"]
        key_string = music_theory.pitch_class_mode_to_string(pitch_class, mode)
        camelot_key = music_theory.string_to_camelot(key_string)

        # Convert track duration to MM:SS format
        duration_ms = track["duration_ms"]
        track_length = ms_to_minutes_seconds(duration_ms)

        track_data = {
            "Track Name": track_name,
            "Artist": artist,
            "Track Length": track_length,
            "Key": key_string,
            "BPM": bpm,
            "Camelot Key": camelot_key,
            "Camelot Number": music_theory.get_camelot_number(camelot_key),
            "Time Signature": audio_features["time_signature"],
            "Danceability": audio_features["danceability"],
            "Energy": audio_features["energy"],
            "Loudness": audio_features["loudness"],
            "Speechiness": audio_features["speechiness"],
            "Acousticness": audio_features["acousticness"],
            "Instrumentalness": audio_features["instrumentalness"],
            "Liveness": audio_features["liveness"],
            "Valence": audio_features["valence"],
        }
        data.append(track_data)

    return data



# Function to convert milliseconds to MM:SS format
def ms_to_minutes_seconds(duration_ms):
    duration = datetime.timedelta(milliseconds=duration_ms)
    minutes = duration.seconds // 60
    seconds = duration.seconds % 60
    return f"{minutes:02d}:{seconds:02d}"