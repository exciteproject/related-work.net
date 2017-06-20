from __future__ import absolute_import, unicode_literals, print_function
import sys
import os
import subprocess
import json

from celery import Celery


def log(s):
    print(s, file=sys.stderr)


#
# Celery Setup
#
app = Celery(
    'capp',  # needs to be the same as the filename
    broker='redis://localhost:6379/3',
)

app.conf.update(
    broker_transport_options={'visibility_timeout': 60 * 10},
    result_expires=3600,
    task_publish_retry=True,
    task_publish_retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 60,
        'interval_max': 5 * 60,  # max wait
    },
    worker_concurrency=1
)

#
# Tasks
#

# Download Arxiv Metadata
from MetaImport import fetch as _fetch
from store_fs import store as store_fs


@app.task
def fetch_arxiv_meta(date_from, date_to, target="/export/home/dkostic/arxiv/meta/"):
    # target = "/EXCITE/datasets/arxiv/meta/"

    s = store_fs(target)
    key = ":".join([date_from, date_to])
    if s.exists(key):
        return "Done Already"
    else:
        s.set(key, _fetch(date_from, date_to))
        return "OK"


def schedule_fetch_arxiv_meta(dates_list):
    # dates = [("2009-02-01", "2009-03-01"), ("2010-06-01", "2010-07-01"), ("2010-08-01", "2010-09-01"),
    #          ("2010-10-01", "2010-11-01"), ("2011-06-01", "2011-07-01")]
    # dates2 = [("2016-01-01", "2016-02-01"), ("2016-02-01", "2016-03-01"), ("2016-03-01", "2016-04-01"),
    #           ("2016-04-01", "2016-05-01"), ("2016-05-01", "2016-06-01"), ("2016-06-01", "2016-07-01"),
    #           ("2016-07-01", "2016-08-01"), ("2016-08-01", "2016-09-01"), ("2016-09-01", "2016-10-01"),
    #           ("2016-10-01", "2016-11-01"), ("2016-11-01", "2016-12-01"), ("2016-12-01", "2017-01-01")]
    # dates3 = [("2017-02-01", "2017-03-01"), ("2017-03-01", "2017-04-01")]
    # dates3.extend(dates)
    for date in dates_list:
        print(fetch_arxiv_meta.delay(date[0], date[1]))


## Create MetaDB
from store_meta_pg import store as store_pg


@app.task
def insert_arxiv_meta_bucket(key, src_file="/EXCITE/datasets/arxiv/meta/"):
    log("Inserting bucket {}".format(key))
    src = store_fs(src_file)
    dst = store_pg(database="rw", user="rw")
    n = 0
    for record in src.get(key):
        rid = record[0]
        rdict = record[1]
        dst.queue_arxiv_meta(rid, rdict)
        n += 1
        if n % 1000 == 0: log(dst.flush())
    log(dst.flush())


def schedule_insert_arxiv_meta_bucket():
    folder = "/EXCITE/datasets/arxiv/meta"
    all_files = os.listdir(folder)
    all_files.remove("README.md")
    for file in all_files:
        print(insert_arxiv_meta_bucket.delay(file))


@app.task
def fetch_arxiv_pdf(arxiv_id, target="/EXCITE/datasets/arxiv/pdf_daily"):
    url = "https://arxiv.org/pdf/" + arxiv_id + ".pdf"
    command = "wget --user-agent=Lynx '" + url + "' -P " + target
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)

    # print(result.stdout.decode('utf-8'))


@app.task
def fetch_arxiv_source(arxiv_id, target="/EXCITE/datasets/arxiv/source_daily"):
    url = "https://arxiv.org/e-print/" + arxiv_id
    command = "wget --user-agent=Lynx '" + url + "' -P " + target
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    print(result.stdout.decode('utf-8'))


# Extract Buckets
from pathlib import Path
from subprocess import call


@app.task
def bucket_extract(name):
    log("Extracting bucket: " + name)
    src = Path("/EXCITE/datasets/arxiv/pdf")
    dst = Path("/EXCITE/datasets/arxiv/pdfs")
    if not dst.exists():
        dst.mkdir()
    call(['tar', 'xf', str(src / name), '-C', str(dst)])


def schedule_bucket_extract():
    src = Path("/EXCITE/datasets/arxiv/pdf")
    for entry in src.iterdir():
        log("Scheduling extraction: " + entry.name)
        bucket_extract.delay(entry.name)


def run(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)
    return (line.decode("utf8").rstrip('\n') for line in iter(p.stdout.readline, b''))


## Extract References
from RefExtract import RefExtract
from store_refs_pg import store as store_refs
from celery.signals import celeryd_after_setup, worker_shutdown

dst, mst = False, False


@celeryd_after_setup.connect
def init_worker(**kwargs):
    global dst
    print('Initializing database connection for worker.')
    dst = store_refs(user="rw", database="rw")


@worker_shutdown.connect
def shutdown_worker(**kwargs):
    global dst
    dst.close()


@app.task
def ref_extract_s3(gz_name):
    global dst
    if not dst:
        dst = store_refs(user="rw", database="rw")
    log("Extracting references from: " + gz_name)
    meta_id = Path(gz_name).name[:-3]  # remove .gz
    refs = RefExtract(gz_name)
    for ref in refs:
        dst.queue_ref(meta_id, ref)
    dst.flush()
    log("Wrote {} references".format(len(refs)))


def schedule_ref_extract():
    src = "/EXCITE/datasets/arxiv/paper"
    # there might be millons of files, use find to stream results
    for name in run("""
    find /EXCITE/datasets/arxiv/paper -type f -name '*.gz'
    """):
        log("Scheduling ref extraction: " + name)
        ref_extract_s3.delay(name)


def ref_extract_daily(file_name):
    global dst
    if not dst:
        dst = store_refs(user="rw", database="rw")
    log("Extracting references from: " + file_name)
    meta_id = Path(file_name).name[:-3]  # remove .gz
    refs = RefExtract(file_name)
    print(refs)
    for ref in refs:
        dst.queue_ref(meta_id, ref)
    dst.flush()
    log("Wrote {} references".format(len(refs)))


from store_refs_pdf_pg import store as store_r_pdf

store_refs_pdf = False


@app.task
def layout_extract_from_pdf(file_names, file_loc):
    os.chdir("/export/home/dkostic/refext")
    cmd_input = [
        '{{"inputFilePath":"{}/{}", "outputFilePath":"/EXCITE/datasets/arxiv_layout/{}.tsv"}}'.format(file_loc, name,
                                                                                                      name) for name in
        file_names]
    cmd_input = '\n'.join(cmd_input)
    # print(cmd_input)
    command = 'mvn exec:java -Dexec.mainClass="de.exciteproject.refext.io.StandardInOutLayoutExtractor"'
    result = subprocess.run(command, stdout=subprocess.PIPE, input=cmd_input.encode(), shell=True)
    print(result.stdout.decode('utf-8'))
    print("Layout extraction finished. Number of files: {}".format(len(file_names)))


@app.task
def ref_extract_from_layout(file_names):
    os.chdir("/export/home/dkostic/refext")
    global store_refs_pdf
    if not store_refs_pdf:
        store_refs_pdf = store_r_pdf(user="rw", database="rw")
    cmd_input = ['{{"inputFilePath":"/EXCITE/datasets/arxiv_layout/{}.tsv"}}'.format(name, name) for name in file_names]
    cmd_input = '\n'.join(cmd_input)
    print(cmd_input)
    command = 'mvn exec:java -Dexec.mainClass="de.exciteproject.refext.io.StandardInOutReferenceExtractor"  ' \
              '-Dexec.args="-crfModel /EXCITE/scratch/eval/amsd2017/git/amsd2017/evaluation/refext/trained/0/models/model.ser" -q'
    result = subprocess.run(command, stdout=subprocess.PIPE, input=cmd_input.encode(), shell=True)
    tsv = result.stdout.decode('utf-8')
    print(tsv)
    for line in tsv:
        if line[0] == "{":
            print(line)
            reference = json.loads(line)
            meta_id = reference["name"]
            for ref in reference["references"]:
                store_refs_pdf.queue_ref(meta_id, ref)
    store_refs_pdf.flush()
    log("Wrote {} references".format(len(tsv)))


def schedule_layout_from_pdf(path="/EXCITE/datasets/arxiv/pdfs/0001"):
    src = Path(path)
    files = [name.name for name in src.iterdir()]
    print(files[:10])
    layout_extract_from_pdf(files, path)


def schedule_ref_from_layout(path="/EXCITE/datasets/arxiv/pdfs/0001"):
    src = Path(path)
    files = [name.name for name in src.iterdir()]
    ref_extract_from_layout(files)


# Reference matching
from store_matches_pg import store as store_matches
from Matching.MatchScript import Match


@app.task
def ref_matching(meta_id, ref_text, ref_id):
    global mst
    if not mst:
        mst = store_matches(user="rw", database="rw")
    match = Match(ref_text)
    if match:
        mst.queue_match(ref_id, match, meta_id)
        if len(mst.q) % 1000 == 0:
            print("DB flush - matches")
            mst.flush()


def schedule_ref_matching():
    refs = store_refs(user="rw", database="rw")
    for reference in refs.get_all_references():
        ref_matching.delay(reference[0], reference[1], reference[2])


if __name__ == "__main__":
    pass
    # print(fetch_arxiv_meta(("2010-06-01","2010-07-01")))
    # print(fetch_arxiv_meta.delay("2017-01-01","2017-02-01"))
    # schedule_fetch_arxiv_meta([("2017-05-06", "2017-05-08")])
    # insert_arxiv_meta_bucket("2012-04-01:2012-05-01")
    # schedule_insert_arxiv_meta_bucket()
    # schedule_bucket_extract()
    # print(ref_extract('/EXCITE/datasets/arxiv/paper/1310/1310.0623.gz'))
    # schedule_ref_extract()
    # schedule_ref_matching()
    # layout_extract_from_pdf.delay("109-12826")
    schedule_layout_from_pdf()
    # schedule_ref_from_layout()
