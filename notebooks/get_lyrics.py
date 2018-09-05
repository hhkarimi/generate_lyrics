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


def main():
    logger = set_logger()
    args = parse_args()
    client = set_client(client_access_token)
    get_artists_songs(client, args.artists_names, verbose=args.verbose, overwrite=args.overwrite)


if __name__ == '__main__':
    main()
