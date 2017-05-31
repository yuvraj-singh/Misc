"""
Actual download script

Input : form_data.json
"""

import requests
from bs4 import BeautifulSoup
import sys
import json
import re
import urlparse
import shutil
import cgi

URL = "https://www.iexindia.com/marketdata/areaprice.aspx"
FORM_DATA_FILENAME = "form_data.json"

# Get arguments (date, format) from comamnd line
sdate = "20/05/2017" # default starting date
edate = "20/05/2017" # default  ending date
if len(sys.argv) == 2:
	print "incorrect number of arguments...... Downloading prices for 20/05/2017"

if len(sys.argv) >= 3:
	sdate = sys.argv[1]
	edate = sys.argv[2]

format = "EXCEL"
if len(sys.argv) >= 4:
	format = sys.argv[3]
###

# Load default form data
with open(FORM_DATA_FILENAME) as f:
	form_data = json.load(f)

session = requests.Session()
print ("Downloading source html page for fetching request parameters..." )
r = session.get(URL)
s = BeautifulSoup(r.text, 'html.parser')

__VIEWSTATE = s.find('input', {"name": "__VIEWSTATE"})["value"]
__VIEWSTATEGENERATOR = s.find('input', {"name": "__VIEWSTATEGENERATOR"})["value"]
__EVENTVALIDATION = s.find('input', {"name": "__EVENTVALIDATION"})["value"]

form_data["__VIEWSTATE"] = __VIEWSTATE
form_data["__VIEWSTATEGENERATOR"] = __VIEWSTATEGENERATOR
form_data["__EVENTVALIDATION"] = __EVENTVALIDATION
form_data["ctl00$InnerContent$calFromDate$txt_Date"] = sdate
form_data["ctl00$InnerContent$calToDate$txt_Date"] = edate

print ("Downloading html page for requested date : " + sdate+"-"+edate)
r = session.post(URL, data=form_data)

def find_control_id(html_page):
	"""
	Finf correct ControlID for downloading exported files
	"""
	MAGIC_ID = "ctl00_InnerContent_reportViewer_ctl03"
	MAGIC_STRING = '$get("{id}")'.format(id=MAGIC_ID)
	lines = html_page.split("\n");

	required_line_no = None
	for (i, line) in enumerate(lines):
		if MAGIC_STRING in line:
			required_line_no = i
			break
	line = lines[i+1]
	parts = line.split('"')
	s = None
	for part in parts:
		if "ControlID" in part:
			s = part
			break
	parsed = urlparse.urlparse(s.replace("\\u0026", "&"))
	qp = urlparse.parse_qs(parsed.query)
	return qp["ControlID"][0]


def find_export_url(html_page, format="EXCEL"):
	"""
	Trickery to find export links -> PDF / EXCEL / WORD
	Figured out by looking at the js source & some luck (in case of format)

	Format values :
	1. PDF
	2. EXCEL (found with a bit of luck; this file is read successfully in ubuntu)
	"""
	MAGIC_STRING = "\/Reserved.ReportViewerWebControl\.axd\?Culture="

	s = BeautifulSoup(html_page, 'html.parser')
	imgs = s.find_all('img')
	url = None
	for img in imgs:
		if re.compile(MAGIC_STRING).search(img["src"]) is not None:
			url = img["src"]
			break
	#print url
	parsed_url = urlparse.urlparse(url)
	query_params = urlparse.parse_qs(parsed_url.query)
	p = query_params # for ease in typing

	export_base_url = "/Reserved.ReportViewerWebControl.axd?Culture={Culture}&CultureOverrides={CultureOverrides}&UICulture={UICulture}&UICultureOverrides={UICultureOverrides}&ReportStack={ReportStack}&ControlID={ControlID}&Mode={Mode}&OpType=Export&FileName={FileName}&ContentDisposition=OnlyHtmlInline&Format={Format}"
	export_filename = "Iex" # can use any filename; does not matter; so using default value

	ControlID = find_control_id(html_page)

	url = export_base_url.format(
			Culture = p["Culture"][0],
			CultureOverrides = p["CultureOverrides"][0],
			UICulture = p["UICulture"][0],
			UICultureOverrides = p["UICultureOverrides"][0],
			ReportStack = p["ReportStack"][0],
			ControlID = ControlID,
			Mode = p["Mode"][0],
			FileName = export_filename,
			Format = format
		)

	# Now join with base url
	return urlparse.urljoin(URL, url)

def download_file(url):
	"""
	Download exported file name
	Refer : https://stackoverflow.com/questions/34252553/downloading-file-in-python-with-requests
	"""
	r = session.get(url, stream=True)
	dl_filename = cgi.parse_header(r.headers['Content-Disposition'])[-1]['filename']

	print ("Downloading file : " + dl_filename)

	with open(dl_filename, 'wb') as f:
		r.raw.decode_content = True
		shutil.copyfileobj(r.raw, f)

	print ("Successfully downloaded [OK]")


# print find_export_url(r.text)
download_file(
	find_export_url(r.text, format)
)
