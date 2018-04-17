#! python3
# -*- coding: utf-8 -*-
import re
import time
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
import requests
from pyquery import PyQuery as Pq
from headers import headers
from config import client, db

time_param = time.time() * 1000
all_pages = ['http://renwu.hexun.com/search.aspx?z=All&Filter=All&page={}'.format(i) for i in range(1, 324)]
basic_net_url = 'http://renwu.hexun.com/dp/GetRelationFlash.ashx?fp_id={}&flag=1&t={}'


def send_request(url):
    r = requests.get(url, headers=headers)
    d = Pq(r.text)
    urls = [i.attr('href') for i in d('.slistBox ul li a').items()]
    return urls


def concurrent():
    collection = db['figure_url']
    pool = Pool(processes=cpu_count())
    urls = pool.map(send_request, all_pages)
    print(urls)
    pool.close()
    pool.join()
    for item in urls:
        for url in item:
            print(url)
            collection.insert_one({'url': url})
    return urls


def extract_info():
    figure_url = db['figure_url']
    figure_info = db['figure_info']

    for elem in figure_url.find():
        url = elem['url']
        print(url)
        r = requests.get(url, headers=headers)
        r.encoding = None
        d = Pq(r.text)
        res = {}
        for item in d('.setBase .right ul li').items():
            if len(item.text()):
                info_list = item.text().split('：')
                if len(info_list) == 2:
                    info_key = info_list[0].replace('\u3000\u3000', '')
                    info_value = info_list[1]
                    res[info_key] = info_value

        for item in d('.main .contBox').items():
            info_key = item('h3 div').text()
            info_value = item('.cont p').text()
            res[info_key] = info_value

        figure_info.insert_one(res)


def extract_graph_info():
    figure_url = db['figure_url']
    figure_graph_info = db['figure_graph_info']
    for elem in figure_url.find():
        url = elem['url']
        print(url)
        url_number = re.findall(r'figure_\d+', url)[0].replace('figure_', '')
        net_url = basic_net_url.format(url_number, time_param)
        r = requests.get(net_url, headers=headers)
        r.encoding = 'utf-8'
        print(type(r.text))
        figure_graph_info.insert_one({'tree': r.text})


if __name__ == '__main__':
    concurrent()
    extract_info()
    extract_graph_info()
