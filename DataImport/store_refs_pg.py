from __future__ import print_function
import psycopg2

# The meta DB shall only hold values that are currently needed in the
# system. If we later need more information, we can go to the original
# sources. We should not try to capture all information that is
# present in the records.

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS refs (
  meta_id VARCHAR(50),
  ref TEXT
);
"""

SQL_DROP = """
DROP TABLE IF EXISTS refs;
"""

SQL_INSERT = """
INSERT INTO refs(meta_id, ref)
VALUES          (%s,      %s)
ON CONFLICT DO NOTHING;
"""

SQL_GET = """
SELECT * FROM refs WHERE meta_id = %s
"""

SQL_DELETE = """
DELETE FROM refs WHERE meta_id = %s;
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

    def queue_ref(self, meta_id, ref):
        "Queue data for insertion"
        self.q.append([meta_id, ref])

    def flush(self):
        "Write out queue to DB"
        n = len(self.q)
        self.cur.executemany(SQL_INSERT, self.q);
        self.con.commit()
        self.q = [] # clear queue
        return self.cur.statusmessage

    def get(self, meta_id):
        "Lookup citations for a paper"
        self.cur.execute(SQL_GET, (meta_id,))
        return self.cur.fetchall()

    def delete(self, meta_id):
        "Delete all references of a paper in the db"
        self.cur.execute(SQL_DELETE, (meta_id,))
        self.con.commit()
        return self.cur.statusmessage

    def close(self):
        self.con.close()
    
if __name__ == "__main__":
    s = store(user="rw", database="rw")
    print(s.table_create())
    print(s.queue_ref("test-id", "test-ref"))
    print(s.queue_ref("test-id", "test-ref-2"))
    print(s.flush())
    print(s.get("test-id"))
    print(s.delete("test-id"))
    print(s.close())
