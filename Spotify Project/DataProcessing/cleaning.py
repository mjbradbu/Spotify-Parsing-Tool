from api_elements import SpotifyAPI, GeniusAPI, set_artist_and_song, get_top_songs
import os
from dotenv import load_dotenv
from collections import Counter

class parsing:
    def parse_data(artist_name, song_name):
        load_dotenv()
        spotify = SpotifyAPI()
        spotify.get_token()
        artist = spotify.search_for_artist(artist_name)

        user_song_lyrics = []
        genius_token = os.getenv('client_access_token_genius')
        genius_api = GeniusAPI(genius_token)
        user_song_lyrics = genius_api.get_lyrics(song_name, artist_name)
    
        user_song_dict = {}
        top_songs_dict = {}

        if artist:
            artist_id = artist['id']
            songs = spotify.get_songs(artist_id)
            top_songs_dict = {song['name']: [] for song in songs}
            for top_song in top_songs_dict:
                lyrics = genius_api.get_lyrics(top_song, artist_name)
                if lyrics:
                    top_songs_dict[top_song] = lyrics.split()
            user_song_lyrics = user_song_lyrics.split()
            user_song_dict[song_name] = user_song_lyrics
    
        return user_song_dict, top_songs_dict
    def count_word_occurrences(songs_lyrics_list):
        all_song_word_count = []
        for songs_lyrics in songs_lyrics_list:
            song_word_count = {}
            for song, lyrics in songs_lyrics.items():
                word_count = Counter(lyrics)
                song_word_count[song] = word_count
            all_song_word_count.append(song_word_count)
        return all_song_word_count

if __name__ == "__main__":
    load_dotenv()
    spotify = SpotifyAPI()
    artist_name, song_name = set_artist_and_song()

    spotify.get_token()
    artist = spotify.search_for_artist(artist_name)

    if artist:
        user_song_lyrics, top_songs_lyrics = parsing.parse_data(artist_name, song_name)

        #print(f"{song_name} song lyrics: {user_song_lyrics}")
        #print("Top songs and their respective lyrics:")
        #for song, lyrics in top_songs_lyrics.items():
            #print(f"{song}: {lyrics}")

        all_songs = [user_song_lyrics, top_songs_lyrics]

# Combining user and top song lyrics into a list
        all_songs = [user_song_lyrics, top_songs_lyrics]

# Counting word occurrences for user and top song lyrics separately
        all_song_word_count = parsing.count_word_occurrences(all_songs)

# Printing the word count for each song
        for i, songs_word_count in enumerate(all_song_word_count):
            if i == 0:
                print("User Song Word Count:")
            else:
                print("Top Songs Word Count:")

            for song, word_count in songs_word_count.items():
                print(f"{song}:")
                for word, count in word_count.items():
                    print(f"{word}: {count} times")
                print()