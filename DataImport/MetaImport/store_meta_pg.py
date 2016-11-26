from __future__ import print_function
import psycopg2

# The meta DB shall only hold values that are currently needed in the
# system. If we later need more information, we can go to the original
# sources. We should not try to capture all information that is
# present in the records.

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS meta(
  id VARCHAR(50) PRIMARY KEY, -- arxiv ID in this case
  author TEXT,   -- All authors concatenated by ' and '
  title TEXT,
  abstract TEXT,
  subject TEXT,  -- E.g. Quantum Physics
  date CHAR(10), -- ISO DATE
  year INTEGER  -- for indexing
);
"""

SQL_DROP = """
DROP TABLE IF EXISTS meta;
"""

SQL_INSERT = """
INSERT INTO meta(id, author, title, abstract, subject, date, year)
VALUES          (%s, %s,     %s,    %s,       %s,      %s,   %s)
ON CONFLICT DO NOTHING;
"""

SQL_GET = """
SELECT * FROM meta WHERE id = %s;
"""

SQL_DELETE = """
DELETE FROM meta WHERE id = %s;
"""

class store:
    def __init__(self, **kwargs):
        self.con = psycopg2.connect(**kwargs)
        self.cur = self.con.cursor()
        self.q   = [] # fresh list

    def table_create(self):
        self.cur.execute(SQL_CREATE);
        self.con.commit();
        return self.cur.statusmessage

    def table_drop(self):
        self.cur.execute(SQL_DROP);
        self.con.commit()
        return self.cur.statusmessage

    def queue_arxiv_meta(self, _id, meta_dict):
        "Queue data for insertion"
        author   = ' and '.join(meta_dict['creator'])
        title    = meta_dict['title'][0]
        abstract = meta_dict['description'][0]
        subject  = ', '.join(meta_dict['subject'])
        date     = meta_dict['date'][0]
        year     = date[0:4]
        self.q.append([_id, author, title, abstract, subject, date, year])

    def flush(self):
        "Write out queue to DB"
        n = len(self.q)
        self.cur.executemany(SQL_INSERT, self.q);
        self.con.commit()
        return self.cur.statusmessage

    def get(self, _id):
        self.cur.execute(SQL_GET, (_id,))
        return self.cur.fetchone()

    def delete(self, _id):
        self.cur.execute(SQL_DELETE, (_id,))
        self.con.commit()
        return self.cur.statusmessage

if __name__ == "__main__":
    import json
    with open("arxiv_meta_example.json", "r") as fh:
        EXAMPLE=json.load(fh)
    key = EXAMPLE[0]
    meta_dict = EXAMPLE[1]
    s = store(user="rw", database="rw")
    print(s.table_create())
    print(s.queue_arxiv_meta(key, meta_dict))
    print(s.flush())
    print(s.get(key))
    print(s.delete(key))
