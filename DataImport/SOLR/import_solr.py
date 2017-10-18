# -*- coding: utf-8 -*-

import requests
import pandas as pd

base_url = "http://sowiportbeta.gesis.org/devwork/service/solr/solr_query.php?do=normal&api_key=Ia9Pxl880hC2DytCK0VD&"


def get_num_found(query_field):
    query_params = {}
    query_params["q"] = "db_origin_str:" + query_field
    query_params["start"] = str(0)
    query_params["rows"] = str(1)
    query_params["fl"] = filters
    query_params["format"] = "json"
    r = requests.get(base_url, params=query_params)
    response_details = r.json()
    numFound = response_details["response"]["numFound"]
    return numFound


def query_solr(query_field, filters, start, rows):
    query_params = {}
    query_params["q"] = "db_origin_str:" + query_field
    query_params["start"] = str(start)
    query_params["rows"] = str(rows)
    query_params["fl"] = filters
    query_params["format"] = "json"
    r = requests.get(base_url, params=query_params)
    print(r.url)
    response_details = r.json()
    docs = response_details["response"]["docs"]
    return docs


origins = ["GESIS-SELFARCHIVE", "GESIS-SSOAR", "GESIS-BIB", "GESIS-SOFIS",
           "SPRINGER-SOJ", "SOCIALTHEORY-SOT", "GESIS-SOLIS", "PROQUEST-PAO",
           "FES-BIB", "GESIS-SMARTHARVESTING", "UBK-OPAC"]

filters = ("id,person_author_txtP_mv,title_full,title,title_en_txt,classification_txtP_mv,doctype_lit_str,"
           "journal_title_txt_mv,person_author_normalized_str_mv,zsabk_str,language,topic,norm_publishDate_str,"
           "norm_title_str,norm_title_full_str,isbn,issn,norm_pagerange_str,Sseries_vol_str_mv,zsnummer_str,"
           "recorddoi_str_mv,recordurn_str_mv,recordurl_str_mv,recordfulltext_str_mv")
results = []
for query_field in origins:
    num_found = get_num_found(query_field)
    print("** NUM FOUND **")
    print(num_found)
    start = 0
    for i in range(0, num_found, 10000):
        start = i
        rows = 10000
        if start+rows > num_found: rows = num_found - start
        results.extend(query_solr(query_field, filters, start, rows))
    print("***TOTAL RESULTS***")
    print(len(results))

df = pd.DataFrame(results)
df.to_csv("data.csv", index=False)



# select id, norm_title_full_str from table where db_origin_str=3AGESIS-SSOAR limit 1;
