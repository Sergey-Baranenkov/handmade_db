from PyQt5 import QtWidgets
from main_window_class import Main_window
from matplotlib import pyplot as plt
from time import time


def main():
    app = QtWidgets.QApplication([])
    main_menu = Main_window()

    # main_menu.load_db("/home/araxal/dbtest/test")
    # n = 10000
    # collision_cf = 1000
    # select_timer = []
    #
    # main_menu.delete_row({'поле1': "*", 'поле2': "*", "поле3": "*"})
    # add_timer = []
    # for i in range(n):
    #     s = time()
    #     main_menu.add_row({'поле1': str(i), 'поле2': str(i % collision_cf), 'поле3': str(i % int(collision_cf / 2))})
    #     s = time() - s
    #     add_timer.append(s if s < 0.02 else 0)
    #     s = time()
    #     main_menu.select_row({'поле1': str(i), 'поле2': str(i % collision_cf), 'поле3': str(i % int(collision_cf / 2))})
    #     s = time() - s
    #     select_timer.append(s if s < 0.02 else 0)
    #
    # plt.plot([i for i in range(n)], add_timer)
    # plt.show()
    #
    # plt.plot([i for i in range(n)], select_timer)
    # plt.show()
    #
    # delete_timer = []
    # for i in range(n):
    #     s = time()
    #     main_menu.delete_row({'поле1': str(i), 'поле2': str(i % collision_cf), 'поле3': str(i % int(collision_cf / 2))})
    #     s = time() - s
    #     delete_timer.append(s if s < 0.02 else 0)
    #
    # plt.plot([i for i in range(n)], delete_timer)
    # plt.show()

    main_menu.show()
    exit(app.exec())


if __name__ == '__main__':
    main()
