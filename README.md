# EditorConfig-cf -- EditorConfig Checker and Formatter

This python program uses the rule given in [EditorConfig][] files to check and fix your coding style.

It is still under development, but your contribution is highly appreciated, since I do not use all languages!

## Usage

    python /path/to/editorconfig_cf.py [check|format] [file1] [file2] [file3] ...

where `[file1]`, `[file2]`, `[file3]`, ... are the source files you want to check or format.

## How It Works

This script does not touch your code directly; instead, it calls language specific beautifier to check and fix.

When given a file, it first see what type this file is according to its extension. After determining the type of the
source file, EditorConfig-cf tries to call the corresponding beautifiers it knows. If a beautifier is found to be
usable, EditorConfig-cf calls the beautifier to check or fix the source code and outputs the fixed code into a file with
`.ecfix` extension.

For example, when dealing with a C source file named `main.c`, EditorConfig-cf tries to call [uncrustify][]. If
uncrustify is available, it will be used to format this C source file, and write the output into `main.c.ecfix`.

## Contribution

### How Can I Add Beautifier for My Favorite language?

The framework is already there, what you need is to add your own handling function to handle this type of file with the
beautifier in the `handling` directory, then insert a few lines to tell some information about the beautifier (such as name,
for what language).

Here are the details.

#### Add Handling Function for Your Beautifier

Create a new file for your beautifier in the `handling` directory. You need to define a function with the following prototype:

    handling(executable, input_file_path, output_file_path, editorconfig_properties)

Where `executable` is the `executable` of the beautifier to be passed in, `input_file_path` is the file needs to be
formatted, `output_file_path` is where the formatted file should be written into, `editorconfig_properties` is the
output of EditorConfig library passed in (see [EditorConfig Python Core Document][] for what this variable is), `c_or_f`
shows whether this is checking ('c') or formatting ('f'). You need to fill this function so that the framework can call
this function to handle the specific type of file with the specific beautifier. You will tell the location of this
function later.

#### Add Meta Information of Beautifier

Edit `editorconfig_cf.py`, check the function `get_language_info` and `get_beautifier_info`. Check the existing
beautifier and insert meta info of the beautifier you are going to add.

#### Add Tests in the `tests` Directory

This should be fairly straightforward. Simply refer the other tests and modify it.

### Contribution License

If you added any new files, remember you need to add a license header as the other files do. If you code is less than 50
effective lines, you can simply copy a header from another file and copyright it under my name. If you do not want to
copyright it under my name, I will not be against copyright under your name. But your license must be compatible with
the other part of the project, that is, a permissive license (Apache v2, BSD, MIT, etc.) or LGPLv3+ (the `+` sign is
important!). LGPLv2 or GPL are not acceptable.

## License

Copyright (C) Hong Xu <hong@topbug.net>

Unless otherwise stated, most files are licensed under [GNU Lesser General Public License Version 3][] or later. See the
header of each file for license details.

[uncrustify]: http://uncrustify.sourceforge.net
[EditorConfig]: http://editorconfig
[EditorConfig Python Core Document]: http://pydocs.editorconfig.org/en/latest/usage.html
[GNU Lesser General Public License Version 3]: https://www.gnu.org/licenses/lgpl.html
