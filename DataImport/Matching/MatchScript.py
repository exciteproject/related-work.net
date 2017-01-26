#!/usr/bin/env python
#
# Executable version of Match.py
#

from Matching.Match import Match
from multiprocessing import Pool
import argparse, sys, os, re
from store_refs_pg import store as store_refs
from store_matches_pg import store as store_matches

sys.path.append('../tools')
#from shared import yield_lines_from_dir, yield_lines_from_file
#solve this

DEBUG = 0
LOG = sys.stderr


def main():
    global DEBUG
    # 
    # Parse commandline arguments
    #
    
    #ref_file = "../DATA/ALL_REF.txt"
    #match_file = "../DATA/ALL_MATCH.txt"

    # Setup Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('ref_table', nargs='?', help = 'path to text file/text dir containing references', type=str, default='refs')
    parser.add_argument('match_table', nargs='?', help = 'write output here', type=str, default='matches')
    parser.add_argument('--stream', help = 'read input from stdin', action="store_true", default=False)
    parser.add_argument('-m', help = 'number of parallel processes', type=int, default=1)
    parser.add_argument('-v','--verbose', help = 'Give detailed status information',type=int)

    args = parser.parse_args()
    if args.verbose:
        DEBUG = 1

    ref_table = args.ref_table
    match_table = args.match_table
    num_proc = args.m
    print(
        """\n\nReading reference strings from {0}.\nMatching using {1} parallel processes.\nWriting to {1}.\n""".format(
            ref_table, match_table, num_proc))

    #
    # Execute program
    #

    # Get input line iterator from different sources
    # if args.stream:
    #     in_iter = sys.stdin
    # elif os.path.isfile(ref_file):
    #     in_iter = yield_lines_from_file(ref_file)
    # elif os.path.isdir(ref_file):
    #     in_iter = yield_lines_from_dir(ref_file,'.txt')
    # else:
    #     raise IOError('File not found: '+ ref_file)
    #
    #
    # if num_proc >= 1:
    #     p=Pool(num_proc)
    #     out_iter = p.imap_unordered(get_match,in_iter,chunksize=100)
    # else:
    #     out_iter = get_match(in_iter)
    #
    #
    # with open(match_file,'w') as out_fh:
    #     for i, line in enumerate(out_iter):
    #         if i % 1000 == 0:
    #             LOG.write( 'Matching line %d \n' % i )
    #
    #         out_fh.write(line + "\n")


def get_match(meta_id,line):
    # Example record:
    # line = '1001.0056|K. Behrend [ .... ] .  128 (1997), 45--88.\n'
    # ID, rec = line.split('|')[:2]

    # cleanup
    # rec = rec.strip()
    # ID = repair_arxiv_id(meta_id)

    # Match
    print("before MATCH()")
    match = Match(line)
    print(match)
    if match:
        print("usa u if")
        return match
    else:

        return None
            
    # if match:
    #     return  ID + "|" + rec + "|" + match
    # else:
    #     return  ID + "|" + rec + "|"
    

def repair_arxiv_id(arxiv_id):
    """
    Reinserts '/' in old arxiv id's

    Examples:
    >>> repair_arxiv_id('math-ph1234567') 
    'math-ph/1234567'

    >>> repair_arxiv_id('1024.1242')
    '1026.1242'
    """

    # initialize compiled regexp as static variable = attribute
    if not 'regexp' in dir(repair_arxiv_id):
        repair_arxiv_id.regexp = re.compile(r'([a-zA-Z-]{2,9})(\d{7})')
        
    m = repair_arxiv_id.regexp.match(arxiv_id)
    if m:
        return m.group(1) + '/' + m.group(2)
    else:
        return arxiv_id


if __name__ == '__main__':
    main()
