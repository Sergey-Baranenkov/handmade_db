from PyQt5.QtWidgets import QFileDialog
from src.main_window import Ui_MainWindow as mw_dialog
from my_functools import check_encoding, get_hash_path, get_indexes, get_unique_indexes, get_options
from initial import *
from info_messages_class import *

from PyQt5 import QtWidgets
from PyQt5.QtGui import QRegExpValidator
from os import access, W_OK, R_OK, X_OK, chdir, mkdir, makedirs
from shutil import rmtree, copytree
from os.path import basename, isfile, getsize, isdir
from collections import OrderedDict
from datetime import datetime
from create_table_class import Create_table_dialog


def select_path(path_line):
    path_line.setText(QFileDialog.getExistingDirectory())


class Main_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        self.ui = mw_dialog()
        self.ui.setupUi(self)
        self.ui.functional_widget.setEnabled(False)
        self.ui.main_table.setEnabled(False)

        self.ui.execute_command.clicked.connect(self.executor)
        self.ui.select_r.toggled.connect(self.func_radio)
        self.ui.count.setMaximum(1000000000)
        self.ui.add_r.toggled.connect(self.func_radio)
        self.ui.delete_r.toggled.connect(self.func_radio)
        self.ui.update_r.toggled.connect(self.func_radio)
        self.ui.export_button.clicked.connect(self.export_csv)
        self.ui.make_backup_button.clicked.connect(self.create_backup)
        self.ui.create_db_button.clicked.connect(self.create_new_table_dialog)
        self.ui.load_existing_db_button.clicked.connect(self.load_db)
        self.path = None
        self.fields = None
        self.strlen = 0

    def create_backup(self):
        try:
            b_name = str(datetime.now())
            copytree(".", "./" + b_name)
            show_information_message("Успешно")
        except Exception as e:
            show_critical_message(str(e))

    def export_csv(self):
        mt = self.ui.main_table
        with open(str(datetime.now()) + ".csv", "w") as f:
            f.write(",".join([mt.horizontalHeaderItem(i).text() for i in range(mt.columnCount())]) + "\n")
            for i in range(mt.rowCount()):
                row = []
                for j in range(mt.columnCount()):
                    row.append(mt.item(i, j).text())
                f.write(",".join(row) + "\n")
        show_information_message("Успешно!")

    def func_radio(self):
        if not self.sender().isChecked():
            return

        if self.sender().text() == "Обновить":
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

    def add_row(self, fields, p_hashes=None):
        if p_hashes is None:
            p_hashes = {}

        with open("gaps.txt", "r+", encoding=db_encoding) as gaps_f:
            all_gaps = gaps_f.read().split()
            write_index = int(all_gaps.pop() if all_gaps else getsize("main_table.txt") / self.strlen)
            gaps_f.truncate(0)
            gaps_f.seek(0)
            if all_gaps:
                gaps_f.write(" ".join(all_gaps) + " ")

        record_string = ""
        for header, value in fields.items():
            record_string += value.ljust(self.fields[header][0], spec_symbol)
            hash_path_with_root = header + "/" + (
                get_hash_path(value) if p_hashes.get(value) is None else p_hashes[value])
            makedirs(hash_path_with_root, exist_ok=True)
            open(hash_path_with_root + "/" + uf_fname, "a", encoding=db_encoding).close()

            _, i = get_indexes(hash_path_with_root, value)

            with open(hash_path_with_root + "/" + uf_fname, "r+", encoding=db_encoding) as file:
                ending = ""
                if i is not None:
                    file.seek(i[1])
                    ending = file.read()
                    file.truncate(i[1] - 1)

                file.seek(0, 2)

                start = "{0}{1}".format(value, spec_symbol) if i is None else ""
                file.write(start + str(write_index) + " \n" + ending)

        with open("main_table.txt", "r+", encoding=db_encoding) as mt_file:
            mt_file.seek(write_index * self.strlen)
            mt_file.write(record_string)

    def select_row(self, fields):
        indexes = get_unique_indexes(fields)[0]
        el_count = 0
        max_count = self.ui.count.value()

        if indexes == "*":
            with open("main_table.txt", "r", encoding=db_encoding) as f, \
                    open("gaps.txt", "r", encoding=db_encoding) as gaps:

                gaps_dict = {}.fromkeys([int(i) for i in gaps.read().split()], True)
                while field := f.read(self.strlen):
                    if gaps_dict.get(el_count) is True:
                        el_count += 1
                        max_count += 1
                        continue

                    if el_count >= max_count:
                        break
                    self.main_table_add_row(self.string_splitter(field))
                    # self.string_splitter(field)
                    el_count += 1

        elif len(indexes):
            with open("main_table.txt", "r", encoding=db_encoding) as f:
                for index in indexes:
                    if el_count >= max_count:
                        break
                    f.seek(index * self.strlen)
                    self.main_table_add_row(self.string_splitter(f.read(self.strlen)))
                    el_count += 1
        else:
            raise Exception("Ничего не найдено!")

    def delete_row(self, fields):
        unique_indexes, add_info = get_unique_indexes(fields, add_info_needed=True)
        if unique_indexes == "*":
            for header in self.fields.keys():
                rmtree(header)
                mkdir(header)
                open("main_table.txt", "w", encoding=db_encoding).close()
                open("gaps.txt", "w", encoding=db_encoding).close()
            return

        if not len(unique_indexes):
            raise Exception("Ничего не найдено")

        elif len(add_info) != len(fields.keys()):
            any_keys_headers = [h for h in fields.keys() if h not in add_info.keys()]

            with open("main_table.txt", "r", encoding=db_encoding) as mt:
                for index in unique_indexes:
                    mt.seek(index * self.strlen)
                    split = self.string_splitter(mt.read(self.strlen), only_required_fields=any_keys_headers)
                    for i, key in enumerate(any_keys_headers):
                        path = get_hash_path(split[i])
                        add_info[key].add((path + "/" + uf_fname, get_indexes(key + "/" + path, field_name=split[i])))

        for header, info in add_info.items():
            for field in info:
                with open(header + "/" + field[0], "r+", encoding=db_encoding) as f:
                    f.seek(field[1][1][1])
                    ending = f.read()
                    if diff := set(field[1][0]) - unique_indexes:
                        f.truncate(field[1][1][0] + len(fields[header]) + 1)
                        f.seek(0, 2)
                        f.write(" ".join([str(i) for i in diff]) + " \n" + ending)
                    else:
                        f.truncate(field[1][1][0])
                        f.seek(0, 2)
                        f.write(ending)

        with open("gaps.txt", "a", encoding=db_encoding) as gaps_f:
            gaps_f.write(" ".join([str(i) for i in unique_indexes]) + " ")

    def update_row(self, row_from, row_to):
        p_hashes = self.check_what_fields(row_to, check_pkey=False)
        for header, value in row_to.items():
            if self.fields[header][1] == 1 and value != row_from[header] and isfile(header + "/" + p_hashes[value] + "/" + uf_fname):
                raise Exception("Такой первичный ключ уже существует!")
            
        self.delete_row(row_from)
        self.add_row(row_to, p_hashes)

    def executor(self):
        if self.ui.add_r.isChecked():
            try:
                fields = get_options(self.ui.small_input_table, 0)
                p_hashes = self.check_what_fields(fields)
                self.add_row(fields, p_hashes)
                show_information_message("Успешно")
            except Exception as e:
                show_critical_message(str(e))

        elif self.ui.select_r.isChecked():
            self.ui.main_table.setRowCount(0)
            try:
                self.select_row(get_options(self.ui.small_input_table, 0))
                show_information_message("Успешно")
            except Exception as e:
                show_critical_message(str(e))

        elif self.ui.delete_r.isChecked():
            try:
                self.delete_row(get_options(self.ui.small_input_table, 0))
                show_information_message("Успешно")
            except Exception as e:
                show_critical_message(str(e))

        elif self.ui.update_r.isChecked():
            try:
                row_from = get_options(self.ui.big_input_table, 0)
                row_to = get_options(self.ui.big_input_table, 1)
                self.update_row(row_from, row_to)
                show_information_message("Успешно")
            except Exception as e:
                show_critical_message(str(e))

    def main_table_add_row(self, field):
        new_row_index = self.ui.main_table.rowCount()
        self.ui.main_table.setRowCount(new_row_index + 1)
        for i, el in enumerate(field):
            self.ui.main_table.setItem(new_row_index, i, QtWidgets.QTableWidgetItem(el))

    def string_splitter(self, string, only_required_fields=None):
        start, end = 0, 0
        if only_required_fields is None:
            only_required_fields = []
        split_string = []

        for header, info in self.fields.items():
            end += info[0]

            if only_required_fields and header not in only_required_fields:
                start = end
                continue

            i = string.find(spec_symbol, start, end)  # ищем спец символ
            i = end if i == -1 else i

            split_string.append(string[start:i])
            start = end

        return split_string

    def load_db(self, my_path=""):
        path = my_path if my_path else QtWidgets.QFileDialog.getExistingDirectory()
        if not isdir(path):
            return
        chdir(path)
        fields = OrderedDict()

        try:
            with open("db_config.cfg", "r") as cfg:
                mt = self.ui.main_table
                st = self.ui.small_input_table
                bt = self.ui.big_input_table
                mt.setColumnCount(0)
                st.setColumnCount(0)
                bt.setColumnCount(0)

                lines = cfg.read().splitlines()

                for i, field in enumerate(lines):
                    field = field.split(spec_symbol)
                    if not access(field[0], X_OK | W_OK | R_OK):
                        show_critical_message("База данных не валидна!\n"
                                              "Невозможно найти папку для поля {0}!".format(field[0]))
                        return
                    else:
                        fields[field[0]] = [int(field[1]), int(field[2])]
                        cc = i + 1
                        mt.setColumnCount(cc)
                        st.setColumnCount(cc)
                        bt.setColumnCount(cc)
                        mt.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(field[0]))

                        st.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(field[0]))
                        item = QtWidgets.QLineEdit()
                        item.setValidator(QRegExpValidator(spec_s_regex_restrictor))
                        st.setCellWidget(0, i, item)

                        bt.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(field[0]))
                        item = QtWidgets.QLineEdit()
                        item.setValidator(QRegExpValidator(spec_s_regex_restrictor))
                        bt.setCellWidget(0, i, item)
                        item = QtWidgets.QLineEdit()
                        item.setValidator(QRegExpValidator(spec_s_regex_restrictor))
                        bt.setCellWidget(1, i, item)

            self.fields = fields
            self.path = path
            self.strlen = sum([v[0] for v in fields.values()])
            self.ui.db_name.setText(basename(path))

            self.ui.functional_widget.setEnabled(True)
            self.ui.main_table.setEnabled(True)
        except IOError:
            show_critical_message("База данных не валидна!\ndb_config.cfg не найден!")

    def check_what_fields(self, fields, check_pkey=True):
        p_hashes = {}
        print(fields)
        for header, value in fields.items():
            if not check_encoding(value, db_encoding):
                raise Exception("Поле {0} не соответствует доступным символам!".format(header))
            if value == "*":
                raise Exception("* - зарезервированный символ для поиска по всему полю")

            print(header, value, self.fields[header][1], self.fields[header][0])
            if self.fields[header][1] == 1:  # если primary key
                hash_path = get_hash_path(value)
                if len(get_indexes(header + "/" + hash_path, value)[0]) and check_pkey:
                    raise Exception("Primary key {0} уже существует!".format(header))
                p_hashes[value] = hash_path

            if len(value) > self.fields[header][0]:
                raise Exception(
                    "Поле {0} превышает допустимую длину на {1}!".format(header, len(value) - self.fields[header][0]))
        return p_hashes

    def create_new_table_dialog(self):
        dialog = Create_table_dialog(self)
        dialog.exec()
