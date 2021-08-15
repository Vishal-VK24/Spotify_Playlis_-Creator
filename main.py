from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/",
        client_id="bb618edb4fd04f5bac46743b751e7730",
        client_secret="ef34696c4dcf49fda337a4a602a06c8f",
        show_dialog=True,
        cache_path="token.txt"
    )
)
def Playlist_create():
    date = input("enter the date to search top songs")
    response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
    playlist = sp.user_playlist_create(user=sp.current_user()['id'], name=f"{date} billboard top songs", public=False)
    track_list = []
    for i in titles:
        try:
            uri = sp.search(q=f"{i.getText()}", type="track")["tracks"]["items"][0]["uri"]
            track_list.append(uri)
        except:
            pass
    sp.playlist_add_items(playlist_id=playlist['id'], items=track_list)


Playlist_create()