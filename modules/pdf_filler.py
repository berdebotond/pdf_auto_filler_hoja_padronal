
import time
import os
import fitz  # PyMuPDF
import sys

def convert_to_pdf_form_data(db_data):
    birth_date = db_data.get('birth_date')
    if birth_date:
        birth_spanish_time_format = str(time.strftime('%d/%m/%Y', time.strptime(birth_date, '%Y-%m-%d')))
    else:
        birth_spanish_time_format = None
    
    pdf_data_for_filling = {
        'untitled1': db_data.get('street_type'),
        'untitled2': db_data.get('street_name'),
        'untitled3': db_data.get('building_number'),
        'untitled4': db_data.get('building_letter'),
        'untitled5': db_data.get('building_number'),
        'untitled6': db_data.get('building_portal'),
        'untitled8': str(db_data.get('building_floor')),
        'untitled9': str(db_data.get('building_door_number')),
        'untitled10': True,
        'untitled12': db_data.get('surname'),
        'untitled13': db_data.get('first_name'),
        'untitled14': db_data.get('second_name'),
        'untitled17': birth_spanish_time_format,
        'untitled18': db_data.get('city_of_birth'),
        'untitled19': db_data.get('country_of_birth'),
        'untitled20': db_data.get('nationality'),
        'untitled24': db_data.get('id_number'),
        'untitled25': db_data.get('study_level'),
        'untitled26': db_data.get('phone'),
        'untitled27': db_data.get('email'),
        'untitled33': db_data.get('prev_province_spain'),
        'untitled34': db_data.get('prev_country'),
        'untitled105': db_data.get('landlord_name'),
        'untitled106': db_data.get('landlord_id'),
        'untitled107': str(db_data.get('people_sum_involved')),
    }
    # id type
    if db_data.get("id_documnet_type") == "NIE":
        pdf_data_for_filling['untitled23'] = True
    elif db_data.get("id_documnet_type") == "DNI":
        pdf_data_for_filling['untitled21'] = True
    elif db_data.get("id_documnet_type") == "Passport":
        pdf_data_for_filling['untitled22'] = True
    # gender
    if db_data.get('gender') == 'Man':
        pdf_data_for_filling['untitled15'] = True
    else:
        pdf_data_for_filling['untitled16'] = True
    # case type
    if db_data.get('document_case_type') == 'change residency':
        pdf_data_for_filling['untitled28'] = True
    elif db_data.get('document_case_type') == 'omission':
        pdf_data_for_filling['untitled29'] = True
    elif db_data.get('document_case_type') == 'birth':
        pdf_data_for_filling['untitled30'] = True
    elif db_data.get('document_case_type') == 'change address':
        pdf_data_for_filling['untitled31'] = True
    elif db_data.get('document_case_type') == 'change personal data':
        pdf_data_for_filling['untitled32'] = True
    
    return pdf_data_for_filling

def get_executable_dir():
    """ Get the directory of the executable, if running as an executable """
    if hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def fill_pdf(pdf_path, data, additonal_users = None):
    doc = fitz.open(pdf_path)
    data = convert_to_pdf_form_data(data)
    if additonal_users:
        data = add_additional_users(data, additonal_users)
    print(f"pdf data for filling {data}")
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for widget in page.widgets():
            field_name = widget.field_name
            if field_name in data:
                field_value = data[field_name]
                
                if isinstance(field_value, bool):
                    widget.field_value = True
                else:
                    widget.field_value = str(field_value)
                widget.update()

    
    output_dir = os.path.join(get_executable_dir(), 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"Hoja_Padronal_filled_{data['untitled12']}_{data['untitled13']}_{data['untitled2'].replace(' ', '_')}.pdf")
    doc.delete_page(1)
    doc.save(output_path)
    
    print(f"PDF filled and saved to {output_path}")


def add_additional_users(data, additional_users):
    base_pdf_index = 1
    fields_per_user = 23 # Number of fields per additional user
    data['untitled107'] = str(len(additional_users) + 1).replace("(","").replace(",)","")
    

    checked = False
    for user_index, user in enumerate(additional_users):
        if user_index >= 4:
            break  # Ensure we do not add more than 4 users
        current_base_index = base_pdf_index + user_index * fields_per_user
        print(current_base_index)
        print("______________")
        birth_spanish_time_format = str(time.strftime('%d/%m/%Y', time.strptime(user["birth_date"], '%Y-%m-%d')))
        if not checked:
            data['untitled48.field13'] = user['id_number'],
            data['untitled48.field15'] = user['phone'],
            checked = True
        else:
            data[f'field{current_base_index+14}'] = user["phone"]
            data[f'field{current_base_index+12}'] = user["id_number"]

        data[f'field{current_base_index}'] = user["surname"]
        data[f'field{current_base_index+1}'] = user["first_name"]
        data[f'field{current_base_index+2}'] = user["second_name"]
        data[f'field{current_base_index+5}'] = birth_spanish_time_format
        data[f'field{current_base_index+6}'] = user["city_of_birth"]
        data[f'field{current_base_index+7}'] = user["country_of_birth"]
        data[f'field{current_base_index+8}'] = user["nationality"]
        data[f'field{current_base_index+15}'] = user['email']

        data[f'field{current_base_index+13}'] = user["study_level"]
        data[f'field{current_base_index+21}'] = user["prev_province_spain"]
        data[f'field{current_base_index+22}'] = user["prev_country"]

        if user["id_documnet_type"] == "NIE":
            data[f'field{current_base_index+11}'] = True
        elif user["id_documnet_type"] == "DNI":
            data[f'field{current_base_index+9}'] = True
        elif user["id_documnet_type"] == "Passport":
            data[f'field{current_base_index+10}'] = True
        # gender
        if user['gender'] == 'Man':
            data[f'field{current_base_index+3}'] = True
        else:
            data[f'field{current_base_index+4}'] = True
        # case type
        if user['document_case_type'] == 'change residency':
            data[f'field{current_base_index+16}'] = True
        elif user['document_case_type'] == 'omission':
            data[f'field{current_base_index+17}'] = True
        elif user['document_case_type'] == 'birth':
            data[f'field{current_base_index+18}'] = True
        elif user['document_case_type'] == 'change address':
            data[f'field{current_base_index+19}'] = True
        elif user['document_case_type'] == 'change personal data':
            data[f'field{current_base_index+20}'] = True

    return data
