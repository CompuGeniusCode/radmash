import os
import re

from jinja2 import Environment, FileSystemLoader
from titlecase import titlecase

PDF_DIR = 'divrei_torah/maamarei_mordechai'
TEMPLATE_DIR = 'templates'

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# for filename in os.listdir(PDF_DIR):
#     if filename.endswith('.pdf'):
#         new_filename = filename.lower().removeprefix("_")
#         os.rename(os.path.join(PDF_DIR, filename), os.path.join(PDF_DIR, new_filename))


parsha_order = ["Bereishis", "Noach", "Lech Lecha", "Vayera", "Chayei Sarah", "Toldos", "Vayetzei", "Vayishlach",
                "Vayeshev", "Channukah", "Miketz", "Vayigash", "Vaychi", "Shmos", "Vaera", "Bo", "Beshalach", "Yisro",
                "Mishpatim", "Terumah", "Titzaveh", "Purim", "Ki Sisa", "Vayakel - Pekudei", "Vayakel", "Pekudei",
                "Vayikra", "Tzav", "Shmini", "Tazria - Metzora", "Tazria", "Metzora", "Achrei Mos - Kedoshim",
                "Achrei Mos", "Kedoshim", "Emor", "Behar - Bechukosai", "Behar", "Bechukosai", "Bamidbar and Shavuos",
                "Bamidbar", "Shavuos", "Naso", "Behaaloscha", "Shlach", "Korach", "Chukas", "Balak", "Pinchas",
                "Matos - Maasei", "Matos", "Maasei", "Devarim", "Vaeschanan", "Eikev", "Re'eh", "Shoftim",
                "Ki Tzeitzei", "Ki Savo", "Nitzavim", "Vayeilech", "Haazinu and Succos", "Haazinu", "Vezot Haberachah"]


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

    pdfs.sort(key=lambda x: (x[0], parsha_order.index(x[1]) if x[1] in parsha_order else float('inf')))

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

    index_html = render_template('index.html', {'grouped_pdfs': grouped_pdfs})
    with open('test.html', 'w') as f:
        f.write(index_html)


if __name__ == '__main__':
    generate_html()
