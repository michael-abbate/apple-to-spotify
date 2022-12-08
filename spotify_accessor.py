from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util
import json
import os
import time
from dotenv import load_dotenv
load_dotenv(".env")

# Spotify Token Access
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
if sp == True:
  print('Successfully logged in...')

# Get Spotify Username
def get_username():
    username = input('Enter Username: ')
    print(username)
    check = input('Is this your username? (Y/N): ')
    if check.upper() == 'Y':
        return username
    else:
        new_username = input('Reenter Username: ')
        return new_username


# Create Spotify playlist ID
def create_playlist(username,playlist_name):

    username = username
    # playlist_name = input('Enter playlist name: ')
    # ^ pass in playlist name within the loop instead of asking for it every time

    # timeout = time.time() + 10   # 5 seconds from now
    # while True:
    #     print('generating token')
    # os.remove(f".cache-{'username'}")   
    token = util.prompt_for_user_token(username=username, scope='playlist-modify-public', client_id=client_id,
                                            client_secret=client_secret,
                                        redirect_uri="http://localhost:8889/callback"
                                        )  
        # if token or time.time() > timeout: 
        #     print('breaking')           
        #     break                               
        
        # raise Exception("cant get token")
    # print(token)
    if token:
        print('got the token...')
        # try:
        sp = spotipy.Spotify(auth=token)

        # print('sp:', sp.me)
        sp.trace = False
        print('creating playlist...')
        
        # try:
        playlists = sp.user_playlist_create(user=username, name=playlist_name)
        # except TimeoutError:
        #     raise TimeoutError("cant create playlist")
        print('returning playlist...')
        return playlists['id']
        # except:
        #     raise Exception('error error error')
    else:
        print('Ran into token error.')


# Get trackID for songs
def get_track_id(song_name1, artist_name1, album_name1):
    print("Adding songs to playlist!")
    id_list = []
    my_array = []
    album_list = []
    song_list = []

    i = 0
    while i < len(song_name1):
        artist = artist_name1[i]
        track = song_name1[i]
        print(artist, track)

        try:
            # print('inside try')
            track_id = sp.search(q='artist:' + artist + ' track:' + track, type='track')
        except:
            raise Exception('couldnt find track')
        for songsID in track_id['tracks']['items']:
            id_list.append(songsID['id'])
            # print(song_name1[i])
            if not id_list:
                album_list.append(album_name1[i])
                song_list.append(song_name1[i])
            else:
                my_array.append(id_list[0])
            id_list = []
            i += 1

        
    return my_array, album_list, song_list


# Get trackID for songs
def get_missing_track_id(missing_albums1, missing_tracks1):
    id_list = []
    my_array = []

    i = 0
    while i < len(missing_tracks1):
        album = missing_albums1[i]
        track = missing_tracks1[i]

        track_id = sp.search(q='album:' + album + ' track:' + track, type='track')
        for songsID in track_id['tracks']['items']:
            id_list.append(songsID['id'])
        if not id_list:
            print('Could not add: ' + missing_tracks1[i])
        else:
            my_array.append(id_list[0])
        id_list = []
        i += 1
    return my_array


# Add songs to Spotify Playlist
def add_songs_to_playlist(username, playlist_id, track_ids):

    username = username
    playlist_id = playlist_id
    track_ids = track_ids

    token = util.prompt_for_user_token(username=username, scope='playlist-modify-public', client_id=client_id,
                                       client_secret=client_secret, redirect_uri="http://localhost:8888/callback")

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        print(track_ids)
        print(len(track_ids))
        for track in track_ids:
            # results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
            try:
                sp.user_playlist_add_tracks(username, playlist_id, [track])
            except:
                print("ERROR:", track)

        print('Finished transferring playlist')
        # return results


def add_song_ids(multiple_tracks1, more_tracks1):
    result = multiple_tracks1 + more_tracks1
    return result