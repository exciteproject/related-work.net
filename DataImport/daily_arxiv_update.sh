#!/bin/bash

cd ~/related-work.net/
source setup.sh
cd ~/related-work.net/DataImport/
python daily_meta.py download_meta
cd /EXCITE/datasets/arxiv/meta_daily
DATE=$(date +%F)
YEAR=$(date +%Y)
TOMORROW=$(date +%F -d "next day")
mv "$DATE:$TOMORROW" "$DATE"
cp "$DATE" "../meta_daily_unpacked/$YEAR/$DATE.json"
cd ~/related-work.net/DataImport/
python daily_meta.py insert_meta
python daily_meta.py download_pdf
python daily_meta.py download_source
cd /EXCITE/datasets/arxiv/source_daily/$DATE
#for f in *; do mv "$f" "$f.tar.gz"; done
python daily_meta.py extract_refs