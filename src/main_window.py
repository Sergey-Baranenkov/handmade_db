# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1129, 659)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_5.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.create_db_button = QtWidgets.QToolButton(self.centralwidget)
        self.create_db_button.setObjectName("create_db_button")
        self.horizontalLayout_5.addWidget(self.create_db_button)
        self.load_existing_db_button = QtWidgets.QToolButton(self.centralwidget)
        self.load_existing_db_button.setObjectName("load_existing_db_button")
        self.horizontalLayout_5.addWidget(self.load_existing_db_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.db_name = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(28)
        self.db_name.setFont(font)
        self.db_name.setAlignment(QtCore.Qt.AlignCenter)
        self.db_name.setObjectName("db_name")
        self.horizontalLayout_4.addWidget(self.db_name)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.functional_widget = QtWidgets.QWidget(self.centralwidget)
        self.functional_widget.setObjectName("functional_widget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.functional_widget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 10, -1, 10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.add_r = QtWidgets.QRadioButton(self.functional_widget)
        self.add_r.setChecked(True)
        self.add_r.setObjectName("add_r")
        self.verticalLayout_2.addWidget(self.add_r)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.select_r = QtWidgets.QRadioButton(self.functional_widget)
        self.select_r.setObjectName("select_r")
        self.horizontalLayout_7.addWidget(self.select_r)
        self.count = QtWidgets.QSpinBox(self.functional_widget)
        self.count.setMinimum(1)
        self.count.setObjectName("count")
        self.horizontalLayout_7.addWidget(self.count)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.update_r = QtWidgets.QRadioButton(self.functional_widget)
        self.update_r.setObjectName("update_r")
        self.verticalLayout_2.addWidget(self.update_r)
        self.delete_r = QtWidgets.QRadioButton(self.functional_widget)
        self.delete_r.setObjectName("delete_r")
        self.verticalLayout_2.addWidget(self.delete_r)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.stackedWidget = QtWidgets.QStackedWidget(self.functional_widget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.small_input_table = QtWidgets.QTableWidget(self.page)
        self.small_input_table.setRowCount(1)
        self.small_input_table.setObjectName("small_input_table")
        self.small_input_table.setColumnCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.small_input_table.setVerticalHeaderItem(0, item)
        self.horizontalLayout_2.addWidget(self.small_input_table)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.page_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.big_input_table = QtWidgets.QTableWidget(self.page_2)
        self.big_input_table.setRowCount(2)
        self.big_input_table.setObjectName("big_input_table")
        self.big_input_table.setColumnCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.big_input_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.big_input_table.setVerticalHeaderItem(1, item)
        self.horizontalLayout_3.addWidget(self.big_input_table)
        self.stackedWidget.addWidget(self.page_2)
        self.horizontalLayout_6.addWidget(self.stackedWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 10, -1, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.export_button = QtWidgets.QPushButton(self.functional_widget)
        self.export_button.setObjectName("export_button")
        self.verticalLayout.addWidget(self.export_button)
        self.make_backup_button = QtWidgets.QPushButton(self.functional_widget)
        self.make_backup_button.setObjectName("make_backup_button")
        self.verticalLayout.addWidget(self.make_backup_button)
        self.execute_command = QtWidgets.QPushButton(self.functional_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.execute_command.sizePolicy().hasHeightForWidth())
        self.execute_command.setSizePolicy(sizePolicy)
        self.execute_command.setObjectName("execute_command")
        self.verticalLayout.addWidget(self.execute_command)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        self.verticalLayout_3.addWidget(self.functional_widget)
        self.main_table = QtWidgets.QTableWidget(self.centralwidget)
        self.main_table.setEnabled(False)
        self.main_table.setObjectName("main_table")
        self.main_table.setColumnCount(0)
        self.main_table.setRowCount(0)
        self.verticalLayout_3.addWidget(self.main_table)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.create_db_button.setText(_translate("MainWindow", "Создать новую бд"))
        self.load_existing_db_button.setText(_translate("MainWindow", "Загрузить существующую бд"))
        self.db_name.setText(_translate("MainWindow", "имя бд"))
        self.add_r.setText(_translate("MainWindow", "Добавить"))
        self.select_r.setText(_translate("MainWindow", "Выбрать"))
        self.update_r.setText(_translate("MainWindow", "Обновить"))
        self.delete_r.setText(_translate("MainWindow", "Удалить"))
        item = self.small_input_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Что"))
        item = self.big_input_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Что"))
        item = self.big_input_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Новое знач"))
        self.export_button.setText(_translate("MainWindow", "Экспортировать"))
        self.make_backup_button.setText(_translate("MainWindow", "Создать бэкап"))
        self.execute_command.setText(_translate("MainWindow", "Исполнить команду"))
