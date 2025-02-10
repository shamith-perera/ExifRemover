import sys
import os
import random
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QCheckBox, QSpacerItem, QSizePolicy, QProgressBar
)
from PyQt5.QtCore import Qt, QSettings, QThread, pyqtSignal
from PIL import Image
from PyQt5.QtGui import QIcon


class ExifRemoverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_settings()

    def initUI(self):
        self.setWindowTitle("EXIF Remover")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet("background-color: #f5f5f5;")

        # Enable drag and drop
        self.setAcceptDrops(True)

        layout = QVBoxLayout()

        self.label = QLabel("Remove EXIF Metadata from Images", self)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333333; margin-bottom: 20px;")
        layout.addWidget(self.label)

        # Select Images Button
        self.selectButton = self.create_button("Select Image(s)", "#4CAF50", self.select_images)
        layout.addWidget(self.selectButton)

        # Spacer for some space between elements
        layout.addItem(QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.selectedImagesLabel = QLabel("Selected Images: 0", self)
        self.selectedImagesLabel.setStyleSheet("font-size: 14px; color: #555555;")
        layout.addWidget(self.selectedImagesLabel)

        # Clear Selected Images Button
        self.clearButton = self.create_button("Clear Selected Images", "#FF6347", self.clear_selected_images)
        layout.addWidget(self.clearButton)

        # Spacer for some space between elements
        layout.addItem(QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Rename Files Checkbox
        self.renameCheckBox = QCheckBox("Rename files", self)
        self.renameCheckBox.setStyleSheet("font-size: 14px; color: #333333;")
        layout.addWidget(self.renameCheckBox)

        # Output Folder Selection
        self.outputFolderLabel = QLabel("Output Folder: Not selected", self)
        self.outputFolderLabel.setStyleSheet("font-size: 14px; color: #555555;")
        layout.addWidget(self.outputFolderLabel)

        # Change Output Folder Button
        self.selectOutputButton = self.create_button("Change Output Folder", "#2196F3", self.select_output_folder)
        layout.addWidget(self.selectOutputButton)

        # Spacer for some space before the start button
        layout.addItem(QSpacerItem(10, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Start Button
        self.startButton = self.create_button("Start", "#4CAF50", self.start_processing)
        layout.addWidget(self.startButton)

        # Cancel Button
        self.cancelButton = self.create_button("Cancel", "#FF5722", self.cancel_processing, disabled=True)
        layout.addWidget(self.cancelButton)

        # Progress Bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        # Set the layout for the main window
        self.setLayout(layout)

        self.output_folder = None  # Initialize output folder to None
        self.files_to_process = []  # Store the selected files
        self.worker_thread = None  # Worker thread for long-running task

    def create_button(self, text, color, on_click, disabled=False):
        button = QPushButton(text, self)
        button.setStyleSheet(f"""
            font-size: 14px; padding: 12px; background-color: {color}; 
            color: white; border-radius: 8px; border: none; text-align: center;
            transition: background-color 0.3s ease, opacity 0.3s ease;
        """)
        button.clicked.connect(on_click)

        # Add hover effect for buttons
        button.setStyleSheet(button.styleSheet() + f"""
            QPushButton:hover {{
                background-color: {self.darken_color(color, 0.2)};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                opacity: 0.6;
            }}
        """)
        
        if disabled:
            button.setEnabled(False)

        return button

    def darken_color(self, color, factor):
        """Helper function to darken the color."""
        rgb = self.hex_to_rgb(color)
        darkened_rgb = [max(0, int(c * (1 - factor))) for c in rgb]
        return self.rgb_to_hex(darkened_rgb)

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB."""
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]

    def rgb_to_hex(self, rgb):
        """Convert RGB to hex color."""
        return '#' + ''.join(f'{c:02x}' for c in rgb)

    def load_settings(self):
        """Load the last selected output folder from settings."""
        settings = QSettings("ExifRemover", "ExifRemover")
        last_output_folder = settings.value("output_folder", None)
        if last_output_folder:
            self.output_folder = last_output_folder
            self.outputFolderLabel.setText(f"Output Folder: {last_output_folder}")

    def save_settings(self):
        """Save the selected output folder to settings."""
        if self.output_folder:
            settings = QSettings("ExifRemover", "ExifRemover")
            settings.setValue("output_folder", self.output_folder)

    def dragEnterEvent(self, event):
        """Handle drag enter event. Accept drag only if it's an image file."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop event to add files when dropped onto the window."""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        # Filter for image files
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff'))]
        
        if image_files:
            self.files_to_process.extend(image_files)
            self.update_selected_images_label()

    def select_images(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "", "Image Files (*.jpg *.jpeg *.png *.tiff)", options=options
        )

        if files:
            # Append the selected files to the existing list of selected images
            self.files_to_process.extend(files)
            self.update_selected_images_label()

    def clear_selected_images(self):
        # Clear the list of selected images
        self.files_to_process = []
        self.update_selected_images_label()

    def update_selected_images_label(self):
        # Update the label showing the number of selected images
        num_selected = len(self.files_to_process)
        self.selectedImagesLabel.setText(f"Selected Images: {num_selected}")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.outputFolderLabel.setText(f"Output Folder: {folder}")
            self.save_settings()  # Save the selected output folder

    def start_processing(self):
        """Start the process of removing EXIF metadata."""
        self.startButton.setDisabled(True)
        self.cancelButton.setEnabled(True)

        # Check if no images are selected
        if not self.files_to_process:
            QMessageBox.warning(self, "No Images Selected", "Please select some images first.")
            self.startButton.setEnabled(True)  # Re-enable the button
            self.cancelButton.setEnabled(False)
            return
        
        # Check if no output folder is selected
        if not self.output_folder:
            QMessageBox.warning(self, "No Output Folder Selected", "Please select an output folder.")
            self.startButton.setEnabled(True)  # Re-enable the button
            self.cancelButton.setEnabled(False)
            return

        # Check if the output folder exists, if not, prompt the user
        if not os.path.exists(self.output_folder):
            QMessageBox.warning(self, "Invalid Output Folder", "The selected output folder does not exist.")
            self.startButton.setEnabled(True)
            self.cancelButton.setEnabled(False)
            return

        # Reset progress bar before starting
        self.progressBar.setValue(0)

        # Start the image processing
        self.worker_thread = WorkerThread(self.files_to_process, self.output_folder, self.renameCheckBox.isChecked())
        self.worker_thread.processing_complete.connect(self.processing_complete)
        self.worker_thread.progress_updated.connect(self.update_progress)
        self.worker_thread.start()

    def cancel_processing(self):
        """Cancel the ongoing process."""
        if self.worker_thread:
            self.worker_thread.stop_processing()
            self.worker_thread.wait()  # Ensure the thread is stopped before continuing
        
        QMessageBox.information(self, "Process Cancelled", "The process has been cancelled.")
        
        # Reset progress bar
        self.progressBar.setValue(0)

        # Re-enable the start button after the cancellation
        self.cancelButton.setEnabled(False)
        self.startButton.setEnabled(True)

    def processing_complete(self, output_folder, success_count, failed_files):
        """Processing complete handler."""
        # Show the result in a message box
        QMessageBox.information(self, "Process Complete", 
                                f"Successfully processed {success_count} image(s).\n"
                                f"{len(failed_files)} failed.\n"
                                f"Output folder: {output_folder}")
        
        # Clear selected images after successful completion
        self.files_to_process = []
        self.update_selected_images_label()

        # Reset progress bar and buttons
        self.progressBar.setValue(0)
        
        # Re-enable the start button after the process is complete
        self.startButton.setEnabled(True)
        self.cancelButton.setEnabled(False)

    def update_progress(self, value):
        """Update the progress bar during processing."""
        self.progressBar.setValue(value)


class WorkerThread(QThread):
    """Thread for processing images in the background."""
    progress_updated = pyqtSignal(int)
    processing_complete = pyqtSignal(str, int, list)

    def __init__(self, files, output_folder, rename_files):
        super().__init__()
        self.files = files
        self.output_folder = output_folder
        self.rename_files = rename_files
        self._stop_flag = False

    def run(self):
        success_count = 0
        failed_files = []
        total_files = len(self.files)

        for idx, file in enumerate(self.files):
            if self._stop_flag:
                break

            filename = os.path.basename(file)
            if self.rename_files:
                filename = self.generate_random_filename(os.path.splitext(filename)[1])

            output_file = os.path.join(self.output_folder, filename)
            if self.remove_exif(file, output_file):
                success_count += 1
            else:
                failed_files.append(file)

            # Update progress
            progress = int(((idx + 1) / total_files) * 100)
            self.progress_updated.emit(progress)

        self.processing_complete.emit(self.output_folder, success_count, failed_files)

    def stop_processing(self):
        """Stop the ongoing processing."""
        self._stop_flag = True

    def remove_exif(self, input_file, output_file):
        try:
            image = Image.open(input_file)
            data = list(image.getdata())

            image_without_exif = Image.new(image.mode, image.size)
            image_without_exif.putdata(data)
            image_without_exif.save(output_file)
            return True
        except Exception as e:
            print(f"Error processing {input_file}: {e}")
            return False

    def generate_random_filename(self, extension, length=12):
        """Generate a random filename with a mix of letters, digits, and special characters."""
        characters = string.ascii_letters + string.digits + "-_@#"
        random_string = ''.join(random.choices(characters, k=length))
        return f"{random_string}{extension}"


def main():
    app = QApplication(sys.argv)
    ex = ExifRemoverApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

