# Uncrustify handling function.

def handling(executable, input_file_path, output_file_path, editorconfig_properties):
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
