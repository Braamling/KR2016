# import networkx as nx
import webbrowser
import csv


class Graph():
    def __init__(self, states, paths):
        self.edges = paths
        self.nodes = states

    def render_graph(self):
        self.store_graph()
        print "Opening webbrowser - http://localhost:8000"
        webbrowser.open('http://localhost:8000')

    def store_graph(self):
        with open('output.csv', 'w') as csvfile:
            fieldnames = ['source', 'target', 'value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for edge in self.edges:
                writer.writerow({'source': edge[0],
                                 'target': edge[1],
                                 'value': 5.0})

    def __eq__(self, other):
        return (self.get_quantity() is other.get_quantity() and
                self.get_derivitive() is other.get_derivitive())
