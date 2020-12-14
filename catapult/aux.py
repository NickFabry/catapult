#!/usr/bin/env python
# -*- coding: utf-8 -*-



""" This is part of a python CLI application template, specifically the
auxiliary functions; functions of generic use that don't necessarily
belong to one particular application.

See the README.md for more details.
"""



import sys, os
import argparse
import logging
import datetime
from pathlib import Path

log = logging.getLogger(__name__)



def pdf2str(path):
    """This basic function wraps all the machinery of the pdfminer.six
    library and presents it as a very simple interface. One path to a file in,
    one string returned. It is lifted directly from the docs of the
    pdfminer.six project, specifically:
    
    https://github.com/pdfminer/pdfminer.six/blob/develop/docs/source/\
    tutorials/composable.rst
    
    Note that the input filepath must be a "path-like object", which
    in practice will be either a str or a Path instance. One of the
    reasons for this vs a file object is because pdfminer will only be able
    to work with files opened in binary mode; by only allowing path-likes
    we can enforce that they are interpeted as binary files.
    """
    output_string = StringIO()
    with open(path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return output_string.getvalue()



### MAIN ###
def main(args):
    """This is the primary interface to your program.
    """
    log.status(f'Running main, with args: {args}')



### MAIN RUNNER ###
if __name__ == '__main__':
    pass
### END ###
