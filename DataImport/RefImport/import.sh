#!/bin/bash

# path to file being imported and name of table
IMPORT_DATA=$1
IMPORT_TBL_NAME=$2


# throw away comments
# grep -v "^#" $IMPORT_DATA > import.tmp

# create table if needed
psql -U rw -c "CREATE TABLE IF NOT EXISTS $IMPORT_TBL_NAME (
counter INTEGER,
ref_id VARCHAR(50),
ref_text TEXT)"

# create required indexes
psql -U rw -c "CREATE INDEX ON $IMPORT_TBL_NAME(ref_id)"
# create views
psql -U rw -c "CREATE OR REPLACE VIEW view_$IMPORT_TBL_NAME as
SELECT * FROM $IMPORT_TBL_NAME ORDER BY counter ASC"

# import data into table
python csv_to_pg.py $IMPORT_DATA $IMPORT_TBL_NAME



