from pyresentation.parser import Parser


class Coder(Parser):
    befor = False
    now = False

    def __init__(self, text):
        super().__init__(text)
        self.__class__.now, self.__class__.befor = bool(self.find_headder()), self.__class__.now

    def white_space(self, i=0):
        return (self.get_indent() - i) * 4 * " "

    def main_dict(self) -> dict:
        text = self.text
        w = self.white_space()
        if (self.level + self.gein) == 0:
            return {"pure": "{}\n".format(text)}
        elif self.now:
            return {"frame": "{}\\begin{{frame}}[t]{{{}}}".format(w, text),
                    "block": "{}\\begin{{block}}{{{}}}".format(w, text),
                    "align": "{0}{1}\n{0}\\begin{{flalign*}}".format(w, text),
                    "itemize": "{0}{1}\n{0}\\begin{{itemize}}".format(w, text),
                    "enumerate": "{0}{1}\n{0}\\begin{{enumerate}}".format(w, text),
                    "pure": "{0}{1}".format(w, text)}
        else:
            return {"frame": "{}{}".format(w, text),
                    "block": "{}{}".format(w, text),
                    "align": "{}&{}&".format(w, text),
                    "itemize": "{}\\item {}".format(w, text),
                    "enumerate": "{}\\item {}".format(w, text),
                    "pure": "{}{}\n".format(w, text)}

    end_tag_dict = {"frame": "\\end{frame}\n",  # @
                    "block": "\\end{block}\n",
                    "align": "\\end{flalign*}\n",
                    "itemize": "\\end{itemize}\n",
                    "enumerate": "\\end{enumerate}\n",
                    "pure": ""}

    end_head_dict = {"frame": "\n",  # @
                     "block": "\n",
                     "align": "\n",
                     "itemize": "\n",
                     "enumerate": "\n",
                     "pure": ""}

    end_main_dict = {"frame": "\\\\\n",   # @
                     "block": "\\\\\n",
                     "align": "\\\\\n",
                     "itemize": "\n",
                     "enumerate": "\n",
                     "pure": ""}

    def close_line(self):
        code = list()
        if self.tag == list():
            return code
        if self.gein < 0:
            code.append("\n")
            if self.now:
                for ot in self.tag.pop():
                    code.append(self.white_space(i=-1))
                    code.append(self.end_tag_dict[ot])
            for j in range(self.gein, 0):
                for ot in reversed(self.__class__.tag.pop()):
                    code.append(self.white_space(i=j + 1))
                    code.append(self.end_tag_dict[ot])
            return code
        if self.befor:
            for t in self.tag[-1]:
                code.append(self.end_head_dict[t])
        else:
            for t in self.tag[-1]:
                code.append(self.end_main_dict[t])
        return code

    def open_line(self):
        code = list()
        if "pure" in self.newtag:
            code.append(self.main_dict()["pure"])
        elif self.now:
            if self.gein == 0:
                oldtag = self.__class__.tag.pop()
                for ot in reversed(oldtag):
                    code.append(self.white_space())
                    code.append(self.end_tag_dict[ot])
            for nt in self.newtag:
                code.append(self.main_dict()[nt])
        else:
            for t in self.tag[-1]:
                code.append(self.main_dict()[t])
        return code

    def code(self):
        if self.find_blankline():
            return ""
        code = self.close_line() + self.open_line()
        return "".join(code)

    def __str__(self):
        return super().__str__() + "code:{}".format(self.code())


if __name__ == "__main__":
    test = ("hello world:",
            "    heyper heyper:m",
            "        headline",
            "        payapaya",
            "    hoge",
            "end")
#    for t in test:
#        c = Coder(t)
#        print(c)
    for t in test:
        c = Coder(t)
        print(c.code(), end="")
