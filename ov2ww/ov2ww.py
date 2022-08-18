# !/usr/bin/env python3
"""Produces a WeBWorK classlist from an Omnivox classlist.

See --help for parameters
"""

from argparse import ArgumentParser
import csv
import os.path

def main():

    args = parse_args()

    infile,outfile,processname = configure(args)
    lang = args.lang

    fields,req_fields,rec_fields = definitions()

    with open(infile, 'r') as csvin:
        reader = csv.DictReader(csvin,delimiter=args.delimiter)
        cols = reader.fieldnames
        print(cols)

        for c in req_fields:
            if fields[c][lang] not in cols:
                raise SystemExit(f"{fields[c][lang]} is a required field not found in input file '{infile}'\nNo output produced.")
        for c in rec_fields:
            if fields[c][lang]  not in cols:
                print(f"{fields[c][lang]} is a recommended field not found in {infile}")

        with open(outfile, 'w', encoding='utf-8', newline='') as csvout:
            print("Writing to ",outfile)
            writer = csv.writer(csvout,dialect='unix', quoting=csv.QUOTE_MINIMAL)
            header_row = ["# Field order:", "student_id", "last_name", "first_name", "status", "comment", "section", "recitation", "email_address", "user_id", "password", "permission"]
            writer.writerow(header_row)

            translate = ['Student number']
            for row in reader:
            # Strip off the strange OV formatting '="...."'
                row = {k:v[2:-1] if isinstance(v,str) and v.startswith('=') else v for (k,v) in row.items()}

                classlist_row = [
                    row[fields['student_id'][lang]],
                    processname(row[fields['last_name'][lang]]),
                    processname(row[fields['first_name'][lang]]),
                    "C",
                    "",
                    row[fields['section'][lang]] if fields['section'][lang] in row and row[fields['section'][lang]] else '',
                    "",
                    row[fields['email_address'][lang]] if fields['email_address'][lang] in row and row[fields['email_address'][lang]] else '',
                    row[fields['student_id'][lang]],
                    "",
                    0
                ]

                writer.writerow(classlist_row)

def parse_args():

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('input',    help = "input file from Omnivox\n student number, first and last name are required.  email address and section number are recommended.",
    )
    parser.add_argument('--output', '-o',
    help = "output file name.  '.lst' will be appended if not already there."
    )
    parser.add_argument('--delimiter', '-d',
    help = "Omnivox file delimiter",
    choices = [',',';'],
    default = ',',
    )
    parser.add_argument('--lang', '-l',
    help = "Omnivox file language",
    choices = ['en','fr'],
    default = 'en',
    )
    parser.add_argument('--no_accents',
    help = "Exclude accented characters from the WW file.  unidecode is required",
    default=False,
    action="store_true",
    )

    return(parser.parse_args())

def configure(args):

    infile = args.input
    if not os.path.isfile(infile):
        raise SystemExit(f"Input file, {infile} not found.  Stopping.")

    outfile = args.output
    if outfile == None:
        outfile = os.path.splitext(infile)[0]+'.lst'
    elif not os.path.splitext(outfile)[1] == '.lst':
        outfile = outfile+'.lst'
    
    if args.no_accents:
        try:
            import unidecode
        except ImportError:
            print("The module unidecode was not found. Accented characters will be retained")
            args.no_accents = False

    if args.no_accents:        
        def processname(text):
            return unidecode.unidecode(text)
    else:
        def processname(text):
            return text
    
    return infile, outfile, processname

def definitions():

    fields = {
        'student_id':{
            'en':'Student number',
            'fr':'No étudiant'
        },
        'last_name':{
            'en':'Student name',
            'fr':"Nom de l'étudiant"
        },
        'first_name':{
            'en':'Student first name',
            'fr':"Prénom de l'étudiant"
        },
        'section':{
            'en':'Section',
            'fr':'Groupe'
        },
        'email_address':{
            'en':'Email address',
            'fr':'Adresse de courriel'
        },
    }
    req_fields = [
        'student_id', 
        'last_name', 
        'first_name',
    ]
    rec_fields = [
        'email_address', 
        'section',
    ]
    return fields, req_fields, rec_fields

if __name__ == '__main__':
    main()
