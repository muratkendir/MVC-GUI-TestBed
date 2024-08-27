import yaml
import networkx as nx

class Model:
    def __init__(self, datafile):
        self.datafile = datafile
        self.graph_name = ''
        self.selected_book = ''
        self.referenced_book = ''
        self.referenced_writer = ''
        self.page_number = ''
        self.selected_ref_type = ''
        self.b2b = nx.DiGraph()

    def get_datafile(self):
        with open(self.datafile, 'r') as file:
            book_data = yaml.safe_load(file)
        return book_data

    def get_books_list(self):
        book_data = self.get_datafile()
        books = []
        for x in book_data['books-read']:
            book_name = x['name']
            books.append(book_name)
        return books