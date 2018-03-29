#!/usr/local/bin/python3.6

import argparse
import http.client as httplib
import logging
import sys

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("{0}/{1}.log".format('./log', 'client'))
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)


class Client():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.con = None

    def get_content(self, contentId):
        log.debug("Get content:" + contentId)
        self.con = httplib.HTTPConnection(self.ip, self.port)
        self.con.request('GET', '/content/' + contentId)
        res = self.con.getresponse()
        return res.read().decode("utf-8")

    def close(self):
        if self.con is not None:
            self.con.close()

def main():
    usage = 'Usage: client.py -a <server_address> -o <server_port> -c <contentId>'

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', action='store', dest='host')
    parser.add_argument('-p', action='store', dest='port')
    parser.add_argument('-c', action='store', dest='content_id')
    arg = parser.parse_args()

    if arg.host is None or arg.port is None or arg.content_id is None:
        log.error(usage)
        sys.exit(2)

    client = Client(arg.host, arg.port)
    try:
        rsp = client.get_content(arg.content_id)
    except Exception as e:
        log.error(e)
        sys.exit(2)
    log.info('Access {} in {}'.format(arg.content_id, rsp))
    client.close()


if __name__ == '__main__':
    main()
