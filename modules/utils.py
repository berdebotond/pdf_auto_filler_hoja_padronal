import os
import sys


def get_resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_pdfs():
    pdf_dir = get_resource_path("pdf")
    pdf_files = [f for f in os.listdir(str(pdf_dir)) if f.endswith('.pdf')]
    return pdf_files
