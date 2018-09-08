#!/usr/bin/env python3
import argparse
import json
import logging
import os

import lyricsgenius as lg

from credentials import client_id, client_secret, client_access_token


def set_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--artists_names', help='list of strings: "Eric Clapton" "Bob Dylan" ...',
        nargs='+', type=str, required=True)
    parser.add_argument('--verbose', help="verbosity", default=True, type=bool)
    parser.add_argument('--overwrite', help="overwrite .json if exists", default=False, type=bool)
    args, unknown = parser.parse_known_args()
    return args


def set_client(client_access_token):
    client = lg.Genius(client_access_token)
    return client


def get_artists_songs(genius_client, artists_names, verbose=False, overwrite=False):
    for artists_name in artists_names:
        artists_name = ''.join(artists_name)
        filename = './data/lyrics_by_artist/{}'.format(artists_name.replace(' ', ''))
        if os.path.exists(filename+'.json') and not overwrite:
            print('{}.json already exists.  Overwrite set to False.  Skipping artist {}'.format(
                filename, artists_name))
        else:
            artist_object = genius_client.search_artist(artists_name, max_songs=None, verbose=verbose)
            if not os.path.isdir('./data'): os.mkdir('./data')
            if not os.path.isdir('./data/lyrics_by_artist'): os.mkdir('./data/lyrics_by_artist')
            genius_client.save_artists(artist_object, filename=filename, overwrite=overwrite)


def remove_headers(artists_names):
    for artist_name in artists_names:

        # open file
        filename = './data/lyrics_by_artist/{}.json'.format(artist_name.replace(' ',''))
        with open(filename) as f:
            data = json.load(f)

        # remove headers
        for i in range(0, len(data['artists'][0]['songs'])):
            for header in ['Chorus', 'Refrain', 'Verse', 'Bridge', 'Break', 'Intro', 'Outro', '[', ']', ':',
                           '(', ')', 'x2', 'x3', 'x4', 'x5']:
                data['artists'][0]['songs'][i]['lyrics'] = data['artists'][0]['songs'][i]['lyrics'].replace(header, '')

        # save file
        with open(filename, 'w') as f:
            json.dump(data, f)


def main():
    logger = set_logger()
    args = parse_args()
    client = set_client(client_access_token)
    get_artists_songs(client, args.artists_names, verbose=args.verbose, overwrite=args.overwrite)
    remove_headers(args.artists_names)

if __name__ == '__main__':
    main()
