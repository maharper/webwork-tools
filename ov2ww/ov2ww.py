# !/usr/bin/env python3

import argparse
import unidecode

parser = argparse.ArgumentParser(
    description = "Convert Omnivox classlist to WeBWorK classlist",
)

parser.add_argument('input',#'-i',
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

args = parser.parse_args()

print(args)

import os.path

infile = args.input

if not os.path.isfile(infile):
    print(f"Input file, {infile} not found")
    raise SystemExit()

import csv

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

reader = csv.DictReader(open(infile, 'r'),delimiter=args.delimiter)
cols = reader.fieldnames
print(cols)

for c in ['student_id', 'last_name', 'first_name']:
    if fields[c][args.lang] not in cols:
        print(f"{fields[c][args.lang]} is a required field not found in {infile}")
        exit()
for c in ['Email address', 'Section']:
    if c not in cols:
        print(f"{c} is a recommended field not found in {infile}")

outfile = args.output
if outfile == None:
    outfile = os.path.splitext(infile)[0]+'.lst'
elif not os.path.splitext(outfile)[1] == '.lst':
    outfile = outfile+'.lst'

writer = csv.writer(open(outfile, 'w', encoding='utf-8', newline=''),dialect='unix', quoting=csv.QUOTE_MINIMAL)
header_row = ["# Field order:", "student_id", "last_name", "first_name", "status", "comment", "section", "recitation", "email_address", "user_id", "password", "permission"]
writer.writerow(header_row)
# print(header_row)

translate = ['Student number']
for row in reader:
# Strip off the strange OV formatting '="...."'
    row = {k:v[2:-1] if isinstance(v,str) and v.startswith('=') else v for (k,v) in row.items()}
#    print(row)
    classlist_row = [
        row[fields['student_id'][args.lang]],
        unidecode.unidecode(row[fields['last_name'][args.lang]]),
        unidecode.unidecode(row[fields['first_name'][args.lang]]),
        "C",
        "",
        row[fields['section'][args.lang]] if row[fields['section'][args.lang]] else '',
        "",
        row[fields['email_address'][args.lang]] if row[fields['email_address'][args.lang]] else '',
        row[fields['student_id'][args.lang]],
        "",
        0
    ]
#    print(classlist_row)
    writer.writerow(classlist_row)

