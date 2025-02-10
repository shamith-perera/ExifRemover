# ExifRemover
A Python application to remove EXIF metadata from images with a user-friendly GUI built using PyQt5.

![image](https://github.com/user-attachments/assets/e614eebf-c605-4886-ba7b-a80febf3113d)

## Features:
- Drag and drop support for adding images.
- Option to rename files with random names.
- Option to select the output folder.
- Progress bar showing the status of the EXIF removal process.
- Handles multiple image formats (.jpg, .jpeg, .png, .tiff).

## Installation:
To install the application, 

### For Linux 
download the [.deb package](https://github.com/shamith-perera/ExifRemover/releases/download/v1.0.0/exifremover.deb) and install it using `dpkg`:
```
sudo dpkg -i exifremover.deb
sudo apt-get install -f  # To resolve dependencies if needed
```
#### or

download the [AppImage](https://github.com/shamith-perera/ExifRemover/releases/download/v1.0.0/Exif_Remover-x86_64.AppImage) and run it :
```
chmod +x Exif_Remover-x86_64.AppImage
./Exif_Remover-x86_64.AppImage
```

### For Windows
download and run the [.exe](https://github.com/shamith-perera/ExifRemover/releases/download/v1.0.0/exif_remover.exe) file (portable)



### Alternatively, you can clone this repository and run the application directly (requires Python 3.x, PyQt5, and Pillow):

```
git clone https://github.com/shamith-perera/ExifRemover.git
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
