import tkinter as tk
from tkinter import ttk, messagebox
import json

FILE = "students.json"
PASSWORD = "admin123"

# ---------------- FILE FUNCTIONS ----------------

def load_students():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_students():
    with open(FILE, "w") as f:
        json.dump(students, f, indent=4)

# ---------------- LOGIN ----------------

def check_login():
    if password_entry.get() == PASSWORD:
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Error", "Wrong Password")

# ---------------- MAIN WINDOW ----------------

def open_main_window():

    global roll_entry, name_entry, marks_entry, tree

    root = tk.Tk()
    root.title("Student Management System")
    root.geometry("700x450")

    # Labels
    tk.Label(root, text="Roll").grid(row=0, column=0)
    tk.Label(root, text="Name").grid(row=0, column=1)
    tk.Label(root, text="Marks").grid(row=0, column=2)

    # Entries
    roll_entry = tk.Entry(root)
    roll_entry.grid(row=1, column=0)

    name_entry = tk.Entry(root)
    name_entry.grid(row=1, column=1)

    marks_entry = tk.Entry(root)
    marks_entry.grid(row=1, column=2)

    # Buttons
    tk.Button(root, text="Add Student", command=add_student).grid(row=1, column=3)
    tk.Button(root, text="Delete Student", command=delete_student).grid(row=1, column=4)
    tk.Button(root, text="Search", command=search_student).grid(row=1, column=5)

    # Table
    columns = ("Roll", "Name", "Marks")

    tree = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)

    tree.grid(row=2, column=0, columnspan=6, pady=20)

    load_table()

    root.mainloop()

# ---------------- FUNCTIONS ----------------

def add_student():

    roll = roll_entry.get()
    name = name_entry.get()
    marks = marks_entry.get()

    if roll == "" or name == "" or marks == "":
        messagebox.showerror("Error", "Fill all fields")
        return

    students.append({"roll": roll, "name": name, "marks": marks})

    save_students()

    tree.insert("", tk.END, values=(roll, name, marks))

    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

def delete_student():

    selected = tree.selection()

    if not selected:
        messagebox.showerror("Error", "Select student")
        return

    item = tree.item(selected)
    roll = item["values"][0]

    for s in students:
        if s["roll"] == roll:
            students.remove(s)

    save_students()

    tree.delete(selected)

def search_student():

    roll = roll_entry.get()

    for row in tree.get_children():
        tree.delete(row)

    for s in students:
        if s["roll"] == roll:
            tree.insert("", tk.END, values=(s["roll"], s["name"], s["marks"]))

def load_table():

    for s in students:
        tree.insert("", tk.END, values=(s["roll"], s["name"], s["marks"]))

# ---------------- LOGIN WINDOW ----------------

students = load_students()

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x150")

tk.Label(login_window, text="Admin Password").pack(pady=10)

password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Login", command=check_login).pack(pady=10)

login_window.mainloop()