#!/usr/bin/env python3.8

import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from argparse import ArgumentParser, FileType

SPOTIFY_SCOPE = 'user-library-read user-library-modify playlist-modify-private playlist-modify-public'
SECRETS_CLIENT_ID = 'spotify-api-clientid'
SECRETS_SECRET_ID = 'spotify-api-secret'
SECRETS_REDIRECT_URI = 'spotify-api-redirect_uri'
CACHE_PATH = 'cache_file'

#tracks_filtered = filter(lambda t: len(t['track']['available_markets']) == 0, tracks)
#tracks_info = playlist['tracks']
#tracks = tracks_info['items']
#tracks[1]['track']['available_markets']

#artists_names = ' '.join(map(lambda a: a['name'], filtered_track['track']['artists']))
# result = spotify.search(q=filtered_track['track']['name'] + ' artist:' + artists_names, type='track')
# result['tracks'] : list


# result = spotify.current_user_playlists()
# result = spotify.current_user_saved_albums()
# spotify.current_user_saved_tracks()

def string_artists(artists_list):
    return ' '.join(map(lambda a: a['name'], artists_list))

def find_album_replacment(spotify, album):
    artists_names = string_artists(album['artists'])
    # result = spotify.search(q=album['name'] + ' artist:' + artists_names, type='album')
    result = spotify.search(q=album['name'], type='album')

    try:
        return result['albums']['items'][0]
    except:
        return None


def get_albums_replacments(spotify):
    is_deprecated = lambda p: len(p['album']['available_markets']) == 0

    result = spotify.current_user_saved_albums()
    deprecated_albums = list(filter(is_deprecated, result['items']))

    while result['next']:
        result = spotify.next(result)
        deprecated_albums.extend(list(filter(is_deprecated, result['items'])))

    deprecated_albums = [d['album'] for d in deprecated_albums]

    return [(d, find_album_replacment(spotify, d)) for d in deprecated_albums]


def connect_to_spotify(secrets_file_stream):
    secrets = json.load(secrets_file_stream)
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SPOTIFY_SCOPE,
                        client_id=secrets[SECRETS_CLIENT_ID],
                        client_secret=secrets[SECRETS_SECRET_ID],
                        redirect_uri=secrets[SECRETS_REDIRECT_URI],
                        cache_path=CACHE_PATH))

    return spotify

def pretify_album(album):
    return f"{string_artists(album['artists'])} - {album['name']} ({album['external_urls']['spotify']})"

def question(string_question):
    string_question = string_question + '? [Y/n] '

    answer = input(string_question)
    if answer.lower() == 'n':
        return False

    return True

def should_replace_album(album_tuple):
    return question(f"Replace \"{pretify_album(album_tuple[0])}\" with \"{pretify_album(album_tuple[1])}\"")

def replace_albums(spotify, interactive):
    albums = get_albums_replacments(spotify)

    if len(albums) == 0:
        return

    albums_not_found = list(filter(lambda a: a[1] == None, albums))
    albums = filter(lambda a: a[1] != None, albums)

    if len(albums_not_found) > 0:
        print('Albums not found replacments for:\n' + '\n'.join(map(lambda a: pretify_album(a[0]), albums_not_found)) + '\n')


    if interactive:
        albums = list(filter(should_replace_album, albums))

    albums_ids = [(a[0]['id'], a[1]['id']) for a in albums]

    albums_to_delete, albums_to_add = zip(*albums_ids)

    spotify.current_user_saved_albums_delete(list(albums_to_delete))
    spotify.current_user_saved_albums_add(list(albums_to_add))

def main():
    global INTERACTIVE

    parser = ArgumentParser(description='Fix Spotify Deprecated Songs')
    parser.add_argument('secrets_file', nargs='?', type=FileType('r'), default='secrets.json')
    parser.add_argument('--not-interactive', action='store_true', help='Run in not interactive mode')

    args = parser.parse_args()

    interactive = not args.not_interactive

    spotify = connect_to_spotify(args.secrets_file)
    replace_albums(spotify, interactive)



if __name__ == '__main__':
    main()