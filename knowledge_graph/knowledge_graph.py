#! python3
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import xml.etree.cElementTree as Et
from py2neo import Graph, Node, Relationship
from collections import Counter
from fnvhash import fnv1_32

# mongodb配置
client = MongoClient('localhost', 27017)
db = client['knowledge_graph']
figure_graph_info = db['figure_graph_info']

# neo4j配置
knowledge_graph = Graph('http://localhost:7474', username='knowledge_graph', password='1234')


def create_root_node():
    """
    1. 创建根结点，必须加上名字和id两个属性
    :return:
    """
    for record in figure_graph_info.find():
        graph = knowledge_graph.begin()
        tree_xml = record['tree']
        tree = Et.fromstring(tree_xml)

        for node in tree.iter(tag='USER'):
            center_dict = node.attrib
            print(center_dict)
            root_id = center_dict['id']
            root_name = center_dict['name']
            print(root_id)
            print(root_name)
            root = Node("Person", name=root_name, id=root_id)
            graph.create(root)
            graph.commit()


def create_leaf_zero_node():
    """
    1. 首先叶子结点中不为'0'的结点肯定已经在根结点中了
    2. 那么只需要去创建id为'0'的结点就可以了
    3. 但id为'0'的结点由于id都是相同的，首先要根据名字去重，然后再创建独特的id
    4. 如果原本的id不为'0', 则id信息不变， 如果原本id为'0'，则将id更新过后保存到mongodb中
    :return:
    """
    unique = set()
    for record in figure_graph_info.find():
        tree_xml = record['tree']
        tree = Et.fromstring(tree_xml)

        for node in tree.iter(tag='Item'):
            fringe_dict = node.attrib
            if fringe_dict['id'] == '0':
                graph = knowledge_graph.begin()
                # id为'0'的结点必定不在之前的图数据库中
                leaf_name = fringe_dict['name']
                leaf_desc = fringe_dict['desc']
                if leaf_name not in unique:
                    # 如果leaf_name不在set里面，说明是独特的，就可以在图数据库中创建
                    # 创建之前先要生成uuid， 把uuid也加入到图数据库的属性中
                    # 创建完了之后可以将名字加入set中，来达到去重的目的
                    leaf_id = fnv1_32(str.encode(leaf_name))
                    print(leaf_id)
                    print(leaf_name)
                    if len(leaf_desc) > 0:
                        print(leaf_desc)
                        leaf = Node("Person", name=leaf_name, id=leaf_id, desc=leaf_desc, fake=True)
                    else:
                        leaf = Node("Person", name=leaf_name, id=leaf_id, fake=True)
                    # 增加一个新的字段fake,为了标识网页新增进来的结点
                    graph.create(leaf)
                    graph.commit()
                    unique.add(leaf_name)


def create_relationship():
    """
    1. 创建完了所有的具有独特id的结点后开始建立连接
    2. 遍历xml的结点关系，通过查根结点的id与叶子结点的id建立关系
    3. 去mongodb中顺序查找根结点，去查图形数据库，然后先找到根结点，再去找叶子结点，创建关系
    :return:
    """
    for record in figure_graph_info.find():
        graph = knowledge_graph.begin()
        tree_xml = record['tree']
        tree = Et.fromstring(tree_xml)

        for node in tree.iter(tag='USER'):
            center_dict = node.attrib
            root_id = center_dict['id']
            knowledge_graph.find_one(label='Person', property_key='id', property_value=root_id)

        for node in tree.iter(tag='Item'):
            fringe_dict = node.attrib
            if fringe_dict:
                leaf_name = fringe_dict['name']
                knowledge_graph.find_one(label='Person', property_key='name', property_value=leaf_name)
                contact = fringe_dict['Contact']
                link = Relationship()


if __name__ == '__main__':
    create_root_node()
    print('-----------------------')
    create_leaf_zero_node()
