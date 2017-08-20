import time
import datetime
import os
import sys
import json
from pathlib import Path
from capp import fetch_arxiv_meta, insert_arxiv_meta_bucket, fetch_arxiv_pdf, fetch_arxiv_source, ref_extract_daily, \
schedule_ref_matching_daily

if __name__ == '__main__':
    arg = sys.argv[1]
    today = time.strftime("%Y-%m-%d")
    file_loc = "/EXCITE/datasets/arxiv/meta_daily/"
    if arg == "download_meta":
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow = tomorrow.strftime("%Y-%m-%d")
        print(fetch_arxiv_meta(today, tomorrow, file_loc))
    elif arg == "insert_meta":
        # year = today.split("-")[0]
        print(insert_arxiv_meta_bucket(today, src_file=file_loc))
    elif arg == "download_pdf":
        with open(file_loc + today) as meta_file:
            data = json.load(meta_file)
            for entry in data:
                fetch_arxiv_pdf(entry[0])
                time.sleep(10)
    elif arg == "download_source":
        source_dest = "/EXCITE/datasets/arxiv/source_daily/" + today
        if not os.path.isdir(source_dest):
            os.mkdir(source_dest)
        with open(file_loc + today) as meta_file:
            data = json.load(meta_file)
            for entry in data:
                fetch_arxiv_source(entry[0], source_dest)
    elif arg == "extract_refs":
        source_dest = "/EXCITE/datasets/arxiv/source_daily/" + today + "/"
        os.chdir(source_dest)
        files = os.listdir(".")
        for file in files:
            file_name = source_dest + file
            print(file_name)
            if file_name[-3:] == "pdf":
                print("File is pdf. " + file)
                continue
            try:
                ref_extract_daily(file_name)
            except IOError:
                print("File should be a pdf" + file_name)
                os.rename(file_name, file_name + '.pdf')
                break
    elif arg == "match_refs":
        source_dest = "/EXCITE/datasets/arxiv/source_daily/" + today + "/"
        os.chdir(source_dest)
        files = os.listdir(".")
        files = [file for file in files if file[-3:] != "pdf"]
        schedule_ref_matching_daily(files)