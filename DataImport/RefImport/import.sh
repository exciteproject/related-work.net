#!/bin/bash

# path to file being imported and name of table
IMPORT_DATA=references.csv
IMPORT_TBL_NAME=refs_m

# throw away comments
# grep -v "^#" $IMPORT_DATA > import.tmp

# create table if needed
psql -U rw -c "CREATE TABLE IF NOT EXISTS $IMPORT_TBL_NAME (
ref_id VARCHAR(50) PRIMARY KEY,
ref_text TEXT);"

# create required indexes
psql -U rw -c "CREATE INDEX ref_id_idx ON $IMPORT_TBL_NAME(ref_id);"
# create views
psql -U rw -c "CREATE OR REPLACE VIEW view_$IMPORT_TBL_NAME as
SELECT * FROM $IMPORT_TBL_NAME;"

# import data into table
python csv_to_pg.py $IMPORT_DATA $IMPORT_TBL_NAME

# create rest endpoint to display view
# add an extra location entry to UI/etc/nginx.conf
# section http/server
# make



