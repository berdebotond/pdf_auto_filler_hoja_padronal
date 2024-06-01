import pytest
from modules.supabase_client import fetch_data, update_data, insert_data
from modules.pdf_filler import fill_pdf, get_executable_dir
import os
import json

@pytest.fixture(scope="module")
def supabase_data():
    return fetch_data()

def test_fetch_data(supabase_data):
    assert isinstance(supabase_data, dict)
    assert "data" in supabase_data

def test_update_data(supabase_data):
    if not supabase_data["data"]:
        pytest.skip("No data available to update")
    
    user = supabase_data["data"][0]
    updated_data = user.copy()
    updated_data["first_name"] = "UpdatedName"
    
    update_data(user, updated_data)

    # Verify the update
    refreshed_data = fetch_data()
    updated_user = next((u for u in refreshed_data["data"] if u["id"] == user["id"]), None)
    assert updated_user["first_name"] == "UpdatedName"

def test_insert_data():
    new_user = {
        "email": "testuser@example.com",
        "first_name": "Test",
        "surname": "User",
        "gender": "Man",
        "id_documnet_type": "Passport",
        "document_case_type": "birth"
    }
    
    response = insert_data(new_user)
    
    # Verify the insert
    inserted_data = fetch_data()
    inserted_user = next((u for u in inserted_data["data"] if u["email"] == new_user["email"]), None)
    assert inserted_user is not None

def test_fill_pdf():
    user_data = {
        "email": "testuser@example.com",
        "first_name": "Test",
        "surname": "User",
        "gender": "Man",
        "id_documnet_type": "Passport",
        "document_case_type": "birth",
        "street_name": "temp"
    }
    
    pdf_template_path = os.path.join("pdf", "Hoja_Padronal_Renamed.pdf")
    output_pdf_path = os.path.join("modules/output","Hoja_Padronal_filled_User_Test_temp.pdf")

    
    fill_pdf(pdf_template_path, user_data)
    
    assert os.path.exists(output_pdf_path)
    
    # Clean up
    os.remove(output_pdf_path)
