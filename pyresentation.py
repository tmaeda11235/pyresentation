#! /usr/bin/env python3
from sys import argv, path
from os import linesep
from os.path import abspath, dirname, join

script_path = abspath(__file__)
script_dir = dirname(script_path)
path.append(script_dir)

from reader.coder import Coder  # noqa


headder_path = abspath(join(script_dir, "headder_"))
with open(headder_path, newline="") as f:
    line = f.readline()
    while line:
        print(line, end="")
        line = f.readline()

filepath = abspath(argv[1])
with open(filepath, newline="") as f:
    line = f.readline()  # type: str
    while line:
        c = Coder(line.rstrip())
        code = c.code().replace("\n", linesep)
        print(code, end="")
        line = f.readline()
print(linesep, end="")
