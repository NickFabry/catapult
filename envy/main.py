#!/usr/bin/env python
# -*- coding: utf-8 -*-



""" This is my template for a CLI python script. There are many like it,
but this is mine.
"""



import sys, os
import argparse
import logging
import datetime
from pathlib import Path



def arg_parser():
    parser = argparse.ArgumentParser(
        description='Envy is a template of a CLI based python project. It assumes a primary input file, a primary output file, some optional files, and some flags. If either the primary input or output files are not specified by option, stdin and stdout are used.')
    parser.add_argument('-i', '--input', metavar='FILE',
        type=argparse.FileType(mode='r'), default='-',
        help='The primary input file. If this option is not specified, STDIN is assumed.')
    parser.add_argument('-o', '--output', metavar='FILE',
        type=argparse.FileType(mode='w'), default='-',
        help='The primary output file. If this option is not specified, STDOUT is assumed.')
    parser.add_argument('-a', '--aux', metavar='FILE', 
        default='aux_file.txt',
        help='An auxiliary, optional file. The default is %(default)s.')
    parser.add_argument('-g', '--gflag',
        action='store_true',
        help='An optional flag.')
    parser.add_argument('-l', '--log_level', metavar='LOG LEVEL',
        nargs='?', type=str.upper, const='INFO', default=None,
        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
        help='Enable logging to a a file, args.output/main.log, at the level specified. The default level is %(const)s. The log level choices are DEBUG, INFO, WARNING, ERROR, and CRITICAL. Note that, regardless of the setting of this option, logging is always enabled to stderr, at a level of INFO.')
    parser.add_argument('-t', '--testing', action='store_true',
        help='If this option is set, testing code will be run.')

    return parser


def configure_logging(args):
    """This subroutine configures the printing and logging configuration of the
    entire script.
    """
    # Always enable console logging.
    log_level = getattr(logging, args.log_level, None)  if args.log_level\
                                                        else logging.INFO
    logging.basicConfig(level=log_level,
                        format='%(levelname)-8s: %(message)s')
    # If requested, enable logging to a timestamped logfile.
    if args.log_level:
        log_path = Path(f'{str(Path(sys.argv[0]).stem)}_'
                        f'{datetime.datetime.now().strftime("%Y%m%dT%H%M%S")}'
                        '.log')
        log_file = logging.FileHandler(log_path)
        log_file.setLevel(args.log_level)
        log_formatter = logging.Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M')
        log_file.setFormatter(log_formatter)
        logging.getLogger('').addHandler(log_file)
    logging.info(f'Logging enabled at level {log_level}.')
    logging.info(f'Command: {" ".join(sys.argv)}')
    logging.info(f'CWD: {os.getcwd()}')
    logging.info(args)


### MAIN ###
def main(args):
    configure_logging(args)
    # Main read/write section.
    with args.input as i:
        input_data = i.read()
    logging.info(f'Processed {len(input_data)} lines.')
    modified_data = input_data + '\nPROCESSED.'
    with args.output as o:
        o.write(modified_data)
### END MAIN ###



### MAIN RUNNER ###
if __name__ == '__main__':
    args = arg_parser().parse_args()
    if args.testing:
        print(sys.argv)
        print(args)
    # If the script is invoked interactively from within a python interpeter,
    # add the vars inside of main to the local interperter for inspection.
    # Probably better to do this with frame inspection instead.
    if sys.__stdin__.isatty():
        main(args)
    # ... otherwise, just run.
    else:
        main(args)
### END ###