#!/usr/bin/env python
#
# Automated reference extraction from gz package
#
#                        (CC BY-SA 3.0) 2012 Heinrich Hartmann
# 

from __future__ import print_function
from .RE_gz_extract import gz_extract
from .RE_tex_process import extract_bibitems, remove_tex_tags

DEBUG = 0


def RefExtract(gz_path):
    # 1. Extract *.tex and *.bbl files from gz file
    tex_string = gz_extract(gz_path).decode('utf-8', 'ignore')

    # print("Found LaTex Sources: {}".format(len(tex_string)))

    # 2. Extract bib_items
    bibitems = list(extract_bibitems(tex_string))

    bibitems = list(map(remove_tex_tags, bibitems))

    # print(bibitems)

    return bibitems


def parse_arguments():
    global DEBUG

    parser = argparse.ArgumentParser("Extract references from arXiv source *.gz files")
    parser.add_argument('gzfile', help='path to *.gz-file to process', type=str)
    parser.add_argument('-v', '--verbose', help='Give detailed status information', type=int)

    args = parser.parse_args()
    if args.verbose:
        DEBUG = 1

    gz_path = args.gzfile
    if not os.path.isfile(gz_path):
        raise IOError('File not found: ' + gz_path)
    if not gz_path.endswith('.gz'):
        raise IOError('Not a gz-file: ' + gz_path)

    return gz_path


if __name__ == '__main__':
    import os, sys
    import argparse

    import ipdb as pdb

    BREAK = pdb.set_trace

    gz_path = parse_arguments()

    print(RefExtract(gz_path))

    try:
        pass

    except:
        import sys, traceback

        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
