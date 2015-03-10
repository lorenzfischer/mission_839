import sys
import json
import datetime

while True:
  line = sys.stdin.readline()
  if not line:
    break
  raw_record = json.loads(line)

  # skip foreign institutions, because we don't have juristiction information for them
  if 'foreign' in raw_record['Securities dealer type'].lower():
    continue

  licence_record = {
      "source_url": raw_record['source_url'],                             # Required
      "company_name": raw_record['Name'],                                 # Required
      "company_jurisdiction": "Switzerland",                              # Required
      "licence_jurisdiction": "Switzerland",                              # Required. Where the activity is permitted
      "regulator": "Swiss Financial Market Supervisory Authority FINMA",  # Optional
      "category": "Financial",                                            # Optional. Must be 'Financial' or 'Business'(at the moment)
      #"licence_number": "149923-AB-33",                                  # Optional
      "jurisdiction_classification": raw_record['Licensing'],             # Optional. Can also be an array of strings.
      "status": "Discontinuing",                                          # Optional
      "confidence": "HIGH",                                               # Optional. Must be HIGH, MEDIUM, or LOW
      "sample_date": raw_record['sample_date']                            # Required
  }
  print json.dumps(licence_record, ensure_ascii=False).encode('utf-8')