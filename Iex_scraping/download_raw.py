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
date = "20/05/2017" # default date
if len(sys.argv) >= 2:
	date = sys.argv[1]

format = "EXCEL"
if len(sys.argv) >= 3:
	format = sys.argv[2]
###

# Load default form data
with open(FORM_DATA_FILENAME) as f:
	form_data = json.load(f)

session = requests.Session()
print ("Downloading source html page for fetching request parameters..." )
r = session.get(URL)
s = BeautifulSoup(r.text, 'html.parser')

# Dynamic form parameter
__VIEWSTATE = s.find('input', {"name": "__VIEWSTATE"})["value"]
__VIEWSTATEGENERATOR = s.find('input', {"name": "__VIEWSTATEGENERATOR"})["value"]
__EVENTVALIDATION = s.find('input', {"name": "__EVENTVALIDATION"})["value"]

form_data["__VIEWSTATE"] = __VIEWSTATE
form_data["__VIEWSTATEGENERATOR"] = __VIEWSTATEGENERATOR
form_data["__EVENTVALIDATION"] = __EVENTVALIDATION
form_data["ctl00$InnerContent$calFromDate$txt_Date"] = date
form_data["ctl00$InnerContent$calToDate$txt_Date"] = date

print ("Downloading html page for requested date : " + date)
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
	2. EXCEL (found with a bit of luck; this file is read successfully in mac)
	3. EXCELOPENXML (used in html source -> $find('ctl00_InnerContent_reportViewer').exportReport ; but returned file opens as empty in mac)
	4. WORDOPENXML (not checked)
	"""
	MAGIC_STRING = "\/Reserved.ReportViewerWebControl\.axd\?Culture=" # Could not find this in source & not sure how this is generated; but found this by inspecting the live page in develper console
	# ^ ExportUrlBase; found using `$find('ctl00_InnerContent_reportViewer')._getInternalViewer().ExportUrlBase`
	# ^ would get "/Reserved.ReportViewerWebControl.axd?Culture=1033&CultureOverrides=True&UICulture=1033&UICultureOverrides=True&ReportStack=1&ControlID=3bc60cb2913d4c19af05a04b579480a9&Mode=true&OpType=Export&FileName=PriceMinute&ContentDisposition=OnlyHtmlInline&Format="
	# ^ Guess is that parameters are dynamic; so searched the html returned and found similar url there, so can get the parameters form there..
	# In file : https://www.iexindia.com/Reserved.ReportViewerWebControl.axd?OpType=Resource&Version=11.0.3452.0&Name=ViewerScript
	# ^ If need be can figure out how ExportUrlBase is generated

	# This is found in one IMG tag
	s = BeautifulSoup(html_page, 'html.parser')
	imgs = s.find_all('img')
	url = None
	for img in imgs:
		if re.compile(MAGIC_STRING).search(img["src"]) is not None:
			url = img["src"]
			break
	# print url
	parsed_url = urlparse.urlparse(url)
	query_params = urlparse.parse_qs(parsed_url.query)
	p = query_params # for ease in typing

	export_base_url = "/Reserved.ReportViewerWebControl.axd?Culture={Culture}&CultureOverrides={CultureOverrides}&UICulture={UICulture}&UICultureOverrides={UICultureOverrides}&ReportStack={ReportStack}&ControlID={ControlID}&Mode={Mode}&OpType=Export&FileName={FileName}&ContentDisposition=OnlyHtmlInline&Format={Format}"
	export_filename = "PriceMinute" # can use any filename; does not matter; so using default value
	
	# Also controlID is not correct
	# Need to find correct controlID
	# secret is in -> ctl00_InnerContent_reportViewer_ctl03
	# Found using :
	# $find('ctl00_InnerContent_reportViewer')._getInternalViewer
	# > function (){var a=this._tryGetInternalViewer();if(a==null||this.get_isLoading())throw Error.invalidOperation("The report or page is being updated.  Please wait for the current action to complete.");return a}
	# $find('ctl00_InnerContent_reportViewer')._tryGetInternalViewer
	# > function (){if(this._internalViewerId!=null){var a=$get(this._internalViewerId);if(a!=null)return a.control}return null}
	# $find('ctl00_InnerContent_reportViewer')._internalViewerId
	# > "ctl00_InnerContent_reportViewer_ctl03"
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
