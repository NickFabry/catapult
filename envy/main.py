#!/usr/bin/env python3
# -*- coding: utf-8 -*-



""" This is my template for a CLI python script. There are many like it,
but this is mine.
"""



import sys, os
import argparse



def arg_parser():
    parser = argparse.ArgumentParser(
        description='Envy is a template of a python project.')
    parser.add_argument('-i', '--input', metavar='FILE', 
    	default='a_file.txt',
        help='The file you wish to process. The default is %(default)s.')



### MAIN ###
def main(args):
	pass
### END MAIN ###



### MAIN RUNNER ###
if __name__ == '__main__':
    args = arg_parser().parse_args()
    print(args)
    if sys.__stdin__.isatty():
        locals().update(main(args))
    else:
        main(args)
### END ###