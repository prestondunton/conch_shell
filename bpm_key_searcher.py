import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify API credentials
client_id = "d13135fdb7da489e9d26b5c13f0eb83e"
client_secret = "b7bd8ae9985f4600b963b03649628e00"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def query_audio_features(song_name, artist_name=None):
    # Search for the track
    query = f"track:{song_name}"
    if artist_name is not None:
        query += f' artist:{artist_name}'

    results = sp.search(q=query, type="track", limit=1)
    items = results["tracks"]["items"]

    if len(items) > 0:
        track = items[0]
        track_name = track["name"]
        artist = track["artists"][0]["name"]
        track_id = track["id"]

        # Get audio features for the track
        audio_features = sp.audio_features([track_id])[0]
        key = audio_features["key"]
        tempo = audio_features["tempo"]

        print(f"Track: {track_name}")
        print(f"Artist: {artist}")
        print(f"Key: {key}")
        print(f"Tempo: {tempo} BPM")

        return track_name
    else:
        print("Track not found.")


def main():
    # Set the song you want to search
    song_name = "Midnight City"
    artist_name = "M83"








def pitch_class_mode_to_string(pitch_class, mode):
    pitch_classes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    modes = ["Minor", "Major"]
    return pitch_classes[pitch_class] + " " + modes[mode]

def string_to_camelot(key_string):
    camelot_wheel = {
        "C Major": "8B",
        "G Major": "3B",
        "D Major": "10B",
        "A Major": "5B",
        "E Major": "12B",
        "B Major": "7B",
        "F# Major": "2B",
        "Db Major": "9B",
        "Ab Major": "4B",
        "Eb Major": "11B",
        "Bb Major": "6B",
        "F Major": "1B",
        "A Minor": "8A",
        "E Minor": "3A",
        "B Minor": "10A",
        "F# Minor": "5A",
        "Db Minor": "12A",
        "Ab Minor": "7A",
        "Eb Minor": "2A",
        "Bb Minor": "9A",
        "F Minor": "4A",
        "C Minor": "11A",
        "G Minor": "6A",
        "D Minor": "1A"
    }
    return camelot_wheel.get(key_string, "Unknown")

# Example usage:
pitch_class = 7  # G
mode = 1  # Major
key_string = pitch_class_mode_to_string(pitch_class, mode)
print(key_string)  # Output: G Major

camelot_code = string_to_camelot(key_string)
print(camelot_code)  # Output: 3B

if __name__ == '__main__':
    main()