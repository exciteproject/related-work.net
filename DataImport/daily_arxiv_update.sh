#!/bin/bash

cd ~/related-work.net/
source setup.sh
cd ~/related-work.net/DataImport/
python daily_meta.py download
cd /EXCITE/datasets/arxiv/meta_daily
DATE=$(date +%F)
YEAR=$(date +%Y)
TOMORROW=$(date +%F -d "next day")
mv "$DATE:$TOMORROW" "$DATE"
cp "$DATE" "../meta_daily_unpacked/$YEAR/$DATE.json"
cd ~/related-work.net/DataImport/
python daily_meta.py insert
