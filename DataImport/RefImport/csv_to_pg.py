import psycopg2
import argparse
import traceback

parser = argparse.ArgumentParser()
parser.add_argument('csv_file', help='path to csv file with references', type=str)
parser.add_argument('dest_table', help='destination table to import to', type=str)
args = parser.parse_args()
csv_file = args.csv_file
dest_table = args.dest_table
con = psycopg2.connect(user="rw", database="rw")
cur = con.cursor()
f = open(csv_file, 'r')
try:
    cur.copy_from(f, dest_table, sep=',')
    con.commit()
except psycopg2.ProgrammingError:
    traceback.print_exc()
f.close()

