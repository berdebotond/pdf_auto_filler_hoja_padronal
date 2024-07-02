import json
import tkinter as tk
import traceback
from tkinter import ttk, messagebox
from threading import Thread
from modules.supabase_client import update_data, fetch_data_nie_tie_initial, insert_data, remove_user_from_db, \
    fetch_empadron_data, insert_empadron_data, merge_empadron_data_with_tie_nie
from modules.pdf_filler import fill_pdf, get_executable_dir
import os
import sys
from tkinter.font import Font
from modules.utils import get_resource_path, load_pdfs

# Global variables
users = []
selected_users = []

# Define the enum values
enum_values = {
    "gender": ["Man", "Woman"],
    "id_documnet_type": ["NIE", "DNI", "Passport"],
    "document_case_type": ["change residency", "omission", "birth", "change address", "change personal data"]
}


def generate_pdf():
    if selected_users:
        user_data = selected_users[0]
        additional = selected_users[1:] if len(selected_users) > 1 else None
    else:
        selected_user = user_combobox.get()
        if not selected_user:
            messagebox.showerror("Error", "No user selected.")
            return

        selected_id = selected_user.split(' - ')[-1]
        user_data = next(
            (user for user in users if f"{user['surname']} {user['name']} - {user['id']}" == selected_user),
            None)

        if not user_data:
            messagebox.showerror("Error", "Selected user not found.")
            return
        if "first_name_1" in user_data.keys():
            additional = user_data
        else:
            additional = None
    print("0----------------------")
    print(user_data)
    pdf_name = pdf_combobox.get()
    if not pdf_name:
        messagebox.showerror("Error", "No PDF file selected.")
        return
    print(additional)
    pdf_path = get_resource_path(os.path.join("pdf", pdf_name))

    try:
        fill_pdf(pdf_path, user_data, additional)
        messagebox.showinfo("Success",
                            f"PDF generated successfully for {user_data['surname']} {user_data['name']}.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate PDF: {traceback.format_exc(e)}")


nie_tie_fields = ["name", "surname", "city_of_birth", "country_of_birth", "family_status", "gender",
                  "full_name_of_father", "full_name_of_mother", "spain_address", "house_name", "apt_number", "city",
                  "zip_code", "province", "legal_representative_name", "legal_representative_id",
                  "legal_representative_relation", "consent_communication_electronically", "apply_digital_certificate",
                  "no_consent_data_consultation", "comments", "birth_date", "nationality", "additional_nationality",
                  "passport_number", "id_number", "nie", "mobile_phone", "email", "desired_service",
                  "not_available_appointments", "appointment_deadline", "appointment_location", "referral_source"]

empadron_fields = [
    "id", "street_name", "type", "zip_code", "municipality", "number", "letter", "block", "gate", "stairs", "floor",
    "door", "voluntary_statement", "inhabitants_not_removed", "rent_contract", "landlord_name", "landlord_id_dni_nie",
    "first_name_1", "surname_1", "nie_1", "gender_1", "city_of_birth_1", "country_of_birth_1", "highest_education_1",
    "moved_spain_from_other_country_1", "birth_newborns_1", "moved_within_spain_1", "change_personal_data_1",
    "vote_municipal_level_1", "change_europe_voting_right_1", "first_name_2", "surname_2", "nie_2", "gender_2",
    "city_of_birth_2", "country_of_birth_2", "highest_education_2", "moved_spain_from_other_country_2",
    "birth_newborns_2", "moved_within_spain_2", "change_personal_data_2", "vote_municipal_level_2",
    "change_europe_voting_right_2", "first_name_3", "surname_3", "nie_3", "gender_3", "city_of_birth_3",
    "country_of_birth_3", "highest_education_3", "moved_spain_from_other_country_3", "birth_newborns_3",
    "moved_within_spain_3", "change_personal_data_3", "vote_municipal_level_3", "change_europe_voting_right_3",
    "first_name_4", "surname_4", "nie_4", "gender_4", "city_of_birth_4", "country_of_birth_4", "highest_education_4",
    "moved_spain_from_other_country_4", "birth_newborns_4", "moved_within_spain_4", "change_personal_data_4",
    "vote_municipal_level_4", "change_europe_voting_right_4", "first_name_5", "surname_5", "nie_5", "gender_5",
    "city_of_birth_5", "country_of_birth_5", "highest_education_5", "moved_spain_from_other_country_5",
    "birth_newborns_5", "moved_within_spain_5", "change_personal_data_5", "vote_municipal_level_5",
    "change_europe_voting_right_5", "street_type", "landlord_type"
]


def fetch_users():
    global users
    try:
        db_data = fetch_data_nie_tie_initial()
        empadronamiento_data = fetch_empadron_data()
        empadronamiento_data = merge_empadron_data_with_tie_nie(db_data, empadronamiento_data)
        print(empadronamiento_data)
        for data in db_data:
            data["user_type"] = "nie_tie"
        users = db_data
        empadron_data = []
        for data in empadronamiento_data:
            data["surname"] = "Empadronamiento " + data["surname_1"]
            data["name"] = data["first_name_1"]
            data["user_type"] = "empadron"
            empadron_data.append(data)

        users.extend(empadron_data)
        update_combobox(users)
        update_listbox(users)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch users: {e}")


def fetch_users_thread():
    Thread(target=fetch_users).start()


def update_combobox(users):
    user_details = [f'{user["surname"]} {user["name"]} - {user["id"]}' for user in users]
    user_combobox['values'] = user_details


def search_users(event):
    query = search_entry.get().lower()
    filtered_users = [user for user in users if
                      query in (user.get("email", "").lower() or query in user.get("surname",
                                                                                   "").lower() or query in user.get(
                          "name", "").lower())]
    update_listbox(filtered_users)


def update_listbox(filtered_users):
    search_results_listbox.delete(0, tk.END)
    for user in filtered_users:
        search_results_listbox.insert(tk.END, f'{user["surname"]} {user["name"]} - {user["id"]}')


def select_user(event):
    if not search_results_listbox.curselection():
        return
    selected_text = search_results_listbox.get(search_results_listbox.curselection())
    selected_id = selected_text.split(' - ')[-1]
    user_combobox.set(selected_text)


def update_user():
    selected_user = user_combobox.get()
    if not selected_user:
        messagebox.showerror("Error", "No user selected.")
        return

    selected_user_data = next(
        (user for user in users if f'{user["surname"]} {user["name"]} - {user["id"]}' == selected_user), None)
    if not selected_user_data:
        messagebox.showerror("Error", "User not found.")
        return
    open_update_popup(selected_user_data)


def sync_selection(event):
    selected_text = user_combobox.get()
    selected_id = selected_text.split(' - ')[-1]
    for idx, user in enumerate(users):
        if str(user["id"]) == selected_id:
            search_results_listbox.selection_clear(0, tk.END)
            search_results_listbox.selection_set(idx)
            break


def add_user_to_list():
    selected_text = user_combobox.get()
    selected_id = selected_text.split(' - ')[-1]
    if not selected_id:
        messagebox.showerror("Error", "No user selected.")
        return
    if len(selected_users) >= 4:
        messagebox.showerror("Error", "Maximum of 4 users can be added.")
        return

    user_data = next((user for user in users if str(user["id"]) == selected_id), None)
    if not user_data:
        messagebox.showerror("Error", "Selected user not found.")
        return

    if user_data in selected_users:
        messagebox.showinfo("Info", "User is already in the list.")
        return

    selected_users.append(user_data)
    update_selected_users_listbox()


def remove_user_from_list():
    if not selected_users_listbox.curselection():
        return
    selected_text = selected_users_listbox.get(selected_users_listbox.curselection())
    selected_id = selected_text.split(' - ')[-1]

    user_data = next((user for user in selected_users if str(user["id"]) == selected_id), None)
    if user_data:
        selected_users.remove(user_data)
        update_selected_users_listbox()


def update_selected_users_listbox():
    selected_users_listbox.delete(0, tk.END)
    for user in selected_users:
        selected_users_listbox.insert(tk.END, f'{user["surname"]} {user["name"]}')


def remove_user():
    selected_user = user_combobox.get().split(' - ')[-1]
    if not selected_user:
        messagebox.showerror("Error", "No user selected.")
        return

    selected_user_data = next((user for user in users if str(user["id"]) == selected_user), None)
    if not selected_user_data:
        messagebox.showerror("Error", "User not found.")
        return

    try:
        remove_user_from_db(selected_user_data['id'])
        messagebox.showinfo("Success", "User removed successfully.")
        fetch_users_thread()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove user: {e}")


def open_update_popup(user):
    user_type = user.get("user_type", "nie_tie")
    print(user)
    if user_type == "nie_tie":
        create_nie_tie_popup(user)
    elif user_type == "empadron":
        create_empadron_popup(user)


def create_nie_tie_popup(user):
    popup = tk.Toplevel(root)
    popup.title("Update NIE/TIE User")
    popup.geometry("600x600")

    canvas = tk.Canvas(popup)
    scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    popup_entries = {}
    row = 0
    for key in nie_tie_fields:
        ttk.Label(scrollable_frame, text=f"{key}:").grid(column=0, row=row, padx=10, pady=5, sticky=tk.W)
        if key in enum_values:
            entry = ttk.Combobox(scrollable_frame, values=enum_values[key], state="readonly")
        else:
            entry = ttk.Entry(scrollable_frame)
        entry.grid(column=1, row=row, padx=10, pady=5, sticky="ew")
        entry.insert(0, str(user.get(key, "")))
        popup_entries[key] = entry
        row += 1

    def save_nie_tie():
        updated_data = {key: entry.get() for key, entry in popup_entries.items()}
        update_user_data(user, updated_data)
        fetch_users_thread()
        popup.destroy()

    ttk.Button(scrollable_frame, text="Save", command=save_nie_tie).grid(column=0, row=row, padx=10, pady=10,
                                                                         columnspan=2)


def create_empadron_popup(user):
    popup = tk.Toplevel(root)
    popup.title("Update Empadron User")
    popup.geometry("600x600")

    canvas = tk.Canvas(popup)
    scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    popup_entries = {}
    row = 0
    for key in empadron_fields:
        ttk.Label(scrollable_frame, text=f"{key}:").grid(column=0, row=row, padx=10, pady=5, sticky=tk.W)
        if key in enum_values:
            entry = ttk.Combobox(scrollable_frame, values=enum_values[key], state="readonly")
        else:
            entry = ttk.Entry(scrollable_frame)
        entry.grid(column=1, row=row, padx=10, pady=5, sticky="ew")
        entry.insert(0, str(user.get(key, "")))
        popup_entries[key] = entry
        row += 1

    def save_empadron():
        updated_data = {key: entry.get() for key, entry in popup_entries.items()}
        insert_empadron_data(updated_data)
        fetch_users_thread()

        popup.destroy()

    ttk.Button(scrollable_frame, text="Save", command=save_empadron).grid(column=0, row=row, padx=10, pady=10,
                                                                          columnspan=2)


def update_user_data(user, updated_data):
    try:
        update_data(user['id'], updated_data)
        messagebox.showinfo("Success", "User data updated successfully.")
        fetch_users_thread()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update user: {e}")


def open_add_user_popup(user_type):
    popup = tk.Toplevel(root)
    popup.title(f"Add New {user_type.upper()} User")
    popup.geometry("600x600")

    canvas = tk.Canvas(popup)
    scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    if user_type == "nie_tie":
        fields = nie_tie_fields
        insert_function = insert_data
    else:
        fields = empadron_fields
        insert_function = insert_empadron_data

    popup_entries = {}
    row = 0
    for key in fields:
        ttk.Label(scrollable_frame, text=f"{key}:").grid(column=0, row=row, padx=10, pady=5, sticky=tk.W)
        if key in enum_values:
            entry = ttk.Combobox(scrollable_frame, values=enum_values[key], state="readonly")
        else:
            entry = ttk.Entry(scrollable_frame)
        entry.grid(column=1, row=row, padx=10, pady=5, sticky="ew")
        popup_entries[key] = entry
        row += 1

    def save_new_user():
        new_user_data = {key: entry.get() for key, entry in popup_entries.items()}
        try:
            insert_function(new_user_data)
            messagebox.showinfo("Success", f"New {user_type.upper()} user added successfully.")
            fetch_users_thread()
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add new {user_type.upper()} user: {e}")

    ttk.Button(scrollable_frame, text="Save", command=save_new_user).grid(column=0, row=row, padx=10, pady=10,
                                                                          columnspan=2)



# Initialize the main window
root = tk.Tk()
root.title("PDF Generator & User Data Updater")
root.geometry("1000x800")

# Define custom fonts for icons
icon_font = Font(family='Helvetica', size=12, weight='bold')

# Create and place widgets
ttk.Label(root, text="Select User:").grid(column=0, row=0, padx=10, pady=10, sticky="w")
user_combobox = ttk.Combobox(root, state="readonly")
user_combobox.grid(column=1, row=0, padx=10, pady=10, columnspan=2, sticky="ew")
user_combobox.bind("<<ComboboxSelected>>", sync_selection)

ttk.Label(root, text="Select PDF File:").grid(column=0, row=1, padx=10, pady=10, sticky="w")
pdf_combobox = ttk.Combobox(root, state="readonly")
pdf_combobox.grid(column=1, row=1, padx=10, pady=10, columnspan=2, sticky="ew")
pdf_combobox['values'] = load_pdfs()

generate_button = ttk.Button(root, text="Generate PDF", command=generate_pdf)
generate_button.grid(column=1, row=2, padx=10, pady=10, sticky="ew")

update_button = ttk.Button(root, text="Update User", command=update_user)
update_button.grid(column=2, row=2, padx=10, pady=10, sticky="ew")

add_nie_tie_button = ttk.Button(root, text="Add NIE/TIE User", command=lambda: open_add_user_popup("nie_tie"))
add_nie_tie_button.grid(column=0, row=2, padx=10, pady=10, sticky="ew")

add_empadron_button = ttk.Button(root, text="Add Empadron Data", command=lambda: open_add_user_popup("empadron"))
add_empadron_button.grid(column=1, row=3, padx=10, pady=10, sticky="ew")

ttk.Label(root, text="Search:").grid(column=0, row=4, padx=10, pady=10, sticky="w")
search_entry = ttk.Entry(root)
search_entry.grid(column=1, row=4, padx=10, pady=10, columnspan=2, sticky="ew")
search_entry.bind("<KeyRelease>", search_users)

# Frame for search results and selected users
results_frame = ttk.Frame(root)
results_frame.grid(column=0, row=5, columnspan=3, padx=10, pady=10, sticky="nsew")

search_results_listbox = tk.Listbox(results_frame, height=10, width=80)
search_results_listbox.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")
search_results_listbox.bind("<<ListboxSelect>>", select_user)

# Selected users section
ttk.Label(results_frame, text="Selected users for generation:").grid(column=0, row=1, padx=10, pady=10, sticky="w")

selected_users_frame = ttk.Frame(results_frame)
selected_users_frame.grid(column=0, row=2, padx=10, pady=10, sticky="ew")

selected_users_listbox = tk.Listbox(selected_users_frame, height=4, width=80)
selected_users_listbox.grid(column=0, row=0, columnspan=2, padx=10, pady=10, sticky="nsew")

add_to_list_button = ttk.Button(selected_users_frame, text="+", command=add_user_to_list, width=2)
add_to_list_button.grid(column=0, row=1, padx=10, pady=10, sticky="ew")

remove_from_list_button = ttk.Button(selected_users_frame, text="-", command=remove_user_from_list, width=2)
remove_from_list_button.grid(column=1, row=1, padx=10, pady=10, sticky="ew")

remove_user_button = ttk.Button(root, text="Remove User", command=remove_user)
remove_user_button.grid(column=0, row=3, padx=10, pady=10, sticky="ew")

# Create a canvas and a scrollbar for the input fields
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Add mouse scrolling functionality
def _on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

# Place the canvas and scrollbar on the main window
canvas.grid(column=0, row=6, columnspan=3, padx=10, pady=10, sticky="nsew")
scrollbar.grid(column=3, row=6, sticky="ns")

# Make the grid expand to fill the available space
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(1, weight=1)

# Fetch users data automatically when the application starts
fetch_users_thread()

# Start the main event loop
root.mainloop()

