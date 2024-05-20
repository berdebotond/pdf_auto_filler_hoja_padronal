import json
import os
from supabase import create_client, Client

url: str = os.environ.get(key="SUPABASE_URL", default="https://hetrvidiwvkrxaqeozgc.supabase.co")
key: str = os.environ.get(key="SUPABASE_KEY", default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhldHJ2aWRpd3ZrcnhhcWVvemdjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTM1NTE5NTUsImV4cCI6MjAyOTEyNzk1NX0.dpUKNQ65qsZaiRlrKoj9jiWhvdzhuFFxBP1ENGd_jGs")


supabase_client: Client = create_client(url, key)

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
