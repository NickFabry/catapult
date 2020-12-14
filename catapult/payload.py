#!/usr/bin/env python
# -*- coding: utf-8 -*-



""" This is part of a python CLI application template, specifically the
payload - the part where most of the code lives. It is not expected to be
run directly, but to be imported by other code or by launcher.py.

It is expected that it have a main() function that is called with the 
args from argparse.

See the README.md for more details.
"""



import sys, os
import argparse
import logging
import datetime
from pathlib import Path

log = logging.getLogger(__name__)



### MAIN ###
def main(args):
    """This is the primary interface to your program.
    """
    log.status(f'Running main, with args: {args}')



### MAIN RUNNER ###
if __name__ == '__main__':
    pass
### END ###
