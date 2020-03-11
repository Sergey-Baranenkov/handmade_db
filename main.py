from PyQt5 import QtWidgets
from main_window_class import Main_window
from matplotlib import pyplot as plt
from time import time


def main():
    app = QtWidgets.QApplication([])
    main_menu = Main_window()

    #main_menu.load_db("/home/araxal/dbtest/test")

    main_menu.show()
    exit(app.exec())


if __name__ == '__main__':
    main()
