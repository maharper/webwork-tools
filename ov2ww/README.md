# ov2ww.py

A standalone python script converting classlists obtained from Omnivox into a format suitable for importing into a WeBWorK course.

## Requires:

Python >= 3.?

Older versions of WeBWorK didn't display accented characters properly.
The script can remove accented characters from names, but needs to have the python `unidecode` module available in order to do so.
There has been no problem with accented character display in WeBWorK since at least version 2.16.

## Usage:

```
usage: ov2ww.py [-h] [--output OUTPUT] [--delimiter {,,;}] [--lang {en,fr}] [--no_accents] input

Produces a WeBWorK classlist from an Omnivox classlist.

positional arguments:
  input                 input file from Omnivox student number, first and last name are required. email address and
                        section number are recommended.

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        output file name. '.lst' will be appended if not already there.
  --delimiter {,,;}, -d {,,;}
                        Omnivox file delimiter
  --lang {en,fr}, -l {en,fr}
                        Omnivox file language
  --no_accents          Exclude accented characters from the WW file.
                        unidecode is required
```

The default delimiter is `,`.
If the Omnivox file uses semicolons, specify the optional argument `--delimiter ;` (or `-d ;`).

If the Omnivox interface language is in English when the classlist is requested, the field headers will be in English.
This is what the script is expecting.

If the interface language for Omnivox is French when the classlist file is requested, the field headers will be in French.
In this case, specify the optional argument `--lang fr` (or `-l fr`).

Fields _student number_, _first name_, and _last name_ are **required**, if any of them is missing from the Omnivox file, the WeBWorK classlist will not be produced.
Fields _email address_ and _section number_ are _recommended_.  If any is missing, a warning is given, but the WeBWorK classlist is still produced.
