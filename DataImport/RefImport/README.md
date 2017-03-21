# Reference import scripts
This directory contains scripts for importing extracted references into a database, and a manual how to display them in the UI

# Contents 

* txt_to_csv.py -- creating a large CSV file from many textual reference file in a directory
* csv_to_pg.py -- Importing a CSV file into postgres database
* import.sh -- Bash script that creates postgres tables and indexes, and imports data using csv_to_pg.py

# Workflow

1. Adapt and run import.sh to import data into postgres

## Integrating with existing SSOAR/Arxiv data
1. Alter view `view_ref` to include the new table

Example: `CREATE OR REPLACE VIEW view_ref AS 
SELECT * FROM table_1 
UNION ALL 
SELECT * FROM table_2`

Tables must have matching columns

## Displaying data separately
1. create rest endpoint to display view
 * add an extra location entry to UI/etc/nginx.conf
 * section `http/server`
 * run `sudo make deploy` to redeploy server with new endpoint
 * Example: ```location ~ /gold_standard/(?<id>[A-Za-z0-9/.-]+)  {
            rds_json        on;
            postgres_pass   database;
            postgres_query  "SELECT * FROM view_refs_m where ref_id = '$id'";
            postgres_result_timeout 1;
        }```
2. Add html/javascript
 * To adopt existing html/js:
    1. Make a copy of `UI/htdocs/refview/` in a new folder
    2. Alter `UI/htdocs/refview/script.js` to use new endpoint for references
    3. Alter `UI/htdocs/refview/script.js` to use new column names
    4. Alter `UI/Makefile` to include new folder in `install` section
    5. Run `sudo make install` to copy altered files
    

