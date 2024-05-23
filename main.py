import json
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from modules.supabase_client import fetch_data, update_data, insert_data
from modules.pdf_filler import fill_pdf, get_executable_dir
import os
import sys

# Global variables
users = []

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
    selected_user = user_combobox.get()
    if not selected_user:
        messagebox.showerror("Error", "No user selected.")
        return
    
    for user in users:
        if user["email"] == selected_user:
            try:
                pdf_path = get_resource_path(os.path.join("pdf", "Hoja_Padronal - Las Palmas-1.pdf"))  # Update with actual PDF path
                fill_pdf(pdf_path, user)
                messagebox.showinfo("Success", "PDF generated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate PDF: {e}")
            break

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
    user_emails = [user["email"] for user in users]
    user_combobox['values'] = user_emails

def search_users(event):
    query = search_entry.get().lower()
    filtered_users = [user for user in users if query in user["email"].lower()]
    update_listbox(filtered_users)

def update_listbox(filtered_users):
    search_results_listbox.delete(0, tk.END)
    for user in filtered_users:
        search_results_listbox.insert(tk.END, user["email"])

def select_user(event):
    if not search_results_listbox.curselection():
        return
    selected_email = search_results_listbox.get(search_results_listbox.curselection())
    user_combobox.set(selected_email)
    for user in users:
        if user["email"] == selected_email:
            populate_fields(user)
            break

def populate_fields(user):
    for key, entry in input_entries.items():
        if isinstance(entry, ttk.Combobox):
            entry.set(user.get(key, ""))
        else:
            entry.delete(0, tk.END)
            entry.insert(0, user.get(key, ""))

def update_user():
    selected_user = user_combobox.get()
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
    selected_email = user_combobox.get()
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

# Initialize the main window
root = tk.Tk()
root.title("PDF Generator & User Data Updater")
root.geometry("600x700")

# Create and place widgets
ttk.Label(root, text="Select User:").grid(column=0, row=0, padx=10, pady=10, sticky="w")
user_combobox = ttk.Combobox(root, state="readonly")
user_combobox.grid(column=1, row=0, padx=10, pady=10, sticky="ew")
user_combobox.bind("<<ComboboxSelected>>", sync_selection)

generate_button = ttk.Button(root, text="Generate PDF", command=generate_pdf)
generate_button.grid(column=1, row=1, padx=10, pady=10, sticky="ew")

update_button = ttk.Button(root, text="Update User", command=update_user)
update_button.grid(column=2, row=1, padx=10, pady=10, sticky="ew")

add_button = ttk.Button(root, text="Add New User", command=add_new_user)
add_button.grid(column=0, row=1, padx=10, pady=10, sticky="ew")

ttk.Label(root, text="Search:").grid(column=0, row=2, padx=10, pady=10, sticky="w")
search_entry = ttk.Entry(root)
search_entry.grid(column=1, row=2, padx=10, pady=10, sticky="ew")
search_entry.bind("<KeyRelease>", search_users)

search_results_listbox = tk.Listbox(root)
search_results_listbox.grid(column=1, row=3, padx=10, pady=10, columnspan=2, sticky="nsew")
search_results_listbox.bind("<<ListboxSelect>>", select_user)

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
canvas.grid(column=0, row=4, columnspan=3, padx=10, pady=10, sticky="nsew")
scrollbar.grid(column=3, row=4, sticky="ns")

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
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(1, weight=1)

# Fetch users data automatically when the application starts
fetch_users_thread()

# Start the main event loop
root.mainloop()
