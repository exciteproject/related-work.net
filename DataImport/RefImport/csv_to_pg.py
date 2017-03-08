from RefImport.store_refs_pg_m import store
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('csv_file', help='path to csv file with references', type=str, default='references.csv')
args = parser.parse_args()
csv_file = args.csv_file
s = store(user="rw", database="rw")
f = open(csv_file, 'r')
s.cur.copy_from(f, 'refs_m', sep=',')
f.close()

