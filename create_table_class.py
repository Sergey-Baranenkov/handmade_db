from PyQt5 import QtWidgets
from src.create_table import Ui_Dialog as ct_dialog
from os import chdir, mkdir, chmod, access, W_OK, R_OK, X_OK
from info_messages_class import show_critical_message, show_information_message
from initial import *
from functools import partial


class Create_table_dialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(Create_table_dialog, self).__init__(parent)
        self.parent = parent
        self.ui = ct_dialog()
        self.ui.setupUi(self)
        self.ui.add_field_button.clicked.connect(self.add_field)
        self.ui.help_button.clicked.connect(partial(show_information_message, "ВАЖНО: Имя поле должно быть меньше 255 "
                                                                              "символов "
                                                                              "и состоять только из русских букв и "
                                                                              "цифр\nДлина "
                                                                              " поля должна быть числовой"))
        self.ui.create_table_button.clicked.connect(self.create_table_verification_wrapper)
        self.ui.specify_path_button.clicked.connect(self.load_path)

    def load_path(self):
        self.ui.path_line.setText(QtWidgets.QFileDialog.getExistingDirectory())

    def create_table(self, fields, dir_path, table_name):
        chdir(dir_path)
        try:
            mkdir(table_name)
            chdir(table_name)
        except OSError:
            show_critical_message("Невозможно создать базу данных по заданному пути!\n"
                                  "База данных(папка) {0} уже существует!".format(table_name))
            return

        with open("db_config.cfg", "w") as cfg:
            for field in fields:
                cfg.write("{0}{1}{2}{1}{3}\n".format(field[0], spec_symbol, field[1], field[2]))
                mkdir(field[0])
        open("main_table.txt", "w", encoding=db_encoding).close()
        open("gaps.txt", "w", encoding=db_encoding).close()
        chmod("db_config.cfg", 0o444)

        show_information_message("База данных успешно создана, теперь вы можете ее загрузить!")

    def create_table_verification_wrapper(self):
        directory_path = self.ui.path_line.text()
        table_name = self.ui.table_name.text()
        if not access(directory_path, X_OK | W_OK | R_OK):
            show_critical_message("Невозможно создать базу данных по заданному пути! Задайте правильный путь")
            return
        if not len(table_name):
            show_critical_message("Имя бд не установлено! Установите имя бд")
            return
        fields = []
        for col in range(self.ui.layout_table.columnCount()):
            field_name = self.ui.layout_table.item(0, col).text()
            field_len = self.ui.layout_table.item(1, col).text()
            is_primary = 1 if self.ui.layout_table.item(0, col).background().color() == primary_color else 0

            if field_name.isalnum() and len(field_name) < 255 and field_len.isdigit():
                fields.append([field_name, field_len, is_primary])
            else:
                show_critical_message("Ошибка в заполнении поля " + field_name + ":" + field_len + " посмотрите help!")
                return
        if len(fields) == 0:
            show_critical_message("Не добавлено ни 1 поля!")
        elif len(set([field[0] for field in fields])) != len(fields):
            show_critical_message("Не все поля уникальны!")
        else:
            self.create_table(fields, directory_path, table_name)

    def add_field(self):
        c_count = self.ui.layout_table.columnCount()
        self.ui.layout_table.setColumnCount(c_count + 1)
        self.ui.layout_table.setHorizontalHeaderItem(c_count, QtWidgets.QTableWidgetItem())
        item1 = QtWidgets.QTableWidgetItem("поле")
        item2 = QtWidgets.QTableWidgetItem("5")
        self.ui.layout_table.setItem(0, c_count, item1)
        self.ui.layout_table.setItem(1, c_count, item2)
        button_group = QtWidgets.QWidget()

        del_button = QtWidgets.QPushButton("✖")
        del_button.setMinimumSize(40, 20)
        del_button.setStyleSheet("background-color: red; color:white")
        del_button.clicked.connect(self.delete_field)
        changeMode_button = QtWidgets.QPushButton("⚙")
        changeMode_button.setMinimumSize(40, 20)
        changeMode_button.setStyleSheet("background-color: orange; color: white")
        changeMode_button.clicked.connect(self.change_field_mode)
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(del_button)
        h_layout.addWidget(changeMode_button)
        button_group.setLayout(h_layout)
        self.ui.layout_table.setCellWidget(2, c_count, button_group)

    def delete_field(self):
        col = self.ui.layout_table.indexAt(self.sender().parent().pos()).column()
        self.ui.layout_table.removeColumn(col)

    def change_field_mode(self):
        col = self.ui.layout_table.indexAt(self.sender().parent().pos()).column()
        if self.ui.layout_table.item(0, col).background().color() != primary_color:
            self.ui.layout_table.item(0, col).setBackground(primary_color)
            self.ui.layout_table.item(1, col).setBackground(primary_color)
        else:
            self.ui.layout_table.item(0, col).setBackground(white_color)
            self.ui.layout_table.item(1, col).setBackground(white_color)
