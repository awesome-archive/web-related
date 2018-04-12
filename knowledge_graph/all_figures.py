#! python3
# -*- coding: utf-8 -*-
import re
import time
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
import requests
from pyquery import PyQuery as Pq
import xml.etree.cElementTree as ET
from py2neo import Graph, Node, Relationship
from pymongo import MongoClient
from headers import headers


client = MongoClient('localhost', 27017)
db = client['knowledge_graph']
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
        # break


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
        # tree = ET.fromstring(r.text)
        # figure_graph_info.insert_one(tree)
        figure_graph_info.insert_one({'tree': r.text})
        # break


def build_graph():
    knowledge_graph = Graph('http://localhost:7474', username='knowledge_graph', password='1234')
    figure_graph_info = db['figure_graph_info']
    duplicate = set()
    names = []
    for item in figure_graph_info.find():
        tx = knowledge_graph.begin()
        tree = ET.fromstring(item['tree'])
        center = []
        for elem in tree.iter(tag='USER'):
            center_dict = elem.attrib
            center.append(center_dict)

        fringe = []
        for elem in tree.iter(tag='Item'):
            fringe_dict = elem.attrib
            fringe.append(fringe_dict)

        print(center)
        print(fringe)

        if center[0]['name'] not in duplicate:
            root = Node("Person", name=center[0]['name'], id=center[0]['id'])
            tx.create(root)
            duplicate.add(center[0]['name'])  # 将名字根结点的名字加入了set中, 来达到去重目的
            names.append(center[0]['name'])
            # print(knowledge_graph.find_one(label='Person', property_key='name', property_value=center[0]['name']))
            # debug: 如果打印出来，说明根结点已经存在于图数据库中了,返回结果是None
            if len(fringe) != 0:
                print(len(fringe))
                for elem in fringe:
                    if elem['name'] not in duplicate:
                        elem['name'] = Node("Person", name=elem['name'], id=elem['id'])
                        tx.create(elem['name'])
                        duplicate.add(elem['name'])  # 为了剔除后续for loop中的重复元素
                    # if not knowledge_graph.find_one(label='Person', property_key='id', property_value=elem['id']):
                    #     elem['name'] = Node("Person", name=elem['name'], id=elem['id'])
                    #     tx.create(elem['name'])

                    link = Relationship(root, elem['Contact'], elem['name'])  # 无论是否有重复都是要建立关系连接的
                    tx.create(link)
                    names.append(elem['name'])
                    print(names)
        # tx.commit()
        # print(knowledge_graph.find_one(label='Person', property_key='name', property_value=center[0]['name']))
        # debug: 如果打印出来，验证了必须commit完才会存在于图数据库中, 返回结果了，说明了必须commit()完，图数据库中才会创建结点
        # break


if __name__ == '__main__':
    # concurrent()
    # extract_info()
    # extract_graph_info()
    build_graph()
    # knowledge_graph = Graph('http://localhost:7474', username='knowledge_graph', password='1234')
    # print(knowledge_graph.match_one(start_node='阿罗'))
    # print(knowledge_graph.find_one(label='Person', property_key='name', property_value='科斯'))
    # tx = knowledge_graph.begin()
    # root = Node("Person", name='阿卜杜拉·阿勒沙特')
    # tx.create(root)
    # tx.commit()
