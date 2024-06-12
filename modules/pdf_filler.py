import time
import os
import uuid

import fitz  # PyMuPDF
import sys


def pdf_filler_11(data_to_fill, additional_users):
    # Function to fill data for 11-Formulario_larga_duracixn.pdf
    data = {}
    nie_numbers = data_to_fill.get('nie', ' - - ').split("-")
    print(data_to_fill)
    surnames = data_to_fill.get('surname', '   ').split(" ")
    birth_dates = data_to_fill.get('birth_date', ' - - ').split("-")
    if data_to_fill["gender"] == "female":
        data['field_8'] = True
    else:
        data['field_7'] = True

    # Family status
    family_status_map = {
        "single": 'field_14',
        "married": 'field_15',
        "widowed": 'field_16',
        "divorced": 'field_17',
        "separated": 'field_18'
    }
    checkboxes = ["field_14", "field_15", "field_16", "field_17", "field_18", "field_8", "field_7"]
    family_status_field = family_status_map.get(data_to_fill["family_status"])
    if family_status_field:
        data[family_status_field] = True

    data['field_0'] = data_to_fill.get('passport_number', '')
    data['field_1'] = nie_numbers[0]
    data['field_2'] = nie_numbers[1]
    data['field_3'] = nie_numbers[2]
    data['field_21'] = surnames[0]
    if len(surnames) > 1:
        data['field_4'] = surnames[1]
    data['field_5'] = data_to_fill.get('name', '')
    data['field_58'] = birth_dates[0]
    data['field_57'] = birth_dates[1]
    data['field_10'] = birth_dates[2]
    data['field_11'] = data_to_fill.get('city_of_birth', '')
    data['field_12'] = data_to_fill.get('country_of_birth', '')
    data['field_13'] = data_to_fill.get('nationality', '')
    data['field_19'] = data_to_fill.get('full_name_of_father', '')
    data['field_20'] = data_to_fill.get('full_name_of_mother', '')
    data['field_22'] = data_to_fill.get('spain_address', '')
    data['field_23'] = data_to_fill.get('house_name', '')
    data['field_24'] = data_to_fill.get('apt_number', '')
    data['field_25'] = data_to_fill.get('city', '')
    data['field_26'] = data_to_fill.get('zip_code', '')
    data['field_27'] = data_to_fill.get('province', '')
    data['field_28'] = data_to_fill.get('mobile_phone', '')
    data['field_29'] = data_to_fill.get('email', '')
    data['field_30'] = data_to_fill.get('legal_representative_name', '')
    data['field_31'] = data_to_fill.get('legal_representative_id', '')
    data['field_32'] = data_to_fill.get('legal_representative_relation', '')
    print(data)

    return data, checkboxes


def pdf_filler_15(data_to_fill, additional_users):
    # Function to fill data for 15-Formulario_NIE_y_certificados.pdf
    # Function to fill data for 19-Tarjeta_familiar_comunitario.pdf
    data = {}
    checkboxes = ["field_9", "field_8", "field_15", "field_16", "field_17", "field_18", "field_19"]

    if data_to_fill["gender"] == "female":
        data['field_9'] = True
    else:
        data['field_8'] = False
    if data_to_fill["family_status"] == "single":
        data['field_15'] = True

    elif data_to_fill["family_status"] == "married":
        data['field_16'] = True

    elif data_to_fill["family_status"] == "widowed":
        data['field_17'] = True

    elif data_to_fill["family_status"] == "divorced":
        data['field_18'] = True

    elif data_to_fill["family_status"] == "separated":
        data['field_19'] = True

    nie_numbers = data_to_fill.get('nie', ' - - ').split("-")
    surnames = data_to_fill.get('surname', '   ').split(" ")
    birth_dates = data_to_fill.get('birth_date', ' - - ').split("-")
    data['field_0'] = data_to_fill.get('passport_number', '')
    data['field_1'] = nie_numbers[0]
    data['field_2'] = nie_numbers[1]
    data['field_3'] = nie_numbers[2]
    data['field_4'] = surnames[0]
    if len(surnames) > 1:
        data['field_5'] = surnames[1]
    data['field_6'] = data_to_fill.get('name', '')
    data['field_10'] = birth_dates[0]
    data['field_57'] = birth_dates[1]
    data['field_11'] = birth_dates[2]
    data['field_12'] = data_to_fill.get('city_of_birth', '')
    data['field_13'] = data_to_fill.get('country_of_birth', '')
    data['field_14'] = data_to_fill.get('nationality', '')
    data['field_20'] = data_to_fill.get('full_name_of_father', '')
    data['field_21'] = data_to_fill.get('full_name_of_mother', '')
    data['field_22'] = data_to_fill.get('spain_address', '')
    data['field_23'] = data_to_fill.get('house_name', '')
    data['field_24'] = data_to_fill.get('apt_number', '')  # TODO piso is not provided
    data['field_25'] = data_to_fill.get('city', '')
    data['field_26'] = data_to_fill.get('zip_code', '')
    data['field_27'] = data_to_fill.get('province', '')
    data['field_28'] = data_to_fill.get('mobile_phone', '')
    data['field_29'] = data_to_fill.get('email', '')
    data['field_30'] = data_to_fill.get('legal_representative_name', '')
    data['field_35'] = data_to_fill.get('legal_representative_id', '')
    data['field_31'] = data_to_fill.get('legal_representative_relation', '')
    return data, checkboxes


def pdf_filler_17(data_to_fill, additional_users):
    # Function to fill data for 17-Formulario_TIE.pdf
    data = {}
    checkboxes = ["field_14", "field_15", "field_16", "field_17", "field_18", "field_8", "field_7"]

    if data_to_fill["gender"] == "female":
        data['field_8'] = True
    else:
        data['field_7'] = False
    if data_to_fill["family_status"] == "single":
        data['field_14'] = True
    elif data_to_fill["family_status"] == "married":
        data['field_15'] = True
    elif data_to_fill["family_status"] == "widowed":
        data['field_16'] = True
    elif data_to_fill["family_status"] == "divorced":
        data['field_17'] = True
    elif data_to_fill["family_status"] == "separated":
        data['field_18'] = True
    nie_numbers = data_to_fill.get('nie', ' - - ').split("-")
    surnames = data_to_fill.get('surname', '   ').split(" ")
    birth_dates = data_to_fill.get('birth_date', ' - - ').split("-")
    data['field_0'] = data_to_fill.get('passport_number', '')
    data['field_1'] = nie_numbers[0]
    data['field_2'] = nie_numbers[1]
    data['field_3'] = nie_numbers[2]
    data['field_21'] = surnames[0]
    if len(surnames) > 1:
        data['field_4'] = surnames[1]
    data['field_5'] = data_to_fill.get('name', '')
    data['field_9'] = birth_dates[0]
    data['field_57'] = birth_dates[1]
    data['field_10'] = birth_dates[2]
    data['field_12'] = data_to_fill.get('city_of_birth', '')
    data['field_11'] = data_to_fill.get('country_of_birth', '')
    data['field_13'] = data_to_fill.get('nationality', '')
    data['field_19'] = data_to_fill.get('full_name_of_father', '')
    data['field_20'] = data_to_fill.get('full_name_of_mother', '')
    data['field_22'] = data_to_fill.get('spain_address', '')
    data['field_23'] = data_to_fill.get('house_name', '')
    data['field_24'] = data_to_fill.get('apt_number', '')  # TODO piso is not provided
    data['field_25'] = data_to_fill.get('city', '')
    data['field_26'] = data_to_fill.get('zip_code', '')
    data['field_27'] = data_to_fill.get('province', '')
    data['field_28'] = data_to_fill.get('mobile_phone', '')
    data['field_29'] = data_to_fill.get('email', '')
    data['field_30'] = data_to_fill.get('legal_representative_name', '')
    data['field_31'] = data_to_fill.get('legal_representative_id', '')
    data['field_32'] = data_to_fill.get('legal_representative_relation', '')
    return data, checkboxes


def pdf_filler_18(data_to_fill, additional_users):
    # Function to fill data for 18-Certificado_residencia_comunitaria.pdf
    data = {}
    checkboxes = ["field_14", "field_15", "field_16", "field_17", "field_18", "field_8", "field_7"]

    if data_to_fill["gender"] == "female":
        data['field_8'] = True
    else:
        data['field_7'] = True
    if data_to_fill["family_status"] == "single":
        data['field_14'] = True
    elif data_to_fill["family_status"] == "married":
        data['field_15'] = True
    elif data_to_fill["family_status"] == "widowed":
        data['field_16'] = True
    elif data_to_fill["family_status"] == "divorced":
        data['field_17'] = True
    elif data_to_fill["family_status"] == "separated":
        data['field_18'] = True
    nie_numbers = data_to_fill.get('nie', ' - - ').split("-")
    surnames = data_to_fill.get('surname', '   ').split(" ")
    birth_dates = data_to_fill.get('birth_date', ' - - ').split("-")
    data['field_0'] = data_to_fill.get('passport_number', '')
    data['field_1'] = nie_numbers[0]
    data['field_2'] = nie_numbers[1]
    data['field_3'] = nie_numbers[2]
    data['field_21'] = surnames[0]
    if len(surnames) > 1:
        data['field_4'] = surnames[1]
    data['field_5'] = data_to_fill.get('name', '')
    data['field_9'] = birth_dates[0]
    data['field_57'] = birth_dates[1]
    data['field_10'] = birth_dates[2]
    data['field_13'] = data_to_fill.get('nationality', '')
    data['field_19'] = data_to_fill.get('full_name_of_father', '')
    data['field_20'] = data_to_fill.get('full_name_of_mother', '')
    data['field_22'] = data_to_fill.get('spain_address', '')
    data['field_23'] = data_to_fill.get('house_name', '')
    data['field_24'] = data_to_fill.get('apt_number', '')  # TODO piso is not provided
    data['field_25'] = data_to_fill.get('city', '')
    data['field_26'] = data_to_fill.get('zip_code', '')
    data['field_27'] = data_to_fill.get('province', '')
    data['field_28'] = data_to_fill.get('mobile_phone', '')
    data['field_29'] = data_to_fill.get('email', '')
    data['field_30'] = data_to_fill.get('legal_representative_name', '')
    data['field_31'] = data_to_fill.get('legal_representative_id', '')
    data['field_32'] = data_to_fill.get('legal_representative_relation', '')
    return data, checkboxes


def pdf_filler_23(data_to_fill, additional_users):
    # Function to fill data for 23-Formulario_TIE_RU.pdf
    data = {}
    checkboxes = ["field_14", "field_15", "field_16", "field_17", "field_18", "field_8", "field_7"]

    if data_to_fill["gender"] == "female":
        data['field_8'] = True
    else:
        data['field_7'] = False
    if data_to_fill["family_status"] == "single":
        data['field_14'] = True
    elif data_to_fill["family_status"] == "married":
        data['field_15'] = True
    elif data_to_fill["family_status"] == "widowed":
        data['field_16'] = True
    elif data_to_fill["family_status"] == "divorced":
        data['field_17'] = True
    elif data_to_fill["family_status"] == "separated":
        data['field_18'] = True
    nie_numbers = data_to_fill.get('nie', ' - - ').split("-")
    surnames = data_to_fill.get('surname', '   ').split(" ")
    birth_dates = data_to_fill.get('birth_date', ' - - ').split("-")
    data['field_0'] = data_to_fill.get('passport_number', '')
    data['field_1'] = nie_numbers[0]
    data['field_2'] = nie_numbers[1]
    data['field_3'] = nie_numbers[2]
    data['field_21'] = surnames[0]
    if len(surnames) > 1:
        data['field_4'] = surnames[1]
    data['field_5'] = data_to_fill.get('name', '')
    data['field_9'] = birth_dates[0]
    data['field_57'] = birth_dates[1]
    data['field_10'] = birth_dates[2]
    data['field_13'] = data_to_fill.get('nationality', '')
    data['field_19'] = data_to_fill.get('full_name_of_father', '')
    data['field_20'] = data_to_fill.get('full_name_of_mother', '')
    data['field_22'] = data_to_fill.get('spain_address', '')
    data['field_23'] = data_to_fill.get('house_name', '')
    data['field_24'] = data_to_fill.get('apt_number', '')  # TODO piso is not provided
    data['field_25'] = data_to_fill.get('city', '')
    data['field_26'] = data_to_fill.get('zip_code', '')
    data['field_27'] = data_to_fill.get('province', '')
    data['field_28'] = data_to_fill.get('mobile_phone', '')
    data['field_29'] = data_to_fill.get('email', '')
    data['field_30'] = data_to_fill.get('legal_representative_name', '')
    data['field_31'] = data_to_fill.get('legal_representative_id', '')
    data['field_32'] = data_to_fill.get('legal_representative_relation', '')
    return data, checkboxes


def pdf_filler_19(data_to_fill, additional_users):
    # Function to fill data for 19-Tarjeta_familiar_comunitario.pdf
    data = {}
    checkboxes = ["field_14", "field_15", "field_16", "field_17", "field_18", "field_8", "field_7"]

    if data_to_fill["gender"] == "female":
        data['field_8'] = True
    else:
        data['field_7'] = False
    if data_to_fill["family_status"] == "single":
        data['field_14'] = True

    elif data_to_fill["family_status"] == "married":
        data['field_15'] = True

    elif data_to_fill["family_status"] == "widowed":
        data['field_16'] = True

    elif data_to_fill["family_status"] == "divorced":
        data['field_17'] = True

    elif data_to_fill["family_status"] == "separated":
        data['field_18'] = True

    nie_numbers = data_to_fill.get('nie', ' - - ').split("-")
    surnames = data_to_fill.get('surname', '   ').split(" ")
    birth_dates = data_to_fill.get('birth_date', ' - - ').split("-")
    data['field_0'] = data_to_fill.get('passport_number', '')
    data['field_1'] = nie_numbers[0]
    data['field_2'] = nie_numbers[1]
    data['field_3'] = nie_numbers[2]
    data['field_21'] = surnames[0]
    if len(surnames) > 1:
        data['field_4'] = surnames[1]
    data['field_5'] = data_to_fill.get('name', '')
    data['field_9'] = birth_dates[0]
    data['field_72'] = birth_dates[1]
    data['field_10'] = birth_dates[2]
    data['field_13'] = data_to_fill.get('nationality', '')
    data['field_19'] = data_to_fill.get('full_name_of_father', '')
    data['field_20'] = data_to_fill.get('full_name_of_mother', '')
    data['field_22'] = data_to_fill.get('spain_address', '')
    data['field_23'] = data_to_fill.get('house_name', '')
    data['field_24'] = data_to_fill.get('apt_number', '')  # TODO piso is not provided
    data['field_25'] = data_to_fill.get('city', '')
    data['field_26'] = data_to_fill.get('zip_code', '')
    data['field_27'] = data_to_fill.get('province', '')
    data['field_28'] = data_to_fill.get('mobile_phone', '')
    data['field_29'] = data_to_fill.get('email', '')
    data['field_30'] = data_to_fill.get('legal_representative_name', '')
    data['field_31'] = data_to_fill.get('legal_representative_id', '')
    data['field_32'] = data_to_fill.get('legal_representative_relation', '')
    return data, checkboxes


def pdf_filler_hoja_padronal(data_to_fill, additional_users):
    # Function to fill data for Hoja_Padronal.pdf
    data, checkboxes = convert_to_pdf_form_data(data_to_fill)
    if additional_users:
        data = add_additional_users(data, additional_users)

    return data, checkboxes


def pdf_filler_NIE_TIE(data_to_fill, additional_users):
    # Function to fill data for Data Sheet for NIE_TIE - gottalovespain.pdf
    data = {
        'field_0': data_to_fill.get('name'),
        'field_1': data_to_fill.get('surname', ''),
        "id": data_to_fill.get("id", ""),
    }
    print(data_to_fill.get("id", ""))
    return data, []


pdf_filler_docs_es_ext = {
    "11-Formulario_larga_duracixn.pdf": pdf_filler_11,
    "15-Formulario_NIE_y_certificados.pdf": pdf_filler_15,
    "17-Formulario_TIE.pdf": pdf_filler_17,
    "18-Certificado_residencia_comunitaria.pdf": pdf_filler_18,
    "19-Tarjeta_familiar_comunitario.pdf": pdf_filler_19,
    "23-Formulario_TIE_RU.pdf": pdf_filler_23,
    "Hoja_Padronal.pdf": pdf_filler_hoja_padronal,
    "Data Sheet for NIE_TIE - gottalovespain.pdf": pdf_filler_NIE_TIE,
}


def convert_to_pdf_form_data(db_data):
    birth_date = db_data.get('birth_date')
    if birth_date:
        birth_spanish_time_format = str(time.strftime('%d/%m/%Y', time.strptime(birth_date, '%Y-%m-%d')))
    else:
        birth_spanish_time_format = None
    names = db_data.get('name').split(" ")
    print(names)
    pdf_data_for_filling = {
        'untitled1': db_data.get('street_type', ""),
        'untitled2': db_data.get('street_name', ""),
        'untitled3': db_data.get('house_name', ""),
        'untitled4': db_data.get('building_letter', ""),
        'untitled5': db_data.get('apt_number', ""),
        'untitled6': db_data.get('building_portal', ""),
        'untitled8': str(db_data.get('building_floor', "")),
        'untitled9': str(db_data.get('building_door_number', "")),
        'untitled10': True,
        'untitled12': db_data.get('surname', ""),
        'untitled13': names[0],
        'untitled17': birth_spanish_time_format,
        'untitled18': db_data.get('city_of_birth', ""),
        'untitled19': db_data.get('country_of_birth', ""),
        'untitled20': db_data.get('nationality', ""),
        'untitled24': db_data.get('id_number', ""),
        'untitled25': db_data.get('study_level', ""),
        'untitled26': db_data.get('mobile_phone', ""),
        'untitled27': db_data.get('email', ""),
        'untitled33': db_data.get('prev_province_spain', ""),
        'untitled34': db_data.get('prev_country', ""),
        'untitled105': db_data.get('landlord_name', ""),
        'untitled106': db_data.get('landlord_id', ""),
        'untitled107': str(db_data.get('people_sum_involved', "")),
    }
    if len(names) > 1:
        pdf_data_for_filling['untitled14'] = names[1]

    # id type
    if db_data.get("nie"):
        pdf_data_for_filling['untitled23'] = True
    elif db_data.get("dni"):
        pdf_data_for_filling['untitled21'] = True
    elif db_data.get("passport_number"):
        pdf_data_for_filling['untitled22'] = True
    # gender
    if db_data.get('gender', "") == 'male':
        pdf_data_for_filling['untitled15'] = True
    else:
        pdf_data_for_filling['untitled16'] = True
    # case type
    """TODO
    if db_data.get('desired_service', "") == 'change residency':
        pdf_data_for_filling['untitled28'] = True
    elif db_data.get('desired_service', "") == 'omission':
        pdf_data_for_filling['untitled29'] = True
    elif db_data.get('desired_service', "") == 'birth':
        pdf_data_for_filling['untitled30'] = True
    elif db_data.get('desired_service', "") == 'change address':
        pdf_data_for_filling['untitled31'] = True
    elif db_data.get('desired_service', "") == 'change personal data':
        pdf_data_for_filling['untitled32'] = True
    """
    checkboxes = ["untitled28", "untitled29", "untitled30", "untitled31", "untitled32", "untitled23", "untitled21",
                  "untitled22", "untitled15", "untitled16"]

    return pdf_data_for_filling, checkboxes


def get_executable_dir():
    """ Get the directory of the executable, if running as an executable """
    if hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def rename_pdf_fiedl_in_order(pdf_path):
    doc = fitz.open(pdf_path)
    new_field_name = "field_"
    for page in doc:
        for index, field in enumerate(page.widgets()):
            field.field_name = new_field_name + str(index)
            field.update()
    # add renamed keyword to the saved pdf
    pdf_path = pdf_path.replace(".pdf", "")
    pdf_path = pdf_path.replace("pdfs_to_fill", "tmp_pdfs")
    pdf_path += "fixed.pdf"
    doc.save(pdf_path)
    doc.close()


def fill_pdf(pdf_path, db_data, additional_users=None):
    pdf_name = os.path.basename(pdf_path)
    print(f"pdf name {pdf_name} pdf path{pdf_path}")
    if pdf_name in pdf_filler_docs_es_ext.keys():
        pdf_data_for_filling, checkboxes = pdf_filler_docs_es_ext[pdf_name](db_data, additional_users)
    else:
        raise ValueError(f"No PDF filler function found for {pdf_name}")
    field_index = 0

    doc = fitz.open(pdf_path)

    print(f"pdf data for filling {pdf_data_for_filling}")
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for widget in page.widgets():
            if "Hoja" not in pdf_path:
                widget.field_name = f"field_{field_index}"
            field_index += 1
            widget.update()
            field_name = widget.field_name
            if field_name in pdf_data_for_filling:
                field_value = pdf_data_for_filling[field_name]
                if field_name in checkboxes and widget.field_type == 2:
                    print(f"Checkbox {field_name} set to {field_value} in field type {widget.field_type}")

                    widget.field_value = field_value
                else:
                    widget.field_value = str(field_value)
                widget.update()
            else:
                widget.reset()
                widget.update()
                if widget.field_type == 7:
                    widget.field_value = " "
                    widget.update()

    output_dir = os.path.join(get_executable_dir(), 'output')
    os.makedirs(output_dir, exist_ok=True)

    if pdf_data_for_filling.get("id") and "gottalovespain" in pdf_path:
        id_text = f"ID: {pdf_data_for_filling.get('id')}"
        # Define position for the text annotation
        page = doc.load_page(0)  # Load the first page
        rect = fitz.Rect(10, 10, 100, 30)  # Define a specific location for easier retrieval
        # Add free text annotation with a white color to make it effectively invisible
        page.add_freetext_annot(rect, id_text, fontsize=12)

    output_path = os.path.join(output_dir,
                               f"Filled_{pdf_name}_{str(uuid.uuid4())}.pdf")
    if len(doc) > 1:
        doc.delete_page(1)
    doc.save(output_path)

    print(f"document saved to {output_path} with id {read_pdf_custom_id(output_path)}")
    print(f"PDF filled and saved to {output_path}")


def add_additional_users(data, additional_users):
    base_pdf_index = 1
    fields_per_user = 23  # Number of fields per additional user
    data['untitled107'] = str(len(additional_users) + 1).replace("(", "").replace(",)", "")

    checked = False
    for user_index, user in enumerate(additional_users):
        if user_index >= 4:
            break  # Ensure we do not add more than 4 users
        current_base_index = base_pdf_index + user_index * fields_per_user
        print(current_base_index)
        print("______________")
        birth_spanish_time_format = str(time.strftime('%d/%m/%Y', time.strptime(user["birth_date"], '%Y-%m-%d')))
        if not checked:
            if user.get("dni"):
                data['untitled48.field13'] = user.get("dni")
            if user.get("nie"):
                data['untitled48.field13'] = user.get("nie")
            if user.get("passport_number"):
                data['untitled48.field13'] = user.get("passport_number")
            data['untitled48.field15'] = user.get('mobile_phone'),
            checked = True
        else:
            data[f'field{current_base_index + 14}'] = user.get("mobile_phone")
            if user.get("dni"):
                data[f'field{current_base_index + 12}'] = user.get("dni")
            if user.get("nie"):
                data[f'field{current_base_index + 12}'] = user.get("nie")
            if user.get("passport_number"):
                data[f'field{current_base_index + 12}'] = user.get("passport_number")
        if " " in user.get("name"):
            user["second_name"] = user.get("name").split(" ")[1]
            user["name"] = user.get("name").split(" ")[0]
        data[f'field{current_base_index}'] = user.get("surname")
        data[f'field{current_base_index + 1}'] = user.get("name")
        data[f'field{current_base_index + 2}'] = user.get("second_name")
        data[f'field{current_base_index + 5}'] = birth_spanish_time_format
        data[f'field{current_base_index + 6}'] = user.get("city_of_birth")
        data[f'field{current_base_index + 7}'] = user.get("country_of_birth")
        data[f'field{current_base_index + 8}'] = user.get("nationality")
        data[f'field{current_base_index + 15}'] = user.get('email')

        data[f'field{current_base_index + 13}'] = user.get("study_level")
        data[f'field{current_base_index + 21}'] = user.get("prev_province_spain")
        data[f'field{current_base_index + 22}'] = user.get("prev_country")

        if user.get("nie"):
            data[f'field{current_base_index + 11}'] = True
        elif user.get("dni"):
            data[f'field{current_base_index + 9}'] = True
        elif user.get("passport_number"):
            data[f'field{current_base_index + 10}'] = True
        # gender
        if user.get('gender') == 'male':
            data[f'field{current_base_index + 3}'] = True
        else:
            data[f'field{current_base_index + 4}'] = True
        # case type
        """
        if user.get('document_case_type'] == 'change residency':
            data[f'field{current_base_index + 16}'] = True
        elif user.get('document_case_type'] == 'omission':
            data[f'field{current_base_index + 17}'] = True
        elif user.get('document_case_type'] == 'birth':
            data[f'field{current_base_index + 18}'] = True
        elif user.get('document_case_type'] == 'change address':
            data[f'field{current_base_index + 19}'] = True
        elif user.get('document_case_type'] == 'change personal data':
            data[f'field{current_base_index + 20}'] = True
        """
    return data


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
