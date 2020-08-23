#!/usr/bin/env python3.8

def string_artists(artists_list):
    return ' '.join(map(lambda a: a['name'], artists_list))

def question(string_question):
    string_question = string_question + '? [Y/n] '

    answer = input(string_question)
    if answer.lower() == 'n':
        return False

    return True