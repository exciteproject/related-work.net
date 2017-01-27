import psycopg2

# Storing matched references and metadata

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS matches (
  ref_id VARCHAR(50) CONSTRAINT ref_id PRIMARY KEY,
  meta_id VARCHAR(50)
);
"""

SQL_DROP = """
DROP TABLE IF EXISTS matches;
"""

SQL_INSERT = """
INSERT INTO matches(ref_id, meta_id)
VALUES          (%s,      %s)
ON CONFLICT DO NOTHING;
"""

SQL_GET = """
SELECT * FROM matches WHERE ref_id = %s;
"""

SQL_DELETE = """
DELETE FROM matches WHERE ref_id = %s;
"""


class store:
    def __init__(self, **kwargs):
        self.con = psycopg2.connect(**kwargs)
        self.cur = self.con.cursor()
        self.q = []  # fresh list

    def table_create(self):
        self.cur.execute(SQL_CREATE);
        self.con.commit();
        return self.cur.statusmessage

    def table_drop(self):
        self.cur.execute(SQL_DROP);
        self.con.commit()
        return self.cur.statusmessage

    def queue_match(self, ref_id, meta_id):
        "Queue data for insertion"
        self.q.append([ref_id, meta_id])

    def flush(self):
        "Write out queue to DB"
        n = len(self.q)
        self.cur.executemany(SQL_INSERT, self.q);
        self.con.commit()
        self.q = []  # clear queue
        return self.cur.statusmessage

    def get(self, ref_id):
        "Lookup citations for a paper"
        self.cur.execute(SQL_GET, (ref_id,))
        return self.cur.fetchall()

    def delete(self, ref_id):
        "Delete all references of a paper in the db"
        self.cur.execute(SQL_DELETE, (ref_id,))
        self.con.commit()
        return self.cur.statusmessage

    def close(self):
        self.con.close()


if __name__ == "__main__":
    s = store(user="rw", database="rw")
    print(s.table_create())
    print(s.queue_match("test-ref-id", "test-meta"))
    print(s.queue_match("test-ref-id", "test-meta-2"))
    print(s.flush())
    print(s.get("test-ref-id"))
    print(s.delete("test-ref-id"))
    print(s.close())