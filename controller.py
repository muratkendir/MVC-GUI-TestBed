import networkx as nx
import matplotlib.pyplot as plt
from trans import trans

class Controller:
    def __init__(self, model, view, output):
        self.model = model
        self.view = view
        self.output = output

    def set_graph_name(self, graph):
        self.model.graph_name = graph
        self.view.show_success(f'The graphname is set to < {graph} >.')

    def create_a_graph(self):
        graph_name = self.model.graph_name
        self.model.b2b.name = graph_name
        self.view.show_success(f'The graph < {graph_name} > created!')

    def get_books(self):
        books = self.model.get_books_list()
        return books

    def add_to_graph(self, entries):
        # Get additional attributes from the data file by filtering by the selected book.
        book_data = self.model.get_datafile()
        selected_book = entries['selectedBook']
        selected_books_data = list(filter(lambda book: book['name'] == selected_book, book_data['books-read']))
        selected_books_author = selected_books_data[0]['author']
        b2b = self.model.b2b
        # Get the name of the source and target books and encode the names ASCII to use in edge id
        selected_book_trns = trans(selected_book, 'slug')      
        referenced_book_trns = trans(entries['referencedBook'], 'slug')
        edge_id = selected_book_trns + '---' + referenced_book_trns
        b2b.add_edges_from([(selected_book, entries['referencedBook'], {"id": edge_id, "weight": 1, "page": entries['referencePageNumber'], "ref-type": entries['selectedReferenceType']})])
        self.view.show_success(f'The Book < {selected_book} > successfully referenced to < {entries['referencedBook']} >.')

        # Add the author name as attribute to the node if it is available in data file
        if 'author' in selected_books_data[0].keys():
            b2b.nodes[selected_book]['author'] = selected_books_data[0]['author']
        else:
            self.view.show_error('Author info not found.')
        
        # Add author name to referenced book
        b2b.nodes[ entries['referencedBook'] ]['author'] = entries['referencedAuthor']

    def export_graph(self):
        file_name = self.model.graph_name + '.gexf'
        nx.write_gexf(self.model.b2b, file_name)
        self.view.show_success(f'The graph saved as < {file_name} > !')

    def get_graph(self):
        b2b = self.model.b2b
        return b2b