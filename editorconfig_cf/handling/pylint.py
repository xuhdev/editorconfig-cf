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

def handling(executable, input_file_path, output_file_path, editorconfig_properties, c_or_f):
    """ Pylint handling function. """

    if c_or_f == 'f': # no formatting available
        return 1

    import subprocess
    import sys
    import tempfile

    # The temp config file
    cfg = tempfile.NamedTemporaryFile(mode='w', suffix='.cfg')

    # Check the style and tab width in the first loop
    indent_style = 'space'
    tab_width = 4
    for key, value in editorconfig_properties.items():
        if key == 'indent_style':
            if value == 'space':
                indent_style = 'space'
            elif value == 'tab':
                indent_style = 'tab'
        elif key == 'tab_width':
            tab_width = int(value)

    cfg.write('[FORMAT]\n')
    for key, value in editorconfig_properties.items():
        if key == 'indent_size':
            if value == 'tab':
                cfg.write("indent-string='\\t'\n")
            else:
                valuei = int(value)
                if indent_style == 'space': # value ' 's
                    cfg.write("indent-string='" + ' ' * valuei + "'\n")
                else: # tab indent_style
                    cfg.write("indent-string='" + r'\t' * (valuei // tab_width) + ' ' * (valuei % tab_width) + "'\n")

        if key == 'max_line_length':
            cfg.write('max-line-length={}\n'.format(value))

    # Need to write to disk
    cfg.flush()

    # execute uncrustify
    cmd = [executable, '--rcfile', cfg.name, input_file_path]
    print('Executing: ' + ' '.join(cmd), file=sys.stderr)
    subprocess.call(cmd, shell=False)
    return 0
