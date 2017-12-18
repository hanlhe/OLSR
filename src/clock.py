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

from threading import RLock


class Clock(object):
    """ A Singlton clock.
    Based on [The Singleton](https://goo.gl/T3kxkR)
    """
    __instance = None

    def __new__(cls):
        if Clock.__instance is None:
            Clock.__instance = object.__new__(cls)
            Clock.__instance.val = int()
            Clock.__instance.lock = RLock()
        return Clock.__instance

    def tick(self):
        self.lock.acquire()
        try:
            self.val += 1
        finally:
            self.lock.release()
        return self

    def reset(self):
        self.lock.acquire()
        try:
            self.val = 0
        finally:
            self.lock.release()
        return self

    @property
    def time(self):
        self.lock.acquire()
        try:
            return self.val
        finally:
            self.lock.release()


def main():
    c = Clock()
    print(c.time)
    c.tick()
    print(c.time)
    cp = Clock()
    print(cp.time)
    cp.tick()
    print(c.time, cp.time)
    print(Clock().tick().time)


if __name__ == '__main__':
    main()
