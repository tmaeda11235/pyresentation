import re


class Parser:
    tagdict = {"f": "frame",
               "b": "block",
               "i": "itemize",
               "e": "enumerate",
               "m": "align",
               "p": "pure"}
    tag = list()
    level = 0
    gein = 0
    newtag = tuple()
    text = None

    def __new__(cls, text):
        cls.level += cls.gein
        if cls.newtag != tuple():
            cls.tag.append(cls.newtag)
        cls.gein = 0
        cls.newtag = tuple()
        cls.text = None
        return super().__new__(cls)

    def __init__(self, text):
        self.text_ = text.rstrip()
        self.update_level()
        self.update_tag()
        self.__class__.text = self.show_text()

    def update_level(self):
        if self.find_blankline():
            return 0
        else:
            head = bool(self.find_headder())
            indent = self.get_indent()
            newlevel = head + indent
            self.__class__.gein = newlevel - self.__class__.level
            return self.__class__.gein

    def update_tag(self):
        match = self.find_headder()
        newlevel = self.__class__.level + self.__class__.gein
        if newlevel == 0:
            self.__class__.newtag = ("pure",)
            return self.__class__.newtag
        rtn = list()
        if match:
            pretag = match.group()
            if pretag == ":":
                if newlevel == 1:
                    pretag += "f"
                if newlevel == 2:
                    pretag += "b"
            for t in pretag[1:]:
                rtn.append(self.tagdict[t])
            self.__class__.newtag = tuple(rtn)
            return self.__class__.newtag
        else:
            return tuple()

    def find_headder(self):
        return re.search(r":[fbmiep]*$", self.text_)

    def find_blankline(self):
        if re.search(r"^\s*$", self.text_):
            return True
        else:
            return False

    def get_indent(self):
        match = re.search(r"^\s*", self.text_)
        if match.group():
            return len(match.group()) // 4
        else:
            return 0

    def show_text(self):
        return re.sub(r":[fbmiep]*", "", self.text_).lstrip()

    def __str__(self):
        param = ("{:-^30}\n".format(self.text_),
                 "text:{}\n".format(self.text),
                 "level:{}\n".format(self.level),
                 "gein:{}\n".format(self.gein),
                 "tag:{}\n".format(self.tag),
                 "newtag:{}\n".format(self.newtag))
        return "".join(param)


if __name__ == "__main__":
    test = ("    hello world:",
            "     ",
            "heyper heyper",
            "headline:",
            "    hoge:i",)
    for t in test:
        print(Parser(t))
