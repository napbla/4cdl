from urlparse import urlparse
import argparse
import httplib
import urllib2
import re
import time
import json
import os
import threading

sleep_time = 10
wait_thread_sleep_time = 2
cache_string = "Run out of free thread. Retry after" + \
                str(wait_thread_sleep_time) + "second"
number_of_thread = 10


class downloadThread (threading.Thread):
    def __init__(self, url, folder):
        threading.Thread.__init__(self)
        self.url = url
        self.folder = folder

    def run(self):
        print "Starting download thread for " + self.url
        download(self.url, self.folder)
        print "Exiting download thread for " + self.url


def download(url, folder):
    file_name = '.\\' + folder + '\\' + url.split('/')[-1]
    if not os.path.exists('.\\' + folder + '\\'):
        os.makedirs('.\\' + folder + '\\')

    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url, None, headers)
    u = urllib2.urlopen(req)
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])

    # Check if file is already downloaded
    if os.path.isfile(file_name) and file_size == os.stat(file_name).st_size:
        print "File "+file_name+" is already downloaded"
        return

    # Begin download
    file_size_dl = 0
    block_sz = 1024
    with open(file_name, 'wb') as f:
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r" [%3.2f%%]" % (file_size_dl * 100. / file_size)
            print "Downloading:" + file_name + status


def check_thread(board, sid):
    prev_img_list = []
    while True:
        myConnection = httplib.HTTPSConnection(
            "a.4cdn.org")
        myConnection.request("GET", "/" + board + "/thread/" + sid + ".json")
        reply = myConnection.getresponse()
        print reply.status, reply.reason
        if reply.status == 404:
            print "404 Not found. Please check the URL again!"
            break
        temp_json = reply.read()
        img_list = re.findall(r'"filename":".+?".+?"tim":.+?,', temp_json)
        if not os.path.exists('.\\' + board + sid + '\\'):
            os.makedirs('.\\' + board + sid + '\\')
        with open('.\\' + board + sid + '\\' + sid + ".json", 'wb') as f:
            f.write(temp_json)
        # Print img_list
        myConnection.close()
        for i in img_list[len(prev_img_list):]:
            j = json.loads('{'+i[:-1]+'}')
            download_link = \
                "http://i.4cdn.org/" + board + "/" + str(j['tim']) + j['ext']
            print download_link
            while (threading.activeCount() == number_of_thread):
                print cache_string
                time.sleep(wait_thread_sleep_time)
            downloadThread(download_link, board + sid).start()
        prev_img_list = img_list
        time.sleep(sleep_time)


def parse_thread_URL(url):
    url_components = urlparse(url).path.split('/')
    return url_components[1], url_components[3]


prog_description = 'Download all images and json of a 4chan thread until '\
                'thread dies. Resume and multi-thread download supported.'\
                'From json and the images, the original html can be generated.'
parser = argparse.ArgumentParser(description=prog_description)
parser.add_argument('threadURL', metavar='Thread_URL',
                    help='The thread URL for example '
                    'http://boards.4chan.org/biz/thread/1873336', default=10)
parser.add_argument('-t', '--thread_num', metavar='number',
                    help='The number of download thread, default is 10')
args = parser.parse_args()
number_of_thread = args.thread_num
board, thread_id = parse_thread_URL(args.threadURL)
check_thread(board, thread_id)
