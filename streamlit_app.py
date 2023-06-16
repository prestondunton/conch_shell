import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

import spotify_utils

STORED_PLAYLISTS = {
        "Sal + Preston": "https://open.spotify.com/playlist/2w9RXal3mjqEgvNjRA13qp?si=f1dcb6beb0d34911",
        "Season Finale": "https://open.spotify.com/playlist/2YlweeE0qha0ITfvpeNwSr?si=4e113a106fce4950",
        "June Mix": "https://open.spotify.com/playlist/7pyjrgdqLKeLW3GiVfgNyZ?si=44c8809f7f0241be",
        "Other": None
    }


def style_playlist_df(playlist_df):
    # style the df
    min_value = 1
    max_value = 12
    color_map = plt.cm.get_cmap('twilight', max_value - min_value + 1)

    def apply_color_and_font_color(row):
        value = row['Camelot Number']
        if value != 'Unknown':
            color_index = int(value) - min_value
        else:
            color_index = 0
        color = mcolors.to_hex(color_map(color_index))
        font_color = 'white' if np.mean(mcolors.to_rgb(color)) < 0.5 else 'black'
        return [f'background-color: {color}; color: {font_color}'] * len(row)


    styled_df = playlist_df.style.apply(apply_color_and_font_color, axis=1)
    return styled_df


def main():
    st.set_page_config(layout="wide", page_title="Conch Shell", page_icon=':shell:')

    st.title('Conch Shell - A Spotify Playlist Analyzer')

    playlist_selected = st.selectbox('Select a playlist', STORED_PLAYLISTS.keys())

    if playlist_selected == 'Other':
        playlist_url = st.text_input("Enter Spotify Playlist URL")
    else:
        playlist_url = STORED_PLAYLISTS[playlist_selected]


    if st.button("Analyze"):
        if playlist_url:
            try:

                tracks = spotify_utils.get_playlist_tracks(playlist_url) 
                playlist_df = pd.DataFrame(tracks)
                playlist_df.sort_values(by=["Camelot Number", 'BPM'], inplace=True)

                if not playlist_df.empty:
                    # Rename columns to title case
                    playlist_df.rename(columns=lambda x: x.title(), inplace=True)

                    styled_df = style_playlist_df(playlist_df)

                    # Render the styled DataFrame in Streamlit
                    st.dataframe(styled_df)

                    st.download_button(
                        "Press to Download",
                        playlist_df.to_csv(index=True).encode('utf-8'),
                        "conch_shell_analysis.csv",
                        "text/csv",
                        key='download-csv'
                        )

                else:
                    st.info("No tracks found in the playlist.")
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
        else:
            st.warning("Please enter a Spotify Playlist URL.")


if __name__ == "__main__":
    main()
