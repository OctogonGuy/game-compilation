# Game Compilation

This is a program made in Python with 9 different games included to showcase my Python scripting abilities. It utilizes the Tkinter and pygame libraries.

## Setup

1. Install Python 3.12 (any future version is not compatible with pygame) and Tkinter
   - Ubuntu / Debian
       ```
       sudo apt install python3.12 python3.12-venv python3.12-tk
       ```
   - Fedora / RHEL
       ```
       sudo dnf install python3.12 python3.12-tkinter
       ```
2. Create a virtual environment
    ```
    python3.12 -m venv .venv
    ```
3. Install required libraries
    ```
    source .venv/bin/activate
    pip install -r requirements.txt
    deactivate
    ```
   
## Usage

Run `main.py` in the virtual environment.

```
source .venv/bin/activate
python main.py
deactivate
```
