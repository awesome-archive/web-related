#! python3
# -*- coding: utf-8 -*-
from py2neo import Relationship
import xml.etree.cElementTree as Et
from config import figure_graph_info, knowledge_graph


def create_link():
    for record in figure_graph_info.find():
        tree_xml = record['tree']
        tree = Et.fromstring(tree_xml)

        root_id = []
        for node in tree.iter(tag='USER'):
            center_dict = node.attrib
            root_id.append(center_dict['id'])

        for node in tree.iter(tag='Item'):
            graph = knowledge_graph.begin()
            fringe_dict = node.attrib
            if bool(fringe_dict):
                leaf_name = fringe_dict['name']
                leaf_id = fringe_dict['id']
                root_leaf_contact = fringe_dict['Contact']
                existing_root_node = knowledge_graph.find_one('Person', property_key='id', property_value=root_id[0])
                if leaf_id == '0':
                    # 如果是没有收录网站的人名，通过人名去查询
                    existing_leaf_node = knowledge_graph.find_one('Person', property_key='name',
                                                                  property_value=leaf_name)
                    link = Relationship(existing_root_node, root_leaf_contact, existing_leaf_node)
                    graph.create(link)
                    print(leaf_id, leaf_name)
                else:
                    # 如果本来就是已经收录进网站的人名，通过id去查询
                    existing_leaf_node = knowledge_graph.find_one('Person', property_key='id',
                                                                  property_value=leaf_id)
                    link = Relationship(existing_root_node, root_leaf_contact, existing_leaf_node)
                    graph.create(link)
                    print(leaf_id, leaf_name)
                graph.commit()
            else:
                continue


if __name__ == '__main__':
    create_link()
