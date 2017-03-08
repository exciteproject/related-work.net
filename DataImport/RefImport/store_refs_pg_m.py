import psycopg2

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS refs_m (
  ref_id VARCHAR(50) PRIMARY KEY, -- SSOAR ID number
  ref_text TEXT  -- Reference text
);
"""

SQL_DROP = """
DROP TABLE IF EXISTS refs_m;
"""

SQL_INSERT = """
INSERT INTO refs_m(ref_id, ref_text)
VALUES          (%s, %s)
ON CONFLICT DO NOTHING;
"""

SQL_GET = """
SELECT * FROM refs_m WHERE ref_id = %s;
"""

SQL_DELETE = """
DELETE FROM refs_m WHERE ref_id = %s;
"""

class store:
    def __init__(self, **kwargs):
        self.con = psycopg2.connect(**kwargs)
        self.cur = self.con.cursor()
        self.q   = [] # fresh list

    def table_create(self):
        self.cur.execute(SQL_CREATE)
        self.con.commit()
        return self.cur.statusmessage

    def table_drop(self):
        self.cur.execute(SQL_DROP)
        self.con.commit()
        return self.cur.statusmessage

    def queue_ref(self, ref_id, ref_text):
        "Queue data for insertion"
        self.q.append([ref_id, ref_text])

    def flush(self):
        "Write out queue to DB"
        n = len(self.q)
        self.cur.executemany(SQL_INSERT, self.q)
        self.con.commit()
        self.q = [] # clear queue
        return self.cur.statusmessage

    def get(self, ref_id):
        "Lookup citations for a paper"
        self.cur.execute(SQL_GET, (ref_id,))
        return self.cur.fetchall()

    def get_all_references(self):
        self.cur.execute("SELECT * FROM refs_m;")
        return self.cur

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
    print(s.queue_ref("12345", "test-ref"))
    print(s.queue_ref("12345", "test-ref-2"))
    print(s.flush())
    print(s.get("12345"))
    print(s.delete("12345"))
    print(s.get("12345"))
    print(s.close())
