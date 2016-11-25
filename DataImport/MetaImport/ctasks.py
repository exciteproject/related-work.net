#!/usr/bin/env python
#
# Download ArXiv paper meeta data via OpenAccess API and store them into pickle files
#
# by Heinrich Hartmann, related-work.net,  2012
#
# Builds upon:
#
# (c) 2006 Rufus Pollock, GPL
# provided by infrae.com, available at http://www.infrae.com/download/oaipmh
#
#

from __future__ import absolute_import, unicode_literals, print_function
from . import celery
app = celery.app

import time, os, sys, json
from datetime import datetime

import oaipmh.client, oaipmh.metadata
from oaipmh.error import NoRecordsMatchError

from celery import Celery
import redis

ARXIV_URL = 'http://export.arxiv.org/oai2'
METADATA_PREFIX = 'oai_dc'

def log(str):
    print(str, file=sys.stderr)

#
# WORKER
#
def oa_connect():
    log("Initializing connection")
    client = oaipmh.client.Client(ARXIV_URL)
    out = client.identify()

    # got to update granularity or we barf with:
    # oaipmh.error.BadArgumentError: Max granularity is YYYY-MM-DD:2003-04-10T00:00:00Z
    client.updateGranularity()

    # register a reader on our client to handle oai_dc metadata
    # if we do not attempt to read records will fail with:
    #   .../oaipmh/metadata.py", line 37, in readMetadata
    #   KeyError: 'oai_dc'
    client.getMetadataRegistry().registerReader(
        METADATA_PREFIX,
        oaipmh.metadata.oai_dc_reader
        )
    return client

def parse(oa_head, oa_meta):
    oa_id = oa_head.identifier()
    meta_dict = oa_meta.getMap()
    # oa_id examples:
    # * 'oai:arXiv.org:astro-ph/0001516'
    # * 'oai:arXiv.org:1001.0231'
    # we remove the prefix 'oai:arXiv.org:'
    rec_id = oa_id.split(':')[-1]
    return [rec_id, meta_dict]

def get_records(client, start_date, end_date):
    log("Fetching records: {} - {}".format(start_date, end_date))
    try:
        recs = client.listRecords(
            from_          = start_date,  # yes, it is from_ not from
            until          = end_date,
            metadataPrefix = METADATA_PREFIX
        )
        return [ parse(oa_head, oa_meta) for oa_head, oa_meta, x in recs ]
    except NoRecordsMatchError:
        return []

def fetch_parse(start_date, end_date):
    return get_records(
        connect(),
        datetime.strptime(start_date, "%Y-%m-%d"),
        datetime.strptime(end_date, "%Y-%m-%d")
    )

def fetch_parse_store(start_date, end_date):
    r = redis.StrictRedis(host='localhost', port=6379, db=1)
    key = "oa-meta[" + start_date + "-" + end_date + "]",
    if r.exists(key):
        return "Done already"
    else:
        records = get_records(
            oa_connect(),
            datetime.strptime(start_date, "%Y-%m-%d"),
            datetime.strptime(end_date, "%Y-%m-%d")
        )
        r.set(key, json.dumps(records), nx=True) # no overwrite
        return "Inserted"

def fetch_parse_store_pg(start_date, end_date):
    db = db_connect()
    key = "oa-meta[" + start_date + "-" + end_date + "]",
    if db_test(db, key):
        return "Done already"
    else:
        records = get_records(
            oa_connect(),
            datetime.strptime(start_date, "%Y-%m-%d"),
            datetime.strptime(end_date, "%Y-%m-%d")
        )
        db_insert(db, key, json.dumps(records))
        return "Inserted"

#if __name__ == "__main__":
#    print(json.dumps(fetch_parse("2012-01-01","2012-01-10")))

# db = db_connect()
# print(db_test(db, "123"))
# print(db_insert(db, "123",'{"json":"Hello!"}'))
# print(db_test(db, "123"))
