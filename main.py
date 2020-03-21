from PyQt5 import QtWidgets
from PyQt5 import QtGui


from design import Ui_MainWindow
import stroke_recognition
import sys
import cv2
import numpy as np
FILE_NAME = ""
cv_image = 0


# Класс окна вывода.
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.inputImage.setScaledContents(True)
        # self.ui.inputImage = QtWidgets.QLabel(self)

        # Привязка обработчика на кнопку загрузки фотографии.
        self.ui.loadButton.clicked.connect(self.load_file)

        # Привязка обработчика на кнопку "найти очаг".
        self.ui.findStrokeButton.clicked.connect(self.load_image)

        # Привязка обработчика на кнопку скачивания фотографии.
        self.ui.downloadButton.clicked.connect(self.download_file)

    # Функция-обработчика загрузки снимка.
    def load_file(self):
        global FILE_NAME
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'C:/')
        FILE_NAME = file_name[0]
        self.ui.fileName.setText(FILE_NAME)
        input_pixmap = QtGui.QPixmap(FILE_NAME)
        self.ui.inputImage.setPixmap(input_pixmap)

    # Функция-обработчика кнопки "найти очаг".
    def load_image(self):
        global FILE_NAME, cv_image

        if FILE_NAME != "":
            cv_image = stroke_recognition.find_regions(FILE_NAME)
            height, width, channel = cv_image.shape
            bytes_per_line = 3 * width
            q_image = QtGui.QImage(cv_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
            output_pixmap = QtGui.QPixmap(q_image)
            self.ui.outputImage.setPixmap(output_pixmap)
        else:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Файл не выбран!")

    # Функция-обработчика сохранения снимка.
    def download_file(self):
        global cv_image
        options = QtWidgets.QFileDialog.Options()
        # options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                             "All Files (*);;(*.jpg)",
                                                             options=options)
        print("HI MARK")
        print(cv_image)
        print(not np.any(cv_image))

        print(file_name)
        print(cv_image)

        if not np.any(cv_image):
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Снимок не загружен")
        elif file_name:
            cv2.imwrite(file_name, cv_image)


app = QtWidgets.QApplication([])
application = Window()
application.show()

sys.exit(app.exec())


