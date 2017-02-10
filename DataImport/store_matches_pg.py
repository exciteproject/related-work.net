import psycopg2

# Storing matched references and metadata

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS matches (
  ref_id VARCHAR(50), -- Reference ID, AI number
  target_meta_id VARCHAR(50), -- Paper cited by the reference
  source_meta_id VARCHAR(50), -- Paper containing the reference
  CONSTRAINT ref_unique UNIQUE(ref_id)
);
"""

SQL_INDEX = """
CREATE INDEX IF NOT EXISTS ON matches (target_meta_id);
CREATE INDEX IF NOT EXISTS ON matches (source_meta_id);
"""

SQL_DROP = """
DROP TABLE IF EXISTS matches;
"""

SQL_INSERT = """
INSERT INTO matches(ref_id, target_meta_id, source_meta_id)
VALUES          (%s, %s, %s)
ON CONFLICT DO NOTHING;
"""

SQL_GET = """
SELECT * FROM matches WHERE ref_id = %s;
"""

SQL_GET_CITED_BY = """
SELECT * FROM matches WHERE target_meta_id = %s;
"""

SQL_GET_REFERENCES = """
SELECT * FROM matches WHERE source_meta_id = %s;
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
        self.cur.execute(SQL_INDEX)
        self.con.commit();
        return self.cur.statusmessage

    def table_drop(self):
        self.cur.execute(SQL_DROP);
        self.con.commit()
        return self.cur.statusmessage

    def queue_match(self, ref_id, target_meta_id, source_meta_id):
        "Queue data for insertion"
        self.q.append([ref_id, target_meta_id, source_meta_id])

    def flush(self):
        "Write out queue to DB"
        n = len(self.q)
        self.cur.executemany(SQL_INSERT, self.q);
        self.con.commit()
        self.q = []  # clear queue
        return self.cur.statusmessage

    def get(self, ref_id):
        "Lookup matches by ref_id"
        self.cur.execute(SQL_GET, (ref_id,))
        return self.cur.fetchall()

    def get_cited_by(self, meta_id):
        "Lookup citations for a paper"
        self.cur.execute(SQL_GET_CITED_BY, (meta_id,))
        return self.cur.fetchall()

    def get_references(self, meta_id):
        "Lookup references for a paper"
        self.cur.execute(SQL_GET_REFERENCES, (meta_id,))
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
    print(s.queue_match("test-ref-id", "target-meta", "source-meta"))
    print(s.queue_match("test-ref-id", "target-meta-2", "source-meta-2"))
    print(s.flush())
    print(s.get("test-ref-id"))
    print(s.get_references("source-meta"))
    print(s.get_cited_by("target-meta"))
    print(s.delete("test-ref-id"))
    print(s.close())