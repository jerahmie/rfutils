# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 14:36:30 2018

@author: jerahmie
"""
from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Cole Cole Dielectric Calculator")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

root.mainloop()
