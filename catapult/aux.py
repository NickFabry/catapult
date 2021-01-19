#!/usr/bin/env python
# -*- coding: utf-8 -*-



""" This is part of a python CLI application template, specifically the
auxiliary functions; functions of generic use that don't necessarily
belong to one particular application.

Added some text just to get around git being mad.

See the README.md for more details.
"""



import sys, os
import argparse
import logging
import datetime
from pathlib import Path

# These are here for one function, pdf2str.
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser



log = logging.getLogger(__name__)



def partition(seq, fxn):
    """
    This is Ian Bickering's stab at a partition function in python. A usage
    example follows:

    def group(seq): 
        result = {} 
        for item, category in seq: 
            result.setdefault(category, []).append(item) 
        return result 

    partitioned = group((color, is_primary(color)) for color in colors) 
    by_first_letter = group((name, name[0]) for name in names) 

    I prefer that the partitioning function is passed in, so the above
    call could be replaced with:

    partitioned = group(colors, is_primary)

    Of course, that makes the second call slightly more verbose:

    by_first_letter = group(names, lambda x: x[0])

    I still prefer it! And, I'm going to call it 'partition'.

    A point worth noting is that the order of the elements is stable between
    the initial seq and the subsequences in each partition.

    This function partitions a sequence, partitioning it based on the return
    value of fxn when appled to each item of the sequence. Example:
    >>> partition([1,2,3,4,5,6,7,8,9,10], greatest_prime_divisor
    {None: [1], 2: [2, 4, 8], 3: [3, 9], 5: [5, 10], 7: [7]}
    """

    result = {}
    for item in seq:
        result.setdefault(fxn(item), []).append(item)
    return result


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
