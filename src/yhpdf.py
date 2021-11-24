import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror
import sys
import os
from pathlib import Path
import ghostscript
from PyPDF2 import PdfFileWriter, PdfFileReader


def clear_widget_text(widget):
    widget['text'] = ""


root = tk.Tk()
root.title("[Yash Honda] PDF Splitter/Compressor")
root.geometry('1000x500')

info1, info2, info3 = ttk.Label(root), ttk.Label(root), ttk.Label(root, font=(20))
info1.grid(row=1, column=1, padx=10, pady=30)
info2.grid(row=2, column=1, padx=10, pady=30)
info3.grid(row=3, column=1, padx=10, pady=30)
list_of_vals = {'filename': False, 'dir': False}


def split_and_compress():
    global info3
    clear_widget_text(info3)
    try:
        inputpdf = PdfFileReader(open(str(list_of_vals['filename']), "rb"))
    except FileNotFoundError:
        showerror(title='Error', message="File not found!")

    size_limit = 197500
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open("%s/doc-page%s.pdf" % (list_of_vals['dir'] , i), "wb") as outputStream:
            output.write(outputStream)
        if (size_limit - int(os.stat("%s/doc-page%s.pdf" % (list_of_vals['dir'], i)).st_size)) < 0:
            args = """-dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH -dQUIET -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -sOutputFile=%s/document-page%s.pdf %s/doc-page%s.pdf""" % (list_of_vals['dir'], i, list_of_vals['dir'], i)
            args = args.split()
            ghostscript.Ghostscript(*args)
            os.replace("%s/document-page%s.pdf" % (list_of_vals['dir'], i), "%s/doc-page%s.pdf" % (list_of_vals['dir'], i))
        if (size_limit - int(os.stat("%s/doc-page%s.pdf" % (list_of_vals['dir'], i)).st_size)) < 0:
            args = """-dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH -dQUIET -sDEVICE=pdfwrite -dPDFSETTINGS=/screen -sOutputFile=%s/document-page%s.pdf %s/doc-page%s.pdf""" % (list_of_vals['dir'], i, list_of_vals['dir'], i)
            args = args.split()
            ghostscript.Ghostscript(*args)
            os.replace("%s/document-page%s.pdf" % (list_of_vals['dir'], i), "%s/doc-page%s.pdf" % (list_of_vals['dir'], i))
        if (size_limit - int(os.stat("%s/doc-page%s.pdf" % (list_of_vals['dir'], i)).st_size)) < 0:
            showerror(title='Error', message="ERROR: I couldn't compress page %s to less than 195KB. Consider using an online compressor or re-scanning." % (i+1))
    clear_widget_text(info3)
    info3['text']="Successfully split and compressed to %s pages" % i


def select_file():
    global info1
    clear_widget_text(info1)
    filetypes = (
        ('PDF files', '*.pdf'),
        ('All files', '*.*')
    )

    list_of_vals['filename'] = (fd.askopenfilename(
        title='Select scanned PDF',
        initialdir = str(Path.home()),
        filetypes=filetypes))

    if list_of_vals['filename']:
        info1['text']="File selected: %s" % list_of_vals['filename']


def select_directory():
    global info2
    clear_widget_text(info2)
    list_of_vals['dir'] = fd.askdirectory(title='Select output folder', initialdir = str(Path.home()))

    if list_of_vals['dir']:
        info2['text']="Folder selected: %s" % list_of_vals['dir']


text = ttk.Label(root, text="This is an internal program. You may not copy, distribute, or sell it.")
text.grid(row=0, column=0, padx=10, pady=30)

open_button = ttk.Button(root, text='Select a file', command=select_file)
open_button.grid(row=1, column=0, padx=10, pady=30)


dir_button = ttk.Button(root, text="Select output folder", command=select_directory)
dir_button.grid(row=2, column=0, padx=10, pady=30)

process_button = ttk.Button(root, text="Process PDF", command=split_and_compress)
process_button.grid(row=3, column=0, padx=10, pady=30)

exit_button = ttk.Button(root, text="Exit", command=sys.exit)
exit_button.grid(row=4, column=0, padx=10, pady=30)


text2 = ttk.Label(root, text="All rights reserved.\n(C) Yash Honda 2021")
text2.grid(row=5, column=0, padx=10, pady=30)

root.mainloop()
