"""
GUI for Cole-Cole parameter calculation.
"""

import tkinter as tk


class ColeColeGUI:
    def __init__(self, master):
        frame = tk.Frame(master)

        self.frame_title = tk.Label(master,
                                    text="Cole-Cole Material Property Calculator")
        self.frame_title.pack()
        frame.pack()
        ef_label_text = tk.StringVar()
        ef_label_text.set("Inf. Freq. Rel. Permittivity")
        label_ef = tk.Label(master, textvariable = ef_label_text, height=4)
        label_ef.pack(side=tk.LEFT)
        self.ef = tk.Entry(master,textvariable=tk.StringVar(None), width=20)
        self.ef.pack(side=tk.LEFT)
        frame.pack()
        self.quit_button = tk.Button(frame,
                                     text="QUIT",
                                     command=frame.quit)
        
        self.quit_button.pack(side=tk.LEFT)
        self.calculate_button = tk.Button(frame,
                                          text="RUN",
                                          command=self.say_hi)
        self.calculate_button.pack(side=tk.LEFT)
        frame.pack()

    def say_hi(self):
        print("Hello World!")

if __name__ == "__main__":
    root = tk.Tk()
    cc = ColeColeGUI(root)
    root.mainloop()
    root.destroy()
