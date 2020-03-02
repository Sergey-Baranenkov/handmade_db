from PyQt5 import QtWidgets
from main_window_class import Main_window
from matplotlib import pyplot as plt
from time import time


def main():
    app = QtWidgets.QApplication([])
    main_menu = Main_window()
    main_menu.load_db("/home/araxal/dbtest/test")
    n = 1000
    collision_cf = 1000

    main_menu.delete_row({'п1': "_*", 'п2': "_*"})
    add_timer = []
    for i in range(n):
        s = time()
        main_menu.add_row({'п1': str(i), 'п2': str(i % collision_cf)})
        s = time() - s
        add_timer.append(s if s < 0.1 else 0)

    plt.plot([i for i in range(n)], add_timer)
    plt.show()

    delete_timer = []
    for i in range(n):
        s = time()
        main_menu.delete_row({'п1': str(i), 'п2': str(i % collision_cf)})
        s = time() - s
        delete_timer.append(s if s < 0.1 else 0)

    plt.plot([i for i in range(n)], delete_timer)
    plt.show()

    #main_menu.show()
    #exit(app.exec())


if __name__ == '__main__':
    main()
