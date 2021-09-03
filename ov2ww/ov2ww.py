# !/usr/bin/env python3

import os.path
import argparse
import csv

# Used to strip accents from names if the WeBWorK version can't handle accents
import unidecode

parser = argparse.ArgumentParser(
    description = "Convert Omnivox classlist to WeBWorK classlist",
)

parser.add_argument('input',
    help = "input file from Omnivox\n student number, first and last name are required.  email address and section number are recommended.",
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

parser.add_argument('--accents','-a',
    )
args = parser.parse_args()

infile = args.input
if not os.path.isfile(infile):
    raise SystemExit(f"Input file, {infile} not found")

outfile = args.output
if outfile == None:
    outfile = os.path.splitext(infile)[0]+'.lst'
elif not os.path.splitext(outfile)[1] == '.lst':
    outfile = outfile+'.lst'

lang = args.lang

def definitions():
    global fields 
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
    
definitions()

with open(infile, 'r') as csvin:
    reader = csv.DictReader(csvin,delimiter=args.delimiter)
    cols = reader.fieldnames
    print(cols)

    for c in ['student_id', 'last_name', 'first_name']:
        if fields[c][lang] not in cols:
             raise SystemExit(f"{fields[c][lang]} is a required field not found in input file '{infile}'\nNo output produced.")
    for c in ['email_address', 'section']:
        if fields[c][lang]  not in cols:
            print(f"{fields[c][lang]} is a recommended field not found in {infile}")

    with open(outfile, 'w', encoding='utf-8', newline='') as csvout:
        writer = csv.writer(csvout,dialect='unix', quoting=csv.QUOTE_MINIMAL)
        header_row = ["# Field order:", "student_id", "last_name", "first_name", "status", "comment", "section", "recitation", "email_address", "user_id", "password", "permission"]
        writer.writerow(header_row)

        translate = ['Student number']
        for row in reader:
        # Strip off the strange OV formatting '="...."'
            row = {k:v[2:-1] if isinstance(v,str) and v.startswith('=') else v for (k,v) in row.items()}

            classlist_row = [
                row[fields['student_id'][lang]],
                unidecode.unidecode(row[fields['last_name'][lang]]),
                unidecode.unidecode(row[fields['first_name'][lang]]),
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
