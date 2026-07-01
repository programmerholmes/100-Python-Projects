from bs4 import BeautifulSoup
import requests
import spotipy
from soupsieve import select_one
from spotipy.oauth2 import SpotifyOAuth  # for private user-specific data
from spotipy.oauth2 import SpotifyClientCredentials  # for public data
import pprint

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

spotify_url = "https://www.billboard.com/charts/hot-100/"

CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                        redirect_uri="http://127.0.0.1:9090",
                                         client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                        show_dialog=True, cache_path="token.txt"))

user_id = sp.current_user()["id"]

response = requests.get(url=spotify_url + date)
spotify_webpage = response.text

soup = BeautifulSoup(spotify_webpage, "html.parser")

titles = soup.find_all(name="h3", id="title-of-a-story", class_= "c-title a-font-basic u-letter-spacing-0010 u-max-width-397 lrv-u-font-size-16 lrv-u-font-size-14@mobile-max u-line-height-22px u-word-spacing-0063 u-line-height-normal@mobile-max a-truncate-ellipsis-2line lrv-u-margin-b-025 lrv-u-margin-b-00@mobile-max")

# Both the versions work the same, you can use find_all or select to achieve the same results.
# titles = soup.select(selector="li ul li h3")

song_list = []
for title in titles:
    song= title.getText()
    song_list.append(song.strip())

print(song_list)


song_uris = []
year = date.split("-")[0]
for song in song_list:
    result = sp.search(q=f"track: {song} year: {year}", type='track')
    pprint.pp(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris)