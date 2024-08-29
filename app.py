from controller import Controller
from model import Model
import argparse
parser = argparse.ArgumentParser(prog='Book2Book')
parser.add_argument('-g', '--gui', default='tkinter', help='Select one of the GUI library: Tkinter | Some other ...')
args = parser.parse_args()
if args.gui == 'tkinter':
    print('Default GUI selected.')
    from view import tk, View, Output
else:
    from view import tk, View, Output

from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Books to Books References - Graph Creator')
        self.geometry("800x800")

        # create a model
        model = Model('b2b-data.yaml')

        # create a view and place it on the root window
        view = View(self)

        output=Output(self)

        # create a controller
        controller = Controller(model, view, output)

        # set the controller to view
        view.set_controller(controller)
        output.set_controller(controller)
        # Get the books from YAML file
        view.set_books()

if __name__ == '__main__':
    app = App()
    app.mainloop()