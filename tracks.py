#!/usr/bin/env python3.8

from collections import defaultdict

from utils import question, string_artists, add_tracks_to_playlist, remove_tracks_from_playlist, add_tracks_to_saved, remove_tracks_from_saved

TRACK_KEY_ID = 0
TRACK_KEY_NAME = 1
TRACK_KEY_STR = 2

def pretify_track(track):
    return f"{string_artists(track['artists'])} - {track['name']}"

def track_to_dict_key(track):
    return track['id'], track['name'], pretify_track(track)

def is_deprecated_track(track):
    return len(track['track']['available_markets']) == 0 and not track['track']['is_local']

def get_deperacted_from_saved_tracks(spotify):
    result = spotify.current_user_saved_tracks()
    deprecated_tracks = list(filter(is_deprecated_track, result['items']))

    while result['next']:
        result = spotify.next(result)
        deprecated_tracks.extend(list(filter(is_deprecated_track, result['items'])))

    deprecated_tracks = [d['track'] for d in deprecated_tracks]

    return deprecated_tracks

def get_all_playlists(spotify):
    result = spotify.current_user_playlists()
    playlists = result['items']
    my_id = spotify.current_user()['id']

    while result['next']:
        result = spotify.next(result)
        playlists.extend(result['items'])

    playlists = list(filter(lambda p: p['id'] == my_id, playlists))
    return playlists

def get_deperacted_tracks_from_playlist(spotify, playlist):
    playlist = spotify.user_playlist('spotify', playlist['id'])

    result = playlist['tracks']
    deprecated_tracks = list(filter(is_deprecated_track, result['items']))

    while result['next']:
        result = spotify.next(result)
        deprecated_tracks.extend(list(filter(is_deprecated_track, result['items'])))

    deprecated_tracks = [d['track'] for d in deprecated_tracks]

    return deprecated_tracks

def get_deperacted_tracks_from_playlists(spotify):
    playlists = get_all_playlists(spotify)
    tracks_dict = defaultdict(list)

    for playlist in playlists:
        tracks = get_deperacted_tracks_from_playlist(spotify, playlist)
        for track in tracks:
            tracks_dict[track_to_dict_key(track)].append(playlist)

    return tracks_dict

def find_track_replacment(spotify, track):
    result = spotify.search(q=track[TRACK_KEY_NAME], type='track')

    try:
        return result['tracks']['items'][0]
    except:
        return None

def should_replace_track(track_tuple):
    return question(f"[SAVED] Replace \"{track_tuple[0][TRACK_KEY_STR]}\" with \"{pretify_track(track_tuple[1])}\"")

def replace_saved_tracks(spotify, saved_tracks, interactive):
    saved_tracks = [(d, find_track_replacment(spotify, d)) for d in saved_tracks]

    if len(saved_tracks) == 0:
        return

    saved_tracks_not_found = list(filter(lambda t: t[1] == None, saved_tracks))
    saved_tracks = filter(lambda t: t[1] != None, saved_tracks)

    if len(saved_tracks_not_found) > 0:
        print('Tracks not found replacments for:\n' + '\n'.join(map(lambda t: t[0][TRACK_KEY_STR], saved_tracks_not_found)) + '\n')

    if interactive:
        saved_tracks = list(filter(should_replace_track, saved_tracks))

    track_ids = [(t[0][TRACK_KEY_ID], t[1]['id']) for t in saved_tracks]

    if len(track_ids) == 0:
        return

    tracks_to_delete, tracks_to_add = zip(*track_ids)

    remove_tracks_from_saved(spotify, list(tracks_to_delete))
    add_tracks_to_saved(spotify, list(tracks_to_add))

def should_replace_playlist_track(track_tuple):
    saved = ''

    if 'Saved' in track_tuple[2]:
        saved = '[SAVED]'

    appears = ', '.join(map(lambda p: '"' + p['name'] + '"', track_tuple[2]))

    return question(f"{saved} Replace \"{track_tuple[0][TRACK_KEY_STR]}\" with \"{pretify_track(track_tuple[1])}\", Appears on: {appears}")

def replace_in_playlist(spotify, playlist_id, tracks):
    if len(tracks[0]) == 0:
        return

    tracks_to_delete, tracks_to_add = zip(*tracks)

    remove_tracks_from_playlist(spotify, playlist_id, tracks_to_delete)
    add_tracks_to_playlist(spotify, playlist_id, tracks_to_add)


def replace_playlists_tracks(spotify, tracks_dict, interactive):
    tracks = [(t, find_track_replacment(spotify, t), p) for t, p in tracks_dict.items()]

    if len(tracks) == 0:
        return

    tracks_not_found = list(filter(lambda t: t[1] == None, tracks))
    tracks = filter(lambda t: t[1] != None, tracks)

    if len(tracks_not_found) > 0:
        print('Tracks not found replacments for:\n' + '\n'.join(map(lambda t: t[0][TRACK_KEY_STR], tracks_not_found)) + '\n')

    if interactive:
        tracks = list(filter(should_replace_playlist_track, tracks))

    playlists_to_tracks_dict = defaultdict(list)
    saved_tracks = []

    for t in tracks:
        playlists = t[2]
        for p in playlists:
            if p == 'Saved':
                saved_tracks.append((t[0][TRACK_KEY_ID], t[1]['id']))
            else:
                playlists_to_tracks_dict[p['id']].append((t[0][TRACK_KEY_ID], t[1]['id']))

    if len(saved_tracks) > 0:
        tracks_to_delete, tracks_to_add = zip(*saved_tracks)

        remove_tracks_from_saved(spotify, list(tracks_to_delete))
        add_tracks_to_saved(spotify, list(tracks_to_add))

    for p_id, tracks in playlists_to_tracks_dict.items():
        replace_in_playlist(spotify, p_id, tracks)


def replace_tracks(spotify, interactive):
    deprecated_saved_tracks = get_deperacted_from_saved_tracks(spotify)
    deprecated_saved_tracks = [track_to_dict_key(t) for t in deprecated_saved_tracks]

    deperacted_tracks_from_playlists = get_deperacted_tracks_from_playlists(spotify)

    for track, playlists in deperacted_tracks_from_playlists.items():
        if track in deprecated_saved_tracks:
            playlists.insert(0, 'Saved')
            deprecated_saved_tracks.remove(track)

    replace_saved_tracks(spotify, deprecated_saved_tracks, interactive)
    replace_playlists_tracks(spotify, deperacted_tracks_from_playlists, interactive)







