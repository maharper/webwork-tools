# ov2ww.py

A standalone python script converting classlists obtained from Omnivox into a format suitable for importing into a WeBWorK course.

## Requires:

Python >= 3.?

## Usage:

```
usage: ov2ww.py [-h] [--output OUTPUT] [--delimiter {,,;}] [--lang {en,fr}]
                input

Convert Omnivox classlist to WeBWorK classlist

positional arguments:
  input                 input file from Omnivox student number, first and
                        last name are required. email address and section
                        number are recommended.

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        output file name. '.lst' will be appended if not
                        already there.
  --delimiter {,,;}, -d {,,;}
                        Omnivox file delimiter
  --lang {en,fr}, -l {en,fr}
                        Omnivox file language
```

The default for delimiter is `,`, specify the optional argument `-d ;` if the csv file from Omnivox uses semicolons.

It appears that if the interface language for Omnivox is French when the classlist file is requested
then the classlist produced is in French, with French column headers.  In this case, specify `-l fr`.

Fields _student number_, _first name_, and _last name_ are **required**.
Fields _email address_ and _section number_ are _recommended_.
