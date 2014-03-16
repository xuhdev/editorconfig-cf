#!/usr/bin/python

from __future__ import print_function

BEAUTIFIER_OPTIONS_CONFIG = 1
BEAUTIFIER_OPTIONS_INPUT = 2
BEAUTIFIER_OPTIONS_OUTPUT = 3

global_options = {
        'editorconfig':      'editorconfig',
        'output_suffix':     '.ecfix'
        }

extension_language_map = {
        'c': 'c',
        'cpp': 'cpp',
        'h': 'cpp',
        'hpp': 'cpp'
        }

class EditorConfigFixError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def uncrustify_handling(executable, input_file_path, output_file_path, editorconfig_properties):
    import subprocess
    import sys
    import tempfile

    # The temp config file
    cfg = tempfile.NamedTemporaryFile(mode='w', suffix='.cfg')
    for key, value in editorconfig_properties.items():
        if key == 'tab_width':
            cfg.write('input_tab_size = ' + value + '\n')
            cfg.write('output_tab_size = ' + value + '\n')
        if key == 'indent_size':
            if value == 'tab':
                if 'tab_width' in editorconfig_properties:
                    cfg.write('indent_columns = ' + cfg['tab_width'] + '\n')
                else:
                    cfg.write('indent_columns = 8\n')
            else:
                cfg.write('indent_columns = ' + value + '\n')
        if key == 'indent_style':
            if value == 'space':
                cfg.write('indent_with_tabs = 0\n')
            elif value == 'tab':
                cfg.write('indent_with_tabs = 1\n')
        if key == 'end_of_line':
            cfg.write('newlines = ' + value + '\n')

    # Need to write to disk
    cfg.flush()

    # execute uncrustify
    cmd = [executable, '-c', cfg.name, '-f', input_file_path, '-o', output_file_path]
    print('Executing: ' + ' '.join(cmd), file=sys.stderr)
    return subprocess.call(cmd, shell=False)


def get_language_info(lang):
    """
    Obtain the information needed for a given language.
    """

    if lang == 'c':
        return dict(
                id=             'c',
                name=           'C',
                beautifier=     ['uncrustify'])
    elif lang == 'cpp':
        return dict(
                id=             'cpp',
                name=           'C++',
                beautifier=     ['uncrustify'])
    else:
        return None

def get_beautifier_info(lang, beautifier):
    """
    Obtain the information needed for a given beautifier.
    """

    if beautifier == 'uncrustify':
        return dict(
                id=             'uncrustify',
                name=           'Uncrustify',
                language=       'c',
                executable=     'uncrustify',
                func_handling=  uncrustify_handling)
    else:
        return None

def fix_one_file(file_path):
    """
    Fix one file with a file path file_path
    """
    import os
    import editorconfig

    path = os.path.abspath(file_path)

    _, ext = os.path.splitext(path)

    # check the corresponding language
    ext = ext[1:]
    if ext not in extension_language_map:
        return 2

    lang = extension_language_map[ext]
    lang_info = get_language_info(lang)

    # get editorconfig properties
    ec_properties = editorconfig.get_properties(path)

    succeed = -1
    for b in lang_info['beautifier']:
        b_info = get_beautifier_info(lang, b)
        # If the spawning succeeds, then we are finished; otherwise, let's try
        # the next beautifier 
        if b_info['func_handling'](b_info['executable'], path, path + global_options['output_suffix'], ec_properties) == 0:
            succeed = 0
            break

    if succeed != 0:
        raise EditorConfigFixError('Failed to fix "' + path + '"')

def fix_files(file_paths):
    """
    Recursively fix the files with paths of file_paths 
    """
    import os,sys

    for file_path in file_paths:
        if os.path.isdir(file_path):
            for f in os.listdir(file_path):
                fix_files(os.path.join(file_path, f))

        try:
            fix_one_file(file_path)
        except EditorConfigFixError as e:
            print('Warning: ' + e, file=sys.stderr)

def main():
    import sys
    import os
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'f:')
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

    fix_files(files_to_process)

if __name__ == '__main__':
    main()
