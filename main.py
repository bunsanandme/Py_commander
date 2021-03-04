from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
import subprocess
from styleSheet import style
import datetime


def logger(func):
    def wrapper(*args):
        file = open(('logs.txt'), "a")
        today = datetime.datetime.today()
        file.write("{}-".format(today.strftime("%Y/%m/%d %H:%M")))
        result = func(*args)
        file.write("{}-".format(func.__name__) + "[INFO]: Entering {}\n".format(result))

    return wrapper


# Обьявляем класс самого окна
# Обьявление начальнух двух директорий(поменяй на диски твоего компьютера)
# И также флаг, в каком окне сейчас работаем
# True - правое, False - левое
path = ""


class PyCo(QMainWindow):
    directory = "E:"
    directory2 = "C:/"
    first_selected = True

    # Конструктор класса
    # Вызываем методы интерфейса и наследуемся

    def __init__(self):
        super(PyCo, self).__init__()
        self.setupMenus()
        self.interface()

    # Методы переключения флага
    # Методов два для разных панелей

    def selection1(self):
        self.first_selected = True

    def selection2(self):
        self.first_selected = False

    # Интерфейс самих окон
    # Все это лежит на нескольких слоях
    # Добавляем два QListWidget, именно это наши директории
    # Привязываем двойное нажатие для смены директории
    # Также привязываем выделение к смене флагов
    # Здесь добавляем также кнопки и привязываем действия
    # Добавляем CSS для стиля окон и корректируем геометрию

    def interface(self):
        self.folder_icon = QIcon("folder.png")
        self.file_icon = QIcon("file.png")
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        self.list1 = QListWidget()
        self.list1.itemDoubleClicked.connect(self.change_directory1)
        self.list1.itemSelectionChanged.connect(self.selection1)
        self.update_list1()
        self.list2 = QListWidget()
        self.list2.itemDoubleClicked.connect(self.change_directory2)
        self.list2.itemSelectionChanged.connect(self.selection2)
        self.update_list2()
        self.grid.addWidget(self.list1, 0, 0, 1, 1)
        self.grid.addWidget(self.list2, 0, 1, 1, 1)
        self.hbox2 = QHBoxLayout()
        self.hbox2.setSpacing(0)
        self.hbox1 = QHBoxLayout()
        self.hbox1.setSpacing(0)
        self.but1 = QPushButton(self)
        self.but1.setText("Создать")
        self.but1.clicked.connect(self.make_directory)
        self.but2 = QPushButton(self)
        self.but2.setText("Переименовать")
        self.but2.clicked.connect(self.rename_directory)
        self.but3 = QPushButton(self)
        self.but3.setText("Копировать")
        self.but3.clicked.connect(self.copy_directory)
        self.but4 = QPushButton(self)
        self.but4.setText("Переместить")
        self.but4.clicked.connect(self.move_directory)
        self.but6 = QPushButton(self)
        self.but6.setText("Удалить")
        self.but6.clicked.connect(self.delete_directory)
        self.but7 = QPushButton(self)
        self.but7.setText("Выход")
        self.but7.clicked.connect(QCoreApplication.instance().quit)
        self.hbox1.addWidget(self.but1)
        self.hbox1.addWidget(self.but2)
        self.hbox1.addWidget(self.but3)
        self.hbox1.addWidget(self.but4)
        self.hbox1.addWidget(self.but6)
        self.hbox1.addWidget(self.but7)
        mainLayout.addLayout(self.grid)
        mainLayout.addLayout(self.hbox2)
        mainLayout.addLayout(self.hbox1)
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        self.setStyleSheet(style)

        self.setGeometry(70, 70, 500, 500)
        self.setWindowIcon(QIcon('total2.png'))
        self.setWindowTitle("PyCo")

    # Окно с ошибкой

    def error_message(self):
        ret = QMessageBox.abort(self, 'Ошибка',
                                "Отказано в доступе",
                                QMessageBox.Ok, QMessageBox.Ok)

    # Окно с информацией
    # Выскакиевает при нажатии "О программе"

    def about_message(self):
        ret = QMessageBox.question(self, 'Информация',
                                   "Хех, тут ничего :)",
                                   QMessageBox.Ok, QMessageBox.Ok)

    def open_logs(self):
        os.system("start logs.txt")

    def delete_logs(self):
        with open("logs.txt", "w"):
            pass

    # Инициализация верхнего меню
    # Добавляем меню и привязываем действия

    def setupMenus(self):
        self.open_logsAction = QAction("Просмотреть логи", self)
        self.open_logsAction.triggered.connect(self.open_logs)
        self.delete_logsAction = QAction("Очистить логи", self)
        self.delete_logsAction.triggered.connect(self.delete_logs)
        self.aboutAction = QAction("О программе...", self)
        self.aboutAction.triggered.connect(self.about_message)
        self.helpMenu = self.menuBar().addMenu("Помощь")
        self.helpMenu.addAction(self.open_logsAction)
        self.helpMenu.addAction(self.delete_logsAction)
        self.helpMenu.addAction(self.aboutAction)

    # Самый важный метод - обновления окна
    # Вытаскиваем все директории по пути и добавляем на виджет

    def update_list1(self):
        self.list1.clear()
        if self.directory.split("/").__len__() != 1:
            self.list1.addItem("...")
        names = os.listdir(self.directory)

        for name in names:
            path = self.directory + "/" + name
            if os.path.isdir(path):
                item = QListWidgetItem(self.folder_icon, name)
                self.list1.addItem(item)
            else:
                item = QListWidgetItem(self.file_icon, name)
                self.list1.addItem(item)

    # Смена директории
    # Если нажали "...", то возвращаемся на каталог выше
    # Иначе спускаемся ниже
    @logger
    def change_directory1(self, item):
        name = item.text()
        if name == "...":
            self.directory = self.directory.split("/")
            del self.directory[-1]
            self.directory = '/'.join(self.directory)
            self.update_list1()
        else:
            if os.path.isfile(self.directory + "/" + name):
                process = subprocess.Popen("start {}".format(name), cwd=self.directory, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
                self.update_list1()
            else:
                self.directory += "/" + item.text()
                path = self.directory
                self.update_list1()
        return self.directory

    # Аналогично выше, только для второй панели

    def update_list2(self):
        self.list2.clear()
        if self.directory2.split("/").__len__() != 2:
            self.list2.addItem("...")
        names = os.listdir(self.directory2)

        for name in names:
            path = self.directory2 + "/" + name
            if os.path.isdir(path):
                item = QListWidgetItem(self.folder_icon, name)
                self.list2.addItem(item)
            else:
                item = QListWidgetItem(self.file_icon, name)
                self.list2.addItem(item)

    @logger
    def change_directory2(self, item):
        name = item.text()
        if name == "...":
            self.directory2 = self.directory2.split("/")
            del self.directory2[-1]
            self.directory2 = '/'.join(self.directory2)
            self.update_list2()
        else:
            if os.path.isfile(self.directory2 + "/" + name):
                process = subprocess.Popen("start {}".format(name), cwd=self.directory2, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
                self.update_list2()
            else:
                self.directory2 += "/" + item.text()
                self.update_list2()
        return self.directory2

    # Смена директории
    # Имитируем процесс через командную строки
    # Также делаем диалоговое окно, где вводим название
    # Повторяем для второй панельки код в зависимости от флага

    def make_directory(self):
        if self.first_selected:
            text, ok = QInputDialog.getText(self, 'Создание',
                                            'Название директории:')
            command = "mkdir \"{}\"".format(text)
            if ok:
                process = subprocess.Popen(command, cwd=self.directory, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
                out, err = process.communicate()
                if err:
                    self.error_message()
            self.update_list1()
        else:
            text, ok = QInputDialog.getText(self, 'Создание',
                                            'Название директории:')
            command = "mkdir \"{}\"".format(text)
            if ok:
                process = subprocess.Popen(command, cwd=self.directory2, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
                out, err = process.communicate()
                if err:
                    self.error_message()
            self.update_list2()

    # Переименование папки
    # Действия аналогичны для создания папки
    # И также для второй панели

    # Все функции кнопок работют аналогично верхним

    def rename_directory(self):
        if self.first_selected:
            for item in self.list1.selectedItems():
                old_name = item.text()
            text, ok = QInputDialog.getText(self, 'Переименование',
                                            'Новое название директории:')
            command = "ren \"{}\" \"{}\"".format(old_name, text)
            if ok:
                process = subprocess.Popen(command, cwd=self.directory, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
                out, err = process.communicate()
                if err:
                    self.error_message()
            self.update_list1()
        else:
            for item in self.list2.selectedItems():
                old_name = item.text()
                text, ok = QInputDialog.getText(self, 'Переименование',
                                                'Новое название директории:')
                command = "ren \"{}\" \"{}\"".format(old_name, text)
                if ok:
                    process = subprocess.Popen(command, cwd=self.directory2, stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE, shell=True)
                    out, err = process.communicate()
                    if err:
                        self.error_message()
                self.update_list2()

    # Удаление папки(важно!)

    def delete_directory(self):
        if self.first_selected:
            for item in self.list1.selectedItems():
                old_name = item.text()
            command = "rmdir /s /q \"{}\"".format(old_name)
            process = subprocess.Popen(command, cwd=self.directory, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            if err:
                self.error_message()
            self.update_list1()
        else:
            for item in self.list2.selectedItems():
                old_name = item.text()
            command = "rmdir /s /q \"{}\"".format(old_name)
            process = subprocess.Popen(command, cwd=self.directory2, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            if err:
                self.error_message()
            self.update_list2()

    # Копирование папки
    # Здесь идет два процесса, смена директори и копирование

    def copy_directory(self):
        if self.first_selected:
            for item in self.list1.selectedItems():
                old_name = item.text()
            text, ok = QInputDialog.getText(self, 'Копирование',
                                            'Путь для копирования:')
            command = "xcopy {} {}".format(old_name, text)
            if ok:
                process = subprocess.Popen("cd {}".format(self.directory), cwd=self.directory, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
                process = subprocess.Popen(command, cwd=self.directory, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
                out, err = process.communicate()
                if err:
                    self.error_message()
            self.directory = text
            self.update_list1()
        else:
            for item in self.list2.selectedItems():
                old_name = item.text()
            text, ok = QInputDialog.getText(self, 'Копирование',
                                            'Путь для копирования:')

            command = "xcopy {} {}".format(old_name, text)
            if ok:
                process = subprocess.Popen("cd {}".format(self.directory2), cwd=self.directory2, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
                process = subprocess.Popen(command, cwd=self.directory2, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
                out, err = process.communicate()
                if err:
                    self.error_message()
            self.directory2 = text
            self.update_list2()

    # Перемещение папки
    # Аналогично с копированием

    def move_directory(self):
        if self.first_selected:
            for item in self.list1.selectedItems():
                old_name = item.text()
            text, ok = QInputDialog.getText(self, 'Перемещение',
                                            'Путь для перемещения:')
            command = "move {} {}".format(self.directory + '/' + old_name, text + "/" + old_name)
            if ok:
                process = subprocess.Popen(command, cwd=self.directory, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
                out, err = process.communicate()
                if err:
                    self.error_message()
            self.directory = text
            self.update_list1()
        else:
            for item in self.list2.selectedItems():
                old_name = item.text()
            text, ok = QInputDialog.getText(self, 'Перемещение',
                                            'Путь для перемещения:')
            command = "move {} {}".format(self.directory2 + '/' + old_name, text + "/" + old_name)
            if ok:
                process = subprocess.Popen(command, cwd=self.directory2, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
                out, err = process.communicate()
                if err:
                    self.error_message()
            self.directory = text
            self.update_list2()


# Запускаем программку, как-то так!

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PyCo()
    window.show()
    sys.exit(app.exec_())
