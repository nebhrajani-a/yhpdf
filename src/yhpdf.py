
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import askquestion
import sys
import os
from pathlib import Path
import ghostscript
from PyPDF2 import PdfFileWriter, PdfFileReader

root = tk.Tk()
root.title("[Yash Honda] PDF Splitter/Compressor")
root.geometry('480x480')

list_of_vals = {'filename': False, 'dir': False}

def split_and_compress():
    try:
        inputpdf = PdfFileReader(open(str(list_of_vals['filename']), "rb"))
    except FileNotFoundError:
        showerror(title='Error', message="File not found!")

    size_limit = 197500
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open("%s/doc-page%s.pdf" % (list_of_vals['dir'] ,i), "wb") as outputStream:
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
    op = askquestion(title='Success', message='Successfully processed %s. Open output folder?' % (list_of_vals['filename']))
    if op == 'yes':
        os.startfile(list_of_vals['dir'])

def select_file():
    filetypes = (
        ('PDF files', '*.pdf'),
        ('All files', '*.*')
    )

    list_of_vals['filename'] = (fd.askopenfilename(
        title='Select scanned PDF',
        initialdir = str(Path.home()),
        filetypes=filetypes))

    if list_of_vals['filename']:
        showinfo(
            title='Selected File',
            message="Selected file %s" % (list_of_vals['filename'])
        )

def select_directory():
    list_of_vals['dir'] = fd.askdirectory(title='Select output folder', initialdir = str(Path.home()))

    if list_of_vals['dir']:
        showinfo(
            title='Selected folder',
            message="Selected folder %s" % (list_of_vals['dir'])
        )


text = ttk.Label(root, text="This is an internal program. You may not copy, distribute, or sell it.")
text.pack(expand=True)

open_button = ttk.Button(root, text='Select a file', command=select_file)
open_button.pack(expand=True)


dir_button = ttk.Button(root, text="Select output folder", command=select_directory)
dir_button.pack(expand=True)

process_button = ttk.Button(root, text="Process PDF", command=split_and_compress)
process_button.pack(expand=True)

exit_button = ttk.Button(root, text="Exit", command=sys.exit)
exit_button.pack(expand=True)


text2 = ttk.Label(root, text="All rights reserved.\n(C) Yash Honda 2021")
text2.pack(expand=True)

root.mainloop()
