# !/usr/bin/env python3

import argparse
import unidecode

parser = argparse.ArgumentParser(
    description = "Convert Omnivox classlist to WeBWorK classlist",
)

parser.add_argument('--input','-i',
    help = "input file from Omnivox\n student number, first and last name are required.  email address and section number are recommended.",
    )

parser.add_argument('--output', '-o',
    help = "output file name.  '.lst' will be appended if not already there."
    )

args = parser.parse_args()

import os.path

infile = args.input

if not os.path.isfile(infile):
    print(f"Input file, {infile} not found")
    exit

import csv

reader = csv.DictReader(open(infile, 'r'))
cols = reader.fieldnames
print(cols)

for c in ['Student number', 'Student name', 'Student first name']:
    if c not in cols:
        print(f"{c} is a required field not found in {infile}")
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

translate = ['Student number']
for row in reader:
    row = {k:v[2:-1] if isinstance(v,str) else '' for (k,v) in row.items()}
    print(row)
    classlist_row = [
        row['Student number'],
        unidecode.unidecode(row['Student name']),
        unidecode.unidecode(row['Student first name']),
        "C",
        "",
        row['Section'] if row['Section'] else '',
        "",
        row['Email address'] if row['Email address'] else '',
        row['Student number'],
        "",
        0
    ]
    writer.writerow(classlist_row)
