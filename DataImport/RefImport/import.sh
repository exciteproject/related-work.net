#!/bin/bash

# path to file being imported and name of table
IMPORT_DATA=ssoar.csv
IMPORT_TBL_NAME=refs_m

# throw away comments
# grep -v "^#" $IMPORT_DATA > import.tmp

# create table if needed
psql -U rw -c "CREATE TABLE IF NOT EXISTS $IMPORT_TBL_NAME (
counter INTEGER,
ref_id VARCHAR(50),
ref_text TEXT)"

# create required indexes
psql -U rw -c "CREATE INDEX ref_id_idx ON $IMPORT_TBL_NAME(ref_id)"
# create views
psql -U rw -c "CREATE OR REPLACE VIEW view_$IMPORT_TBL_NAME as
SELECT * FROM $IMPORT_TBL_NAME ORDER BY counter ASC"

# import data into table
python csv_to_pg.py $IMPORT_DATA $IMPORT_TBL_NAME



