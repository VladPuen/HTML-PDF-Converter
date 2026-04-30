import sys
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from weasyprint import HTML
import requests


class HTML_PDF_Convert(QThread):
    finish_conversion = pyqtSignal(bytes)
    error_msg = pyqtSignal(str)
    def __init__(self, url_set):
        super().__init__()
        self.url_set = url_set
    def run_process(self):
        try:
            def ssl_cert(url_set):
                set_response = requests.get(url_set, verify=True)
                return {
                        "string":set_response.content,
                        "mime_type": set_response.headers.get("Content-Type", "text/html"),
                        }
            html_document = HTML(url=self.url_set, url_fetcher=ssl_cert)
            converted_file = html_document.write_pdf()
            # Send bytes of converted file
            self.finish_conversion.emit(converted_file)
        except Exception as e:
            self.error_msg.emit(str(e))

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
        self.convert_bttn = QPushButton("Convert")
        self.convert_bttn.clicked.connect(self.extract_url)

        url_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        directory_entry_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.directory_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(url_label, 0, 0)
        layout.addWidget(self.url_entry, 0, 1)
        layout.addWidget(directory_entry_label, 1, 0)
        layout.addWidget(self.directory_label, 2, 0, 1, 2)
        layout.addWidget(search_bttn,1, 1)
        layout.addWidget(self.convert_bttn, 3, 0, 1, 2)
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
        url_set= self.url_entry.text()
        if not url_set.strip():
            QMessageBox.warning(self, "Empty URL", "Set a valid url link.")
            return
        # Prevent the user to click again while converting PDF
        self.convert_bttn.setEnabled(False)
        self.convert_bttn.setText("Converting page to PDF...")


        self.convert_signal = HTML_PDF_Convert(url_set)
        self.convert_signal.finished.connect(self.save_pdf_file)
        self.convert_signal.error_msg.connect(self.error_display)
        self.convert_signal.start()

    def save_pdf_file(self, converted_file):
        try:
            directory = Path(self.selected_directory) / "converted_file.pdf"
            directory.write_bytes(converted_file)
        except PermissionError:
            QMessageBox.warning(self, "Permission Denied", "Please select a valid directory or check if directory exists.")
            return
        finally:
            self.convert_bttn.setEnabled(True)
            self.convert_bttn.setText("Convert")
    
    def error_display(self, error_msg):
        QMessageBox.warning(self, "Error", error_msg)
        self.convert_bttn.setEnabled(True)
        self.convert_bttn.setText("Convert")
def main():
    main_app = QApplication(sys.argv)
    url_convert = MainWindow()
    url_convert.show()
    sys.exit(main_app.exec())

if __name__ == "__main__":
    main()