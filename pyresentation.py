#! /usr/bin/env python3
from sys import argv, path
from os.path import abspath, dirname, join

script_path = abspath(__file__)
script_dir = dirname(script_path)
path.append(script_dir)

from coder import Coder  # noqa


headder_path = abspath(join(script_dir, "headder_"))
with open(headder_path) as f:
    line = f.readline()
    while line:
        print(line, end="")
        line = f.readline()

filepath = abspath(argv[1])
with open(filepath) as f:
    line = f.readline()  # type: str
    while line:
        c = Coder(line.rstrip())
        print(c.code(), end="")
        line = f.readline()
