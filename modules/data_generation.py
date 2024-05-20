import random
from faker import Faker

def create_mock_data():
    fake = Faker()
    
    data = {
        'untitled1': fake.random_element(elements=('Street', 'Avenue', 'Boulevard', 'Drive', 'Road')),
        'untitled2': fake.street_name(),                         
        'untitled3': fake.building_number(),                      
        'untitled4': fake.random_element(elements=('A', 'B', 'C', 'D', 'E')), 
        'untitled5': fake.building_number(),                     
        'untitled6': fake.building_number(),                        
        'untitled8': str(random.randint(1, 20)),                    
        'untitled9': str(random.randint(1, 100)),                           
        'untitled12': fake.last_name(),                
        'untitled13': fake.first_name(),           
        'untitled14': fake.first_name(), 
        'untitled15': str(random.randint(0, 1)),  
        'untitled16': str(random.randint(0, 1)),    
        'untitled17': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),  
        'untitled18': fake.city(),  
        'untitled19': fake.country(),    
        'untitled20': fake.country(), 
        'untitled21': str(random.randint(0, 1)), 
        'untitled22': str(random.randint(0, 1)), 
        'untitled23': str(random.randint(0, 1)), 
        'untitled24': fake.ssn(),   
        'untitled25': fake.random_element(elements=('High School', 'Bachelor', 'Master', 'PhD')),                         
        'untitled26': fake.phone_number(),                         
        'untitled27': fake.email(),
        'untitled28': str(random.randint(0, 1)), 
        'untitled29': str(random.randint(0, 1)), 
        'untitled30': str(random.randint(0, 1)), 
        'untitled31': str(random.randint(0, 1)), 
        'untitled32': str(random.randint(0, 1)), 
        'untitled33': fake.state(),                  
        'untitled34': fake.country(),                  
        'untitled105': fake.name(), 
        'untitled106': fake.ssn(), 
        'untitled107': str(random.randint(1, 10)), 
    }
    
    return data

def convert_to_db_schema(data):
    db_data = {
        'street_type': data['untitled1'],
        'street_name': data['untitled2'],
        'building_number': data['untitled3'],
        'building_letter': data['untitled4'],
        'building_portal': data['untitled6'],
        'building_floor': data['untitled8'],
        'building_door_number': data['untitled9'],
        'surname': data['untitled12'],
        'first_name': data['untitled13'],
        'second_name': data['untitled14'],
        'birth_date': data['untitled17'],
        'city_of_birth': data['untitled18'],
        'country_of_birth': data['untitled19'],
        'nationality': data['untitled20'],
        'id_number': data['untitled24'],
        'study_level': data['untitled25'],
        'phone': data['untitled26'],
        'email': data['untitled27'],
        'prev_province_spain': data['untitled33'],
        'prev_country': data['untitled34'],
        'landlord_name': data['untitled105'],
        'landlord_id': data['untitled106'],
        'people_sum_involved': int(data['untitled107']),
    }

    return db_data
