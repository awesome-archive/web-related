#! python3
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as Et
from collections import Counter
from config import figure_graph_info, knowledge_graph


"""
结论：
1. 根结点中结点都是唯一的，但名字有可能是重复的，所以构建结点时要加上id这一属性
2. 叶子节点中的结点不是唯一的，而且名字, id都是重复的，而且id为'0'的是还没有收录到网站里面的
3. 所以第一步应该去创建根节点，要把id属性带上
4. 叶子结点中非零id的结点并没有包含在所有根结点中，也就是说创建完根结点后，还要进行叶子非零结点的创建
"""


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


def count_nonzero_leaf():
    """
    :return:
    """
    root_collection = set()
    for record in figure_graph_info.find():
        tree_xml = record['tree']
        tree = Et.fromstring(tree_xml)

        for node in tree.iter(tag='USER'):
            center_dict = node.attrib
            root_collection.add(center_dict['id'])

    unique = set()
    result = []
    for record in figure_graph_info.find():
        tree_xml = record['tree']
        tree = Et.fromstring(tree_xml)

        for node in tree.iter(tag='Item'):
            fringe_dict = node.attrib
            leaf_id = fringe_dict['id']
            if leaf_id != '0' and leaf_id not in root_collection:
                if leaf_id not in unique:
                    result.append({'name': fringe_dict['name'], 'id': fringe_dict['id']})
                unique.add(fringe_dict['id'])
    return result


__all__ = [count_nonzero_leaf]

