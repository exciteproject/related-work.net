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
import time, os, sys
from datetime import datetime
import oaipmh.client, oaipmh.metadata, oaipmh.error

ARXIV_URL = 'http://export.arxiv.org/oai2'
METADATA_PREFIX = 'oai_dc'

def _log(str):
    print(str, file=sys.stderr)

def _oa_connect():
    _log("Initializing connection")
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

def _parse(oa_head, oa_meta):
    oa_id = oa_head.identifier()
    meta_dict = oa_meta.getMap()
    # oa_id examples:
    # * 'oai:arXiv.org:astro-ph/0001516'
    # * 'oai:arXiv.org:1001.0231'
    # we remove the prefix 'oai:arXiv.org:'
    rec_id = oa_id.split(':')[-1]
    return [rec_id, meta_dict]

def _get_records(client, start_date, end_date):
    _log("Fetching records: {} - {}".format(start_date, end_date))
    try:
        recs = client.listRecords(
            from_          = start_date,  # yes, it is from_ not from
            until          = end_date,
            metadataPrefix = METADATA_PREFIX
        )
        return [ _parse(oa_head, oa_meta) for oa_head, oa_meta, x in recs ]
    except oaipmh.error.NoRecordsMatchError:
        return []

def fetch(start_date, end_date):
    return _get_records(
        _oa_connect(),
        datetime.strptime(start_date, "%Y-%m-%d"),
        datetime.strptime(end_date, "%Y-%m-%d")
    )

if __name__ == "__main__":
    # quick test if this is working
    import json
    print(json.dumps(fetch("2016-01-01","2016-01-10")))
