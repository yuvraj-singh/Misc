# https://www.instagram.com/graphql/query/?query_id=17859156310193001&id=289037519&first=91
import sys
import mechanize
from bs4 import BeautifulSoup
from subprocess import call
import requests
import json
import os

def get_userid(dict):
    userid = dict["entry_data"]["ProfilePage"][0]["user"]["id"]
    print "Successfully found userid"
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

def get_all_urls(id):
    print "Getting image urls .........."
    img_count = get_img_count(dict)
    # img_count = 20
    url  = "https://www.instagram.com/graphql/query/?query_id=17859156310193001&id=" + str(id) + "&first=" + str(img_count)
    r = session.get(url)
    cdict = json.loads(r.text)
    imgurl = cdict["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
    urls = []
    for i in range(0,img_count):
		urls.append(imgurl[i]["node"]["display_url"])
    print "Downloading " + str(img_count) + " images ................"
    return urls

def get_vid_urls(id):
    print "Getting video urls .........."
    img_count = get_img_count(dict)
    # img_count = 20
    url  = "https://www.instagram.com/graphql/query/?query_id=17859156310193001&id=" + str(id) + "&first=" + str(img_count)
    vsession = requests.Session()
    js = vsession.get(url)
    cdict = json.loads(js.text)
    imgurl = cdict["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
    urls = []
    for i in range(0,img_count):
        if imgurl[i]["node"]["is_video"] == True:
            urls.append("https://www.instagram.com/p/" + imgurl[i]["node"]["shortcode"] + "/")
    vurls = []
    vid_count = 0
    for url in urls:
        vsession1 = requests.Session()
        jss = vsession1.get(url)
        ss = BeautifulSoup(jss.text, 'html.parser')
        link = ss.find("meta", {"property" : "og:video:secure_url"})['content']
        vurls.append(link)
        vid_count = vid_count + 1
    print "Downloading " + str(vid_count) + " images ................"
    return vurls

def download(urls):
	for url in urls:
		os.system("mkdir " + username)
		cwd = os.getcwd()
		path = cwd + "/" + username
		os.system("wget -P " + username + " " + url)
if len(sys.argv) == 1:
    print "username required to run the program"
else:
    session = requests.Session()
    mainurl = "https://www.instagram.com/"
    username = sys.argv[1]
    url  = mainurl + username
    r = session.get(url)
    s = BeautifulSoup(r.text, 'html.parser')
    # print r.text
    script = s.findAll('script')[3].text
    script = script[len("window._sharedData = "):-1]
    # print script
    dict = json.loads(script)
    print "Json with latest image url loaded"

    if len(sys.argv) >= 3:
        if sys.argv[2] == "video" :
            download(get_all_urls(get_userid(dict)))
            print "Finished Downloading images ....."
            download(get_vid_urls(get_userid(dict)))
            print "Finished Downloading videos ....."
        else:
            download(get_all_urls(get_userid(dict)))
            print "Finished Downloading"
    else:
        download(get_all_urls(get_userid(dict)))
        print "Finished Downloading"
