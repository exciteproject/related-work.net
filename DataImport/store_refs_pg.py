from __future__ import print_function
import psycopg2

# The refs table contains a unique ID, 
# source meta id, and reference text for every reference

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS refs (
  ref_id SERIAL PRIMARY KEY, -- Auto increment field
  meta_id_source VARCHAR(50),  -- Meta id of the paper containing the reference
  ref_text TEXT  -- Reference text
);
"""

SQL_DROP = """
DROP TABLE IF EXISTS refs;
"""

SQL_INSERT = """
INSERT INTO refs(meta_id_source, ref_text)
VALUES(%s, %s)
ON CONFLICT DO NOTHING;
"""

SQL_GET = """
SELECT * FROM refs WHERE meta_id_source = %s;
"""

SQL_GET_MANY = """
SELECT * FROM refs WHERE meta_id_source IN %s;
"""

SQL_DELETE = """
DELETE FROM refs WHERE meta_id_source = %s;
"""

class store:
    def __init__(self, **kwargs):
        self.con = psycopg2.connect(**kwargs)
        self.cur = self.con.cursor('server-cursor')
        self.q = []  # fresh list

    def table_create(self):
        self.cur.execute(SQL_CREATE)
        self.con.commit()
        return self.cur.statusmessage

    def table_drop(self):
        self.cur.execute(SQL_DROP)
        self.con.commit()
        return self.cur.statusmessage

    def queue_ref(self, meta_id_source, ref_text):
        "Queue data for insertion"
        self.q.append([meta_id_source, ref_text])

    def flush(self):
        "Write out queue to DB"
        n = len(self.q)
        cursor2 = self.con.cursor()  # replaced named cursor with a new cursor
        cursor2.executemany(SQL_INSERT, self.q)
        self.con.commit()
        self.q = [] # clear queue
        return self.cur.statusmessage

    def get(self, meta_id_source):
        "Lookup citations for a paper"
        self.cur.execute(SQL_GET, (meta_id_source,))
        return self.cur.fetchall()

    def get_many(self, meta_id_list):
        "Lookup citations for a paper"
        self.cur.execute(SQL_GET_MANY, (tuple(meta_id_list),))
        return self.cur.fetchall()

    def get_all_references(self):
        self.cur.execute("SELECT * FROM refs")
        return self.cur

    def delete(self, meta_id_source):
        "Delete all references of a paper in the db"
        self.cur.execute(SQL_DELETE, (meta_id_source,))
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
    print(s.get("test-id"))
    print(s.close())
