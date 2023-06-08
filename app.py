import os
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

STORED_PLAYLISTS = {
        "Sal + Preston": "https://open.spotify.com/playlist/2w9RXal3mjqEgvNjRA13qp?si=f1dcb6beb0d34911",
        "Other": None
    }


# Set up Spotify API credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



#def get_playlist_name(url):
#    playlist_id = url.split('/')[-1]
#    playlist = sp.playlist(playlist_id)
#    return playlist['name']

def string_to_camelot(key_string):
    camelot_wheel = {
        "C Major": "8B",
        "G Major": "9B",
        "D Major": "10B",
        "A Major": "11B",
        "E Major": "12B",
        "B Major": "1B",
        "F# / Gb Major": "2B",
        "C# / Db Major": "3B",
        "G# / Ab Major": "4B",
        "D# / Eb Major": "5B",
        "A# / Bb Major": "6B",
        "F Major": "7B",

        "C Minor": "5A",
        "G Minor": "6A",
        "D Minor": "7A",
        "A Minor": "8A",
        "E Minor": "9A",
        "B Minor": "10A",
        "F# / Gb Minor": "11A",
        "C# / Db Minor": "12A",
        "G# / Ab Minor": "1A",
        "D# / Eb Minor": "2A",
        "A# / Bb Minor": "3A",
        "F Minor": "4A",

        
    }
    return camelot_wheel.get(key_string, "Unknown")

# Function to convert pitch class and mode to string representation
def pitch_class_mode_to_string(pitch_class, mode):
    pitch_classes = ["C", "C# / Db",  "D", "D# / Eb", "E", "F", "F# / Gb", "G", "G# / Ab", "A", "A# / Bb", "B"]
    modes = ["Minor", "Major"]
    return pitch_classes[pitch_class] + " " + modes[mode]


def get_camelot_number(camelot_key):
    try:
        return int(camelot_key[:-1])
    except: 
        return "Unknown"


# Function to convert milliseconds to MM:SS format
def ms_to_minutes_seconds(duration_ms):
    duration = datetime.timedelta(milliseconds=duration_ms)
    minutes = duration.seconds // 60
    seconds = duration.seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def get_playlist_tracks(playlist_url):
    # Get playlist ID from the playlist URL
    playlist_id = playlist_url.split("/")[-1].split("?")[0]

    # Retrieve playlist tracks
#    tracks = sp.playlist_tracks(playlist_id)
#    print(tracks)

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
        key_string = pitch_class_mode_to_string(pitch_class, mode)
        camelot_key = string_to_camelot(key_string)

        # Convert track duration to MM:SS format
        duration_ms = track["duration_ms"]
        track_length = ms_to_minutes_seconds(duration_ms)

        # Collect desired information in a dictionary
        track_data = {
            "Track Name": track_name,
            "Artist": artist,
            "Track Length": track_length,
            "Key": key_string,
            "BPM": bpm,
            "Camelot Key": camelot_key,
            "Camelot Number": get_camelot_number(camelot_key),
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

    # Create a DataFrame from the collected track data
    df = pd.DataFrame(data)

    return df


def main():
    st.set_page_config(layout="wide", page_title="Conch Shell", page_icon=':shell:')

    st.title('Conch Shell - A Spotify Playlist Analyzer')

    # Input playlist URL
    playlist_selected = st.selectbox('Select a playlist', STORED_PLAYLISTS.keys())

    if playlist_selected == 'Other':
        playlist_url = st.text_input("Enter Spotify Playlist URL")
    else:
        playlist_url = STORED_PLAYLISTS[playlist_selected]


    if st.button("Analyze"):
        if playlist_url:
            try:
                playlist_df = get_playlist_tracks(playlist_url)
                playlist_df.sort_values(by=["Camelot Number", 'BPM'], inplace=True)
#                playlist_name = get_playlist_name(playlist_url)
#                st.header(playlist_name)
                if not playlist_df.empty:
                    # Rename columns to title case
                    playlist_df.rename(columns=lambda x: x.title(), inplace=True)

                    # style the df
                    min_value = 1
                    max_value = 12
                    color_map = plt.cm.get_cmap('twilight', max_value - min_value + 1)

                   # Function to apply color to rows and adjust font color based on background color
                    def apply_color_and_font_color(row):
                        value = row['Camelot Number']
                        if value != 'Unknown':
                            color_index = int(value) - min_value
                        else:
                            color_index = 0
                        color = mcolors.to_hex(color_map(color_index))
                        font_color = 'white' if np.mean(mcolors.to_rgb(color)) < 0.5 else 'black'
                        return [f'background-color: {color}; color: {font_color}'] * len(row)
 

                    # Checkbox to toggle row coloring
#                    show_colors = st.checkbox('Show Row Colors')
                    show_colors = True

                    # Apply color and font color to the DataFrame rows if checkbox is selected
                    styled_df = playlist_df.style.apply(apply_color_and_font_color, axis=1) if show_colors else playlist_df.style

                    # Render the styled DataFrame in Streamlit
                    st.dataframe(styled_df)



                else:
                    st.info("No tracks found in the playlist.")
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
        else:
            st.warning("Please enter a Spotify Playlist URL.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
