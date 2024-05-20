import time
import fitz  # PyMuPDF

def convert_to_pdf_form_data(db_data):
    birtd_date = db_data['birth_date']
    birtd_spanish_time_fomrat = str(time.strftime('%d/%m/%Y', time.strptime(birtd_date, '%Y-%m-%d')))
    pdf_data_for_filling = {
        'untitled1': db_data['street_type'],
        'untitled2': db_data['street_name'],
        'untitled3': db_data['building_number'],
        'untitled4': db_data['building_letter'],
        'untitled5': db_data['building_number'],
        'untitled6': db_data['building_portal'],
        
        'untitled8': str(db_data['building_floor']),
        'untitled9': str(db_data['building_door_number']),
        'untitled10': True,
        'untitled12': db_data['surname'],
        'untitled13': db_data['first_name'],
        'untitled14': db_data['second_name'],
        'untitled17': birtd_spanish_time_fomrat,
        'untitled18': db_data['city_of_birth'],
        'untitled19': db_data['country_of_birth'],
        'untitled20': db_data['nationality'],
        'untitled24': db_data['id_number'],
        'untitled25': db_data['study_level'],
        'untitled26': db_data['phone'],
        'untitled27': db_data['email'],
        'untitled33': db_data['prev_province_spain'],
        'untitled34': db_data['prev_country'],
        'untitled105': db_data['landlord_name'],
        'untitled106': db_data['landlord_id'],
        'untitled107': str(db_data['people_sum_involved']),
    }
    # id type
    if db_data["id_documnet_type"] == "NIE":
        pdf_data_for_filling['untitled23'] = True
    elif db_data["id_documnet_type"] == "DNI":
        pdf_data_for_filling['untitled21'] = True
    elif db_data["id_documnet_type"] == "Passport":
        pdf_data_for_filling['untitled22'] = True
    # gender
    print(db_data['gender'])
    if db_data['gender'] == 'Man':
        pdf_data_for_filling['untitled15'] = True
    else:
        pdf_data_for_filling['untitled16'] = True
    # case type
    if db_data['document_case_type'] == 'change residency':
        pdf_data_for_filling['untitled28'] = True
    elif db_data['document_case_type'] == 'omission':
        pdf_data_for_filling['untitled29'] = True
    elif db_data['document_case_type'] == 'birth':
        pdf_data_for_filling['untitled30'] = True
    elif db_data['document_case_type'] == 'change address':
        pdf_data_for_filling['untitled31'] = True
    elif db_data['document_case_type'] == 'change personal data':
        pdf_data_for_filling['untitled32'] = True
    
    print(pdf_data_for_filling)
    return pdf_data_for_filling

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
            else:
                print(f"Field {field_name} not found in PDF form.")
                               
    output_path = f"Hoja_Padronal_filled_{data['untitled12']}_{data['untitled13']}_{data['untitled2'].replace(' ', '_')}.pdf"
    doc.delete_page(1)
    doc.save(output_path)
    
    print(f"PDF filled and saved to {output_path}")
