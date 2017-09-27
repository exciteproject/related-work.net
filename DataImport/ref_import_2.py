import os
import psycopg2

con = psycopg2.connect(user="rw", database="rw")
cur = con.cursor()
SQL_INSERT = """
INSERT INTO refs_2(meta_id_source, ref_text)
VALUES(%s, %s)
ON CONFLICT DO NOTHING;
"""

path = '/EXCITE/scratch/arxiv/result/bio'
all_dirs = os.listdir(path)
num_files = 0
num_refs = 0
for dir in all_dirs:
    files = os.listdir(os.path.join(path, dir))
    num_files += len(files)
    for file in files:
        queue = []
        with open(os.path.join(path, dir, file)) as f:
            for line in f:
                queue.append([os.path.splitext(file)[0], line])
                num_refs+=1
        # print(queue)
        cur.executemany(SQL_INSERT, queue)
        con.commit()
print("Number of files: " + num_files)
print("Number of references: " + num_refs)
