import re
import sys
import os.path


filepath = os.path.abspath(sys.argv[1])


def sign(x):
    return x and (1, -1)[x < 0]


tagdict = {"f": "flame",
           "b": "block",
           "i": "itemize",
           "e": "enumerate",
           "m": "align"}


class parser:
    tag = list()
    level = 0

    @classmethod
    def update_level(cls, text):
        if re.match("^\s*$", text):
            return 0
        match = re.search(r"^\s+", text)
        colon = bool(re.search(r":[fbiem]*$", text))
        rtn = colon
        if match:
            space = len(match.group())
            rtn += space // 4 - cls.level
        else:
            rtn += -cls.level
        cls.level += rtn
        return rtn

    @classmethod
    def update_tag(cls, text):
        match = re.search(r":[fbiem]*$", text)
        rtn = list()
        if match:
            pretag = match.group()
            if pretag == ":":
                if cls.level == 1:
                    pretag += "f"
                if cls.level == 2:
                    pretag += "b"
            for t in pretag[1:]:
                rtn.append(tagdict[t])
                cls.tag.append(tuple(rtn))
            return cls.tag[-1]
        else:
            return False

    @classmethod
    def headder(cls):
        if cls.level == 0:
            return "\\frame{"
        if "itemize" in cls.tag[-1] or "enumerate" in cls.tag[-1]:
            return "\item"

    @classmethod
    def footer(cls):
        if cls.level == 0:
            return "}"

    @classmethod
    def add_tag(cls, text):
        changed_level = cls.update_level(text)
        if 0 < changed_level:
            rtn = cls.open_tag(text)
        elif changed_level < 0:
            rtn = cls.close_tag(changed_level)
        else:
            rtn = "\n"
        return rtn

    @classmethod
    def open_tag(cls, text):
        rtn = str()
        new_tags = cls.update_tag(text)
        if new_tags:
            for i, nt in enumerate(new_tags):
                rtn += "\\begin{{{0}}}".format(nt)
                if nt == "frame" or nt == "block":
                    rtn += "{{{0}}}\n".format(text.lstrip())
                else:
                    rtn += "\n"
        return rtn

    @classmethod
    def close_tag(cls, changed_level):
        rtn = "\n"
        n = abs(changed_level)
        for i in range(n):
            old_tags = cls.tag.pop()
            for ot in old_tags:
                rtn += "\\end{{{0}}}\n".format(ot)
        return rtn


with open(filepath) as f:
    line = f.readline().rstrip()
    while line:
        print(parser.add_tag(line), end="")
        print(line, end="")
        line = f.readline().rstrip()
print(parser.add_tag("s"))
