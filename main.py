import json
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from modules.supabase_client import fetch_data, update_data, insert_data, remove_data
from modules.pdf_filler import fill_pdf, get_executable_dir
import os
import sys
from tkinter.font import Font

# Global variables
users = []
selected_users = []

# Define the enum values
enum_values = {
    "gender": ["Man", "Woman"],
    "id_documnet_type": ["NIE", "DNI", "Passport"],
    "document_case_type": ["change residency", "omission", "birth", "change address", "change personal data"]
}

def get_resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def generate_pdf():
    if selected_users:
        user_data = selected_users[0]
        if len(selected_users) > 1:
            del selected_users[0]
            additional = selected_users
        else:
            additional = None 
    else:
        additional = None
        selected_user = user_combobox.get()
        if not selected_user:
            messagebox.showerror("Error", "No user selected.")
            return
        selected_email = selected_user.split(' - ')[-1]
        user_data = next((user for user in users if user["email"] == selected_email), None)
        if not user_data:
            messagebox.showerror("Error", "Selected user not found.")
            return

    try:
        print(f"Additional {additional}")
        pdf_path = get_resource_path(os.path.join("pdf", "Hoja_Padronal_Renamed.pdf"))  # Update with actual PDF path
        fill_pdf(pdf_path, user_data, additional)
        messagebox.showinfo("Success", f"PDF generated successfully for {user_data}.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate PDF: {e}")

def fetch_users():
    global users
    try:
        db_data = fetch_data()
        users = db_data.get("data", [])
        update_combobox(users)
        update_listbox(users)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch users: {e}")

def fetch_users_thread():
    Thread(target=fetch_users).start()

def update_combobox(users):
    user_details = [f'{user["surname"]} {user["first_name"]} - {user["email"]}' for user in users]
    user_combobox['values'] = user_details

def search_users(event):
    query = search_entry.get().lower()
    filtered_users = [user for user in users if query in user["email"].lower() or query in user["surname"].lower() or query in user["first_name"].lower()]
    update_listbox(filtered_users)

def update_listbox(filtered_users):
    search_results_listbox.delete(0, tk.END)
    for user in filtered_users:
        search_results_listbox.insert(tk.END, f'{user["surname"]} {user["first_name"]} - {user["email"]}')

def select_user(event):
    if not search_results_listbox.curselection():
        return
    selected_text = search_results_listbox.get(search_results_listbox.curselection())
    selected_email = selected_text.split(' - ')[-1]
    user_combobox.set(selected_text)
    for user in users:
        if user["email"] == selected_email:
            populate_fields(user)
            break

def populate_fields(user):
    for key, entry in input_entries.items():
        value = user.get(key, "")
        if value is None:
            value = ""
        if isinstance(entry, ttk.Combobox):
            entry.set(value)
        else:
            entry.delete(0, tk.END)
            entry.insert(0, str(value))  # Ensure the value is a string


def update_user():
    selected_user = user_combobox.get().split(' - ')[-1]
    if not selected_user:
        messagebox.showerror("Error", "No user selected.")
        return
    
    selected_user_data = next((user for user in users if user["email"] == selected_user), None)
    if not selected_user_data:
        messagebox.showerror("Error", "User not found.")
        return
    
    updated_data = {key: entry.get() for key, entry in input_entries.items()}
    try:
        update_data(selected_user_data, updated_data)
        messagebox.showinfo("Success", "User data updated successfully.")
        fetch_users_thread()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update user: {e}")

def sync_selection(event):
    selected_text = user_combobox.get()
    selected_email = selected_text.split(' - ')[-1]
    for idx, user in enumerate(users):
        if user["email"] == selected_email:
            search_results_listbox.selection_clear(0, tk.END)
            search_results_listbox.selection_set(idx)
            populate_fields(user)
            break

def add_new_user():
    new_user_data = {key: entry.get() for key, entry in input_entries.items()}
    if not new_user_data["email"]:
        messagebox.showerror("Error", "Email is required to add a new user.")
        return
    
    try:
        insert_data(new_user_data)
        messagebox.showinfo("Success", "New user added successfully.")
        fetch_users_thread()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add new user: {e}")

def add_user_to_list():
    selected_text = user_combobox.get()
    selected_email = selected_text.split(' - ')[-1]
    if not selected_email:
        messagebox.showerror("Error", "No user selected.")
        return
    if len(selected_users) >= 4:
        messagebox.showerror("Error", "Maximum of 4 users can be added.")
        return
    
    user_data = next((user for user in users if user["email"] == selected_email), None)
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
    selected_email = selected_text.split(' - ')[-1]
    
    user_data = next((user for user in selected_users if user["email"] == selected_email), None)
    if user_data:
        selected_users.remove(user_data)
        update_selected_users_listbox()

def update_selected_users_listbox():
    selected_users_listbox.delete(0, tk.END)
    for user in selected_users:
        selected_users_listbox.insert(tk.END, f'{user["surname"]} {user["first_name"]} - {user["email"]}')

def remove_user():
    selected_user = user_combobox.get().split(' - ')[-1]
    if not selected_user:
        messagebox.showerror("Error", "No user selected.")
        return
    
    selected_user_data = next((user for user in users if user["email"] == selected_user), None)
    if not selected_user_data:
        messagebox.showerror("Error", "User not found.")
        return
    
    try:
        remove_data(selected_user_data['id'])
        messagebox.showinfo("Success", "User removed successfully.")
        fetch_users_thread()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove user: {e}")

# Initialize the main window
root = tk.Tk()
root.title("PDF Generator & User Data Updater")
root.geometry("800x800")

# Define custom fonts for icons
icon_font = Font(family='Helvetica', size=12, weight='bold')

# Create and place widgets
ttk.Label(root, text="Select User:").grid(column=0, row=0, padx=10, pady=10, sticky="w")
user_combobox = ttk.Combobox(root, state="readonly")
user_combobox.grid(column=1, row=0, padx=10, pady=10, columnspan=2, sticky="ew")
user_combobox.bind("<<ComboboxSelected>>", sync_selection)

generate_button = ttk.Button(root, text="Generate PDF", command=generate_pdf)
generate_button.grid(column=1, row=1, padx=10, pady=10, sticky="ew")

update_button = ttk.Button(root, text="Update User", command=update_user)
update_button.grid(column=2, row=1, padx=10, pady=10, sticky="ew")

add_button = ttk.Button(root, text="Add New User", command=add_new_user)
add_button.grid(column=0, row=1, padx=10, pady=10, sticky="ew")

ttk.Label(root, text="Search:").grid(column=0, row=2, padx=10, pady=10, sticky="w")
search_entry = ttk.Entry(root)
search_entry.grid(column=1, row=2, padx=10, pady=10, columnspan=2, sticky="ew")
search_entry.bind("<KeyRelease>", search_users)

# Frame for search results and selected users
results_frame = ttk.Frame(root)
results_frame.grid(column=0, row=3, columnspan=3, padx=10, pady=10, sticky="nsew")

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
remove_user_button.grid(column=0, row=2, padx=10, pady=10, sticky="ew")

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
canvas.grid(column=0, row=5, columnspan=3, padx=10, pady=10, sticky="nsew")
scrollbar.grid(column=3, row=5, sticky="ns")

# Create input fields dynamically based on the database keys (excluding 'id')
input_entries = {}
user_sample = fetch_data().get("data", [{}])[0]

row = 0
for key in user_sample.keys():
    if key != 'id':
        ttk.Label(scrollable_frame, text=f"{key}:").grid(column=0, row=row, padx=10, pady=5, sticky=tk.W)
        
        if key in enum_values:
            entry = ttk.Combobox(scrollable_frame, values=enum_values[key], state="readonly")
        else:
            entry = ttk.Entry(scrollable_frame)
        
        entry.grid(column=1, row=row, padx=10, pady=5, sticky="ew")
        input_entries[key] = entry
        row += 1

# Make the grid expand to fill the available space
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(1, weight=1)

# Fetch users data automatically when the application starts
fetch_users_thread()

# Start the main event loop
root.mainloop()
