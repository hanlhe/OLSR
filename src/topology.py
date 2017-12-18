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

from copy import deepcopy
from threading import RLock


class Topology:
    _topology = dict()
    _lock = RLock()

    def __init__(self, _network_conf=None):
        self._topo = dict()
        self.sender = set()
        self.receiver = set()
        if _network_conf is None:
            _network_conf = "topology.txt"
        with open(_network_conf, "r") as netconf:
            for line in netconf:
                time, status, node1, node2 = line.split()
                i_time = int(time)
                self.sender.add(node1)
                self.receiver.add(node2)
                if i_time in self._topo:
                    self._topo[i_time] = (self._topo[i_time]
                                          + [(status, node1, node2)])
                else:
                    self._topo[i_time] = [(status, node1, node2)]

    def _add_link(self, node1, node2):
        """Add specific link to _topology."""
        if node1 in self._topology:
            self._topology[node1].add(node2)
        else:
            self._topology[node1] = {node2}

    def _del_link(self, node1, node2):
        """Delete specific link to _topology."""
        try:
            self._topology[node1].remove(node2)
            if self._topology[node1] == set():
                del sel._topology[node1]
        except KeyError:
            print("Invalid link to remove.")

    def update(self, timestamp):
        self._lock.acquire()
        try:
            for status, node1, node2 in self._topo[timestamp]:
                if status == 'UP':
                    self._add_link(node1, node2)
                    pass
                elif status == "DOWN":
                    self._del_link(node1, node2)
                    pass
                else:
                    print("Topology file is broken.")
        except KeyError:
            # print("No change at this time.")
            pass
        finally:
            self._lock.release()

    def get_connected_node(self, sender):
        return self._topology[sender]

    def get_current_topology(self):
        self._lock.acquire()
        try:
            current_topology = deepcopy(self._topology)
        finally:
            self._lock.release()
        return current_topology


def main():
    t = Topology()
    print("Topology file is parsed as:\n{}\n".format(t._topo))
    for i in t._topo:
        t.update(i)
        print("Topology at timestamp {} is:\n{}\n".format(i,
                                                          t._topology))


if __name__ == '__main__':
    main()
