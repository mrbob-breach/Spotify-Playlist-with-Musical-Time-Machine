from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
import os


"""Get Billboard top 100 songs into a list"""
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
year = date[:4]
URL = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
song_list = [song.getText().strip() for song in soup.select("li ul li h3")]


"""Use Spotipy to get the 100 URI's for the Billboard top 100 songs"""
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT = "http://example.com"
SCOPE = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT,
                                               scope=SCOPE))

song_uris = []
for song in song_list:
    try:
        song_searched = sp.search(
        q=f"track:{song} year:{year}",
        type='track',
        limit=1,
        )
        song_uris.append(song_searched['tracks']['items'][0]['uri'])
    except IndexError:
        pass


"""Create a new playlist of those songs"""
user_id = sp.current_user()['id']

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=False,
    collaborative=False,
    description=''
)


sp.playlist_add_items(
    playlist_id=playlist['id'],
    items=song_uris,
    position=None
)



