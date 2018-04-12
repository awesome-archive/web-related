#! python3
# -*- coding: utf-8 -*-
import time
import requests
from pyquery import PyQuery as Pq
import xml.etree.cElementTree as ET
from py2neo import Graph, Node, Relationship
from pymongo import MongoClient
from headers import headers


time_param = time.time() * 1000
basic_info_url = 'http://renwu.hexun.com/figure_{}.shtml'
basic_net_url = 'http://renwu.hexun.com/dp/GetRelationFlash.ashx?fp_id={}&flag=1&t={}'
example_info_url = basic_info_url.format(1458)
example_net_url = basic_net_url.format(1458, time_param)
client = MongoClient('localhost', 27017)
db = client['knowledge_graph']


def get_info():
    r = requests.get(example_net_url, headers=headers)
    r.encoding = 'utf-8'
    return r.text


def divide_info(xml_str):
    # print(xml_str)
    tree = ET.fromstring(xml_str)
    center = []
    for elem in tree.iter(tag='USER'):
        center_dict = elem.attrib
        center.append(center_dict)

    fringe = []
    for elem in tree.iter(tag='Item'):
        fringe_dict = elem.attrib
        fringe.append(fringe_dict)
    return center, fringe


def extract_info():
    collection = db['figure_info']
    r = requests.get(example_info_url, headers=headers)
    r.encoding = None
    d = Pq(r.text)
    res = {}
    for item in d('.setBase .right ul li').items():
        # print(item.text().split('：'))
        info_list = item.text().split('：')
        info_key = info_list[0].replace('\u3000\u3000', '')
        info_value = info_list[1]
        res[info_key] = info_value

    for item in d('.main .contBox').items():
        info_key = item('h3 div').text()
        info_value = item('.cont p').text()
        res[info_key] = info_value
    print(res)
    collection.insert_one(res)


def draw_graph(center, fringe):
    # print(center)
    # print(fringe)
    test_graph = Graph('http://localhost:7474', username='test', password='test')
    tx = test_graph.begin()
    root = Node("Person", name=center[0]['name'], gender="M")
    tx.create(root)
    leaves = {}
    for elem in fringe:
        leaves[elem['name']] = [Node("Person", name=elem['name'], gender="M"), elem['Contact']]
        elem['name'] = Node("Person", name=elem['name'], gender="M")
        tx.create(elem['name'])

        link = Relationship(root, elem['Contact'], elem['name'])
        tx.create(link)

    tx.commit()

    # print(root)
    # print(leaves)


if __name__ == '__main__':
    extract_info()
    # a, b = divide_info(get_info())
    # draw_graph(a, b)
    # print(a, b)
    # extract_info()
    # test_graph = Graph('http://localhost:7474', username='test', password='test')
    # a = Node('Person', name='Alice')
    # b = Node('Person', name='Bob')
    # r = Relationship(a, 'KNOWS', b)
    # print(a, b, r)
    # tx = test_graph.begin()
    # john = Node("User", name="John", gender="M", age="28")
    # tx.create(john)
    #
    # mary = Node("User", name="Mary", gender="F", age="26")
    # tx.create(mary)
    #
    # jm = Relationship(john, "FRIENDS_WITH", mary)
    # tx.create(jm)
    #
    # tx.commit()
