import applemusic_xml_parser as axp
import spotify_accessor as sa
import os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
load_dotenv(".env")

playlist_path = "/Users/mabbate/michael-abbate/apple-to-spotify/playlists"
playlist_archive_path = "/Users/mabbate/michael-abbate/apple-to-spotify/playlist_archive"

my_username = os.getenv('USERNAME')

playlist_dict = {
    "calm.xml":"Calm",
    "jakescott.xml":"The Jake Scott Paper Co.",
    "mayer.xml":"Coach Mayer",
    "sunday.xml":"Sunday Morning",
    "gym.xml": "gym"
}

for playlist_xml in os.scandir(playlist_path):
    print("Retreiving:", playlist_xml.name)
    playlist = playlist_xml
    tree = ET.parse(playlist)
    root = tree.getroot()
    song_name = axp.get_song_name(root)
    final_song_name = axp.remove_feat_from_song(song_name)
    artist_name = axp.get_artist_name(root)
    album_name = axp.get_album_name(root)
    # final_album_name = axp.remove_feat_from_album(album_name)

    playlist_name = playlist_dict[playlist_xml.name]
    print("Name of Spotify playlist:", playlist_name)
    
    # print("preparing0")

    my_playlist_id = sa.create_playlist(my_username,playlist_name)
    # print("preparing")

    multiple_tracks, missing_albums, missing_tracks = sa.get_track_id(final_song_name, artist_name, album_name)
    
    more_tracks = sa.get_missing_track_id(missing_albums, missing_tracks)
    all_songs = sa.add_song_ids(multiple_tracks, more_tracks)

    # print(all_songs)
    if len(all_songs) <= 100: 
        # print("songs:",all_songs)
        sa.add_songs_to_playlist(my_username, my_playlist_id, all_songs)
    else:
        num_total_songs = len(all_songs)
        print("Total Number of Songs to add:", num_total_songs)
        start, end = 1, 100
        buckets_needed = (len(all_songs) // 100) + 1
        print(f"Need to upload songs with {buckets_needed} different requests...")
        for i in range(1,buckets_needed+1):
            print(f"Adding songs {start} to {end}...")
            # all_songs[0:100] will return IDs 0 to 99 which is 100 IDs total.
            songs_to_add = all_songs[start-1:end]            
            sa.add_songs_to_playlist(my_username, my_playlist_id, songs_to_add)
            start+=100
            end+=100
            if end>num_total_songs:
                end = num_total_songs
