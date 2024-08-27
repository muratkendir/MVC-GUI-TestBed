import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pylab import draw_networkx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(width=400, height=400)
        self.grid(row=0, column=0, rowspan=8, columnspan=8, padx=10, pady=10)
        # Graph Creator inputs
        self.graph_name_lbl = ttk.Label(self, text="Type a name for the graph : ")
        self.graph_name_lbl.grid(row=1, column=0, padx=10, pady=10)
        self.graph_name = ttk.Entry(self)
        self.graph_name.grid(row=1, column=1, padx=10, pady=10,sticky = tk.W)

        self.create_graph = ttk.Button(self, text = "Create the graph",  command = self.create_graph_clicked)
        self.create_graph.grid(row=1, column=2, padx=10, pady=10)

        # Book Selection
        self.selected_book = tk.StringVar()
        self.selected_book.set("Select a book")
        self.drop_lbl = ttk.Label(self, text="Choose a book: ")
        self.drop_lbl.grid(row=2, column=0, padx=10, pady=10)
        self.books= []
        self.drop = ttk.OptionMenu( self , self.selected_book, *self.books)
        self.drop.grid(row=2, column=1, columnspan=2, padx=10, pady=10,sticky = tk.W)

        # Specify the referenced book
        self.ref_book_lbl = ttk.Label(self, text="Referenced book:")
        self.ref_book_lbl.grid(row=3, column=0, padx=10, pady=10)
        self.ref_book = ttk.Entry(self)
        self.ref_book.grid(row=3, column=1, columnspan=2, padx=10, pady=10,sticky = tk.EW)

        # Specify the writer of reference book
        self.ref_author_lbl = ttk.Label(self, text="Writer of the book")
        self.ref_author_lbl.grid(row=4, column=0, padx=10, pady=10)
        self.ref_author = ttk.Entry(self)
        self.ref_author.grid(row=4, column=1, columnspan=2, padx=10, pady=10,sticky = tk.EW)

        # Set the page number of the relavant reference:
        self.ref_page_lbl = ttk.Label(self, text="Page Number: ")
        self.ref_page_lbl.grid(row=5, column=0, padx=10, pady=10)
        self.ref_page = ttk.Entry(self)
        self.ref_page.grid(row=5, column=1, padx=10, pady=10,sticky = tk.EW)

        # Set the reference type
        self.types = ['Select a type', 'Footnote', 'Bibliography']
        self.types_select = tk.StringVar()
        self.types_select.set("Select a type")
        self.types_lbl = ttk.Label(self, text="Select a type for reference: ")
        self.types_lbl.grid(row=6, column=0, padx=10, pady=10)
        self.types_list = ttk.OptionMenu( self ,self.types_select, *self.types )
        self.types_list.grid(row=6, column=1, padx=10, pady=10,sticky = tk.EW)

        # Add the reference to the graph
        self.add_to_graph = ttk.Button(self, text = "Add Reference to Graph",  command = self.add_to_graph_clicked)
        self.add_to_graph.grid(row=7, column=0, padx=10, pady=10,sticky = tk.EW)

        # Save graph as file
        self.export_graph_button = ttk.Button(self, text = "Export graph as file",  command = self.export_graph_clicked)
        self.export_graph_button.grid(row=7, column=1, padx=10, pady=10,sticky = tk.EW)

        # message
        self.message_label = ttk.Label(self, text='', foreground='red')
        self.message_label.grid(row=8, column=0, columnspan=3, sticky=tk.W)

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def set_books(self):
        if self.controller:
            books = self.controller.get_books()
            self.drop.set_menu(books[0],*books)

    def create_graph_clicked(self):
        if self.controller:
            graph = self.graph_name.get()
            self.controller.set_graph_name(graph)
            self.controller.create_a_graph()

    def add_to_graph_clicked(self):
        if self.controller:
            entries = {"graphName" : self.graph_name.get(), 
                "selectedBook" : self.selected_book.get(),
                "referencedBook" : self.ref_book.get(),
                "referencedAuthor" : self.ref_author.get(),
                "referencePageNumber" : self.ref_page.get(),
                "selectedReferenceType" : self.types_select.get()
                }
            self.controller.add_to_graph(entries)
            self.reset_references()
    def export_graph_clicked(self):
        if self.controller:
            self.controller.export_graph()

    def show_error(self, message):
        """
        Show an error message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)

    def show_success(self, message):
        """
        Show a success message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

    def hide_message(self):
        """
        Hide the message
        :return:
        """
        self.message_label['text'] = ''

    def reset_references(self):
        """
        Reset the fields of the reference.
        :return:
        """
        self.ref_book.delete(0, 'end')
        self.ref_author.delete(0, 'end')
        self.ref_page.delete(0, 'end')
        self.types_select.set(self.types[0])

class Output(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(width=400, height=400)
        self.grid(row=8, column=0, rowspan=8, columnspan=3,padx=10, pady=10)
        self.draw_graph_button = ttk.Button(self, text = "Draw the Graph",  command = self.draw_graph)
        self.draw_graph_button.grid(row=8, column=1, padx=10, pady=10,sticky = tk.EW)
        
    def draw_graph(self):
        if self.controller:
            graph = self.controller.get_graph()
            draw_networkx(graph, pos=nx.spring_layout(graph), node_color="#a2ad00", edge_color="#E37222")

            canvas = tk.Canvas(self, width=200, height=200)
            canvas.grid(row=9, column=0, padx=10, pady=10,sticky = tk.EW)
            figure, axes = plt.gcf(), plt.gca()
            figure_tk = FigureCanvasTkAgg(figure, master=canvas)
            figure_tk.get_tk_widget().pack(side="top", fill="both", expand=True)
            figure_tk.draw()

    def set_controller(self, controller):
        self.controller = controller