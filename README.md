# ExifRemover
A Python application to remove EXIF metadata from images with a user-friendly GUI built using PyQt5.

## Features:
- Drag and drop support for adding images.
- Option to rename files with random names.
- Option to select the output folder.
- Progress bar showing the status of the EXIF removal process.
- Handles multiple image formats (.jpg, .jpeg, .png, .tiff).

## Installation:
To install the application, download the [.deb package](https://github.com/shamith-perera/ExifRemover/releases/download/v1.0.0/exifremover.deb) and install it using `dpkg`:
```
sudo dpkg -i exifremover.deb
sudo apt-get install -f  # To resolve dependencies if needed
```


Alternatively, you can clone this repository and run the application directly (requires Python 3.x, PyQt5, and Pillow):

```
git clone https://github.com/your-username/ExifRemover.git
cd ExifRemover
pip install -r requirements.txt
python exif_remover.py
```
Note: Make sure you have pip installed for Python and the necessary dependencies (PyQt5, Pillow).

## Dependencies:
- PyQt5
- Pillow

## Usage:
1. Launch the application.
2. Select images by dragging and dropping them or using the "Select Image(s)" button.
3. Choose an output folder.
4. Optionally, check the "Rename files" checkbox to rename images randomly.
5. Click "Start" to begin processing.
6. The progress bar will update as EXIF metadata is removed.
