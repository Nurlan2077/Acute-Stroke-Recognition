from PyQt5 import QtWidgets
from PyQt5 import QtGui
from design import Ui_MainWindow

import os
import stroke_recognition
import sys
import cv2
import numpy as np

FILE_NAME = ""  # Глоб. переменная для хранения выбранного изображения.
cv_image = 0    # Глоб. переменная для обработанного изображения.


# Класс окна вывода.
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Привязка обработчика на кнопку загрузки фотографии.
        self.ui.loadButton.clicked.connect(self.load_file)

        # Привязка обработчика на кнопку "найти очаг".
        self.ui.findStrokeButton.clicked.connect(self.process_image)

        # Привязка обработчика на кнопку скачивания фотографии.
        self.ui.downloadButton.clicked.connect(self.download_file)

    # Функция загрузки снимка.
    def load_file(self):
        global FILE_NAME
        options = QtWidgets.QFileDialog.Options()
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Загрузка файла', 'C:/',  "(*.jpg)",
                                                          options=options)

        FILE_NAME = file_name[0]                    # Получает путь к файлу.
        self.ui.fileName.setText(FILE_NAME)         # Выводит путь к файлу на интерфейс.

        input_pixmap = QtGui.QPixmap(FILE_NAME)     # Инициализирует pixmap для изображения.
        self.ui.inputImage.setPixmap(input_pixmap)  # Выводит изображение на интерфейс.

    # Функция-обработчика кнопки "найти очаг".
    def process_image(self):
        global FILE_NAME, cv_image

        # Если путь к файлу не пуст,
        # то начинает его обработку.
        if FILE_NAME != "":
            # Получает обработанное изображения и количество очагов на нём.
            cv_image, regions_num = stroke_recognition.find_regions(FILE_NAME)

            # Выводит на интерфейс количество очагов.
            self.ui.label.setText("Количество найденных очагов: " + str(regions_num))

            height, width, channel = cv_image.shape     # Получает информацию об изображении.
            bytes_per_line = 3 * width                  # Вспомог. переменная для перевода в qt pixmap.

            # Переводит в qt pixmap.
            q_image = QtGui.QImage(cv_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)

            # Инициализирует изображение для вывода на интерфейс.
            output_pixmap = QtGui.QPixmap(q_image)

            # Выводит обработанное изображение.
            self.ui.outputImage.setPixmap(output_pixmap)
        else:
            # Если путь к файлу пуст, выводит предупреждение.
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Файл не выбран!")

    # Функция-обработчика сохранения снимка.
    def download_file(self):
        global cv_image

        # Получает настройки для вывода диалогового окна скачивания изображения.
        options = QtWidgets.QFileDialog.Options()

        # Выводит диалоговое окно.
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Скачивание снимка",
                                                             "",
                                                             "*.jpg",
                                                             options=options)

        print(file_name)
        print(cv_image)

        # Если нет обработанного изображения.
        if not np.any(cv_image):
            # Выводит предупреждение.
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Снимок не загружен")

        elif file_name:
            file_name = file_name.split("/")    # Получает путь к файлу.
            path = file_name[:-1]               # Получает директорию к файлу.
            file_name = file_name[- 1]          # Получает название файла.
            path = "/".join(path)               # Переводит директорию в строку.

            print(file_name)
            print(path)

            # Меняет директорию.
            os.chdir(path)
            print(cv2.imwrite(file_name, cv_image))


app = QtWidgets.QApplication([])
application = Window()
application.show()

sys.exit(app.exec())


