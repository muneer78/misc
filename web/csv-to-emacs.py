#!/usr/bin/env python3
"""Convert Google Contacts CSV export to Emacs Org mode format."""

import csv
import sys
from pathlib import Path


def sanitize_value(value):
    """Clean up value for org mode output."""
    if not value:
        return ""
    return value.strip().replace("\n", " ")


def convert_contacts_to_org(csv_file, output_file=None):
    """Convert Google Contacts CSV to Org mode format."""

    if output_file is None:
        output_file = Path(csv_file).stem + ".org"

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        with open(output_file, 'w', encoding='utf-8') as out:
            out.write("#+TITLE: Contacts from Google\n")
            out.write("#+STARTUP: overview\n\n")

            for row in reader:
                # Build full name from components
                prefix = sanitize_value(row.get('Name Prefix', ''))
                first = sanitize_value(row.get('First Name', ''))
                middle = sanitize_value(row.get('Middle Name', ''))
                last = sanitize_value(row.get('Last Name', ''))
                suffix = sanitize_value(row.get('Name Suffix', ''))
                nickname = sanitize_value(row.get('Nickname', ''))

                # Construct full name
                name_parts = [p for p in [prefix, first, middle, last, suffix] if p]
                name = ' '.join(name_parts) if name_parts else "Unknown Contact"

                # Write contact as org heading
                out.write(f"* {name}\n")
                out.write(":PROPERTIES:\n")

                # Add nickname if present
                if nickname:
                    out.write(f":NICKNAME: {nickname}\n")

                # Add phonetic names if present
                phonetic_first = sanitize_value(row.get('Phonetic First Name', ''))
                phonetic_middle = sanitize_value(row.get('Phonetic Middle Name', ''))
                phonetic_last = sanitize_value(row.get('Phonetic Last Name', ''))
                phonetic_parts = [p for p in [phonetic_first, phonetic_middle, phonetic_last] if p]
                if phonetic_parts:
                    phonetic_name = ' '.join(phonetic_parts)
                    out.write(f":PHONETIC: {phonetic_name}\n")

                # Add email
                email = sanitize_value(row.get('E-mail 1 - Value', ''))
                if email:
                    out.write(f":EMAIL: {email}\n")

                # Add phone
                phone = sanitize_value(row.get('Phone 1 - Value', ''))
                if phone:
                    out.write(f":PHONE: {phone}\n")

                # Add organization
                org = sanitize_value(row.get('Organization 1 - Name', ''))
                if org:
                    out.write(f":ORGANIZATION: {org}\n")

                # Add title
                title = sanitize_value(row.get('Organization 1 - Title', ''))
                if title:
                    out.write(f":TITLE: {title}\n")

                # Add address
                address = sanitize_value(row.get('Address 1 - Formatted', ''))
                if address:
                    out.write(f":ADDRESS: {address}\n")

                # Add birthday
                birthday = sanitize_value(row.get('Birthday', ''))
                if birthday:
                    out.write(f":BIRTHDAY: {birthday}\n")

                # Add website
                website = sanitize_value(row.get('Website 1 - Value', ''))
                if website:
                    out.write(f":WEBSITE: {website}\n")

                out.write(":END:\n")

                # Add notes as body text
                notes = sanitize_value(row.get('Notes', ''))
                if notes:
                    out.write(f"\n{notes}\n")

                out.write("\n")

    print(f"Conversion complete! Output written to: {output_file}")

csv_file = '/Users/muneer78/Downloads/Google Contacts.csv'
output_file = '/Users/muneer78/Downloads/contacts.org'

convert_contacts_to_org(csv_file, output_file)