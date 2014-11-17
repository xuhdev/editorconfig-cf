#!/usr/bin/python

# Copyright (C) 2014 Hong Xu <hong@topbug.net>
#
# This file is part of EditorConfig-cf.
#
# EditorConfig-cf is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# EditorConfig-cf is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along with EditorConfig-cf.  If not, see
# <http://www.gnu.org/licenses/>.

from __future__ import print_function

BEAUTIFIER_OPTIONS_CONFIG = 1
BEAUTIFIER_OPTIONS_INPUT = 2
BEAUTIFIER_OPTIONS_OUTPUT = 3

global_options = {
        'editorconfig':      'editorconfig',
        'output_suffix':     '.ecfmt'
        }

extension_language_map = {
        'c': 'c',
        'cpp': 'cpp',
        'h': 'cpp',
        'hpp': 'cpp',
        'py': 'python'
        }

class EditorConfigCfError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def get_language_info(lang, c_or_f):
    """
    Obtain the information needed for a given language. c_or_f indicates whether it's a checker or formatter.
    """
    if c_or_f == 'f': # formatter
        if lang == 'c':
            return dict(
                    id= 'c',
                    name= 'C',
                    beautifier= ['uncrustify'])
        elif lang == 'cpp':
            return dict(
                    id= 'cpp',
                    name= 'C++',
                    beautifier= ['uncrustify'])
        else:
            return None

    elif c_or_f == 'c':
        if lang == 'python':
            return dict(
                    id= 'python',
                    name= 'Python',
                    beautifier= ['pylint'])
        else:
            return None

def get_beautifier_info(lang, beautifier):
    """
    Obtain the information needed by a given beautifier
    """
    if beautifier == 'uncrustify':
        import handling.uncrustify

        return dict(
                id=             'uncrustify',
                name=           'Uncrustify',
                language=       'c',
                executable=     'uncrustify',
                func_handling=  handling.uncrustify.handling)
    elif beautifier == 'pylint':
        import handling.pylint

        return dict(
                id=             'pylint',
                name=           'Pylint',
                language=       'python',
                executable=     'pylint',
                func_handling=  handling.pylint.handling)
    else:
        return None

def process_one_file(file_path, c_or_f):
    """
    Format one file with a file path file_path
    """
    import os
    import shutil
    import editorconfig

    path = os.path.abspath(file_path)

    _, ext = os.path.splitext(path)

    # check the corresponding language
    ext = ext[1:]
    if ext not in extension_language_map:
        return 2

    lang = extension_language_map[ext]
    lang_info = get_language_info(lang, c_or_f)

    # get editorconfig properties
    ec_properties = editorconfig.get_properties(path)

    succeed = -1
    for b in lang_info['beautifier']:
        b_info = get_beautifier_info(lang, b)
        if shutil.which(b_info['executable']) == None: # The executable does not exist
            continue
        # If the spawning succeeds, then we are finished; otherwise, let's try the next beautifier
        if b_info['func_handling'](b_info['executable'], path, path + global_options['output_suffix'], ec_properties, c_or_f) == 0:
            succeed = 0
            break

    if succeed != 0:
        raise EditorConfigCfError('Failed to check/format "' + path + '"')

def process_files(file_paths, c_or_f):
    """
    Recursively format the files with paths of file_paths
    """
    import os,sys

    for file_path in file_paths:
        if os.path.isdir(file_path):
            for f in os.listdir(file_path):
                format_files(os.path.join(file_path, f))

        try:
            process_one_file(file_path, c_or_f)
        except EditorConfigCfError as e:
            print('Warning: ' + e, file=sys.stderr)

def main():
    import sys
    import os
    import getopt

    if len(sys.argv) == 1:
        print('Subcommand missing', file=sys.stderr)

    # check subcommand -- check or format
    if sys.argv[1] == 'check' or sys.argv[1] == 'c':
        c_or_f = 'c'
    elif sys.argv[1] == 'format' or sys.argv[1] == 'f':
        c_or_f = 'f'
    else:
        print('Unknown subcommand.', file=sys.stderr)
        sys.exit(1)

    try:
        opts, args = getopt.getopt(sys.argv[2:], 'f:')
    except:
        print('Argument error.', file=sys.stderr)
        sys.exit(1)

    files_to_process = []

    for option, arg in opts:
        # Read a list of file paths from the specified file
        if option == '-f':
            f = None
            if arg == '-':
                f = sys.stdin
            else:
                f = open(arg, 'r')

            files_to_process.extend(f.readlines())

    # add the rest of args to the list of files to be processed
    files_to_process.extend(args)

    # strip all the entries in files_to_process
    files_to_process = [f.strip() for f in files_to_process]

    process_files(files_to_process, c_or_f)

if __name__ == '__main__':
    main()
