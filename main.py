from src.create_table import Ui_Dialog as ct_dialog
from src.main_window import Ui_MainWindow as mw_dialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QRegExpValidator
from os import access, W_OK, R_OK, X_OK, chdir, mkdir, chmod, makedirs, remove
from shutil import rmtree
from os.path import basename, isfile, getsize
from hashlib import sha3_256 as hasher
from collections import OrderedDict

primary_color = QColor(176, 224, 230)
white_color = QColor(255, 255, 255)
db_encoding = "cp1251"
spec_symbol = "‡"
regex = QRegExp("[^{0}]*".format(spec_symbol))
uf_fname = "test.f"


def check_encoding(string, encoding):
    try:
        string.encode(encoding, string)
        return True
    except UnicodeEncodeError:
        return False


def show_critical_message(message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(message)
    msg.exec()


def show_information_message(message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(message)
    msg.exec()


def get_indexes(path, field_name):
    print("PATH:", path)
    path = path + "/" + uf_fname
    if not isfile(path):
        return None, None
    # файл найден
    i = 0
    with open(path, "r", encoding=db_encoding) as f:
        for line in f:
            print("line",line)
            i += len(line)
            line = line.rstrip().split(":", maxsplit=1)
            print("i", i,[int(idx) for idx in line[1].split()])
            if line[0] == field_name:
                return [int(idx) for idx in line[1].split()], i
    return None, None


def get_hash_path(word):
    #h = hasher(word.encode()).hexdigest()
    h = "aa"
    hp = "/".join([h[i:i + 2] for i in range(0, len(h), 2)])
    return hp


def get_unique_indexes(columns, paths_needed=False):
    paths_hashes = {}
    indexes = None
    field_found_flag = False
    for header, value in columns.items():
        if value == "_*":
            continue
        try:
           pass
        except:
            indexes = set()
            break
    return indexes, paths_hashes


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
        # self.ui.export_button.clicked.connect(self.tryHasher)
        self.ui.create_db_button.clicked.connect(self.create_new_table_dialog)
        self.ui.load_existing_db_button.clicked.connect(self.load_db)
        self.path = None
        self.fields = None
        self.strlen = 0

    def func_radio(self):
        if not self.sender().isChecked():
            return

        if self.sender().text() == "Обновить":
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)


    def add_row(self):
        columns = self.get_field(self.ui.small_input_table, 0)

        for header, value in columns.items():
            if not check_encoding(value, db_encoding):
                show_critical_message("Поле {0} не соответствует доступным символам!".format(header))
                return
            elif value == "_*":
                show_critical_message("_* - зарезервированный символ для поиска по всему полю")
                return

            # если primary key
            if self.fields[header][1] == 1:
                if len(value) == 0:
                    show_critical_message("Primary key поле {0} не заполнено!".format(header))
                    return

                hash_path = get_hash_path(value)
                if get_indexes(header + "/" + hash_path, value)[0] is not None:
                    show_critical_message("Primary key {0} уже существует!".format(header))
                    return

                p_hashes[value] = hash_path

            elif len(value) > self.fields[header][0]:
                show_critical_message(
                    "Поле {0} превышает допустимую длину на {1}!".format(header, len(value) - self.fields[header][0]))
                return

        with open("gaps.txt", "r+", encoding=db_encoding) as gaps:
            all_gaps = gaps.read().split()
            write_index = int(all_gaps.pop()) if all_gaps else int(getsize("main_table.txt") / self.strlen)
            gaps.truncate(0)
            if all_gaps:
                gaps.write(" ".join(all_gaps) + " ")

        print("write_index", write_index)
        # формируем строку для записи и добавляем индексы
        record_string = ""
        for header, value in columns.items():
            record_string += value.ljust(self.fields[header][0], spec_symbol)
            hash_path_with_root = header + "/" + (
                get_hash_path(value) if p_hashes.get(value) is None else p_hashes[value])
            makedirs(hash_path_with_root, exist_ok=True)
            open(hash_path_with_root + "/" + uf_fname, "a", encoding=db_encoding).close()

            indexes, i = get_indexes(hash_path_with_root, value)
            print("indexes, i", indexes, i)

            with open(hash_path_with_root + "/" + uf_fname, "r+", encoding=db_encoding) as file:
                ending = ""
                if i is not None:
                    file.seek(i)
                    ending = file.read()
                    file.truncate(i - 1)

                file.seek(0, 2)

                start = "{0}:".format(value) if indexes is None else ""
                file.write(start + str(write_index) + " \n" + ending)

        with open("main_table.txt", "r+", encoding=db_encoding) as mt_file:
            mt_file.seek(write_index * self.strlen)
            mt_file.write(record_string)


    def executor(self):
        p_hashes = {}
        if self.ui.add_r.isChecked():
            self.add_row()
        elif self.ui.select_r.isChecked():
            self.ui.main_table.setRowCount(0)
            indexes = get_unique_indexes(self.get_field(self.ui.small_input_table, 0))[0]
            el_count = 0
            max_count = self.ui.count.value()

            if indexes is None:
                with open("main_table.txt", "r", encoding=db_encoding) as f, open("gaps.txt", "r", encoding=db_encoding) as gaps:
                    print(gaps.read().split())
                    gaps_dict = {}.fromkeys([int(i) for i in gaps.read().split()], True)
                    while field := f.read(self.strlen):
                        if gaps_dict.get(el_count) is not None:
                            el_count += 1
                            max_count += 1
                            continue

                        if el_count >= max_count:
                            break
                        self.main_table_add_row(self.string_splitter(field))
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
                show_critical_message("Ничего не найдено!")

        elif self.ui.delete_r.isChecked():
            indexes, paths_hashes = get_unique_indexes(self.get_field(self.ui.small_input_table, 0),
                                                            paths_needed=True)
            if indexes is None:
                open("main_table.txt", "w", encoding=db_encoding).close()
                open("gaps.txt", "w", encoding=db_encoding).close()
                for field in self.fields.keys():
                    rmtree(field)
                    mkdir(field)
            elif len(indexes):
                for header, path in paths_hashes.items():
                    f = open(path, "r+", encoding=db_encoding)
                    new_indexes = set([int(index) for index in f.read().split()]) - indexes
                    if len(new_indexes):
                        f.truncate(0)
                        f.write(" ".join([str(i) for i in new_indexes]) + " ")
                        f.close()
                    else:
                        f.close()
                        remove(path)

                empty_string = spec_symbol * self.strlen
                with open("gaps.txt", "a", encoding=db_encoding) as gaps:
                    gaps.write(" ".join([str(i) for i in indexes]) + " ")

                with open("main_table.txt", "r+", encoding=db_encoding) as f:
                    for index in indexes:
                        f.seek(index * self.strlen)
                        f.write(empty_string)
            else:
                show_critical_message("Ничего не было удалено так как под маску не подходит ни 1 поле!")
        else:
            # Обновить
            print("Обновить")

    def main_table_add_row(self, field):
        new_row_index = self.ui.main_table.rowCount()
        self.ui.main_table.setRowCount(new_row_index + 1)
        for i, el in enumerate(field):
            self.ui.main_table.setItem(new_row_index, i, QtWidgets.QTableWidgetItem(el))

    def string_splitter(self, string):
        split_string = []
        start = 0
        end = 0
        for info in self.fields.values():
            tmp_s = ""
            end += info[0]
            while start != end and string[start] != spec_symbol:
                tmp_s += string[start]
                start += 1
            start = end
            split_string.append(tmp_s)
        return split_string

    def get_field(self, table, row):
        columns = OrderedDict()
        for i in range(table.columnCount()):
            item = table.cellWidget(row, i)
            columns[table.horizontalHeaderItem(i).text()] = item.text()
        return columns

    def load_db(self):
        path = QtWidgets.QFileDialog.getExistingDirectory()
        if not path:
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
                    field = field.split(":")
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
                        item.setValidator(QRegExpValidator(regex))
                        st.setCellWidget(0, i, item)

                        bt.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(field[0]))
                        item = QtWidgets.QLineEdit()
                        item.setValidator(QRegExpValidator(regex))
                        bt.setCellWidget(0, i, item)
                        item = QtWidgets.QLineEdit()
                        item.setValidator(QRegExpValidator(regex))
                        bt.setCellWidget(1, i, item)

            self.fields = fields
            self.path = path
            self.strlen = sum([v[0] for v in fields.values()])
            self.ui.db_name.setText(basename(path))

            self.ui.functional_widget.setEnabled(True)
            self.ui.main_table.setEnabled(True)
        except IOError:
            show_critical_message("База данных не валидна!\ndb_config.cfg не найден!")

    def create_new_table_dialog(self):
        dialog = Create_table_dialog(self)
        dialog.exec()


def select_path(path_line):
    path_line.setText(QtWidgets.QFileDialog.getExistingDirectory())


class Create_table_dialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(Create_table_dialog, self).__init__(parent)
        self.parent = parent
        self.ui = ct_dialog()
        self.ui.setupUi(self)
        self.ui.add_field_button.clicked.connect(self.add_field)
        self.ui.help_button.clicked.connect(self.get_help)
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
                cfg.write("{0}:{1}:{2}\n".format(field[0], field[1], field[2]))
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

    def get_help(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(
            "ВАЖНО: Имя поле должно быть меньше 255 символов и состоять только из русских букв и цифр\n"
            "Длина поля должна быть числовой")
        msg.setDetailedText(
            "Добавить поле - добавляет новое поле \n"
            "Красная кнопка - удаляет поле\n"
            "Желтая кнопка - меняет тип поля: синий цвет - первичный ключ, белый - обычное поле")
        msg.exec()

    def add_field(self):
        c_count = self.ui.layout_table.columnCount()
        self.ui.layout_table.setColumnCount(c_count + 1)
        self.ui.layout_table.setHorizontalHeaderItem(c_count, QtWidgets.QTableWidgetItem())
        item1 = QtWidgets.QTableWidgetItem("000")
        item2 = QtWidgets.QTableWidgetItem("111")
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


def main():
    app = QtWidgets.QApplication([])
    main_menu = Main_window()
    main_menu.show()
    exit(app.exec())


if __name__ == '__main__':
    main()
