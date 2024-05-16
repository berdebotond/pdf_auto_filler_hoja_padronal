# PDF Generator Project

This project is a Python application for generating PDFs from user data stored in a Supabase database. It uses a combination of Tkinter for the GUI, Faker for generating mock data, PyMuPDF for PDF manipulation, and a Supabase client for database interactions.

## Project Structure

The project is organized into the following modules:

- `supabase_module.py`: Handles interactions with the Supabase database.
- `data_generator.py`: Generates mock data and converts it to the required schema.
- `pdf_handler.py`: Manages the conversion of database data to PDF form data and fills the PDF.
- `main.py`: Contains the GUI logic for selecting users and generating PDFs.

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/pdf-generator-project.git
cd pdf-generator-project
```
Create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
Install the required dependencies:

```
pip install -r requirements.txt
```

Ensure you have the necessary credentials for Supabase and update the supabase_client.py file with your Supabase project details.
## Usage

To start the application, run the main.py script:
```
python main.py
```

Use the "Fetch Users" button to retrieve user data from the Supabase database.
Select a user from the dropdown menu.
Click "Generate PDF" to fill the PDF form with the selected user's data.

## Modules

### supabase_module.py
Handles the interactions with the Supabase database.
### insert_data(data):
Inserts data into the Supabase table.
### fetch_data(): 
Fetches data from the Supabase table.
### data_generator.py 
Generates mock data and converts it to the required database schema.
### create_mock_data(): 
Creates mock data using Faker.
### convert_to_db_schema(data): 
Converts mock data to the database schema.
### pdf_handler.py
Manages the conversion of database data to PDF form data and fills the PDF.
### convert_to_pdf_form_data(db_data): 
Converts database data to PDF form data.
### fill_pdf(pdf_path, data): 
Fills the PDF with the provided data.
### main.py
Contains the GUI logic for selecting users and generating PDFs.
### enerate_pdf(): 
Generates a PDF for the selected user.
### fetch_users(): 
Fetches users from the database and updates the dropdown menu.

## Requirements

Python 3.7+