""" This project is about creating top1 00 songs from any year
dating back 20 years ago"""
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
# Using the dotenv module to keep my CLIENT_ID and SECRET
load_dotenv()

# Spotify client ID and secret.
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://example.com"

# Creating two lists to store the names of the artists and the songs.
artists_songs = []
artists = []
# Prompting the user for a preferred year
year_ticket = input("Punch in you time travel (Type in this format: YYYY-MM-DD): ")
# Assigning the Top 100 Billboard url to a constant as a endpoint
# using the f string to insert the users preferred year to url.
TRAVEL_POINT = f"https://www.billboard.com/charts/hot-100/{year_ticket}/#"
response = requests.get(TRAVEL_POINT).text
# Creating a soup with Beautiful Soup with response from the request
content = BeautifulSoup(response, "html.parser")
# scrapping the html to get the artists names and the name of the songs.
the_names = content.find_all(name="span", class_="c-label")
# for name in the_names:
#     the_artist = name.getText()
#     musician = the_artist.strip()
#     if musician == "NEW" or musician == "-":
#         pass
#     elif len(musician) == 1 or len(musician) == 2 or len(musician) == 3:
#         pass
#     else:
#         artists.append(musician)
# The above code commented out is for collecting the names of the artists.

the_songs = content.find_all(name="h3", id="title-of-a-story")
for song in the_songs:
    song_title = song.getText()
    song_name = song_title.strip()
    if song_name == "Songwriter(s):" or song_name == "Producer(s):" or song_name == "Imprint/Promotion Label:":
        pass
    else:
        artists_songs.append(song_name)

the_list = artists_songs[3:-13]


# SPOTIFY AUTHENTICATION SECTION.
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

song_uris = []
year = year_ticket.split("-")[0]
for song in the_list:
    search_result = sp.search(q=f"tracks:{song} year:{year}", type="track")
    # print(search_result)
    try:
        uri = search_result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


new_playlist = sp.user_playlist_create(user=user_id, name=f"{year_ticket} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=new_playlist["id"], items=song_uris)
