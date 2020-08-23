#!/usr/bin/env python3.8

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

def get_saved_tracks_replacments(spotify):
    import IPython
    IPython.embed()


def replace_tracks(spotify, interactive):
    saved_tracks = get_saved_tracks_replacments(spotify)