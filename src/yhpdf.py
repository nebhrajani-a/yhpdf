# pylint: disable=consider-using-with
'''
Provides yhpdf.py, standalone GUI application to process PNQ RTO PDFs.
'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror
from dataclasses import dataclass
from pathlib import Path
import sys
import os

import ghostscript
from PyPDF2 import PdfFileWriter, PdfFileReader


@dataclass
class PDFInfo:
    '''
    Class that contains filename, directory for PDF to process.
    Also holds information labels.
    '''
    boxes: list
    filename: str = None
    directory: str = None


def select_file(info: PDFInfo):
    '''Interface for file selection, setter for info.filename'''
    info.boxes[0]['text'] = ""
    filetypes = (('PDF files', '*.pdf'), ('All files', '*.*'))

    info.filename = (fd.askopenfilename(title='Select scanned PDF',
                                        initialdir=str(Path.home()),
                                        filetypes=filetypes))

    if info.filename:
        info.boxes[0]['text'] = f"File selected: {info.filename}"


def select_directory(info: PDFInfo):
    '''Interface for directory selection, setter for info.directory'''
    info.boxes[1]['text'] = ""
    info.directory = fd.askdirectory(title='Select output folder',
                                     initialdir=str(Path.home()))

    if info.directory:
        info.boxes[1]['text'] = f"Folder selected: {info.directory}"


def split_and_compress(info: PDFInfo, gui: bool):
    '''Split and compress the actual PDF'''
    def page_too_large(i: int):
        size_limit = 197500
        filesize = int(os.stat(f"{info.directory}/doc-page{i}.pdf").st_size)
        return (size_limit - filesize) < 0

    def call_gs(mode: str, i: int):
        args = [
            "-dCompatibilityLevel=1.4", "-dNOPAUSE", "-dBATCH", "-dQUIET",
            "-sDEVICE=pdfwrite", f"-dPDFSETTINGS=/{mode}",
            f"-sOutputFile={info.directory}/document-page{i}.pdf",
            f"{info.directory}/doc-page{i}.pdf"
        ]
        ghostscript.Ghostscript(*args)
        os.replace(f"{info.directory}/document-page{i}.pdf",
                   f"{info.directory}/doc-page{i}.pdf")

    def report_err(i: int):
        showerror(
            title='Error',
            message=f"ERROR: I couldn't compress page {i+1} to less"
            "than 195KB. Consider using an online compressor or re-scanning.")

    err_dict = {}

    if gui:
        info.boxes[2]['text'] = ""

    try:
        inputpdf = PdfFileReader(open(str(info.filename), "rb"))
    except FileNotFoundError:
        if gui:
            showerror(title='Error', message="File not found!")
        return None

    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))

        with open(f"{info.directory}/doc-page{i}.pdf", "wb") as ostr:
            output.write(ostr)


        if page_too_large(i):
            call_gs("ebook", i)

        if page_too_large(i):
            call_gs("screen", i)

        if page_too_large(i):
            if gui:
                report_err(i)
            else:
                err_dict[i] = True

    if gui:
        info.boxes[2][
            'text'] = f"Successfully split and compressed to {i} pages"
    else:
        return err_dict


def main():
    '''Main function'''
    root = tk.Tk()
    root.title("[Yash Honda] PDF Splitter/Compressor")
    root.geometry('1000x500')

    boxes = [ttk.Label(root), ttk.Label(root), ttk.Label(root, font=(20))]
    boxes[0].grid(row=1, column=1, padx=10, pady=30)
    boxes[1].grid(row=2, column=1, padx=10, pady=30)
    boxes[2].grid(row=3, column=1, padx=10, pady=30)

    info = PDFInfo(boxes)

    text = ttk.Label(root,
                     text="This is an internal program. You may not copy, "
                     "distribute, or sell it.")
    text.grid(row=0, column=0, padx=10, pady=30)

    open_button = ttk.Button(root,
                             text='Select a file',
                             command=lambda: select_file(info))
    open_button.grid(row=1, column=0, padx=10, pady=30)

    dir_button = ttk.Button(root,
                            text="Select output folder",
                            command=lambda: select_directory(info))
    dir_button.grid(row=2, column=0, padx=10, pady=30)

    process_button = ttk.Button(
        root,
        text="Process PDF",
        command=lambda: split_and_compress(info, gui=True))
    process_button.grid(row=3, column=0, padx=10, pady=30)

    exit_button = ttk.Button(root, text="Exit", command=sys.exit)
    exit_button.grid(row=4, column=0, padx=10, pady=30)

    text2 = ttk.Label(root, text="All rights reserved.\n(C) Yash Honda 2021")
    text2.grid(row=5, column=0, padx=10, pady=30)

    root.mainloop()


if __name__ == '__main__':
    main()
