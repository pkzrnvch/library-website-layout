import math
import os
import json
from math import ceil

from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


def rebuild():
    os.makedirs('./pages', exist_ok=True)
    books_per_page = 20
    with open('book_descriptions.json') as json_file:
        books = json.load(json_file)
    book_chunks = chunked(books, books_per_page)
    total_pages = ceil(len(books) / books_per_page)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    for page, book_chunk in enumerate(book_chunks, start=1):
        book_pairs = list(chunked(book_chunk, 2))
        rendered_page = template.render(
            book_pairs=book_pairs,
            total_pages=total_pages,
            current_page_number=page,
        )
        with open(f'./pages/index{page}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    rebuild()
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')


if __name__ == '__main__':
    main()
