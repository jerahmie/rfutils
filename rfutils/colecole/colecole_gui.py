"""
GUI for Cole-Cole parameter calculation.
"""

import tkinter as tk
from tkinter import ttk

class ColeColeGUI(object):
    def __init__(self, master):
        ccp_row = 5  # cole-cole parameters row
        self.entry_state = 'normal'
        default_text_width = 10
        pad_width_a = 2
        pad_width_b = 10

        #self.f0.set("297.0")  # MHz
        #self.fmin.set("0.0")  # MHz
        #self.fmax.set("600.0") # MHz
        self.master = master
        self.master.title("Cole-Cole Parameter Calculator")
        separator_style = ttk.Style()
        separator_style.configure("BW.TSeparator", background = "black")
        self.frame_title = ttk.Label(master,
                                     text="Cole-Cole Material Property Calculator",
                                     font = ("Arial", 16))
        
        self.frame_title.grid(row = 0, column = 1, columnspan = 3)

        # Section: Frequency
        ttk.Label(master,
                  text = "f0 (MHz)", 
                  font = ("Arial", 12)).grid(row = 3, column = 0)
        self.entry_f0 = ttk.Entry(master, )
        ttk.Label(master,
                  text = "f0 (MHz)", 
                  font = ("Arial", 12)).grid(row = 3, column = 2)
        ttk.Label(master,
                  text = "f0 (MHz)", 
                  font = ("Arial", 12)).grid(row = 3, column = 4)
        # Section: Material Selection
        tissue_var = tk.StringVar()
        tissue_choices =  ["", "custom", "skin", "bone"]
        tissue_var.set(tissue_choices[1])
        tissue_menu = ttk.OptionMenu(master, tissue_var, *tuple(tissue_choices))
        tissue_menu.grid(row = 4, column = 2)

        # Section: Cole-Cole coefficients
        sep1 = ttk.Separator(master,
                             orient =tk.HORIZONTAL,
                             style = "BW.TSeparator")
        sep1.grid(row = 2,
                  column = 0,
                  sticky = tk.EW,
                  columnspan = 6,
                  pady=5)
        
        label_style = ttk.Style()
        label_style.configure("BW.TLabel", foreground="black", bg="white")
        ttk.Label(master, 
                  text = "Inf. Freq. Rel. Permittivity",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 1,
                                            column = 0,
                                            padx = pad_width_a,
                                            sticky = tk.E)
        ttk.Label(master,
                  text = "\u03c3",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 1,
                                            column = 2,
                                            padx = pad_width_a)
        ttk.Label(master,
                  text = "\u0394 1",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 2,
                                            column = 0,
                                            padx = pad_width_a,
                                            sticky = tk.E)
        ttk.Label(master,
                  text = "\u03c4 1",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 2,
                                            column = 2,
                                            padx = pad_width_a)
        ttk.Label(master,
                  text = "\u03b1 1",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 2,
                                            column = 4,
                                            padx = pad_width_a)
        ttk.Label(master,
                  text = "\u0394 2",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 3,
                                            column = 0,
                                            padx = pad_width_a,
                                            sticky = tk.E)
        ttk.Label(master,
                  text = "\u03c4 2",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 3,
                                            column = 2,
                                            padx = pad_width_a)
        ttk.Label(master,
                  text = "\u03b1 2",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 3,
                                            column = 4,
                                            padx = pad_width_a)
        ttk.Label(master,
                  text = "\u0394 3",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 4,
                                            column = 0,
                                            padx = pad_width_a,
                                            sticky = tk.E)
        ttk.Label(master,
                  text = "\u03c4 3",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 4,
                                            column = 2,
                                            padx = pad_width_a)
        ttk.Label(master,
                  text = "\u03b1 3",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 4,
                                            column = 4,
                                            padx = pad_width_a)
        ttk.Label(master,
                  text  = "\u0394 4",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 5,
                                            column = 0,
                                            padx = pad_width_a,
                                            sticky = tk.E)
        ttk.Label(master,
                  text = "\u03c4 4",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 5,
                                            column = 2,
                                            padx = pad_width_a)
        ttk.Label(master,
                  text = "\u03b1 4",
                  anchor = tk.E,
                  style = "BW.TLabel").grid(row = ccp_row + 5,
                                            column = 4,
                                            padx = pad_width_a)
        self.ef = tk.StringVar()
        self.ef.set("0.0")
        self.sigma = tk.StringVar()
        self.sigma.set("0.0")
        self.alpha1 = tk.StringVar()
        self.alpha1.set("0.0")
        self.alpha2 = tk.StringVar()
        self.alpha2.set("0.0")
        self.alpha3 = tk.StringVar()
        self.alpha3.set("0.0")
        self.alpha4 = tk.StringVar()
        self.alpha4.set("0.0")
        self.delta1 = tk.StringVar()
        self.delta1.set("0.0")
        self.delta2 = tk.StringVar()
        self.delta2.set("0.0")
        self.delta3 = tk.StringVar()
        self.delta3.set("0.0")
        self.delta4 = tk.StringVar()
        self.delta4.set("0.0")
        self.tau1 = tk.StringVar()
        self.tau1.set("0.0")
        self.tau2 = tk.StringVar()
        self.tau2.set("0.0")
        self.tau3 = tk.StringVar()
        self.tau3.set("0.0")
        self.tau4 = tk.StringVar()
        self.tau4.set("0.0")
        # Cole-Cole parameter entries
        self.entry_ef = ttk.Entry(self.master,
                                  textvariable = self.ef,
                                  justify = tk.RIGHT,
                                  state = self.entry_state,
                                  width = 20)
        self.entry_ef.grid(row = ccp_row + 1,
                           column = 1,
                           padx = pad_width_b)
        self.entry_sigma = ttk.Entry(self.master,
                                     textvariable = self.sigma,
                                     justify = tk.RIGHT,
                                     state = self.entry_state,
                                     width = 20)
        self.entry_sigma.grid(row = ccp_row + 1,
                              column = 3,
                              padx = pad_width_b)
        self.entry_delta1 = ttk.Entry(self.master,
                                      textvariable = self.delta1,
                                      justify = tk.RIGHT,
                                      state = self.entry_state,
                                      width = 20)
        self.entry_delta1.grid(row = ccp_row + 2,
                               column = 1,
                               padx = pad_width_b)
        self.entry_delta2 = ttk.Entry(self.master,
                                      textvariable = self.delta2,
                                      justify = tk.RIGHT,
                                      state = self.entry_state,
                                      width = 20)
        self.entry_delta2.grid(row = ccp_row + 3,
                               column = 1,
                               padx = pad_width_b)
        self.entry_delta3 = ttk.Entry(self.master,
                                      textvariable = self.delta3,
                                      justify = tk.RIGHT,
                                      state = self.entry_state,
                                      width = 20)
        self.entry_delta3.grid(row = ccp_row + 4,
                               column = 1,
                               padx = pad_width_b)
        self.entry_delta4 = ttk.Entry(self.master,
                                      textvariable = self.delta4,
                                      justify = tk.RIGHT,
                                      state = self.entry_state,
                                      width = 20)
        self.entry_delta4.grid(row = ccp_row + 5,
                               column = 1,
                               padx = pad_width_b)
        self.entry_tau1 = ttk.Entry(self.master,
                                    textvariable = self.tau1,
                                    justify = tk.RIGHT,
                                    state = self.entry_state,
                                    width = 20)
        self.entry_tau1.grid(row = ccp_row + 2,
                             column = 3,
                             padx = pad_width_b)
        self.entry_tau2 = ttk.Entry(self.master,
                                    textvariable = self.tau2,
                                    justify = tk.RIGHT,
                                    state = self.entry_state,
                                    width = 20)
        self.entry_tau2.grid(row = ccp_row + 3,
                             column = 3,
                             padx = pad_width_b)
        self.entry_tau3 = ttk.Entry(self.master,
                                    textvariable = self.tau3,
                                    justify = tk.RIGHT,
                                    state = self.entry_state,
                                    width = 20)
        self.entry_tau3.grid(row = ccp_row + 4,
                             column = 3,
                             padx = pad_width_b)
        self.entry_tau4 = ttk.Entry(self.master,
                                    textvariable = self.tau4,
                                    justify = tk.RIGHT,
                                    state = self.entry_state,
                                    width = 20)
        self.entry_tau4.grid(row = ccp_row + 5,
                             column = 3,
                             padx = pad_width_b)
        self.entry_alpha1 = ttk.Entry(self.master,
                                      textvariable = self.alpha1,
                                      justify = tk.RIGHT,
                                      state = self.entry_state,
                                      width = 20)
        self.entry_alpha1.grid(row = ccp_row + 2,
                               column = 5,
                               padx = pad_width_b)
        self.entry_alpha2 = ttk.Entry(self.master,
                                      textvariable = self.alpha2,
                                      justify = tk.RIGHT,
                                      state = self.entry_state,
                                      width = 20)
        self.entry_alpha2.grid(row = ccp_row + 3,
                               column = 5,
                               padx = pad_width_b)
        self.entry_alpha3 = ttk.Entry(self.master,
                                      textvariable = self.alpha3,
                                      justify = tk.RIGHT,
                                      state = self.entry_state,
                                      width = 20)
        self.entry_alpha3.grid(row = ccp_row + 4,
                               column = 5,
                               padx = pad_width_b)
        ccp_row_last = ccp_row + 5
        self.entry_alpha4 = ttk.Entry(self.master,
                                      textvariable = self.alpha4,
                                      justify = tk.RIGHT,
                                      state = self.entry_state,
                                      width = 20)
        self.entry_alpha4.grid(row = ccp_row_last,
                               column = 5,
                               padx = pad_width_b)

        button_row = ccp_row_last + 1

        self.quit_button = ttk.Button(master,
                                      text="QUIT",
                                      command=self.master.quit)
        self.quit_button.grid(row = button_row, column = 0)

        self.calculate_button = ttk.Button(master,
                                           text="RUN",
                                           command=self.print_values)
        self.calculate_button.grid(row = button_row ,column = 1)

    def update_entries(self):
        """Update the Cole-Cole parameter entries to reflect current material or 
        enabel the state to allow entry for custom parameters.
        """
        self.entry_ef['state'] = self.entry_state
        self.entry_sigma['state'] = self.entry_state
        self.entry_alpha1['state'] = self.entry_state
        self.entry_alpha2['state'] = self.entry_state
        self.entry_alpha3['state'] = self.entry_state
        self.entry_alpha4['state'] = self.entry_state
        self.entry_tau1['state'] = self.entry_state
        self.entry_tau2['state'] = self.entry_state
        self.entry_tau3['state'] = self.entry_state
        self.entry_tau4['state'] = self.entry_state
        self.entry_delta1['state'] = self.entry_state
        self.entry_delta2['state'] = self.entry_state
        self.entry_delta3['state'] = self.entry_state
        self.entry_delta4['state'] = self.entry_state

    def print_values(self):
        """Dump the class values to stdout.
        """
        if 'disabled' == self.entry_state:
            self.entry_state = 'normal'
        self.update_entries()
        print(r"\n  inf freq. epsilon: ", self.ef.get())
        print(r"  sigma: ", self.sigma.get())
        print(r"  delta1: ", self.delta1.get())
        print(r"  delta2: ", self.delta2.get())
        print(r"  delta3: ", self.delta3.get())
        print(r"  delta4: ", self.delta4.get())
        print(r"    tau1: ", self.tau1.get())
        print(r"    tau2: ", self.tau2.get())
        print(r"    tau3: ", self.tau3.get())
        print(r"    tau4: ", self.tau4.get())
        print(r"  alpha1: ", self.alpha1.get())
        print(r"  alpha2: ", self.alpha2.get())
        print(r"  alpha3: ", self.alpha3.get())
        print(r"  alpha4: ", self.alpha4.get())

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    cc = ColeColeGUI(root)
    tk.mainloop()
    #root.destroy()
