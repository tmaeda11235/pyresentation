import sys
import os.path
import coder


scriptpath = os.path.dirname(__file__)
headderpath = os.path.abspath(os.path.join(scriptpath, "headder_"))
with open(headderpath) as f:
    line = f.readline()
    while line:
        print(line, end="")
        line = f.readline()

filepath = os.path.abspath(sys.argv[1])
with open(filepath) as f:
    line = f.readline()
    while line:
        c = coder.Coder(line)
        print(c.code(), end="")
        line = f.readline()
print("\n")
