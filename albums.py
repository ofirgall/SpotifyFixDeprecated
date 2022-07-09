#!/usr/bin/env python3.8

from utils import question, string_artists

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

def pretify_album(album):
    return f"{string_artists(album['artists'])} - {album['name']} ({album['external_urls']['spotify']})"

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
