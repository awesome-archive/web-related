#! python3
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as Et
from py2neo import Node
from fnvhash import fnv1_32
from analyze_node import count_nonzero_leaf
from config import figure_graph_info, knowledge_graph


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


def create_nonzero_leaf_node():
    """
    1. 创建之前发现的id不为0而且不在根结点中的叶子结点
    :return:
    """
    nonzero_leaf = count_nonzero_leaf()
    for element in nonzero_leaf:
        graph = knowledge_graph.begin()
        leaf = Node("Person", name=element['name'], id=element['id'])
        graph.create(leaf)
        graph.commit()


def create_zero_leaf_node():
    """
    1. 创建id为0的叶子结点
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


if __name__ == '__main__':
    create_root_node()
    create_nonzero_leaf_node()
    create_zero_leaf_node()
