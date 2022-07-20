# pylint: disable=global-variable-not-assigned, consider-using-with

"""
Provides yhpdf.py, standalone GUI application to process PNQ RTO PDFs.
"""

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
    """Clear widget text"""
    widget['text'] = ""


root = tk.Tk()
root.title("[Yash Honda] PDF Splitter/Compressor")
root.geometry('1000x500')

INFO1, INFO2, INFO3 = ttk.Label(root), ttk.Label(root), ttk.Label(root,
                                                                  font=(20))
INFO1.grid(row=1, column=1, padx=10, pady=30)
INFO2.grid(row=2, column=1, padx=10, pady=30)
INFO3.grid(row=3, column=1, padx=10, pady=30)
list_of_vals = {'filename': False, 'dir': False}


def split_and_compress():
    """Split and compress the actual PDF"""
    global INFO3
    clear_widget_text(INFO3)
    try:
        inputpdf = PdfFileReader(open(str(list_of_vals['filename']), "rb"))
    except FileNotFoundError:
        showerror(title='Error', message="File not found!")

    size_limit = 197500
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open(f"{list_of_vals['dir']}/doc-page{i}.pdf",
                  "wb") as output_stream:
            output.write(output_stream)
        if (size_limit -
                int(os.stat(f"{list_of_vals['dir']}/doc-page{i}.pdf").st_size)
            ) < 0:
            args = [
                "-dCompatibilityLevel=1.4", "-dNOPAUSE", "-dBATCH", "-dQUIET",
                "-sDEVICE=pdfwrite", "-dPDFSETTINGS=/ebook",
                f"-sOutputFile={list_of_vals['dir']}/document-page{i}.pdf",
                f"{list_of_vals['dir']}/doc-page{i}.pdf"
            ]
            ghostscript.Ghostscript(*args)
            os.replace(f"{list_of_vals['dir']}/document-page{i}.pdf",
                       f"{list_of_vals['dir']}/doc-page{i}.pdf")

        if (size_limit -
                int(os.stat(f"{list_of_vals['dir']}/doc-page{i}.pdf").st_size)
            ) < 0:
            args = [
                "-dCompatibilityLevel=1.4", "-dNOPAUSE", "-dBATCH", "-dQUIET",
                "-sDEVICE=pdfwrite", "-dPDFSETTINGS=/screen",
                f"-sOutputFile={list_of_vals['dir']}/document-page{i}.pdf",
                f"{list_of_vals['dir']}/doc-page{i}.pdf"
            ]
            ghostscript.Ghostscript(*args)
            os.replace(f"{list_of_vals['dir']}/document-page{i}.pdf",
                       f"{list_of_vals['dir']}/doc-page{i}.pdf")

        if (size_limit -
                int(os.stat(f"{list_of_vals['dir']}/doc-page{i}.pdf").st_size)
            ) < 0:
            showerror(
                title='Error',
                message=f"ERROR: I couldn't compress page {i+1} to less than 195KB. \
                Consider using an online compressor or re-scanning.")
    clear_widget_text(INFO3)
    INFO3['text'] = f"Successfully split and compressed to {i} pages"


def select_file():
    """Interface for file selection"""
    global INFO1
    clear_widget_text(INFO1)
    filetypes = (('PDF files', '*.pdf'), ('All files', '*.*'))

    list_of_vals['filename'] = (fd.askopenfilename(title='Select scanned PDF',
                                                   initialdir=str(Path.home()),
                                                   filetypes=filetypes))

    if list_of_vals['filename']:
        INFO1['text'] = f"File selected: {list_of_vals['filename']}"


def select_directory():
    """Interface for directory selection"""
    global INFO2
    clear_widget_text(INFO2)
    list_of_vals['dir'] = fd.askdirectory(title='Select output folder',
                                          initialdir=str(Path.home()))

    if list_of_vals['dir']:
        INFO2['text'] = f"Folder selected: {list_of_vals['dir']}"


text = ttk.Label(
    root,
    text=
    "This is an internal program. You may not copy, distribute, or sell it.")
text.grid(row=0, column=0, padx=10, pady=30)

open_button = ttk.Button(root, text='Select a file', command=select_file)
open_button.grid(row=1, column=0, padx=10, pady=30)

dir_button = ttk.Button(root,
                        text="Select output folder",
                        command=select_directory)
dir_button.grid(row=2, column=0, padx=10, pady=30)

process_button = ttk.Button(root,
                            text="Process PDF",
                            command=split_and_compress)
process_button.grid(row=3, column=0, padx=10, pady=30)

exit_button = ttk.Button(root, text="Exit", command=sys.exit)
exit_button.grid(row=4, column=0, padx=10, pady=30)

text2 = ttk.Label(root, text="All rights reserved.\n(C) Yash Honda 2021")
text2.grid(row=5, column=0, padx=10, pady=30)

root.mainloop()
