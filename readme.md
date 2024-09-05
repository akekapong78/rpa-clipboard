# RPA Clipboard Manager

![RPA Clipboard Manager Screenshot](assets/capture.png)

The **RPA Clipboard Manager** is a simple yet powerful Python-based GUI application designed to help users manage and manipulate clipboard content. The application allows users to extract specific functions from the clipboard, save clipboard entries to a JSON file, load entries from a file, and easily set clipboard content from the application.

## Features

- **Add Clipboard**: Automatically extract and add functions from the clipboard to the application.
- **Set Clipboard**: Select and set any saved entry to the clipboard.
- **Load from File**: Load previously saved clipboard entries from a JSON file.
- **Save to File**: Save the current clipboard entries to a JSON file for later use.
- **Clear List**: Clear all entries in the list and the clipboard.

## Installation

### Prerequisites

- Python 3.x
- `pip` package installer

### Install Required Libraries

To run the application, you need to install the following libraries:

```bash
pip install pyautogui pygetwindow pillow pyperclip pyinstaller

pyinstaller main.py --onefile --windowed

```