"""Convert textual UML representation to source code"""

# Copyright 2024 René Fischer - renefischer@fischer-homenet.de
#
# MIT License
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sys import argv
import sys
import os
import logging


def getopts(argvalues):
    """Function parsing command line options"""
    opts = {}  # Empty dictionary to store key-value pairs.
    while argvalues:  # While there are arguments left to parse...
        if argvalues[0][0] == '-':  # Found a "-name value" pair.
            if len(argvalues) > 1:
                if argvalues[1][0] != '-':
                    opts[argvalues[0]] = argvalues[1]
                else:
                    opts[argvalues[0]] = True
            elif len(argvalues) == 1:
                opts[argvalues[0]] = True

        # Reduce the argument list by copying it starting from index 1.
        argvalues = argvalues[1:]
    return opts

if __name__ == '__main__':
    myargs = getopts(argv)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    if '-i' in myargs:
        print("Using input " +myargs['-i'])
    else:
        sys.exit(1)
    if '-o' in myargs:
        print("Using output " +myargs['-o'])
    else:
        sys.exit(1)

    if '-v' in myargs:
        logging.basicConfig(level=logging.INFO)
