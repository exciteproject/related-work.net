from __future__ import absolute_import, unicode_literals
from celery import Celery

#
# Celery Setup
#
app = Celery(
    'capp', # needs to be the same as the filename
    broker='redis://localhost:6379/3',
)

# Optional configuration, see the application user guide.
app.conf.update(
    broker_transport_options = {'visibility_timeout': 60 * 10 },
    result_expires=3600,
    task_publish_retry=True,
    task_publish_retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 60,
        'interval_max':  5*60, # max wait
    },
    worker_concurrency = 1
)

#
# Tasks
#

from arxiv_meta_fetch import fetch as _fetch
from store_fs import store

@app.task
def fetch_arxiv_meta(*args):
    s = store("/EXCITE/datasets/arxiv/meta/")
    key = ":".join(args)
    if s.exists(key):
        return "Done Already"
    else:
        s.set(key, _fetch(*args))
        return "OK"

if __name__ == "__main__":
    print(fetch_arxiv_meta("2016-01-10","2016-01-11"))
    print(fetch_arxiv_meta.delay("2016-01-10","2016-01-12"))
