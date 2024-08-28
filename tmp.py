import sys

import uuid

import fitz  # PyMuPDF
from supabase import create_client, Client
import os
from country_name_translator import translate_countries_from_en_es

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL", "https://hetrvidiwvkrxaqeozgc.supabase.co")
key: str = os.environ.get("SUPABASE_KEY",
                          "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhldHJ2aWRpd3ZrcnhhcWVvemdjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTM1NTE5NTUsImV4cCI6MjAyOTEyNzk1NX0.dpUKNQ65qsZaiRlrKoj9jiWhvdzhuFFxBP1ENGd_jGs")

supabase: Client = create_client(url, key)

# Define the mapping for the PDF fields for each document type
nie_tie_pdf_fields_data = {
    "name": "field1",
    "surname": "field2",
    "city_of_birth": "field3",
    "country_of_birth": "field4",
    "full_name_of_father": "field5",
    "full_name_of_mother": "field6",
    "spain_address": "field7",
    "house_name": "field8",
    "apt_number": "field9",
    "city": "field10",
    "zip_code": "field11",
    "province": "field12",
    "legal_representative_name": "field13",
    "legal_representative_id": "field14",
    "legal_representative_relation": "field15",
    "comments": "field16"
}

parse_initial_data_fields = {
    "name": "field1",
    "surname": "field2",
    "birth_date": "field3",
    "nationality": "field4",
    "additional_nationality": "field5",
    "passport_number": "field6",
    "id_number": "field7",
    "nie": "field8",
    "email": "field11",
    "city": "field12",
    "province": "Choice1",
    "not_available_appointments": "field13",
    "appointment_deadline": "field14",
    "desired_service": "field16",
    "comments": "field17",
    "referral_source": "field15"
}

empadron_data = {
    "street_name": "field1",  # tio
    "type": "Choice1",  # Calle (street)
    "zip_code": "field2",  # 3451
    "municipality": "field3",  # Canary Islands - Las Palmas
    "number": "field4",  # 24
    "letter": "field5",  # kl
    "block": "field6",  # 23
    "gate": "field7",  # 21
    "stairs": "field8",  # 24
    "floor": "field9",  # 32
    "door": "field10",  # 23
    "inhabitants_not_removed": "Button3,Button4,Choice2",  # No, No, 4
    "rent_contract": "Button5,Button6,Button7",  # No, Off, Off
    "landlord_name": "field11",  # test 1 land
    "landlord_id_dni_nie": "field12",  # land_id
    "landlord_type": "Button8,Button9",  # Off, Off
    "landlordIsOwner": "Button10",  # No
    "first_name_1": "field13",  # Botond1 mono 2
    "surname_1": "field14",  # Berde lol
    "nie_1": "field15",  # (293)-756-5215
    "male_1": "Button56",  # No
    "female_1": "Button55",  # Off
    "city_of_birth_1": "field16",  # London
    "country_of_birth_1": "field17",  # Mongolia
    "highest_education_1": "Choice8",  # 42 - Higher secondary school graduate
    "first_name_2": "field26",  # first name 2
    "surname_2": "field20",  # surname 2
    "nie_2": "field34",  # nie 2
    "male_2": "Button57",  # No
    "female_2": "Button56",  # Off
    "city_of_birth_2": "field30",  # city birt 2
    "country_of_birth_2": "field18",  # country of birt 2
    "highest_education_2": "Choice9",  # 42 - Higher secondary school graduate
    "first_name_3": "field27",  # first name 3
    "surname_3": "field21",  # surname 3
    "nie_3": "field35",  # nie 3
    "male_3": "Button58",  # Off
    "female_3": "Button57",  # No
    "city_of_birth_3": "field31",  # city birt 3
    "country_of_birth_3": "field19",  # country of birt 3
    "highest_education_3": "Choice10",  # 42 - Higher secondary school graduate
    "first_name_4": "field28",  # first name 4
    "surname_4": "field22",  # surname 4
    "nie_4": "field36",  # nie 4
    "male_4": "Button59",  # No
    "female_4": "Button58",  # Off
    "city_of_birth_4": "field32",  # city birt 4
    "country_of_birth_4": "field24",  # country of birt 4
    "highest_education_4": "Choice11",  # 31 - basic secondary school & profesional training
    "first_name_5": "field29",  # first name 5
    "surname_5": "field23",  # surname 5
    "nie_5": "field37",  # nie 5
    "male_5": "Button60",  # Off
    "female_5": "Button59",  # No
    "city_of_birth_5": "field33",  # city birt 5
    "country_of_birth_5": "field25",  # country of birt 5
    "highest_education_5": "Choice11",  # 31 - basic secondary school & profesional training
    "moved_spain_from_other_country_1": "field38",  # No
    "moved_spain_from_other_country_2": "field39",  # No
    "moved_spain_from_other_country_3": "field40",  # No
    "moved_spain_from_other_country_4": "field41",  # No
    "moved_spain_from_other_country_5": "field42",  # No
    "moved_within_spain_1": "Choice3",
    "moved_within_spain_2": "Choice4",
    "moved_within_spain_3": "Choice5",
    "moved_within_spain_4": "Choice6",
    "moved_within_spain_5": "Choice7",  # No
}


def read_pdf_custom_id(pdf_path):
    doc = fitz.open(pdf_path)
    custom_id = None
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for annot in page.annots():
            text = annot.info["content"]
            if text.startswith("ID: "):
                custom_id = text[4:]
                break
        if custom_id:
            break
    print(f"Custom ID: {custom_id}")
    return custom_id


def upload_to_supabase(data, table_name):
    response = supabase.table(table_name).insert(data).execute()
    return response


def check_pdf_type(doc):
    first_page_text = doc.load_page(0).get_text()
    if "Data Sheet for NIE/TIE" in first_page_text:
        return "data_sheet_nie_tie"
    elif "Deadline - till when I need the paperwork:" in first_page_text:
        print("+++++++++++++++++")
        print("estoy aqui")
        return "initial_data_request"
    elif "Empadronamiento" in first_page_text:
        return "empadron_data"
    return None


def process_widget_nie_tie(data, widget):
    if "field" in widget.field_name:
        for key, value in nie_tie_pdf_fields_data.items():
            if widget.field_name == value:
                translation_try = translate_countries_from_en_es(widget.field_value)
                data[key] = translation_try if translation_try != widget.field_value else widget.field_value
    elif "Button" in widget.field_name:
        if widget.field_value == "No":
            if widget.field_name == "Button1":
                data["family_status"] = "single"
            elif widget.field_name == "Button2":
                data["family_status"] = "married"
            elif widget.field_name == "Button3":
                data["family_status"] = "widowed"
            elif widget.field_name == "Button4":
                data["family_status"] = "divorced"
            elif widget.field_name == "Button5":
                data["family_status"] = "separated"
            elif widget.field_name == "Button6":
                data["gender"] = "male"
            elif widget.field_name == "Button7":
                data["gender"] = "female"
            elif widget.field_name == "Button8":
                data["consent_communication_electronically"] = True
            elif widget.field_name == "Button9":
                data["apply_digital_certificate"] = True
            elif widget.field_name == "Button10":
                data["no_consent_data_consultation"] = True
    elif "Choice" in widget.field_name:
        if widget.field_name == "Choice19":
            data["province"] = widget.field_value

    return data


def process_widget_initial_data(data, widget):
    if "field" in widget.field_name:
        if widget.field_name in ["field9", "field10"]:
            if "mobile_phone" not in data:
                data["mobile_phone"] = ""
            data["mobile_phone"] += widget.field_value
        else:
            for key, value in parse_initial_data_fields.items():
                if widget.field_name == value and widget.field_value != "":
                    translation_try = translate_countries_from_en_es(widget.field_value)
                    data[key] = translation_try if translation_try != widget.field_value else widget.field_value
    elif "Button" in widget.field_name:
        if widget.field_value == "No":
            if "Button3" in widget.field_name:
                data["desired_service"] = "White NIE"
            elif "Button4" in widget.field_name:
                data["desired_service"] = "Green NIE"
            elif "Button5" in widget.field_name:
                data["desired_service"] = "TIE"
            elif "Button6" in widget.field_name:
                data["desired_service"] = "Empadronamiento & Travel Discount"
            elif "Button7" in widget.field_name:
                data["desired_service"] = "Autónomo"
            elif widget.field_name == "Button9":
                data["appointment_location"] = "Nearby cities"
            elif widget.field_name == "Button10":
                data["appointment_location"] = "My city"
            elif widget.field_name == "Button11":
                data["referral_source"] = "Slack LUP Nelly"
            elif widget.field_name == "Button12":
                data["referral_source"] = "Friend"
            elif widget.field_name == "Button13":
                data["referral_source"] = "Facebook"
            elif widget.field_name == "Button14":
                data["referral_source"] = "Website"
            elif widget.field_name == "Button15":
                data["referral_source"] = "Flyer"
            elif widget.field_name == "Button16":
                data["referral_source"] = "Poster"
    elif "Choice" in widget.field_name:
        for key, value in parse_initial_data_fields.items():
            if widget.field_name == value and widget.field_value != "":
                translation_try = translate_countries_from_en_es(widget.field_value)
                data[key] = translation_try if translation_try != widget.field_value else widget.field_value
    return data


def process_widget_empadronamiento(data, widget):
    if "field" in widget.field_name or "Text" in widget.field_name:
        for key, value in empadron_data.items():
            if widget.field_name == value:
                translation_try = translate_countries_from_en_es(widget.field_value)
                data[key] = translation_try if translation_try != widget.field_value else widget.field_value
    elif "Button" in widget.field_name:

        if widget.field_name == "Button1":

            if widget.field_value != "Off":
                print("Voluntary statement checkbox is checked by user")
                data["voluntary_statement"] = "True"
            else:
                data["voluntary_statement"] = "False"

        if widget.field_name == "Button5" and widget.field_value != "Off":
            print("Signed hand contract checkbox is checked by user")

            data["rent_contract"] = "signed by hand"

        elif widget.field_name == "Button6" and widget.field_value != "Off":
            print("Official Spanish contract checkbox is checked by user")
            data["rent_contract"] = "official Spanish Certificado digital"

        elif widget.field_name == "Button7" and widget.field_value != "Off":
            print("Signed electronic contract checkbox is checked by user")
            data["rent_contract"] = "signed electronically by other means"

        if widget.field_name == "Button10" and widget.field_value != "Off":
            print("Landlord checkbox is checked by user")
            data["landlord_type"] = "landlord"

        elif widget.field_name == "Button9" and widget.field_value != "Off":
            print("Co-inhabitant checkbox is checked by user")
            data["landlord_type"] = "co-inhabitant"

        if widget.field_name == "Button54" and widget.field_value != "Off":
            print("Male  1 checkbox is checked by user")
            data["gender_1"] = "male"
        elif widget.field_name == "Button53" and widget.field_value != "Off":
            print("Female 1 checkbox is checked by user")
            data["gender_1"] = "female"

        if widget.field_name == "Button14" and widget.field_value != "Off":
            print("Newborns 1 checkbox is checked by user")
            data["birth_newborns_1"] = "True"

        if widget.field_name == "Button16" and widget.field_value != "Off":
            print("Change personal data 1 checkbox is checked by user")
            data["change_personal_data_1"] = True

        if widget.field_name == "Button33":
            if widget.field_value != "Off":
                print("Municipal level 1 checkbox is checked by user")
                data["vote_municipal_level_1"] = True
            else:
                data["vote_municipal_level_1"] = False

        if widget.field_name == "Button35":
            if widget.field_value != "Off":
                print("Europe voting right 1 checkbox is checked by user")
                data["change_europe_voting_right_1"] = True
            else:
                data["change_europe_voting_right_1"] = False

        if widget.field_name == "Button56" and widget.field_value != "Off":
            print("Male 2 checkbox is checked by user")
            data["gender_2"] = "male"
        elif widget.field_name == "Button55" and widget.field_value != "Off":
            print("Female 2 checkbox is checked by user")
            data["gender_2"] = "female"

        if widget.field_name == "Button19" and widget.field_value != "Off":
            data["birth_newborns_2"] = "True"
            print("Newborns 2 checkbox is checked by user")

        if widget.field_name == "Button17" and widget.field_value != "Off":
            data["change_personal_data_2"] = True
            print("Change personal data 2 checkbox is checked by user")

        if widget.field_name == "Button45":
            if widget.field_value != "Off":
                data["vote_municipal_level_2"] = True
                print("Municipal level 2 checkbox is checked by user")
            else:
                data["vote_municipal_level_2"] = False

        if widget.field_name == "Button37":
            if widget.field_value != "Off":
                print("Europe voting right 2 checkbox is checked by user")
                data["change_europe_voting_right_2"] = True
            else:
                data["change_europe_voting_right_2"] = False

        if widget.field_name == "Button58" and widget.field_value != "Off":
            print("Male 3 checkbox is checked by user")
            data["gender_3"] = "male"

        elif widget.field_name == "Button57" and widget.field_value != "Off":
            print("Female 3 checkbox is checked by user")
            data["gender_3"] = "female"

        if widget.field_name == "Button22" and widget.field_value != "Off":
            print("Newborns 3 checkbox is checked by user")
            data["birth_newborns_3"] = "True"

        if widget.field_name == "Button24" and widget.field_value != "Off":
            print("Change personal data 3 checkbox is checked by user")
            data["change_personal_data_3"] = True

        if widget.field_name == "Button47":
            if widget.field_value != "Off":
                print("Municipal level 3 checkbox is checked by user")
                data["vote_municipal_level_3"] = True
            else:
                data["vote_municipal_level_3"] = False

        if widget.field_name == "Button39":
            if widget.field_value != "Off":
                print("Europe voting right 3 checkbox is checked by user")
                data["change_europe_voting_right_3"] = True
            else:
                data["change_europe_voting_right_3"] = False

        if widget.field_name == "Button60" and widget.field_value != "Off":
            print("Male 4 checkbox is checked by user")
            data["gender_4"] = "male"

        elif widget.field_name == "Button59" and widget.field_value != "Off":
            print("Female 4 checkbox is checked by user")
            data["gender_4"] = "female"

        if widget.field_name == "Button27" and widget.field_value != "Off":
            print("Newborns 4 checkbox is checked by user")
            data["birth_newborns_4"] = "True"

        if widget.field_name == "Button29" and widget.field_value != "Off":
            print("Change personal data 4 checkbox is checked by user")
            data["change_personal_data_4"] = True

        if widget.field_name == "Button49":
            if widget.field_value != "Off":
                print("Municipal level 4 checkbox is checked by user")
                data["vote_municipal_level_4"] = True
            else:
                data["vote_municipal_level_4"] = False

        if widget.field_name == "Button41":
            if widget.field_value != "Off":
                print("Europe voting right 4 checkbox is checked by user")
                data["change_europe_voting_right_4"] = True
            else:
                data["change_europe_voting_right_4"] = False

        # perosn 5

        if widget.field_name == "Button62" and widget.field_value != "Off":
            print("Male 5 checkbox is checked by user")
            data["gender_5"] = "male"

        elif widget.field_name == "Button61" and widget.field_value != "Off":
            print("Female 5 checkbox is checked by user")
            data["gender_5"] = "female"

        if widget.field_name == "Button32" and widget.field_value != "Off":
            print("Newborns 5 checkbox is checked by user")
            data["birth_newborns_5"] = "True"

        if widget.field_name == "Button30" and widget.field_value != "Off":
            print("Change personal data 5 checkbox is checked by user")
            data["change_personal_data_5"] = True

        if widget.field_name == "Button51":
            if widget.field_value != "Off":
                print("Municipal level 5 checkbox is checked by user")
                data["vote_municipal_level_5"] = True
            else:
                data["vote_municipal_level_5"] = False

        if widget.field_name == "Button43":
            if widget.field_value != "Off":
                print("Europe voting right 5 checkbox is checked by user")
                data["change_europe_voting_right_5"] = True
            else:
                data["change_europe_voting_right_5"] = False



    elif "Choice" in widget.field_name:
        for key, value in empadron_data.items():
            if widget.field_name == value:
                translation_try = translate_countries_from_en_es(widget.field_value)
                data[key] = translation_try if translation_try != widget.field_value else widget.field_value
    return data


def get_existing_initial_data_id(custom_id):
    response = supabase.table("initial_data_request").select("*").eq("id", custom_id).execute()
    return response.data[0]["id"] if response.data else None


def process_pdfs(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            field_index = 1
            bool_index = 1
            choice_index = 1
            pdf_id = read_pdf_custom_id(os.path.join(folder_path, filename))

            if pdf_id:
                print(f"PDF ID: {pdf_id}")
            else:
                pdf_id = None
            pdf_path = os.path.join(folder_path, filename)
            doc = fitz.open(pdf_path)
            pdf_type = check_pdf_type(doc)
            data = {}

            for page in doc:
                for widget in page.widgets():

                    if widget.field_type == 2:
                        widget.field_name = "Button" + str(bool_index)
                        bool_index += 1
                    elif widget.field_type == 7:
                        widget.field_name = "field" + str(field_index)
                        field_index += 1

                    elif widget.field_type == 3:
                        widget.field_name = "Choice" + str(choice_index)
                        choice_index += 1
                    widget.update()
                    if "Las Palmas" in widget.field_value:
                        print("------------------------------------")
                        print(widget.field_name)
                        print("=========================")
                    #print(f"Widget: {widget.field_name}, Value: {widget.field_value}")
                    if pdf_type == "data_sheet_nie_tie":
                        data = process_widget_nie_tie(data, widget)
                    elif pdf_type == "initial_data_request":
                        data = process_widget_initial_data(data, widget)
                    elif pdf_type == "empadron_data":
                        data = process_widget_empadronamiento(data, widget)
            print(data)

            if pdf_type:

                print(f"Processing {pdf_type}...")
                try:
                    upload_to_supabase(data, pdf_type)
                except Exception as e:
                    print(f"Error uploading to Supabase: {e}")
                    continue
                print(f"Uploaded {pdf_type} to Supabase")


def main():
    # Determine the directory where the script is located
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (PyInstaller)
        application_path = os.path.dirname(sys.executable)
    else:
        # If the application is run as a script
        application_path = os.path.dirname(os.path.abspath(__file__))

    # Define the folder for input PDFs
    input_pdfs_folder = os.path.join(application_path, 'test2')

    # Process PDFs in the input_pdfs folder
    process_pdfs(input_pdfs_folder)


if __name__ == "__main__":
    main()
import sys

import uuid

import fitz  # PyMuPDF
from supabase import create_client, Client
import os
from country_name_translator import translate_countries_from_en_es

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL", "https://hetrvidiwvkrxaqeozgc.supabase.co")
key: str = os.environ.get("SUPABASE_KEY",
                          "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhldHJ2aWRpd3ZrcnhhcWVvemdjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTM1NTE5NTUsImV4cCI6MjAyOTEyNzk1NX0.dpUKNQ65qsZaiRlrKoj9jiWhvdzhuFFxBP1ENGd_jGs")

supabase: Client = create_client(url, key)

# Define the mapping for the PDF fields for each document type
nie_tie_pdf_fields_data = {
    "name": "field1",
    "surname": "field2",
    "city_of_birth": "field3",
    "country_of_birth": "field4",
    "full_name_of_father": "field5",
    "full_name_of_mother": "field6",
    "spain_address": "field7",
    "house_name": "field8",
    "apt_number": "field9",
    "city": "field10",
    "zip_code": "field11",
    "province": "field12",
    "legal_representative_name": "field13",
    "legal_representative_id": "field14",
    "legal_representative_relation": "field15",
    "comments": "field16"
}

parse_initial_data_fields = {
    "name": "field1",
    "surname": "field2",
    "birth_date": "field3",
    "nationality": "field4",
    "additional_nationality": "field5",
    "passport_number": "field6",
    "id_number": "field7",
    "nie": "field8",
    "email": "field11",
    "city": "field12",
    "province": "Choice1",
    "not_available_appointments": "field13",
    "appointment_deadline": "field14",
    "desired_service": "field16",
    "comments": "field17",
    "referral_source": "field15"
}

empadron_data = {
    "street_name": "field1",  # tio
    "type": "Choice1",  # Calle (street)
    "zip_code": "field2",  # 3451
    "municipality": "field3",  # Canary Islands - Las Palmas
    "number": "field4",  # 24
    "letter": "field5",  # kl
    "block": "field6",  # 23
    "gate": "field7",  # 21
    "stairs": "field8",  # 24
    "floor": "field9",  # 32
    "door": "field10",  # 23
    "inhabitants_not_removed": "Button3,Button4,Choice2",  # No, No, 4
    "rent_contract": "Button5,Button6,Button7",  # No, Off, Off
    "landlord_name": "field11",  # test 1 land
    "landlord_id_dni_nie": "field12",  # land_id
    "landlord_type": "Button8,Button9",  # Off, Off
    "landlordIsOwner": "Button10",  # No
    "first_name_1": "field13",  # Botond1 mono 2
    "surname_1": "field14",  # Berde lol
    "nie_1": "field15",  # (293)-756-5215
    "male_1": "Button56",  # No
    "female_1": "Button55",  # Off
    "city_of_birth_1": "field16",  # London
    "country_of_birth_1": "field17",  # Mongolia
    "highest_education_1": "Choice8",  # 42 - Higher secondary school graduate
    "first_name_2": "field26",  # first name 2
    "surname_2": "field20",  # surname 2
    "nie_2": "field34",  # nie 2
    "male_2": "Button57",  # No
    "female_2": "Button56",  # Off
    "city_of_birth_2": "field30",  # city birt 2
    "country_of_birth_2": "field18",  # country of birt 2
    "highest_education_2": "Choice9",  # 42 - Higher secondary school graduate
    "first_name_3": "field27",  # first name 3
    "surname_3": "field21",  # surname 3
    "nie_3": "field35",  # nie 3
    "male_3": "Button58",  # Off
    "female_3": "Button57",  # No
    "city_of_birth_3": "field31",  # city birt 3
    "country_of_birth_3": "field19",  # country of birt 3
    "highest_education_3": "Choice10",  # 42 - Higher secondary school graduate
    "first_name_4": "field28",  # first name 4
    "surname_4": "field22",  # surname 4
    "nie_4": "field36",  # nie 4
    "male_4": "Button59",  # No
    "female_4": "Button58",  # Off
    "city_of_birth_4": "field32",  # city birt 4
    "country_of_birth_4": "field24",  # country of birt 4
    "highest_education_4": "Choice11",  # 31 - basic secondary school & profesional training
    "first_name_5": "field29",  # first name 5
    "surname_5": "field23",  # surname 5
    "nie_5": "field37",  # nie 5
    "male_5": "Button60",  # Off
    "female_5": "Button59",  # No
    "city_of_birth_5": "field33",  # city birt 5
    "country_of_birth_5": "field25",  # country of birt 5
    "highest_education_5": "Choice11",  # 31 - basic secondary school & profesional training
    "moved_spain_from_other_country_1": "field38",  # No
    "moved_spain_from_other_country_2": "field39",  # No
    "moved_spain_from_other_country_3": "field40",  # No
    "moved_spain_from_other_country_4": "field41",  # No
    "moved_spain_from_other_country_5": "field42",  # No
    "moved_within_spain_1": "Choice3",
    "moved_within_spain_2": "Choice4",
    "moved_within_spain_3": "Choice5",
    "moved_within_spain_4": "Choice6",
    "moved_within_spain_5": "Choice7",  # No
}


def read_pdf_custom_id(pdf_path):
    doc = fitz.open(pdf_path)
    custom_id = None
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for annot in page.annots():
            text = annot.info["content"]
            if text.startswith("ID: "):
                custom_id = text[4:]
                break
        if custom_id:
            break
    print(f"Custom ID: {custom_id}")
    return custom_id


def upload_to_supabase(data, table_name):
    response = supabase.table(table_name).insert(data).execute()
    return response


def check_pdf_type(doc):
    first_page_text = doc.load_page(0).get_text()
    if "Data Sheet for NIE/TIE" in first_page_text:
        return "data_sheet_nie_tie"
    elif "Deadline - till when I need the paperwork:" in first_page_text:
        print("+++++++++++++++++")
        print("estoy aqui")
        return "initial_data_request"
    elif "Empadronamiento" in first_page_text:
        return "empadron_data"
    return None


def process_widget_nie_tie(data, widget):
    if "field" in widget.field_name:
        for key, value in nie_tie_pdf_fields_data.items():
            if widget.field_name == value:
                translation_try = translate_countries_from_en_es(widget.field_value)
                data[key] = translation_try if translation_try != widget.field_value else widget.field_value
    elif "Button" in widget.field_name:
        if widget.field_value == "No":
            if widget.field_name == "Button1":
                data["family_status"] = "single"
            elif widget.field_name == "Button2":
                data["family_status"] = "married"
            elif widget.field_name == "Button3":
                data["family_status"] = "widowed"
            elif widget.field_name == "Button4":
                data["family_status"] = "divorced"
            elif widget.field_name == "Button5":
                data["family_status"] = "separated"
            elif widget.field_name == "Button6":
                data["gender"] = "male"
            elif widget.field_name == "Button7":
                data["gender"] = "female"
            elif widget.field_name == "Button8":
                data["consent_communication_electronically"] = True
            elif widget.field_name == "Button9":
                data["apply_digital_certificate"] = True
            elif widget.field_name == "Button10":
                data["no_consent_data_consultation"] = True
    elif "Choice" in widget.field_name:
        if widget.field_name == "Choice19":
            data["province"] = widget.field_value

    return data


def process_widget_initial_data(data, widget):
    if "field" in widget.field_name:
        if widget.field_name in ["field9", "field10"]:
            if "mobile_phone" not in data:
                data["mobile_phone"] = ""
            data["mobile_phone"] += widget.field_value
        else:
            for key, value in parse_initial_data_fields.items():
                if widget.field_name == value and widget.field_value != "":
                    translation_try = translate_countries_from_en_es(widget.field_value)
                    data[key] = translation_try if translation_try != widget.field_value else widget.field_value
    elif "Button" in widget.field_name:
        if widget.field_value == "No":
            if "Button3" in widget.field_name:
                data["desired_service"] = "White NIE"
            elif "Button4" in widget.field_name:
                data["desired_service"] = "Green NIE"
            elif "Button5" in widget.field_name:
                data["desired_service"] = "TIE"
            elif "Button6" in widget.field_name:
                data["desired_service"] = "Empadronamiento & Travel Discount"
            elif "Button7" in widget.field_name:
                data["desired_service"] = "Autónomo"
            elif widget.field_name == "Button9":
                data["appointment_location"] = "Nearby cities"
            elif widget.field_name == "Button10":
                data["appointment_location"] = "My city"
            elif widget.field_name == "Button11":
                data["referral_source"] = "Slack LUP Nelly"
            elif widget.field_name == "Button12":
                data["referral_source"] = "Friend"
            elif widget.field_name == "Button13":
                data["referral_source"] = "Facebook"
            elif widget.field_name == "Button14":
                data["referral_source"] = "Website"
            elif widget.field_name == "Button15":
                data["referral_source"] = "Flyer"
            elif widget.field_name == "Button16":
                data["referral_source"] = "Poster"
    elif "Choice" in widget.field_name:
        for key, value in parse_initial_data_fields.items():
            if widget.field_name == value and widget.field_value != "":
                translation_try = translate_countries_from_en_es(widget.field_value)
                data[key] = translation_try if translation_try != widget.field_value else widget.field_value
    return data


def process_widget_empadronamiento(data, widget):
    if "field" in widget.field_name or "Text" in widget.field_name:
        for key, value in empadron_data.items():
            if widget.field_name == value:
                translation_try = translate_countries_from_en_es(widget.field_value)
                data[key] = translation_try if translation_try != widget.field_value else widget.field_value
    elif "Button" in widget.field_name:

        if widget.field_name == "Button1":

            if widget.field_value != "Off":
                print("Voluntary statement checkbox is checked by user")
                data["voluntary_statement"] = "True"
            else:
                data["voluntary_statement"] = "False"

        if widget.field_name == "Button5" and widget.field_value != "Off":
            print("Signed hand contract checkbox is checked by user")

            data["rent_contract"] = "signed by hand"

        elif widget.field_name == "Button6" and widget.field_value != "Off":
            print("Official Spanish contract checkbox is checked by user")
            data["rent_contract"] = "official Spanish Certificado digital"

        elif widget.field_name == "Button7" and widget.field_value != "Off":
            print("Signed electronic contract checkbox is checked by user")
            data["rent_contract"] = "signed electronically by other means"

        if widget.field_name == "Button10" and widget.field_value != "Off":
            print("Landlord checkbox is checked by user")
            data["landlord_type"] = "landlord"

        elif widget.field_name == "Button9" and widget.field_value != "Off":
            print("Co-inhabitant checkbox is checked by user")
            data["landlord_type"] = "co-inhabitant"

        if widget.field_name == "Button54" and widget.field_value != "Off":
            print("Male  1 checkbox is checked by user")
            data["gender_1"] = "male"
        elif widget.field_name == "Button53" and widget.field_value != "Off":
            print("Female 1 checkbox is checked by user")
            data["gender_1"] = "female"

        if widget.field_name == "Button14" and widget.field_value != "Off":
            print("Newborns 1 checkbox is checked by user")
            data["birth_newborns_1"] = "True"

        if widget.field_name == "Button16" and widget.field_value != "Off":
            print("Change personal data 1 checkbox is checked by user")
            data["change_personal_data_1"] = True

        if widget.field_name == "Button33":
            if widget.field_value != "Off":
                print("Municipal level 1 checkbox is checked by user")
                data["vote_municipal_level_1"] = True
            else:
                data["vote_municipal_level_1"] = False

        if widget.field_name == "Button35":
            if widget.field_value != "Off":
                print("Europe voting right 1 checkbox is checked by user")
                data["change_europe_voting_right_1"] = True
            else:
                data["change_europe_voting_right_1"] = False

        if widget.field_name == "Button56" and widget.field_value != "Off":
            print("Male 2 checkbox is checked by user")
            data["gender_2"] = "male"
        elif widget.field_name == "Button55" and widget.field_value != "Off":
            print("Female 2 checkbox is checked by user")
            data["gender_2"] = "female"

        if widget.field_name == "Button19" and widget.field_value != "Off":
            data["birth_newborns_2"] = "True"
            print("Newborns 2 checkbox is checked by user")

        if widget.field_name == "Button17" and widget.field_value != "Off":
            data["change_personal_data_2"] = True
            print("Change personal data 2 checkbox is checked by user")

        if widget.field_name == "Button45":
            if widget.field_value != "Off":
                data["vote_municipal_level_2"] = True
                print("Municipal level 2 checkbox is checked by user")
            else:
                data["vote_municipal_level_2"] = False

        if widget.field_name == "Button37":
            if widget.field_value != "Off":
                print("Europe voting right 2 checkbox is checked by user")
                data["change_europe_voting_right_2"] = True
            else:
                data["change_europe_voting_right_2"] = False

        if widget.field_name == "Button58" and widget.field_value != "Off":
            print("Male 3 checkbox is checked by user")
            data["gender_3"] = "male"

        elif widget.field_name == "Button57" and widget.field_value != "Off":
            print("Female 3 checkbox is checked by user")
            data["gender_3"] = "female"

        if widget.field_name == "Button22" and widget.field_value != "Off":
            print("Newborns 3 checkbox is checked by user")
            data["birth_newborns_3"] = "True"

        if widget.field_name == "Button24" and widget.field_value != "Off":
            print("Change personal data 3 checkbox is checked by user")
            data["change_personal_data_3"] = True

        if widget.field_name == "Button47":
            if widget.field_value != "Off":
                print("Municipal level 3 checkbox is checked by user")
                data["vote_municipal_level_3"] = True
            else:
                data["vote_municipal_level_3"] = False

        if widget.field_name == "Button39":
            if widget.field_value != "Off":
                print("Europe voting right 3 checkbox is checked by user")
                data["change_europe_voting_right_3"] = True
            else:
                data["change_europe_voting_right_3"] = False

        if widget.field_name == "Button60" and widget.field_value != "Off":
            print("Male 4 checkbox is checked by user")
            data["gender_4"] = "male"

        elif widget.field_name == "Button59" and widget.field_value != "Off":
            print("Female 4 checkbox is checked by user")
            data["gender_4"] = "female"

        if widget.field_name == "Button27" and widget.field_value != "Off":
            print("Newborns 4 checkbox is checked by user")
            data["birth_newborns_4"] = "True"

        if widget.field_name == "Button29" and widget.field_value != "Off":
            print("Change personal data 4 checkbox is checked by user")
            data["change_personal_data_4"] = True

        if widget.field_name == "Button49":
            if widget.field_value != "Off":
                print("Municipal level 4 checkbox is checked by user")
                data["vote_municipal_level_4"] = True
            else:
                data["vote_municipal_level_4"] = False

        if widget.field_name == "Button41":
            if widget.field_value != "Off":
                print("Europe voting right 4 checkbox is checked by user")
                data["change_europe_voting_right_4"] = True
            else:
                data["change_europe_voting_right_4"] = False

        # perosn 5

        if widget.field_name == "Button62" and widget.field_value != "Off":
            print("Male 5 checkbox is checked by user")
            data["gender_5"] = "male"

        elif widget.field_name == "Button61" and widget.field_value != "Off":
            print("Female 5 checkbox is checked by user")
            data["gender_5"] = "female"

        if widget.field_name == "Button32" and widget.field_value != "Off":
            print("Newborns 5 checkbox is checked by user")
            data["birth_newborns_5"] = "True"

        if widget.field_name == "Button30" and widget.field_value != "Off":
            print("Change personal data 5 checkbox is checked by user")
            data["change_personal_data_5"] = True

        if widget.field_name == "Button51":
            if widget.field_value != "Off":
                print("Municipal level 5 checkbox is checked by user")
                data["vote_municipal_level_5"] = True
            else:
                data["vote_municipal_level_5"] = False

        if widget.field_name == "Button43":
            if widget.field_value != "Off":
                print("Europe voting right 5 checkbox is checked by user")
                data["change_europe_voting_right_5"] = True
            else:
                data["change_europe_voting_right_5"] = False



    elif "Choice" in widget.field_name:
        for key, value in empadron_data.items():
            if widget.field_name == value:
                translation_try = translate_countries_from_en_es(widget.field_value)
                data[key] = translation_try if translation_try != widget.field_value else widget.field_value
    return data


def get_existing_initial_data_id(custom_id):
    response = supabase.table("initial_data_request").select("*").eq("id", custom_id).execute()
    return response.data[0]["id"] if response.data else None


def process_pdfs(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            field_index = 1
            bool_index = 1
            choice_index = 1
            pdf_id = read_pdf_custom_id(os.path.join(folder_path, filename))

            if pdf_id:
                print(f"PDF ID: {pdf_id}")
            else:
                pdf_id = None
            pdf_path = os.path.join(folder_path, filename)
            doc = fitz.open(pdf_path)
            pdf_type = check_pdf_type(doc)
            data = {}

            for page in doc:
                for widget in page.widgets():

                    if widget.field_type == 2:
                        widget.field_name = "Button" + str(bool_index)
                        bool_index += 1
                    elif widget.field_type == 7:
                        widget.field_name = "field" + str(field_index)
                        field_index += 1

                    elif widget.field_type == 3:
                        widget.field_name = "Choice" + str(choice_index)
                        choice_index += 1
                    widget.update()
                    if "Las Palmas" in widget.field_value:
                        print("------------------------------------")
                        print(widget.field_name)
                        print("=========================")
                    #print(f"Widget: {widget.field_name}, Value: {widget.field_value}")
                    if pdf_type == "data_sheet_nie_tie":
                        data = process_widget_nie_tie(data, widget)
                    elif pdf_type == "initial_data_request":
                        data = process_widget_initial_data(data, widget)
                    elif pdf_type == "empadron_data":
                        data = process_widget_empadronamiento(data, widget)
            print(data)

            if pdf_type:

                print(f"Processing {pdf_type}...")
                try:
                    upload_to_supabase(data, pdf_type)
                except Exception as e:
                    print(f"Error uploading to Supabase: {e}")
                    continue
                print(f"Uploaded {pdf_type} to Supabase")


def main():
    # Determine the directory where the script is located
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (PyInstaller)
        application_path = os.path.dirname(sys.executable)
    else:
        # If the application is run as a script
        application_path = os.path.dirname(os.path.abspath(__file__))

    # Define the folder for input PDFs
    input_pdfs_folder = os.path.join(application_path, 'test2')

    # Process PDFs in the input_pdfs folder
    process_pdfs(input_pdfs_folder)


if __name__ == "__main__":
    main()
