import fitz  # PyMuPDF

def convert_to_pdf_form_data(db_data):
    mock_data = {
        'untitled1': db_data['street_type'],
        'untitled2': db_data['street_name'],
        'untitled3': db_data['building_number'],
        'untitled4': db_data['building_letter'],
        'untitled5': db_data['building_number'],
        'untitled6': db_data['building_portal'],
        'untitled8': str(db_data['building_floor']),
        'untitled9': str(db_data['building_door_number']),
        'untitled12': db_data['surname'],
        'untitled13': db_data['first_name'],
        'untitled14': db_data['second_name'],
        'untitled15': bool(int(db_data['click_man'])),
        'untitled16': bool(int(db_data['click_woman'])),
        'untitled17': db_data['birth_date'],
        'untitled18': db_data['city_of_birth'],
        'untitled19': db_data['country_of_birth'],
        'untitled20': db_data['nationality'],
        'untitled21': bool(int(db_data['click_id_dni'])),
        'untitled22': bool(int(db_data['click_id_passport'])),
        'untitled23': bool(int(db_data['click_id_nie'])),
        'untitled24': db_data['id_number'],
        'untitled25': db_data['study_level'],
        'untitled26': db_data['phone'],
        'untitled27': db_data['email'],
        'untitled28': bool(int(db_data['click_change_residency'])),
        'untitled29': bool(int(db_data['click_omission'])),
        'untitled30': bool(int(db_data['click_birth'])),
        'untitled31': bool(int(db_data['click_change_address'])),
        'untitled32': bool(int(db_data['click_change_pers_data'])),
        'untitled33': db_data['prev_province_spain'],
        'untitled34': db_data['prev_country'],
        'untitled105': db_data['landlord_name'],
        'untitled106': db_data['landlord_id'],
        'untitled107': str(db_data['people_sum_involved']),
        'untitled108': db_data['other_info']
    }
    return mock_data

def fill_pdf(pdf_path, data):
    doc = fitz.open(pdf_path)
    data = convert_to_pdf_form_data(data)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for widget in page.widgets():
            field_name = widget.field_name
            if field_name in data:
                widget.field_value = data[field_name]
                widget.update()
                
    output_path = f"Hoja_Padronal_filled_{data['untitled12']}_{data['untitled13']}_{data['untitled2'].replace(' ', '_')}.pdf"
    doc.save(output_path)
    print(f"PDF filled and saved to {output_path}")
