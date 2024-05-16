import tkinter as tk
from tkinter import ttk, messagebox
from modules.supabase_client import fetch_data
from modules.pdf_filler import fill_pdf

def generate_pdf():
    selected_user = user_combobox.get()
    if not selected_user:
        messagebox.showerror("Error", "No user selected.")
        return
    
    for user in users:
        if user["email"] == selected_user:
            pdf_path = "/Users/botondberde/pdf_filler_GC_Jonna/Hoja_Padronal - Las Palmas-1.pdf"  # Update with actual PDF path
            fill_pdf(pdf_path, user)
            messagebox.showinfo("Success", "PDF generated successfully.")
            break

def fetch_users():
    global users
    db_data = fetch_data()
    users = db_data.get("data", [])
    update_combobox(users)

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
    selected_email = search_results_listbox.get(search_results_listbox.curselection())
    user_combobox.set(selected_email)

# Initialize the main window
root = tk.Tk()
root.title("PDF Generator")

# Create and place widgets
ttk.Label(root, text="Select User:").grid(column=0, row=0, padx=10, pady=10)
user_combobox = ttk.Combobox(root, state="readonly")
user_combobox.grid(column=1, row=0, padx=10, pady=10)

fetch_button = ttk.Button(root, text="Fetch Users", command=fetch_users)
fetch_button.grid(column=2, row=0, padx=10, pady=10)

generate_button = ttk.Button(root, text="Generate PDF", command=generate_pdf)
generate_button.grid(column=1, row=3, padx=10, pady=10)

ttk.Label(root, text="Search:").grid(column=0, row=1, padx=10, pady=10)
search_entry = ttk.Entry(root)
search_entry.grid(column=1, row=1, padx=10, pady=10)
search_entry.bind("<KeyRelease>", search_users)

search_results_listbox = tk.Listbox(root)
search_results_listbox.grid(column=1, row=2, padx=10, pady=10, columnspan=2)
search_results_listbox.bind("<<ListboxSelect>>", select_user)

# Fetch users data automatically when the application starts
fetch_users()

# Start the main event loop
root.mainloop()
