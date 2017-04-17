import psycopg2
import traceback
import json
json_file = "/EXCITE/datasets/arxiv/hashes.json"

con = psycopg2.connect(user="rw", password="rw", database="rw")
cur = con.cursor()
with open(json_file, 'r') as f:
    try:
        lines = f.readlines()
        lines = [json.loads(x) for x in lines]
        args_str = ','.join(cur.mogrify("(%s,%s,%s,%s)", (x['arxiv_id'], x['md5'], x['sha1'], x['sha256'])).decode() for x in lines)
        cur.execute("INSERT INTO hashes VALUES " + args_str)
        con.commit()
    except psycopg2.ProgrammingError:
        traceback.print_exc()


