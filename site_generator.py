import os
import re

from jinja2 import Environment, FileSystemLoader
from titlecase import titlecase

PDF_DIR = 'divrei_torah/maamarei_mordechai'
TEMPLATE_DIR = 'templates'

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

parsha_order = ["Bereishis", "Noach", "Lech Lecha", "Vayera", "Chayei Sarah", "Toldos", "Vayetzei", "Vayishlach",
                "Vayeshev", "Channukah", "Miketz", "Vayigash", "Vayechi", "Shmos", "Vaera", "Bo", "Beshalach", "Yisro",
                "Mishpatim", "Teruma", "Titzaveh", "Purim", "Ki Sisa", "Vayakel - Pekudei", "Vayakel", "Pekudei",
                "Vayikra", "Tzav", "Shmini", "Pesach", "Tazria - Metzora", "Tazria", "Metzora", "Achrei Mos - Kedoshim",
                "Achrei Mos", "Kedoshim", "Emor", "Behar - Bechukosai", "Behar", "Bechukosai", "Bamidbar and Shavuos",
                "Bamidbar", "Shavuos", "Rus", "Naso", "Beha'aloscha", "Shlach", "Korach", "Chukas", "Balak", "Pinchas",
                "Matos - Maasei", "Matos", "Maasei", "Devarim", "Vaeschanan", "Eikev", "Re'eh", "Shoftim",
                "Ki Tzeitzei", "Ki Savo", "Nitzavim - Vayeilech", "Nitzavim - Rosh Hashanah", "Nitzavim",
                "Rosh Hashanah", "Vayeilech", "Yom Kippur", "Haazinu and Succos", "Haazinu", "Succos",
                "Vezot Haberachah"]


def parse_filename(filename):
    match = re.match(r'(.+)_(\d{4})\.pdf', filename)
    if match:
        parsha, year = match.groups()
        parsha = titlecase(parsha.replace('_', ' '))
        return year, parsha
    return None, None


def get_sort_key(pdf):
    year, parsha, filename = pdf
    parsha_stripped = parsha.removesuffix(' Bonus Shtikel')
    if parsha_stripped in parsha_order:
        return year, parsha_order.index(parsha_stripped)
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

    index_html = render_template('maamarei_mordechai_template.html', {'grouped_pdfs': grouped_pdfs})
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
