from random import randint
import logging

THRESHOLD = 90

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("{0}/{1}.log".format('./log', 'client'))
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)


class Edges(object):
    instance = None

    def __init__(self):
        self.edges = {}         # map of edge_id: { edge status}
        self.contents = {}      # map of content_id: (edge set that can serve)

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def update_edge(self, id, edge):
        log.info('Update edge: {}'.format(edge))

        self.renew_edge_status(edge)
        if edge['status'][0] == 'ok':
            new_contents_set = set(edge['contents'])
        else:
            new_contents_set = set()

        old_edge = self.edges.get(id, None)
        if old_edge is None or old_edge['status'][0] != 'ok':
            old_contents_set = set()
        else:
            old_contents_set = set(self.edges[id]['contents'])

        # update cached content map.

        self.remove_content(id, old_contents_set - new_contents_set)
        self.add_content(id, new_contents_set - old_contents_set)
        self.edges[id] = edge

    def get_edge(self, content_id):
        #todo(duan): to keep client connect the same edge, can use hashcode of
        #of the ip:port to select edge.
        log.debug('find {} in {}'.format(content_id, self.contents))
        candidates = self.contents.get(content_id, [])
        length = len(candidates)
        if len(candidates) == 0:
            return None
        else:
            return candidates[randint(0, length-1)]

    def remove_content(self, edge_id, contents):
        log.debug('Remove contents: {}'.format(contents))
        for content in contents:
            edges = self.contents.get(content, [])
            if edge_id in edges:
                edges.remove(edge_id)

    def add_content(self, edge_id, contents):
        log.debug('Add contents: {}'.format(contents))
        for content in contents:
            edges = self.contents.get(content, [])
            edges.append(edge_id)
            self.contents[content] = edges

    def renew_edge_status(self, edge):
        if edge['status'][0] != 'ok':
            return

        for _, value in edge['workload'].items():
            if value > THRESHOLD:
                edge['status'] = 'overload'
                log.info('Edge: ' + edge['name'] + ' overload!')
                break

        #todo: add failure rate
