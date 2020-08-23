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

from albums import replace_albums
from tracks import replace_tracks

def connect_to_spotify(secrets_file_stream):
    secrets = json.load(secrets_file_stream)
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SPOTIFY_SCOPE,
                        client_id=secrets[SECRETS_CLIENT_ID],
                        client_secret=secrets[SECRETS_SECRET_ID],
                        redirect_uri=secrets[SECRETS_REDIRECT_URI],
                        cache_path=CACHE_PATH))

    return spotify

def main():
    global INTERACTIVE

    parser = ArgumentParser(description='Fix Spotify Deprecated Songs')
    parser.add_argument('secrets_file', nargs='?', type=FileType('r'), default='secrets.json')
    parser.add_argument('--not-interactive', action='store_true', help='Run in not interactive mode')

    args = parser.parse_args()

    interactive = not args.not_interactive

    spotify = connect_to_spotify(args.secrets_file)
    replace_albums(spotify, interactive)
    replace_tracks(spotify, interactive)



if __name__ == '__main__':
    main()