import os
import subprocess
import sys
import urllib.request
from io import BytesIO

from PIL import Image
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QComboBox, QMainWindow, QFileDialog, QLabel, QHBoxLayout, QVBoxLayout, \
    QWidget, QTextEdit, QSpinBox, QLineEdit, QDialog, QPushButton, QFormLayout, QMessageBox

# Check if dependencies are installed
try:
    from PyQt6 import QtGui, QtCore
except ImportError:
    print("Installing dependencies...")

    # Install dependencies
    required_packages = ["pyqt6", "pillow"]
    for package in required_packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    print("Dependencies installed.")

    # Import dependencies
    from PyQt6 import QtGui, QtCore

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("mods balls cruncher")
        self.widget = QComboBox()
        self.widget.addItem("Choose Action")
        self.widget.addItem("Select Images")
        self.widget.addItem("Compress Images")
        self.widget.currentTextChanged.connect(self.text_changed)

        # Fetch and display the logos
        python_logo_url = "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
        bitcoin_logo_url = "https://bitcoin.org/img/icons/opengraph.png"
        python_logo = self.fetch_image(python_logo_url, 0.3)
        bitcoin_logo = self.fetch_image(bitcoin_logo_url, 0.3)
        python_logo_label = QLabel()
        python_logo_label.setPixmap(python_logo)
        python_logo_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        bitcoin_logo_label = QLabel()
        bitcoin_logo_label.setPixmap(bitcoin_logo)
        bitcoin_logo_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        # Create a layout for the logos and the combobox
        layout = QVBoxLayout()
        logos_layout = QHBoxLayout()
        logos_layout.addWidget(python_logo_label)
        logos_layout.addWidget(bitcoin_logo_label)
        layout.addLayout(logos_layout)
        layout.addWidget(self.widget)

        # Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.image_paths = []  # Initialize image_paths as a list
        self.setMinimumSize(QSize(400, 300))  # Set minimum size of the window

        self.event_text = QTextEdit()
        self.event_text.setReadOnly(True)
        layout.addWidget(self.event_text)

    def fetch_image(self, url, scale):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        img_data = response.read()
        img = Image.open(BytesIO(img_data))
        width, height = img.size
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        qimg = self.convert_image_to_pixmap(resized_img)
        return qimg

    def convert_image_to_pixmap(self, img):
        image = img.convert("RGBA")
        data = image.tobytes("raw", "RGBA")
        qimage = QtGui.QImage(data, image.size[0], image.size[1], QtGui.QImage.Format.Format_RGBA8888)
        pixmap = QtGui.QPixmap.fromImage(qimage)
        return pixmap

    def text_changed(self, s):  # s is a str
        try:
            if s == "Select Images":
                self.select_images()
            elif s == "Compress Images" and self.image_paths:
                self.open_compression_dialog()
            else:
                self.add_event("Please select images first.")
        except Exception as e:
            self.add_event(f"Error in text_changed: {e}")

    def select_images(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.bmp)")
        if file_dialog.exec():
            self.image_paths.extend(file_dialog.selectedFiles())  # Extend the list with selected image paths
            num_images = len(self.image_paths)
            self.add_event(f"{num_images} images loaded for compression.")
        else:
            self.add_event("No images selected.")

    def open_compression_dialog(self):
        dialog = CompressionDialog(self)
        dialog.exec()

    def compress_images(self, quality, resolution, fragments, output_folder):
        try:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                
            for image_path in self.image_paths:
                self.compress_image(image_path, quality, resolution, fragments, output_folder)
                
            self.add_event(f"All images saved to {output_folder}")
        except Exception as e:
            self.add_event(f"Error in compress_images: {e}")

    def compress_image(self, image_path, quality, resolution, fragments, output_folder):
        try:
            with Image.open(image_path) as img:
                # Resize image
                img = img.resize(resolution, Image.LANCZOS)

                # Convert image to RGB mode
                rgb_img = img.convert('RGB')

                # Save with specified quality
                base = os.path.basename(image_path)
                for i in range(fragments):
                    fragment = rgb_img.crop((0, i * resolution[1] // fragments, resolution[0], (i + 1) * resolution[1] // fragments))
                    output_path = os.path.join(output_folder, f"{os.path.splitext(base)[0]}_part{i+1}.jpg")
                    fragment.save(output_path, "JPEG", quality=quality)

            self.add_event(f"Image {image_path} saved to {output_folder}")
        except Exception as e:
            self.add_event(f"Error in compress_image: {e}")

    def add_event(self, event):
        self.event_text.append(event)


class CompressionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Compression Options")
        self.setModal(True)

        self.quality_spinbox = QSpinBox()
        self.quality_spinbox.setRange(1, 100)
        self.quality_spinbox.setValue(20)
        
        self.width_edit = QLineEdit()
        self.height_edit = QLineEdit()
        
        self.fragments_spinbox = QSpinBox()
        self.fragments_spinbox.setRange(1, 100)
        self.fragments_spinbox.setValue(10)
        
        self.output_folder_edit = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_output_folder)
        
        self.compress_button = QPushButton("Compress")
        self.compress_button.clicked.connect(self.compress_images)

        layout = QFormLayout()
        layout.addRow("Compression Quality:", self.quality_spinbox)
        layout.addRow("Desired Width:", self.width_edit)
        layout.addRow("Desired Height:", self.height_edit)
        layout.addRow("Number of Fragments:", self.fragments_spinbox)
        layout.addRow("Output Folder:", self.output_folder_edit)
        layout.addRow(self.browse_button)
        layout.addRow(self.compress_button)

        self.setLayout(layout)

    def browse_output_folder(self):
        output_folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        self.output_folder_edit.setText(output_folder)

    def compress_images(self):
        quality = self.quality_spinbox.value()
        width = int(self.width_edit.text())
        height = int(self.height_edit.text())
        fragments = self.fragments_spinbox.value()
        output_folder = self.output_folder_edit.text()

        if not os.path.exists(output_folder):
            QMessageBox.critical(self, "Error", "Invalid output folder path.")
            return

        parent = self.parent()
        parent.compress_images()
        self.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
