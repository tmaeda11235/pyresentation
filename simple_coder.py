from parser import Parser
from prompter import Prompter


class Coder(Parser):
    befor = False
    now = False

    def __init__(self, text):
        super().__init__(text)
        self.__class__.now, self.__class__.befor = bool(self.newtag), self.__class__.now

    def white_space(self, i=0):
        return (self.get_indent() + i) * 4 * " "

    def close_line(self):
        w = self.white_space
        text = self.text
        if self.gein < 0:
            rtn = []
            for i in range(abs(self.gein), 0, -1):
                rtn.append("\n" + w(i - 1))  # making indent. "-1" is normaliser.
                oldtag = self.__class__.tag.pop()[0]
                template = Prompter.tag_end[oldtag]
                rtn.append(template.format(w(i), text))
            return "".join(rtn)
        if self.gein == 0:
            if self.now:
                return Prompter.tag_end[self.newtag[0]].format(w(), text)
            elif self.befor:
                return "\n"
            else:
                return Prompter.content_end[self.tag[-1][0]].format(w(), text)
        if self.gein > 0:
            return "\n"

    def open_line(self):
        w = self.white_space
        text = self.text
        if self.now:
            return Prompter.tag[self.newtag[0]].format(w(), text)
        else:
            return Prompter.content[self.tag[-1][0]].format(w(), text)

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
    Prompter()
    for t in test:
        c = Coder(t)
        print(c.code(), end="")
