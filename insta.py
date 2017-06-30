# https://www.instagram.com/graphql/query/?query_id=17859156310193001&id=289037519&first=91
import sys
import mechanize
from bs4 import BeautifulSoup
from subprocess import call
import requests
import json
import os

session = requests.Session()
mainurl = "https://www.instagram.com/"
username = sys.argv[1]
url  = mainurl + username
r = session.get(url)
s = BeautifulSoup(r.text, 'html.parser')
script = s.findAll('script')[3].text
script = script[len("window._sharedData = "):-1]
dict = json.loads(script)
print "Json with image url loaded"

def get_userid(dict):
    userid = dict["entry_data"]["ProfilePage"][0]["user"]["id"]
    return userid

def get_img_count(dict):
    img_count = dict["entry_data"]["ProfilePage"][0]["user"]["media"]["count"]
    return img_count

def get_latesturls(dict):
	imgurl = dict["entry_data"]["ProfilePage"][0]["user"]["media"]["nodes"]
	urls = []
	img_count = get_img_count(dict)
	if img_count > 12:
		img_count = 12
	for i in range(0,img_count):
		urls.append(imgurl[i]["display_src"])
	return urls

def get_allurls(id):
    img_count = get_img_count(dict)
    url  = "https://www.instagram.com/graphql/query/?query_id=17859156310193001&id=" + str(id) + "&first=" + str(img_count)
    r = session.get(url)
    cdict = json.loads(r.text)
    imgurl = cdict["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
    urls = []
    for i in range(0,img_count):
		urls.append(imgurl[i]["node"]["display_url"])
    return urls

def download(urls):
	for url in urls:
		os.system("mkdir " + username)
		cwd = os.getcwd()
		path = cwd + "/" + username
		os.system("wget -P " + username + " " + url)


download(get_allurls(get_userid(dict)))
# download(get_latesturls(dict))
