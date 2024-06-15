"""
Program: random_sentence_generator_gui.py
Author: Alex Gill
Displays randomly generated sentences in a GUI.
"""
from tkinter import *
from tkinter import ttk
from random_sentence_generator import *

def set_window_resize(window):
    """Centers the window and prevents it from being shrunken past its
    default size."""
    window.update_idletasks()
    width = window.winfo_width()
    frm_width = window.winfo_rootx() - window.winfo_x()
    win_width = width + frm_width * 2
    height = window.winfo_height()
    tlb_height = window.winfo_rooty() - window.winfo_y()
    win_height = height + tlb_height + frm_width
    x = window.winfo_screenwidth() // 2 - win_width // 2
    y = window.winfo_screenheight() // 2 - win_height // 2
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    window.minsize(width=width, height=height)


def main():
    # Create the root
    root = Tk()
    root.title('Random Sentence Generator')
    root.geometry('400x200')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=9)
    root.rowconfigure(1, weight=1)

    # Create a style for the label
    s = ttk.Style()
    s.configure('TLabel', font=('Arial', 14), wraplength=400, justify=CENTER)

    # Create the sentence label
    sentence_text = StringVar(root,
        'Click the button below to generate sentences.')
    sentence_label = ttk.Label(root, textvariable=sentence_text)
    sentence_label.grid(row=0, column=0)

    # Create the generate button
    generate_button = ttk.Button(root, text='Generate', command=lambda:
        sentence_text.set(sentence()))
    generate_button.grid(row=1, column=0)

    # Center the window
    set_window_resize(root)

    # Start the event loop
    root.mainloop()


if __name__ == '__main__':
    main()