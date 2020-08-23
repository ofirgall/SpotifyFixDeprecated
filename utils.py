#!/usr/bin/env python3.8

ADD_TRACKS_PER_REQUEST_LIMIT = 100
REMOVE_TRACKS_PER_REQUEST_LIMIT = 100 # No idea if its the limit but i dont want to test it

SAVED_ADD_TRACKS_PER_REQUEST_LIMIT = 50
SAVED_REMOVE_TRACKS_PER_REQUEST_LIMIT = 50

def to_chunks(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def add_tracks_to_playlist(spotify, playlist, tracks_to_add):
    tracks_to_add_chunks = to_chunks(tracks_to_add, ADD_TRACKS_PER_REQUEST_LIMIT)

    for i, chunk in enumerate(tracks_to_add_chunks):
        spotify.user_playlist_add_tracks('spotify', playlist, chunk)
        print("Tracks Added Chunk %u/%u" %  (i, len(tracks_to_add_chunks)))

def remove_tracks_from_playlist(spotify, playlist, tracks_to_remove):
    tracks_to_remove = to_chunks(tracks_to_remove, REMOVE_TRACKS_PER_REQUEST_LIMIT)

    for i, chunk in enumerate(tracks_to_remove):
        spotify.user_playlist_remove_all_occurrences_of_tracks('spotify', playlist, chunk)
        print("Tracks Removed Chunk %u/%u" % (i, len(tracks_to_remove)))

def add_tracks_to_saved(spotify, tracks_to_add):
    tracks_to_add_chunks = to_chunks(tracks_to_add, SAVED_ADD_TRACKS_PER_REQUEST_LIMIT)

    for i, chunk in enumerate(tracks_to_add_chunks):
        spotify.current_user_saved_tracks_add(chunk)
        print("Tracks Added Chunk %u/%u" %  (i, len(tracks_to_add_chunks)))

def remove_tracks_from_saved(spotify, tracks_to_remove):
    tracks_to_remove = to_chunks(tracks_to_remove, SAVED_REMOVE_TRACKS_PER_REQUEST_LIMIT)

    for i, chunk in enumerate(tracks_to_remove):
        spotify.current_user_saved_tracks_delete(chunk)
        print("Tracks Removed Chunk %u/%u" % (i, len(tracks_to_remove)))

def string_artists(artists_list):
    return ' '.join(map(lambda a: a['name'], artists_list))

def question(string_question):
    string_question = string_question + '? [Y/n] '

    answer = input(string_question)
    if answer.lower() == 'n':
        return False

    return True