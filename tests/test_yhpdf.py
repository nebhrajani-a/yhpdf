import sys
import os
import re

sys.path.append('src')
import yhpdf as yh


def test_split_and_compress(tmp_path):
    myinfo = yh.PDFInfo([])
    path = os.path.abspath('./tests/sample_pdfs')
    for i, pdf in enumerate(
            map(lambda x: path + '/' + x, os.listdir("./tests/sample_pdfs"))):
        d = tmp_path / str(i)
        d.mkdir()
        myinfo.filename = pdf
        myinfo.directory = d
        errs = yh.split_and_compress(myinfo, gui=False)
        sizes = {
            re.findall(r'\d+', f)[0]: os.path.getsize(d / f)
            for f in os.listdir(d)
        }
        print(sizes)
        for j, size in sizes.items():
            if size > 200000 and int(j) not in errs:
                raise Exception
