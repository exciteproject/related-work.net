import time
import datetime
import sys
from capp import fetch_arxiv_meta, insert_arxiv_meta_bucket

if __name__ == '__main__':
    arg = sys.argv[1]
    today = time.strftime("%Y-%m-%d")
    if arg == "download":
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow = tomorrow.strftime("%Y-%m-%d")
        target = "/EXCITE/datasets/arxiv/meta_daily/"
        print(fetch_arxiv_meta(today, tomorrow, target))
    elif arg == "insert":
        # year = today.split("-")[0]
        print(insert_arxiv_meta_bucket(today, src_file="/EXCITE/datasets/arxiv/meta_daily/"))
