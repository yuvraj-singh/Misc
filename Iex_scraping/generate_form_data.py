"""
Get post request data as json.

Input : form_data.txt (Text file containing request data sent)
OUTPUT : form_data.json

Assumptions :
Only dynamic parameters (for us) are : __VIEWSTATE, __VIEWSTATEGENERATOR, __EVENTVALIDATION, ctl00$InnerContent$calFromDate$txt_Date, ctl00$InnerContent$calToDate$txt_Date
Others can be supplied with the values in the file
"""

IN_FILENAME = "form_data.txt"
OUT_FILENAME = "form_data.json"

import json

data_json = {}
with open(IN_FILENAME) as f:
	for line in f:
		parts = line.strip().split(":")
		# Assume no index errors
		name = parts[0]
		value = ":".join(parts[1:])
		data_json[name] = value

with open(OUT_FILENAME, 'w') as f:
	json.dump(data_json, f)