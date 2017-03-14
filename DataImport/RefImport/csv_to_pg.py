from store_refs_pg_m import store
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('csv_file', help='path to csv file with references', type=str)
parser.add_argument('dest_table', help='destination table to import to', type=str)
args = parser.parse_args()
csv_file = args.csv_file
dest_table = args.dest_table
s = store(user="rw", database="rw")
f = open(csv_file, 'r')
s.cur.copy_from(f, dest_table, sep=',')
s.con.commit()
f.close()

