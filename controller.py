import networkx as nx
import matplotlib.pyplot as plt

class Controller:
    def __init__(self, model, view, output):
        self.model = model
        self.view = view
        self.output = output

    def set_graph_name(self, graph):
        self.model.graph_name = graph
        # print('G: ' + self.model.graph_name)

    def create_a_graph(self):
        graph_name = self.model.graph_name
        self.model.b2b.name = graph_name
        # show a success message
        self.view.show_success(f'The graph < {graph_name} > created!')

    def get_books(self):
        books = self.model.get_books_list()
        return books

    def add_to_graph(self, entries):
        # Get additional attributes from the data file by filtering by the selected book.
        # print(entries)
        book_data = self.model.get_datafile()
        selected_book = entries['selectedBook']
        selected_books_data = list(filter(lambda book: book['name'] == selected_book, book_data['books-read']))
        selected_books_author = selected_books_data[0]['author']
        # print("Author: ", selected_books_author)
        b2b = self.model.b2b
        b2b.add_edges_from([(selected_book, entries['referencedBook'], {"weight": 1, "page": entries['referencePageNumber'], "ref-type": entries['selectedReferenceType']})])

        # Add the author name as attribute to the node if it is available in data file
        if 'author' in selected_books_data[0].keys():
            b2b.nodes[selected_book]['author'] = selected_books_data[0]['author']
            print('Author info found and added to node.')
        else:
            print('Author info not found.')
        
        # Add author name to referenced book
        b2b.nodes[ entries['referencedBook'] ]['author'] = entries['referencedAuthor']

    def export_graph(self):
        file_name = self.model.graph_name + '.gexf'
        nx.write_gexf(self.model.b2b, file_name)
        self.view.show_success(f'The graph saved as < {file_name} > !')

    def get_graph(self):
        b2b = self.model.b2b
        return b2b

    # def save(self, email):
    #     """
    #     Save the email
    #     :param email:
    #     :return:
    #     """
    #     try:

    #         # save the model
    #         self.model.email = email
    #         self.model.save()

    #         # show a success message
    #         self.view.show_success(f'The email {email} saved!')

    #     except ValueError as error:
    #         # show an error message
    #         self.view.show_error(error)