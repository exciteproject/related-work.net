import psycopg2

# Storing matched references and metadata

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS matches (
  ref_id VARCHAR(50),
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
SELECT * FROM matches WHERE meta_id = %s;
"""

SQL_DELETE = """
DELETE FROM matches WHERE meta_id = %s;
"""