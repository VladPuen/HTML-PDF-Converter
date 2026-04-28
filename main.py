import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from weasyprint import HTML
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("URL to HTML converter")
        self.resize(400, 200)
        layout = QGridLayout()
        self.setLayout(layout)


        url_label = QLabel("Enter URL:")
        self.url_entry = QLineEdit("")

        directory_entry_label = QLabel("Enter directory to save: ")
        self.directory_label = QLabel("")
        search_bttn = QPushButton("Fetch save location")
        search_bttn.clicked.connect(self.directory_search)
        convert_bttn = QPushButton("Convert")
        # convert_bttn.clicked.connect(self.extract_url)

        url_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        directory_entry_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(url_label, 0, 0)
        layout.addWidget(self.url_entry, 0, 1)
        layout.addWidget(directory_entry_label, 1, 0)
        layout.addWidget(self.directory_label, 2, 1)
        layout.addWidget(search_bttn,1, 1)
        layout.addWidget(convert_bttn, 3, 0)
    def directory_search(self):
        file_direct = QFileDialog()
        file_direct.setWindowTitle("Open Folder")
        file_direct.setFileMode(QFileDialog.FileMode.Directory)
        file_direct.setViewMode(QFileDialog.ViewMode.List)
        if file_direct.exec():
            selected_directory = file_direct.selectedFiles()[0]
            self.directory_label.setText(selected_directory)

    # def extract_url(self):
    #     convert_sucess = pyqtSignal()
    #     try:
    #         url = self.url_entry.text()
    #         html_document = HTML(string=url, base_url="")
    #     except:
    #         print("Error reading URL.")

        

# class url_field(QDialog):
def main():
    main_app = QApplication(sys.argv)
    url_convert = MainWindow()
    url_convert.show()
    sys.exit(main_app.exec())

if __name__ == "__main__":
    main()