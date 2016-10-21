import pprint
from state_generator import StateGenerator
from bonus_state_generator import BonusStateGenerator
from graph import Graph

import logging


def create_graph():
    init_logging()

    generator = StateGenerator()
    states, paths = generator.generate()

    pprint.pprint(states)
    pprint.pprint(paths)

    graph = Graph(states, paths)
    graph.render_graph()


def create_bonus_graph():
    init_logging()

    generator = BonusStateGenerator()
    states, paths = generator.generate()

    # print "[trace] - Generated states:"
    # pprint.pprint(states)

    # print "[trace] - Generated paths:"
    # pprint.pprint(paths)

    graph = Graph(states, paths)
    graph.render_graph()


def init_logging():
    FORMAT = '%(asctime)-15s - %(method)s - %(message)s'
    logging.basicConfig(format=FORMAT)
    d = {'method': 'init_logging()'}
    logger = logging.getLogger('trace')
    logger.setLevel(20)
    logger.info('Trace initiated', extra=d)


def main():
    # create_graph()
    create_bonus_graph()
    # print len(states)


if __name__ == '__main__':
    main()
