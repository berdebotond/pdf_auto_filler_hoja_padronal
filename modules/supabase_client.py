import json
import os
import sys

from supabase import create_client, Client

"""
url: str = os.environ.get(key="SUPABASE_URL", default="https://hetrvidiwvkrxaqeozgc.supabase.co")
key: str = os.environ.get(key="SUPABASE_KEY",
                          default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhldHJ2aWRpd3ZrcnhhcWVvemdjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTM1NTE5NTUsImV4cCI6MjAyOTEyNzk1NX0.dpUKNQ65qsZaiRlrKoj9jiWhvdzhuFFxBP1ENGd_jGs")

"""


def load_config():
    if hasattr(sys, '_MEIPASS'):
        # If running in a PyInstaller bundle, get the config file from the bundle
        config_path = os.path.join(sys._MEIPASS, 'config.json')
    else:
        # If running in a normal environment, get the config file from the current directory
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    with open(config_path) as config_file:
        return json.load(config_file)


config = load_config()

url: str = config.get("SUPABASE_URL")
key: str = config.get("SUPABASE_KEY")

supabase_client: Client = create_client(url, key)

# Define the table fields
nie_tie_fields = {'id', 'name', 'surname', 'city_of_birth', 'country_of_birth', 'family_status', 'gender',
                  'full_name_of_father', 'full_name_of_mother', 'spain_address', 'house_name', 'apt_number', 'city',
                  'zip_code', 'province', 'legal_representative_name', 'legal_representative_id',
                  'legal_representative_relation', 'consent_communication_electronically', 'apply_digital_certificate',
                  'no_consent_data_consultation', 'comments', 'Initial'}
initial_fields = {'id', 'name', 'surname', 'birth_date', 'nationality', 'additional_nationality', 'passport_number',
                  'id_number', 'nie', 'mobile_phone', 'email', 'city', 'province', 'desired_service',
                  'not_available_appointments', 'appointment_deadline', 'appointment_location', 'referral_source',
                  'comments'}
"""
def insert_data(data):
    response = supabase_client.table('addresses').insert(data).execute()
    if response:
        print("Data inserted successfully.")
    else:
        print(f"Failed to insert data: {response.json()}")


def fetch_data():
    response = supabase_client.table('addresses').select('*').execute()
    if response:
        data = response.json()
        return json.loads(data)
    else:
        print(f"Failed to fetch data: {response.json()}")


def update_data(selected_user, data):
    response = supabase_client.table('addresses').update(data).eq("id", selected_user.get('id')).execute()
    if response:
        print("Data updated successfully.")
    else:
        print(f"Failed to update data: {response.json()}")


def remove_data(user_id):
    response = supabase_client.table('addresses').delete().eq("id", user_id).execute()
    if response:
        print("Data removed successfully.")
    else:
        print(f"Failed to remove data: {response.json()}")

"""


def fetch_enum_values(table, column):
    response = supabase_client.table(table).select(column).execute()
    if response.data:
        return list(set(item[column] for item in response.data if item[column] is not None))
    return []


# Fetch data from both tables
def fetch_data_nie_tie_initial():
    data_sheet_nie_tie = supabase_client.table("data_sheet_nie_tie").select("*").execute()
    initial_data_request = supabase_client.table("initial_data_request").select("*").execute()
    # remove empty data where name or surname is empty
    data_sheet_nie_tie.data = [item for item in data_sheet_nie_tie.data if item.get('name') and item.get('surname')]
    initial_data_request.data = [item for item in initial_data_request.data if item.get('name') and item.get('surname')]

    merged_data = merge_data(data_sheet_nie_tie.data, initial_data_request.data)
    return merged_data


# Merge data based on the foreign key initial_id using a join-like approach
def merge_data(data_sheet_nie_tie, initial_data_request):
    # Create a dictionary for quick lookup of initial data by name and surname
    initial_data_dict = {
        f"{initial.get('name').strip().lower().replace(' ', '')}{initial.get('surname').strip().lower().replace(' ', '')}": initial
        for initial in initial_data_request}
    merged_data = []

    for nie_tie in data_sheet_nie_tie:
        name_surname = (nie_tie.get('name', '').strip().lower().replace(" ", "") + nie_tie.get('surname',
                                                                                               '').strip().lower().replace(
            " ", ""))
        print("-------------------")
        print(name_surname, initial_data_dict)

        if name_surname in initial_data_dict:
            merged_entry = {**nie_tie, **initial_data_dict[name_surname]}
            initial_data_dict.pop(name_surname)
        else:
            merged_entry = {**nie_tie}

        merged_data.append(merged_entry)

    return merged_data

    # Add any remaining initial data that was not found in the nie_tie data
    for name_surname, initial_data in initial_data_dict.items():
        merged_data.append(initial_data)

    return merged_data


# Update data in the appropriate tables
def update_data(id_value, updates):
    # Separate updates for each table
    nie_tie_updates = {k: v for k, v in updates.items() if k in nie_tie_fields}
    initial_updates = {k: v for k, v in updates.items() if k in initial_fields}

    # Perform updates
    if nie_tie_updates:
        supabase_client.table("data_sheet_nie_tie").update(nie_tie_updates).eq("id", id_value).execute()
    if initial_updates:
        initial_id = updates.get('initial_id')
        if initial_id:
            supabase_client.table("initial_data_request").update(initial_updates).eq("id", initial_id).execute()


# Insert data into the appropriate tables
def insert_data(data):
    # Separate data for each table
    nie_tie_data = {k: v for k, v in data.items() if k in nie_tie_fields}
    initial_data = {k: v for k, v in data.items() if k in initial_fields}

    # Perform inserts
    if initial_data:
        response = supabase_client.table("initial_data_request").insert(initial_data).execute()
        if response:
            print("Data inserted successfully into initial_data_request.")
            # Get the inserted initial_data id and use it as initial_id for nie_tie_data
            initial_data_id = response.data[0]['id']
            nie_tie_data['initial_id'] = initial_data_id
        else:
            print(f"Failed to insert data into initial_data_request: {response.json()}")
    if nie_tie_data:
        response = supabase_client.table("data_sheet_nie_tie").insert(nie_tie_data).execute()
        if response:
            print("Data inserted successfully into data_sheet_nie_tie.")
        else:
            print(f"Failed to insert data into data_sheet_nie_tie: {response.json()}")


# Remove user from both tables
def remove_user_from_db(id_value):
    supabase_client.table("data_sheet_nie_tie").delete().eq("id", id_value).execute()
    supabase_client.table("initial_data_request").delete().eq("id", id_value).execute()


# Main function to run the script
def example():
    insert_data({"name": "John", "surname": "Doe", "email": "2D5wK@example.com"})
    merged_data = fetch_data_nie_tie_initial()
    print("Merged Data: ", merged_data)


def fetch_empadron_data():
    empadron_data = supabase_client.table("empadron_data").select("*").execute()
    # rmeove data where first_name_1 or surname_1 is empty
    empadron_data.data = [item for item in empadron_data.data if item.get('first_name_1') and item.get('surname_1')]
    return empadron_data.data


def fetch_empadron_data():
    empadron_data = supabase_client.table("empadron_data").select("*").execute()
    # rmeove data where first_name_1 or surname_1 is empty
    empadron_data.data = [item for item in empadron_data.data if item.get('first_name_1') and item.get('surname_1')]
    return empadron_data.data


def merge_empadron_data_with_tie_nie(merged_data, empadron_data):
    # Create a dictionary for quick lookup of initial data by name and surname
    initial_data_dict = {
        f"{initial.get('name').strip().lower().replace(' ', '')}{initial.get('surname').strip().lower().replace(' ', '')}": initial
        for initial in merged_data}

    merged_data = []

    for empadron in empadron_data:
        # Extract and normalize names and surnames
        for i in range(1, 6):
            first_name = empadron.get(f'first_name_{i}', '').strip().lower().replace(' ', '')
            surname = empadron.get(f'surname_{i}', '').strip().lower().replace(' ', '')
            if first_name and surname:
                name_surname = first_name + surname
                if name_surname in initial_data_dict:
                    merged_entry = {**empadron, **initial_data_dict[name_surname]}
                    merged_data.append(merged_entry)
                    initial_data_dict.pop(name_surname)
                    break
    # add the remaining empadron data that was not found in the nie_tie data
    for empadron in empadron_data:
        first_name = empadron.get('first_name_1', '').strip().lower().replace(' ', '')
        surname = empadron.get('surname_1', '').strip().lower().replace(' ', '')
        name_surname = first_name + surname
        if name_surname not in initial_data_dict:

            merged_data.append(empadron)
    return merged_data


def insert_empadron_data(data):
    response = supabase_client.table("empadron_data").insert(data).execute()
    if response:
        print("Data inserted successfully into empadron_data.")
    else:
        print(f"Failed to insert data into empadron_data: {response.json()}")


"""exmaple data 
Merged Data:  [{'id': 110, 'name': 'Botond', 'surname': 'Berde', 'city_of_birth': 'London', 'country_of_birth': 'Mongolia', 'family_status': 'married', 'gender': 'female', 'full_name_of_father': 'father222 name exmpale', 'full_name_of_mother': 'Mother name exmpale22', 'spain_address': 'calle tio', 'house_name': '11', 'apt_number': '24', 'city': 'Las Palmas de Gran', 'zip_code': '3451', 'province': 'Canary Islands - Las Palmas', 'legal_representative_name': 'Lie Hawkinss', 'legal_representative_id': '123454', 'legal_representative_relation': 'father', 'consent_communication_electronically': True, 'apply_digital_certificate': True, 'no_consent_data_consultation': True, 'comments': None, 'first_names': 'Botond', 'surnames': 'Berde', 'birth_date': '1982-05-11', 'nationality': 'Uruguay', 'additional_nationality': 'Rumania', 'passport_number': 'O74KQQ5As', 'id_number': 'GT8664TWEs', 'nie': '(293)756-5215', 'mobile_phone': '+34345678987', 'email': 'Califorsasnia@exmaple.com', 'desired_service': 'Majom', 'not_available_appointments': '2023-10-27', 'appointment_deadline': '2025-03-29', 'appointment_location': 'Nearby cities', 'referral_source': 'Facebook'}, {'id': 112, 'name': 'Botond2', 'surname': 'Berde', 'city_of_birth': 'London', 'country_of_birth': 'Mongolia', 'family_status': 'married', 'gender': 'female', 'full_name_of_father': 'father222 name exmpale', 'full_name_of_mother': 'Mother name exmpale22', 'spain_address': 'calle tio', 'house_name': '11', 'apt_number': '24', 'city': 'Madrid/Ba', 'zip_code': '3451', 'province': 'Canarias', 'legal_representative_name': 'Lie Hawkinss', 'legal_representative_id': '123454', 'legal_representative_relation': 'father', 'consent_communication_electronically': True, 'apply_digital_certificate': True, 'no_consent_data_consultation': True, 'comments': None, 'nationality': '', 'surnames': '', 'passport_number': '', 'first_names': '', 'mobile_phone': '', 'email': '', 'not_available_appointments': '', 'appointment_location': '', 'desired_service': '', 'referral_source': '', 'additional_nationality': '', 'appointment_deadline': '', 'nie': '', 'id_number': '', 'birth_date': ''}, {'legal_representative_id': '', 'family_status': '', 'country_of_birth': '', 'full_name_of_father': '', 'no_consent_data_consultation': '', 'full_name_of_mother': '', 'zip_code': '', 'house_name': '', 'surname': '', 'legal_representative_name': '', 'legal_representative_relation': '', 'consent_communication_electronically': '', 'city_of_birth': '', 'gender': '', 'apply_digital_certificate': '', 'apt_number': '', 'name': '', 'spain_address': '', 'id': 111, 'first_names': 'Botond1', 'surnames': 'Berde', 'birth_date': '1982-05-11', 'nationality': 'Uruguay', 'additional_nationality': 'Rumania', 'passport_number': 'O74KQQ5As', 'id_number': 'GT8664TWEs', 'nie': '(293)756-5215', 'mobile_phone': '+34345678987', 'email': 'Califorsasnia@exmaple.com', 'city': 'Las Palmas de Gran', 'province': 'Canary Islands - Las Palmas', 'desired_service': 'Majom', 'not_available_appointments': '2023-10-27', 'appointment_deadline': '2025-03-29', 'appointment_location': 'Nearby cities', 'referral_source': 'Facebook', 'comments': None}]

"""
