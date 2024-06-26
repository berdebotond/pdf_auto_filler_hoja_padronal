import time
import os
import uuid
import fitz  # PyMuPDF
import sys


def check_street(spain_address):
    street_map = {
        "calle": "Calle (street)",
        "avenida": "Avenida (avenue)",
        "plaza": "Plaza (plaza)",
        "carretera": "Carretera (road)",
        "paseo": "Paseo (promenade)"
    }
    for key, value in street_map.items():
        if key in spain_address.lower():
            return value, spain_address.lower().replace(key, "")
    return spain_address, spain_address


def fill_common_fields(data_to_fill):
    nie_numbers = data_to_fill.get('nie', ' - - ').split("-")
    surnames = data_to_fill.get('surname', '   ').split(" ")
    birth_dates = data_to_fill.get('birth_date', ' - - ').split("-")

    data = {
        'field_0': data_to_fill.get('passport_number', ''),
        'field_1': nie_numbers[0] if len(nie_numbers) > 0 else '',
        'field_2': nie_numbers[1] if len(nie_numbers) > 1 else '',
        'field_3': nie_numbers[2] if len(nie_numbers) > 2 else '',
        'field_4': surnames[1] if len(surnames) > 1 else '',
        'field_5': data_to_fill.get('name', ''),
        'field_9': birth_dates[0] if len(birth_dates) > 0 else '',
        'field_57': birth_dates[1] if len(birth_dates) > 1 else '',
        'field_10': birth_dates[2] if len(birth_dates) > 2 else '',
        'field_12': data_to_fill.get('city_of_birth', ''),
        'field_11': data_to_fill.get('country_of_birth', ''),
        'field_13': data_to_fill.get('nationality', ''),
        'field_19': data_to_fill.get('full_name_of_father', ''),
        'field_20': data_to_fill.get('full_name_of_mother', ''),
        'field_22': data_to_fill.get('spain_address', ''),
        'field_23': data_to_fill.get('house_name', ''),
        'field_24': data_to_fill.get('apt_number', ''),
        'field_25': data_to_fill.get('city', ''),
        'field_26': data_to_fill.get('zip_code', ''),
        'field_27': data_to_fill.get('province', ''),
        'field_28': data_to_fill.get('mobile_phone', ''),
        'field_29': data_to_fill.get('email', ''),
        'field_30': data_to_fill.get('legal_representative_name', ''),
        'field_31': data_to_fill.get('legal_representative_id', ''),
        'field_32': data_to_fill.get('legal_representative_relation', '')
    }

    if len(surnames) > 0:
        data['field_21'] = surnames[0]

    return data


def fill_family_status(data_to_fill):
    family_status_map = {
        "single": 'field_14',
        "married": 'field_15',
        "widowed": 'field_16',
        "divorced": 'field_17',
        "separated": 'field_18'
    }
    checkboxes = list(family_status_map.values()) + ["field_8", "field_7"]
    data = {family_status_map[data_to_fill["family_status"]]: True} if data_to_fill[
                                                                           "family_status"] in family_status_map else {}

    return data, checkboxes


def fill_gender(data_to_fill):
    return {'field_8': True} if data_to_fill["gender"] == "female" else {'field_7': True}


def pdf_filler_template(data_to_fill, additional_users, form_specific_fields=None):
    data = fill_common_fields(data_to_fill)
    family_status_data, checkboxes = fill_family_status(data_to_fill)
    gender_data = fill_gender(data_to_fill)

    data.update(family_status_data)
    data.update(gender_data)

    if form_specific_fields:
        data.update(form_specific_fields(data_to_fill))

    return data, checkboxes


def pdf_filler_11(data_to_fill, additional_users):
    return pdf_filler_template(data_to_fill, additional_users)


def pdf_filler_15(data_to_fill, additional_users):
    return pdf_filler_template(data_to_fill, additional_users)


def pdf_filler_17(data_to_fill, additional_users):
    return pdf_filler_template(data_to_fill, additional_users)


def pdf_filler_18(data_to_fill, additional_users):
    return pdf_filler_template(data_to_fill, additional_users)


def pdf_filler_19(data_to_fill, additional_users):
    return pdf_filler_template(data_to_fill, additional_users)


def pdf_filler_23(data_to_fill, additional_users):
    return pdf_filler_template(data_to_fill, additional_users)


def pdf_filler_hoja_padronal(data_to_fill, additional_users):
    data, checkboxes = pdf_filler_template(data_to_fill, additional_users)
    if additional_users:
        data = add_additional_users(data, additional_users)
    return data, checkboxes


def pdf_filler_NIE_TIE(data_to_fill, additional_users):
    data = {
        'field_0': data_to_fill.get('name'),
        'field_1': data_to_fill.get('surname', ''),
        "id": data_to_fill.get("id", ""),
    }
    return data, []


def pdf_filler_empadronamiento(data_to_fill, additional_users=None):
    street_type, address = check_street(data_to_fill.get('spain_address', ''))
    data = {
        'Text1': address,
        'Choice2': street_type,
        "id": data_to_fill.get("id", ""),
        'Text3': data_to_fill.get('zip_code', ''),
        'Text4': data_to_fill.get('province', ''),
        'Text6': data_to_fill.get('apt_number', ''),
        'Text89': data_to_fill.get('name', ''),
        'Text92': data_to_fill.get('surname', ''),
        'Text94': data_to_fill.get('nie', ''),
        'Text95': data_to_fill.get('city_of_birth', ''),
        'Text96': data_to_fill.get('country_of_birth', ''),
    }
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
    "Empadronamiento Form - gottalovespain.pdf": pdf_filler_empadronamiento
}


def convert_to_pdf_form_data(db_data):
    birth_date = db_data.get('birth_date')
    birth_spanish_time_format = str(
        time.strftime('%d/%m/%Y', time.strptime(birth_date, '%Y-%m-%d'))) if birth_date else None
    names = db_data.get('name').split(" ")

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

    if db_data.get("nie"):
        pdf_data_for_filling['untitled23'] = True
    elif db_data.get("dni"):
        pdf_data_for_filling['untitled21'] = True
    elif db_data.get("passport_number"):
        pdf_data_for_filling['untitled22'] = True

    if db_data.get('gender', "") == 'male':
        pdf_data_for_filling['untitled15'] = True
    else:
        pdf_data_for_filling['untitled16'] = True

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
            if "Hoja" not in pdf_path and "Empadronamiento" not in pdf_path:
                widget.field_name = f"field_{field_index}"
            field_index += 1
            widget.update()
            field_name = widget.field_name
            if field_name in pdf_data_for_filling:
                field_value = pdf_data_for_filling[field_name]
                if field_name in checkboxes and widget.field_type == 2:
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
        page = doc.load_page(0)
        rect = fitz.Rect(10, 10, 100, 30)
        page.add_freetext_annot(rect, id_text, fontsize=12)
    else:
        if len(doc) > 1:
            doc.delete_page(1)
    output_path = os.path.join(output_dir,
                               f"Filled_{pdf_name.replace('.pdf', '')}_{str(uuid.uuid4())}.pdf")

    doc.save(output_path)

    print(f"document saved to {output_path} with id {read_pdf_custom_id(output_path)}")
    print(f"PDF filled and saved to {output_path}")


def add_additional_users(data, additional_users):
    base_pdf_index = 1
    fields_per_user = 23
    data['untitled107'] = str(len(additional_users) + 1).replace("(", "").replace(",)", "")

    checked = False
    for user_index, user in enumerate(additional_users):
        if user_index >= 4:
            break
        current_base_index = base_pdf_index + user_index * fields_per_user
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

        if user.get('gender') == 'male':
            data[f'field{current_base_index + 3}'] = True
        else:
            data[f'field{current_base_index + 4}'] = True
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
    return custom_id
