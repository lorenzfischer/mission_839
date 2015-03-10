# -*- coding: utf-8 -*-

import json
import datetime
import turbotlib
import urllib2
import zipfile
import requests
import xlrd
import pprint

import io

# code copied and adapted from: https://github.com/metaodi/finma-scraper/blob/master/mission_838/scraper.py

def get_rows(content):
    workbook = xlrd.open_workbook(file_contents=content)
    worksheet = workbook.sheet_by_index(0)
    # Extract the row headers
    header_row = worksheet.row_values(3)
    # print header_row
    rows = []
    for row_num in range(worksheet.nrows):
        # Data columns begin at row count 4 (5 in Excel)
        if row_num >= 4:
            rows.append(dict(zip(
                header_row,
                worksheet.row_values(row_num)
            )))
    return rows

FINMA_URL = 'https://www.finma.ch/institute/xls_e/ebeh_status2.xlsx'
#FINMA_URL = 'file:///Users/lfischer/Desktop/ebeh_status2.xlsx'
r = requests.get(FINMA_URL)

for row in get_rows(r.content):
    # headers are:
    # Name	City	Licensing	Bank type			Securities dealer type
    name = row['Name']
    if name and len(name) and not name.startswith(u'Total banks and securities dealers discontinuing their business activities'):
        del row[None]
        row['sample_date'] = datetime.datetime.now().isoformat()
        row['source_url'] = FINMA_URL # so we can copy it in the transformer
        print(json.dumps(row, ensure_ascii=False).encode('utf-8'))