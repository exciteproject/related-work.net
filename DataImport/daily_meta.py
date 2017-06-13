import time
import datetime
import sys
import json
from capp import fetch_arxiv_meta, insert_arxiv_meta_bucket, fetch_arxiv_pdf

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
        with open(file_loc+today) as meta_file:
            data = json.load(meta_file)
            for entry in data:
                fetch_arxiv_pdf(entry[0])
