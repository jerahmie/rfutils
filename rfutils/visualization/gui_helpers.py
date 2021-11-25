import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import pickle


def openfilegui(start_dir=os.getcwd(), title="Open Files",
                 filetypes=(("all files", "*.*"))):
    Tk().withdraw()  # prevent root window from appearing
    start_dir_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'start_dir.tmp')  # start directory pickle 
    if os.path.exists(start_dir_file):
        with open(start_dir_file, 'rb') as fh:
            try:
                start_dir = pickle.load(fh)
            except:               # use current directory if pickle is malformed
                start_dir = os.getcwd()
    else:
           start_dir = os.getcwd()

    # show the open dialog
    data_files = askopenfilenames(initialdir=start_dir, title=title, filetypes=filetypes)
    if len(data_files) > 0:
        # Save current working directory
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'start_dir.tmp'),'wb') as fh:
            pickle.dump(data_files[0], fh)
    return data_files