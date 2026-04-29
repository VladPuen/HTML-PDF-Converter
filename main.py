import sys
from pathlib import Path
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
        self.setWindowIcon(QIcon("media/app_ico.png"))


        url_label = QLabel("Enter URL:")
        self.url_entry = QLineEdit("")

        directory_entry_label = QLabel("Enter directory to save: ")
        self.directory_label = QLabel("")
        search_bttn = QPushButton("Fetch save location")
        search_bttn.clicked.connect(self.directory_search)
        convert_bttn = QPushButton("Convert")
        convert_bttn.clicked.connect(self.extract_url)

        url_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        directory_entry_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.directory_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(url_label, 0, 0)
        layout.addWidget(self.url_entry, 0, 1)
        layout.addWidget(directory_entry_label, 1, 0)
        layout.addWidget(self.directory_label, 2, 0, 1, 2)
        layout.addWidget(search_bttn,1, 1)
        layout.addWidget(convert_bttn, 3, 0, 1, 2)
        layout.setColumnStretch(1, 2)

    def directory_search(self):
            self.file_direct = QFileDialog()
            self.file_direct.setWindowTitle("Open Folder")
            self.file_direct.setFileMode(QFileDialog.FileMode.Directory)
            self.file_direct.setViewMode(QFileDialog.ViewMode.List)
            if self.file_direct.exec():
                self.selected_directory = self.file_direct.selectedFiles()[0]
                self.directory_label.setText(f"Set directory: {self.selected_directory}")

    def extract_url(self):
        try:
            url_set= self.url_entry.text()
            if not url_set.strip():
                QMessageBox.warning(self, "Empty URL", "Set a valid url link.")
                return
            directory = Path(self.selected_directory) / "converted_file.pdf"

            html_document = HTML(url=url_set)
            converted_file = html_document.write_pdf()

            directory.write_bytes(converted_file)
        except AttributeError:
            QMessageBox.warning(self, "Location not selected", "Check directory.")
            return
        except PermissionError:
            QMessageBox.warning(self, "Permission Denied", "Please select a valid directory or check if directory exists.")
            return
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

def main():
    main_app = QApplication(sys.argv)
    url_convert = MainWindow()
    url_convert.show()
    sys.exit(main_app.exec())

if __name__ == "__main__":
    main()