import pprint
from state_generator import StateGenerator
from graph import Graph


def main():
    generator = StateGenerator()
    states, paths = generator.generate()

    pprint.pprint(states)
    pprint.pprint(paths)

    graph = Graph(states, paths)
    graph.render_graph()
    # print len(states)


if __name__ == '__main__':
    main()
