
# REQUIRES (64-bit) GHOSTSCRIPT TO BE INSTALLED ON HOST

import sys
import os
import ghostscript
from PyPDF2 import PdfFileWriter, PdfFileReader


def split_and_compress():
    inputpdf = PdfFileReader(open(str(sys.argv[1]), "rb"))

    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open("doc-page%s.pdf" % (i), "wb") as outputStream:
            output.write(outputStream)
        if (195000 - int(os.stat("doc-page%s.pdf" % (i)).st_size)) < 0:
            args = """-dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH -dQUIET -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -sOutputFile=document-page%s.pdf doc-page%s.pdf""" % ((i), (i))
            args = args.split()
            ghostscript.Ghostscript(*args)
            os.replace("document-page%s.pdf" % (i), "doc-page%s.pdf" % (i))
            if (195000 - int(os.stat("doc-page%s.pdf" % (i)).st_size)) < 0:
                args = """-dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH -dQUIET -sDEVICE=pdfwrite -dPDFSETTINGS=/screen -sOutputFile=document-page%s.pdf doc-page%s.pdf""" % ((i), (i))
                args = args.split()
                ghostscript.Ghostscript(*args)
                os.replace("document-page%s.pdf" % (i), "doc-page%s.pdf" % (i))
            if (195000 - int(os.stat("doc-page%s.pdf" % (i)).st_size)) < 0:
                print("ERROR: I couldn't compress page %s to less than 195KB. Consider using an online compressor or re-scanning." % (i+1))

split_and_compress()
