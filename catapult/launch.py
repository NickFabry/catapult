#!/usr/bin/env python
# -*- coding: utf-8 -*-



""" This is part of a python CLI application template, specifically the
launcher - the part that should be softlinked to and placed in the user's
path to run the application.

The launcher section of program should be concerned with interpreting the
passed in arguments, setting up logging, and calling the main part of your
program... and that should be about it.

See the README.md for more details.
"""



# Standard Library
import argparse
import datetime
import logging
from pathlib import Path
import sys, os

# Third Party

# Local Projects
#   We defer "import payload" until after we set up logging in the main
#   runner, in case one of the modules importing attempts to do something
#   rude with logging.
# import payload



def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present 

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    This function was lifted directly from StackOverflow:
    https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility
    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


def configure_logging(main_name, log_path, log_level='AUDIT',
                      screen_level='STATUS'):
    """This subroutine configures the printing and logging configuration of
    the entire script. Because of the nature of tasks we do, we *always* want
    a log file of some sort. The logging configuration is done entirely
    through the logging module, and thus this function returns no value.

    
    There are four arguments, two mandatory.

    - main_name is a mandatory argument. It should be a string equal to the
    name of the project being imported. This is so the correct logger will
    be configured.

    - log_path is a mandatory argument, and expected to be a string or
    Path object that will be used to write the logfile to.

    - log_level is an optional argument that sets the level of log messages
    that will be recorded to the log_file. By default, it uses one of the
    two custom log levels set by this function, AUDIT.

    - screen_level is an optional argument that sets the level of log messages
    that will be printed to stderr. By default, it uses one of the two custom
    log levels set by this function, STATUS.
    

    We also create two new logging levels. The complete list of levels and
    their expected uses, from most to least severe:

    50: Critical/Fatal - The program can not continue to function, and is
    terminating.

    40: Error - The program has encountered an unfixable error, and can not
    guarantee the correctness or completeness of its output, but may be able
    to continue running.

    30: Warning - The program has encountered an error, but can continue
    functioning, possibly by skipping certain data or making assumptions
    which may not be true. It is recommended the source of the warning be
    fixed for future runs.

    25: Status - A general status message regarding what the program is doing.
    There should be few of these, ideally no more than a few screenfulls
    (i.e. a few hundred lines) in a typical run of the program.

    20 - Info - A detailed status message regarding what piece of data
    the program is processing at a given moment. A more exhaustive version
    of status, but still human-readable in a short time.

    15 - Audit - An extremely detailed message describing the values of all
    the variables the program would use to make decisions. This is expected
    to be output as an audit trail, to enable review of specific cases by
    attorneys or other non-programmers. It is expected to be too long to read
    the entire audit log in a reasonable amount of time.

    10 - Debug - A level of detail unlikely to be needed by anyone other than
    programmers.
    
    
    A complication often encountered is third-party libraries have interesting
    ideas about loggging, and will configure logging.handlers instead of just
    generating log messages, leading to unpredictable logging output. To
    prevent that, we attach a NullHandler to the root logger *before*
    importing any other libraries so we have full control of the logging
    infrastructure. Doing this stops logging.BasicConfig() from running in
    third-party modules.
    """
    # Create new logging levels.
    addLoggingLevel('AUDIT', 15)
    addLoggingLevel('STATUS', 25)

    # Disable the root logger to suppress third-party library logs [3PLL].
    # One can also suppress pesky 3PLL by specifically targeting them.
    # For example:
    # logging.getLogger('PIL.PngImagePlugin').disabled = True
    # logging.getLogger('pdfminer').setLevel(logging.CRITICAL)
    logging.getLogger().addHandler(logging.NullHandler())

    # Configure the project logger
    logger = logging.getLogger(main_name)
    logger.setLevel(log_level)

    # Configure the file logger
    fh = logging.FileHandler(log_path)
    fh.setLevel(log_level)

    # Configure the screen (stderr) display
    sh = logging.StreamHandler()
    sh.setLevel(screen_level)

    # Add formatting to the handlers
    formatter = logging.Formatter('%(asctime)s %(levelname)8s %(name)s | %(message)s')
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger


def test_logging():
    # Testing code...
    print('Test DEBUG')
    logger.debug('Test 1')
    print('Test AUDIT')
    logger.audit('Test 2')
    print('Test INFO')
    logger.info('Test 3')
    print('Test STATUS')
    logger.status('Test 4')
    print('Test WARNING')
    logger.warning('Test 5')
    print('Test ERROR')
    logger.error('Test 6')
    print('Test CRITICAL')
    logger.critical('Test 7')


def get_filepaths(paths, recurse=False): 
    """This simple but vital function takes as input a list of strings
     corresponding to paths.

    If a string in paths is a directory, the fxn returns a list of Path objects
    containing the full, absolute paths to all the files (i.e. not directories)
    contained within the directory.

    If a string in paths is a file itself, the function returns a Path object
    containing the full, absolute path to the single file.

    Ultimately, a list containing one (or more) Path objects pointing to only
    the file objects is returned.

    If recurse is set to True, if a string in paths is a directory, the fxn
    returns a list of Path objects not just to the files contained within the
    directory, but also all subdirectories of the directory of well. This could
    potentially be a massive number of paths, so use with caution.

    Also, this function automatically skips any path components starting with a
    ".", hopefully avoiding nusance files like .DS_Store, .git, etc.

    The dot filtering is here twice because dot files in a directory provided
    in paths would not get caught by the first filter. The first filter is
    there to save the trouble of looking in paths that have leading . in
    higher parts of the path.
    
    The purpose of this function is to allow the user to pass in a mixture of
    directories containing files to be parsed, and direct paths to files to be
    parsed without worrying about which is which.
    """
    filepaths = [] 
    paths = [Path(p).resolve() for p in paths]
    paths = [p for p in paths if '.' not in [n[0] for n in p.parts] ]
    for a_path in paths:
        if a_path.is_file():
            filepaths.append(a_path) 
        elif a_path.is_dir() and recurse==True: 
            for dirpath, dirnames, filenames in os.walk(a_path): 
                for a_file in filenames: 
                    filepaths.append( Path(dirpath) / Path(a_file) )
        elif a_path.is_dir() and recurse==False:
            dirpath, dirnames, filenames = next(os.walk(a_path))
            for a_file in filenames:
                filepaths.append( Path(dirpath) / Path(a_file) )
    filepaths = [p for p in filepaths
                 if '.' not in [n[0] for n in p.parts] ]
    return filepaths


def arg_parser():
    parser = argparse.ArgumentParser(
        description='This launcher is a template of a CLI based python project. It assumes a primary input file, a primary output file, some optional files, and some flags. If either the primary input or output files are not specified by option, stdin and stdout are used. Logging is enabled by default to a timestamped file in the current working directory the script was launched from.')
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
    parser.add_argument('-v', '--verbose', action='count', default=0,
        help='Prints all log messages to stderr, instead of just those of INFO and above (the default.)')
    parser.add_argument('-c', '--console', action='store_true',
        help='This option causes the program to stop at various strategic points and open an ipython shell to allow inspection of live objects. Typing "exit" at this shell will continue the program. Generally used for debugging.')
    parser.add_argument('-l', '--log_level', metavar='LOG_LEVEL',
        type=str.upper, default='AUDIT',
        choices=('DEBUG', 'AUDIT', 'INFO', 'STATUS', 'WARNING',
                 'ERROR', 'CRITICAL'),
        help='Changes the default log level to something other than %(default)s.')
    parser.add_argument('-t', '--testing', action='store_true',
        help='If this option is set, testing code will be run.')

    return parser



### MAIN RUNNER ###
if __name__ == '__main__':
    args = arg_parser().parse_args()
    if args.testing:
        print(sys.argv)
        print(args)
        test_logging()
    log_path = Path(f'{str(Path(sys.argv[0]).stem)}_'
                    f'{datetime.datetime.now().strftime("%Y%m%dT%H%M%S")}'
                    '.log')
    configure_logging('payload', log_path, log_level='AUDIT', screen_level='STATUS')
    import payload
    payload.main(args)
### END ###
