#!/usr/local/bin/python3.6

import argparse
import http.client as httplib
import json
import logging
import sys
import time
import traceback

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("{0}/{1}.log".format('./log', 'edge'))
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)


class Edge():
    def __init__(self, ip, port, file):
        self.ip = ip
        self.port = port
        self.con = None
        self.stop = False
        self.file = './data/' + file + '.json'
        self.id = None
        self.name = None,
        self.status = 'ok',
        self.workload = {}
        self.contents = set()

    def get_content(self, contentId):
        log.debug("Get content:" + contentId)
        con = httplib.HTTPConnection(self.ip, self.port)
        con.request('GET', '/content/' + contentId)
        res = con.getresponse()
        return res.read().decode("utf-8")

    def report_status(self):
        log.debug("Retport status: {} {}".format(self.workload, self.contents))
        con = httplib.HTTPConnection(self.ip, self.port)
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        status = {
            'name': self.name,
            'status': self.status,
            'workload': self.workload,
            'contents': list(self.contents),
        }
        log.debug(json.dumps(status))
        con.request("POST", "/edge/status_report/" + self.id,
                    json.dumps(status), headers)

    def run(self):
        while(not self.stop):
            data = json.load(open(self.file))
            edge_id = list(data.keys())[0]
            edge = data[edge_id]
            self.set_edge(edge_id, edge)
            self.report_status()
            time.sleep(30)

    def set_edge(self, id, data):
        self.id = id
        self.name = data['name']
        self.status = data['status'],
        self.workload = data['workload']
        self.contents = data['contents']

def main():
    usage = 'Usage: edge.py -a <server_address> -o <server_port> -f <config>'

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', action='store', dest='host')
    parser.add_argument('-p', action='store', dest='port')
    parser.add_argument('-f', action='store', dest='file')
    arg = parser.parse_args()

    if arg.host is None or arg.port is None or arg.file is None:
        log.error(usage)
        sys.exit(2)

    edge = Edge(arg.host, arg.port, arg.file)
    try:
        edge.run()
    except Exception as e:
        log.error(e)
        traceback.print_exc()
        sys.exit(2)

if __name__ == '__main__':
    main()
