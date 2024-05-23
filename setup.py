from setuptools import setup, find_packages

setup(
    name="PDF Generator & User Data Updater",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "tkinter",
        "threading",
        "supabase",
        "fpdf2",
    ],
)
