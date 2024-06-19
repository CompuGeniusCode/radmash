import os
import re

from titlecase import titlecase
from jinja2 import Environment, FileSystemLoader

PDF_DIR = 'divrei_torah/maamarei_mordechai'
OUTPUT_DIR = 'output'
TEMPLATE_DIR = 'templates'

os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


# for filename in os.listdir(PDF_DIR):
#     if filename.endswith('.pdf'):
#         new_filename = filename.lower().removeprefix("_")
#         os.rename(os.path.join(PDF_DIR, filename), os.path.join(PDF_DIR, new_filename))


def parse_filename(filename):
    match = re.match(r'(.+)_(\d{4})\.pdf', filename)
    if match:
        parsha, year = match.groups()
        parsha = titlecase(parsha.replace('_', ' '))
        return year, parsha
    return None, None


def get_pdfs():
    pdfs = []
    for filename in os.listdir(PDF_DIR):
        if filename.endswith('.pdf'):
            year, parsha = parse_filename(filename)
            if year and parsha:
                pdfs.append((year, parsha, filename))
    return sorted(pdfs, key=lambda x: (x[0], x[1]))


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

    index_html = render_template('index.html', {'grouped_pdfs': grouped_pdfs})
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w') as f:
        f.write(index_html)


if __name__ == '__main__':
    generate_html()
