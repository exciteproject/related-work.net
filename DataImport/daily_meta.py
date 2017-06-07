import time
import datetime
import sys
from capp import fetch_arxiv_meta

if __name__ == '__main__':
    today = time.strftime("%Y-%m-%d")
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    target = "/EXCITE/datasets/arxiv/meta_daily/"
    fetch_arxiv_meta.delay(today, tomorrow, target)

