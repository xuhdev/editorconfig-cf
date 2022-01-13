def main():
    import getopt
    import os
    import sys

    from . import *

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
    except BaseException:
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
