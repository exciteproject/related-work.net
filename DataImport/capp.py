from __future__ import absolute_import, unicode_literals, print_function
import sys
from celery import Celery

def log(s):
    print(s, file=sys.stderr)

#
# Celery Setup
#
app = Celery(
    'capp', # needs to be the same as the filename
    broker='redis://localhost:6379/3',
)

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

# Download Arxiv Metadata
from MetaImport import fetch as _fetch
from store_fs import store as store_fs
@app.task
def fetch_arxiv_meta(*args):
    s = store("/EXCITE/datasets/arxiv/meta/")
    key = ":".join(args)
    if s.exists(key):
        return "Done Already"
    else:
        s.set(key, _fetch(*args))
        return "OK"

## Create MetaDB
from store_meta_pg import store as store_pg
@app.task
def insert_arxiv_meta_bucket(key):
    log("Inserting bucket {}".format(key))
    src = store_fs("/EXCITE/datasets/arxiv/meta/")
    dst = store_pg(database="rw", user="rw")
    n = 0
    for record in src.get(key):
        rid   = record[0]
        rdict = record[1]
        dst.queue_arxiv_meta(rid, rdict)
        n += 1
        if n % 1000 == 0: log(dst.flush())
    log(dst.flush())

## Extract Buckets
from pathlib import Path
from subprocess import call
@app.task
def bucket_extract(name):
    log("Extracting bucket: " + name)
    src = Path("/EXCITE/datasets/arxiv/src_buckets")
    dst = Path("/EXCITE/datasets/arxiv/paper")
    if not dst.exists():
        dst.mkdir()
    call(['tar', 'xf', str(src / name) , '-C', str(dst)])

def schedule_bucket_extract():
    src = Path("/EXCITE/datasets/arxiv/src_buckets")
    for entry in src.iterdir():
        log("Scheduling extraction: " + entry.name)
        bucket_extract.delay(entry.name)

import subprocess
def run(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)
    return (line.decode("utf8").rstrip('\n') for line in iter(p.stdout.readline, b''))

## Extract References
from RefExtract import RefExtract

@app.task
def ref_extract(gz_name):
    log("Extracting references from: " + gz_name)
    dst = Path("/EXCITE/datasets/arxiv/refs2")
    if not dst.exists():
        dst.mkdir()
    dstore = store_fs(str(dst))
    key = Path(gz_name).name[:-3] # remove .gz
    if False: # dstore.exists(key):
        return "Done Already"
    else:
        refs = RefExtract(gz_name)
        for ref in refs:
            
        if len(refs) > 0:
            dstore.set(key, refs)
            log("Stored {} references.".format(len(refs)))
            return len(refs)
        else:
            log("No references found for.")
            return 0
            
def schedule_ref_extract():
    src = "/EXCITE/datasets/arxiv/paper"
    # there might be millons of files, use find to stream results
    for name in run("""
    find /EXCITE/datasets/arxiv/paper -type f -name '*.gz'
    """):
        log("Scheduling ref extraction: " + name)
        ref_extract.delay(name)

if __name__ == "__main__":
    # print(fetch_arxiv_meta("2016-01-10","2016-01-11"))
    # print(fetch_arxiv_meta.delay("2016-01-10","2016-01-12"))
    # insert_arxiv_meta_bucket("2012-04-01:2012-05-01")
    # schedule_bucket_extract()
    # print(ref_extract('/EXCITE/datasets/arxiv/paper/1310/1310.0623.gz'))
    schedule_ref_extract()
