#! python3
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import xml.etree.cElementTree as Et
from py2neo import Graph
from collections import Counter

# mongodb配置
client = MongoClient('localhost', 27017)
db = client['knowledge_graph']
figure_graph_info = db['figure_graph_info']

# neo4j配置
knowledge_graph = Graph('http://localhost:7474', username='knowledge_graph', password='1234')


def count_root_name():
    """
    看root结点中名字是否有重复的
    :return:
    """
    names = []
    for record in figure_graph_info.find():
        tree_xml = record['tree']
        tree = Et.fromstring(tree_xml)

        for node in tree.iter(tag='USER'):
            center_dict = node.attrib
            names.append(center_dict['name'])

    counts = Counter(names)
    print(counts)
    return counts


def count_root_id():
    """
    看root结点中id是否有重复的
    :return:
    """
    identifier = []
    for record in figure_graph_info.find():
        tree_xml = record['tree']
        tree = Et.fromstring(tree_xml)

        for node in tree.iter(tag='USER'):
            center_dict = node.attrib
            identifier.append(center_dict['id'])

    counts = Counter(identifier)
    print(counts)
    return counts


def count_leaf_name():
    """
    看leaf结点中名字是否有重复的
    :return:
    """
    names = []
    for record in figure_graph_info.find():
        tree_xml = record['tree']
        tree = Et.fromstring(tree_xml)

        for node in tree.iter(tag='Item'):
            fringe_dict = node.attrib
            names.append(fringe_dict['name'])

    counts = Counter(names)
    print(counts)
    return counts


def count_leaf_id():
    """
    看leaf结点中id是否有重复的
    :return:
    """
    identifier = []
    for record in figure_graph_info.find():
        tree_xml = record['tree']
        tree = Et.fromstring(tree_xml)

        for node in tree.iter(tag='Item'):
            fringe_dict = node.attrib
            identifier.append(fringe_dict['id'])

    counts = Counter(identifier)
    print(counts)
    return counts


"""
结论：
1. 根结点中结点都是唯一的，但名字有可能是重复的，所以构建结点时要加上id这一属性
2. 叶子节点中的结点不是唯一的，而且名字, id都是重复的，而且id为'0'的是还没有收录到网站里面的
3. 所以第一步应该去创建根节点，要把id属性带上
"""


if __name__ == '__main__':
    # count_root_name()
    # count_root_id()
    # count_leaf_name()
    # count_leaf_id()
    # from fnvhash import fnv1_32
    # print(fnv1_32(str.encode('邹家华')))

    unique = set()
    info1 = {'name': '迈克尔·穆伦', 'id': '0', 'Contact': '同事', 'link': '', 'img': '../img/default/s_f.gif', 'desc': '第28任美国海军作战部长'}
    info2 = {'name': '弗农·克拉克', 'id': '0', 'Contact': '同事', 'link': '', 'img': '../img/default/s_f.gif', 'desc': '第27任美国海军作战部长'}

