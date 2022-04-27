import json

from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape


def rebuild():
    with open('book_descriptions.json') as json_file:
        books_metadata = json.load(json_file)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        books_metadata=books_metadata
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    rebuild()
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')


if __name__ == '__main__':
    main()
