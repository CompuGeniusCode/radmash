import os
import re

import requests
from jinja2 import Environment, FileSystemLoader
from titlecase import titlecase

PDF_DIR = 'divrei_torah/maamarei_mordechai'
TEMPLATE_DIR = 'templates'

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

parshas_url = "https://raw.githubusercontent.com/CompuGenius-Programs/Radmash/main/parshas.json"
parsha_order = requests.get(parshas_url).json()["parshas"]


def parse_filename(filename):
    match = re.match(r'(.+)_(\d{4})\.pdf', filename)
    if match:
        parsha, year = match.groups()
        parsha = titlecase(parsha.replace('_', ' '))
        return year, parsha
    return None, None


def get_sort_key(pdf):
    year, parsha, filename = pdf
    # parsha = parsha.removesuffix(' Bonus Shtikel')
    if parsha.endswith(' Bonus Shtikel'):
        parsha = parsha[:-len(' Bonus Shtikel')]
    if parsha in parsha_order:
        return year, parsha_order.index(parsha)
    else:
        return year, float('inf')


def get_pdfs():
    pdfs = []
    for filename in os.listdir(PDF_DIR):
        if filename.endswith('.pdf'):
            year, parsha = parse_filename(filename)
            if year and parsha:
                pdfs.append((year, parsha, filename))

    pdfs.sort(key=get_sort_key)
    return pdfs


def render_template(template_name, context):
    template = env.get_template(template_name)
    return template.render(context)


def generate_html():
    pdfs = get_pdfs()

    grouped_pdfs = {}
    for year, parsha, filename in pdfs:
        if year not in grouped_pdfs:
            grouped_pdfs[year] = []
        grouped_pdfs[year].append((parsha, filename))

    grouped_pdfs = dict(sorted(grouped_pdfs.items(), reverse=True))

    this_weeks_dvar_torah = grouped_pdfs[list(grouped_pdfs.keys())[0]][-1]

    with open('_redirects', 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if '/maamarei_mordechai/latest' in line:
                lines[i] = f'/maamarei_mordechai/latest /divrei_torah/maamarei_mordechai/{this_weeks_dvar_torah[1]}\n'
                break
    with open('_redirects', 'w') as f:
        f.writelines(lines)

    context = {
        'grouped_pdfs': grouped_pdfs,
        'this_weeks_dvar_torah': this_weeks_dvar_torah
    }

    index_html = render_template('maamarei_mordechai_template.html', context)
    with open('maamarei_mordechai.html', 'w') as f:
        f.write(index_html)


def fix_filenames():
    for filename in os.listdir(PDF_DIR):
        if filename.endswith('.pdf'):
            new_filename = filename.lower()
            new_filename = new_filename.replace('dvar torah - ', '')
            new_filename = new_filename.replace('dvar torah ', '')
            new_filename = new_filename.replace('dvar torah', '')
            new_filename = new_filename.replace('dvar_torah', '')
            new_filename = new_filename.replace('abridged', '')
            new_filename = new_filename.replace('parshas', '')
            new_filename = new_filename.replace(' ', '_')
            new_filename = new_filename.replace('__', '_')
            new_filename = new_filename.replace('_-_202', '_202')
            new_filename = new_filename.replace('-_202', '_202')

            if 'achrei' in new_filename and 'mos' not in new_filename:
                new_filename = new_filename.replace('achrei', 'achrei_mos')

            if 'matos' in new_filename and 'maasei' not in new_filename:
                new_filename = new_filename.replace('matos', 'matos_-_maasei')

            os.rename(os.path.join(PDF_DIR, filename), os.path.join(PDF_DIR, new_filename))


if __name__ == '__main__':
    fix_filenames()
    generate_html()
