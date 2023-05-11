from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections


def convert_time_to_period(date):
    now_year = date.year
    start_year = datetime.date(year=1920, month=1, day=1)
    delta_year = now_year - start_year.year
    if delta_year % 10 == 1 and delta_year % 100 != 11:
        suffix_year = 'год'
    elif str(delta_year % 10) in ('2', '3', '4') and str(delta_year % 100) not in ('12', '13', '14'):
        suffix_year = 'года'
    else:
        suffix_year = 'лет'
    return f'{delta_year} {suffix_year}'


def converting_from_excel(filename):
    categories_dict = collections.defaultdict(list)
    for category in sorted(set(pandas.read_excel(filename)['Категория'].tolist())):
        for wine in pandas.read_excel(filename, na_values=None, keep_default_na=False).to_dict(orient='records'):
            if wine['Категория'] == category:
                categories_dict[category].append(wine)
    return categories_dict


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        time_period=convert_time_to_period(datetime.datetime.now()),
        production_data=converting_from_excel('wine3.xlsx')
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()


