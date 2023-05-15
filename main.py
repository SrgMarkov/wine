import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
from dotenv import load_dotenv


def convert_time_to_period(now_date):
    date_of_creation = 1920
    delta_year = now_date.year - date_of_creation
    if delta_year % 10 == 1 and delta_year % 100 != 11:
        suffix_year = 'год'
    elif str(delta_year % 10) in ('2', '3', '4') and str(delta_year % 100) not in ('12', '13', '14'):
        suffix_year = 'года'
    else:
        suffix_year = 'лет'
    return f'{delta_year} {suffix_year}'


def convert_from_excel(filename):
    categories = collections.defaultdict(list)
    products = pandas.read_excel(filename, na_values=None, keep_default_na=False).to_dict(orient='records')
    for product in products:
        category = product['Категория']
        categories[category].append(product)
    return categories


def main():
    load_dotenv()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        time_period=convert_time_to_period(datetime.datetime.now()),
        products=convert_from_excel(os.getenv('DIR'))
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()


