# !/usr/bin/env python

# MIT License
#
# Copyright (c) 2017 Hanlin He
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__author__ = "Hanlin He"
__copyright__ = "Copyright 2017, Hanlin He"
__license__ = "MIT License"
__version__ = "1.0.0"
__maintainer__ = "Hanlin He"
__email__ = "hanling.he@gmail.com"
__status__ = "Development"

from _thread import interrupt_main
from sys import argv
from threading import Thread
from time import sleep

from topology import Topology


class Controller:

    def __init__(self, _network_conf=None):
        self.topology = Topology(_network_conf)
        self._update_topology_thread = Thread(target=self._update_topology,
                                              args=())
        # print("Topology file is parsed as:\n{}\n".format(self.topology.topo))
        # for i in self.topology.topo:
        # self.topology.update(i)
        # print("Topology at timestamp {} is:\n{}\n".format(i,
        # self.topology.get_current_topology()))

    def _update_topology(self):
        for i in range(125):
            self.topology.update(i)
            sleep(1)
        interrupt_main()

    def _broadcast_message(self, dsts, msg):
        """Copy msg to all node in dsts.
        Simply call unicast_message function for all dst in dsts.
        """
        for dst in dsts:
            self._unicast_message(dst, msg)

    def _unicast_message(self, dst, msg):
        """Copy msg to specific dst."""
        with open("to" + dst + ".txt", "a") as toX:
            toX.write(msg)

    def _forward_message(self, dsts, msg):
        if msg[0] == '*':
            self._broadcast_message(dsts, msg)
        else:
            self._unicast_message(msg[0], msg)

    def _follow_from_file(self, senders):
        file_handler = dict()
        for node in senders:
            filename = 'from' + node + '.txt'
            try:
                thefile = open(filename, "r")
                thefile.seek(0, 2)
            except IOError:
                open(filename, 'w').close()
                thefile = open(filename, "r")
            file_handler[node] = thefile

        while True:
            for node in senders:
                line = file_handler[node].readline()
                if not line:
                    continue
                yield node, line
            try:
                sleep(0.1)
            except TypeError:
                break

    def start(self):
        self._update_topology_thread.start()
        messages = self._follow_from_file(self.topology.sender)
        try:
            for sender, message in messages:
                self._forward_message(self.topology.get_connected_node(sender),
                                      message)
        except KeyboardInterrupt:
            print("END.")


def main():
    c = Controller() if len(argv) == 1 else Controller(argv[1])
    c.start()


if __name__ == '__main__':
    main()
