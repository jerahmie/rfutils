#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
#root.resizeable(False, False)
sep_style = ttk.Style()
sep_style.configure("TW.Sep", background = "black")
ttk.Label(root, text="Hello...").pack()
ttk.Separator(root, orient = tk.HORIZONTAL, style = "TW.Sep").pack()
ttk.Label(root, text = "...from tkinter!").pack()
tk.mainloop()