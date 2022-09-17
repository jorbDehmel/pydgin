from tkinter import *
from tkinter import ttk
import tkinter.filedialog as fd

import pydgin as pg

"""
GUI for Pydgin translation
"""

class Interface:
    def get_file(self):
        self.path = fd.askopenfile().name
        with open(self.path, 'r') as file:
            text = file.read()
            self.text_edit.delete('1.0', 'end')
            self.text_edit.insert('1.0', text)
        if self.folder_path != '':
            self.label.config(text='Ready!')
        return

    def get_dir(self):
        self.folder_path = fd.askdirectory()
        if self.path != '':
            self.label.config(text='Ready!')
        return

    def translate(self):
        self.comp = pg.Translator(self.path, self.folder_path)
        filename = self.comp.compile()
        self.label.config(text='Successfully translated')
        return filename

    def run(self):
        path = self.translate()

        self.comp.run()

        return

    def save(self):
        with open(self.path, 'w') as file:
            text = self.text_edit.get('1.0', 'end')
            file.write(text)
        self.label.config(text='Saved')
        return

    def save_as(self):
        with fd.asksaveasfile(initialfile='Untitled.pdg', defaultextension=".pdg") as file:
            text = self.text_edit.get('1.0', 'end')
            file.write(text)
        self.label.config(text='Saved')
        return

    def __init__(self):
        self.path = ''
        self.folder_path = ''
        self.comp = -1

        self.root = Tk()
        self.root.title(string='Pydgin Translator')

        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()

        ttk.Label(self.frm, text='Pydgin Translator').grid(column=1, row=0)

        self.text_edit = Text(self.frm)
        self.text_edit.grid(column=0, row=1, columnspan=3)

        self.label = ttk.Label(self.frm, text='Select file')
        self.label.grid(column=0, row=2, columnspan=3)

        ttk.Button(self.frm, text='Open', command=self.get_file).grid(column=0, row=3)
        ttk.Button(self.frm, text='Output folder', command=self.get_dir).grid(column=0, row=4)

        ttk.Button(self.frm, text='Save', command=self.save).grid(column=1, row=3)
        ttk.Button(self.frm, text='Save as', command=self.save_as).grid(column=1, row=4)

        ttk.Button(self.frm, text='Translate', command=self.translate).grid(column=2, row=3)
        ttk.Button(self.frm, text='Translate and run', command=self.run).grid(column=2, row=4)

        ttk.Label(self.frm, text = '2022,  jdehmel@outlook.com').grid(column=1, row = 5)

        self.root.mainloop()
        return


if __name__ == '__main__':
    # Construct tkinter GUI
    Interface()
