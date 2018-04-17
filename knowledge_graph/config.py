#! python3
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from py2neo import Graph

# mongodb配置
client = MongoClient('localhost', 27017)
db = client['knowledge_graph']
figure_graph_info = db['figure_graph_info']

# neo4j配置
knowledge_graph = Graph('http://localhost:7474', username='test', password='1234')


__all__ = [db, client, figure_graph_info, knowledge_graph]