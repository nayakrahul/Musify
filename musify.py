from googlesearch import search
from threading import Thread
from bs4 import BeautifulSoup
from clint.textui import progress
import urllib2
import requests
import sys
import os
import time
import itertools


flag = 0


def progess():
    global flag
    sys.stdout.write("Searching...")
    for c in itertools.cycle('/-\|'):
        sys.stdout.write('\r\t\t' + c)
        sys.stdout.flush()
        time.sleep(0.2)
        if flag:
            break


def play_song(file_path):
    reply = raw_input("Do you want to play the song?(Y/N)")
    if reply == 'Y' or reply == 'y':
        cli = 'play ' + '"' + file_path + '"'
        os.system(cli)
    elif reply == 'N' or reply == 'n':
        return
    else:
        play_song(file_path)


def parse_url(url):
    parse_url_components = url.split('//')
    components = parse_url_components[1].split('/')
    return components


def download_song(download_url):
    file_name = download_url.split('/')[-1]
    music_path = os.path.expanduser('~') + "/Music"
    file_path = os.path.join(music_path, file_name)
    r = requests.get(download_url, stream=True)
    with open(file_path, 'wb') as f:
        global flag
        flag = 1
        sys.stdout.write("\t[DONE]\n")
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(
                chunk_size=1024), expected_size=(total_length / 1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
    return file_path, file_name


def get_download_link(song_url, keyword):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(song_url, headers=hdr)
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response, "lxml")
    # print soup.prettify()
    for link in soup.find_all('a'):
        if link.find(keyword) != -1:
            download_url = link.get('href')
            if download_url.split('.')[-1] == 'mp3':
                return download_url
    return


def google_search(search_term, keyword):
    search_term = search_term + keyword[0]
    song_url = ''
    for url in search(search_term, lang='en', stop=1):
        components = parse_url(url)
        print(url)
        if components[0] == keyword[1] and components[1].find(
                keyword[2]) != -1:
            song_url = url
            return song_url
    return None


def search_song(search_term):
    # song_url_mp3mad = google_search(
    #     search_term, [
    #         " mp3 download mp3mad", "mp3mad.site", "download"])
    song_url_mp3mad = None
    song_url_pagal = google_search(
        search_term, [
            " mp3 download pagalworld", "pagalworld.info", "kbps"])
    # song_url_pagal = None
    # song_url_jatt = google_search(
    #     search_term, [
    #         " mp3 download mr jatt", "mr-jatt.com", "download"])
    song_url_jatt = None
    
    if song_url_mp3mad:
        return song_url_mp3mad, "Download In High Quality"
    if song_url_pagal:
        return song_url_pagal, "[ Download File ]"
    if song_url_jatt:
        return song_url_jatt, "Download in 128 kbps"
    else:
        global flag
        flag = 1
        sys.stdout.write("\tFailed !!\n")
        sys.exit()


def start(search_term):
    song_url, keyword = search_song(search_term)
    download_url = get_download_link(song_url, keyword)
    file_path, file_name = download_song(download_url)
    sys.stdout.write(file_name + " saved to Music !!\n")
    play_song(file_path)


if __name__ == '__main__':
    try:
        t1 = Thread(target=progess, args=())
        t1.start()
        t2 = Thread(target=start, args=(sys.argv[1],))
        t2.start()
    except BaseException:
        print("Error: unable to start thread")
