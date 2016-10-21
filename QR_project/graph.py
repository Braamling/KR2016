# import networkx as nx
import webbrowser
from random import randint
import json


class Graph():
    def __init__(self, states, paths):
        self.edges = paths
        self.nodes = states

    def render_graph(self):
        self.store_json_graph()
        print "Opening webbrowser - http://localhost:8000"
        webbrowser.open('http://localhost:8000')

    def store_json_graph(self):
        graph = {'nodes': [], 'edges': []}

        for node in self.nodes:
            graph['nodes'].append({'title': node.to_string(),
                                   'id': node.get_id(),
                                   'x': node.get_id() * 75,
                                   'y': randint(0,1200)})

        for edge in self.edges:
            graph['edges'].append({'source': edge[0].get_id(),
                                   'target': edge[1].get_id()})

        with open('result.json', 'w') as fp:
            json.dump(graph, fp)



    def __eq__(self, other):
        return (self.get_quantity() is other.get_quantity() and
                self.get_derivitive() is other.get_derivitive())
