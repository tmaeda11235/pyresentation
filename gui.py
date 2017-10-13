import tkinter as tk
import tkinter.filedialog as fdlog
from sys import path
from os.path import abspath, dirname

script_path = abspath(__file__)
script_dir = dirname(script_path)
path.append(script_dir)
from reader.coder import Coder  # noqa


class MainWindow(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master, padx=5, pady=5)
        self.master.title("pyresentation.py")
        self.pack(expand=1)
        self.headline = tk.Label(self, text="変換するファイルを選択してください")
        self.cbtn = ControlButtons(self)
        self.textbox = tk.Text(self, width=100, height=50)
        self.headline.pack(fill="x")
        self.textbox.pack(fill="both", expand=1, side="top")
        self.cbtn.pack()


class ControlButtons(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.filename = None
        self.compile = list()
        self.file = tk.Button(self, text="選択", command=self.get_file)
        self.preview = tk.Button(self, text="プレビュー", command=self.preview)
        self.save = tk.Button(self, text="保存", command=self.save_file)
        self.file.pack(side="left")
        self.preview.pack(side="left")
        self.save.pack(side="left")

    def get_file(self):
        self.filename = fdlog.askopenfilename(filetype=(("text", "*.txt"),
                                                        ("off side text", "*.ost"),
                                                        ("all files", "*.*")))

    def save_file(self):
        fname = fdlog.asksaveasfilename(filetype=(("tex file", "*.tex"), ("all files", "*.*")))
        with open(fname, mode="w", encoding="utf-8")as f:
            f.write("".join(self.compile))

    def preview(self):
        with open(self.filename, newline="", encoding="utf-8") as f:
            line = f.readline()
            while line:
                self.compile.append(Coder(line).code())
                line = f.readline().rstrip()
        self.master.textbox.insert("1.0", "".join(self.compile))


if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root).mainloop()