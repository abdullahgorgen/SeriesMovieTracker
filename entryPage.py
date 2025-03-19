from customtkinter import *
import json
import subprocess
import customtkinter as ctk

# File where user data will be stored
FILE_NAME = "user_data.json"

# Loads user data from the JSON file
def load_users():
    try:
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Saves user data to the JSON file
def save_users(users):
    with open(FILE_NAME, 'w') as file:
        json.dump(users, file, indent=4)

# Displays a popup window
def show_popup(message, color):
    popup = ctk.CTkToplevel() 
    popup.title("Info") 
    popup.geometry("300x150") 
    popup.resizable(False, False)
    popup.configure(fg_color="#242424") 
    
    textColor = color
    label = ctk.CTkLabel(popup, text=message, text_color=textColor, font=("Arial", 14))
    label.pack(pady=(30, 10)) 

    button = ctk.CTkButton(popup, text="OK", command=popup.destroy,
                           fg_color="#3e9e5f", hover_color="#3e9e5f",
                           text_color="white", font=("Arial", 12))
    button.pack(pady=(10, 20))
    popup.attributes("-topmost", True)

# Registration screen
def register():
    def register_user():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            show_popup("Fill in all fields!", "red")
            return

        users = load_users()

        if username in users:
            show_popup("User already exists!", "red")
        else:
            users[username] = password
            save_users(users)
            
            show_popup("Registration successful!", "green")
            show_login_screen()

    def cancel_registration():
        show_login_screen()

    for widget in main_frame.winfo_children():
        widget.destroy()

    login_label = CTkLabel(main_frame, text="Register", font=("Arial", 24, "bold"))
    login_label.grid(row=0, column=0, columnspan=2, pady=30)

    username_label = CTkLabel(main_frame, text="Username:", font=("Helvetica", 14, "bold"))
    username_label.grid(row=1, column=0, padx=20, pady=15, sticky="e")
    username_entry = CTkEntry(main_frame, font=("Arial", 14), width=250)
    username_entry.grid(row=1, column=1, padx=20, pady=15, sticky="w")

    password_label = CTkLabel(main_frame, text="Password:", font=("Helvetica", 14, "bold"))
    password_label.grid(row=2, column=0, padx=20, pady=15, sticky="e")
    password_entry = CTkEntry(main_frame, font=("Arial", 14), show="*", width=250)
    password_entry.grid(row=2, column=1, padx=20, pady=15, sticky="w")

    CTkButton(main_frame, text="Sign Up", font=("Arial", 14), command=register_user).grid(row=3, column=0, columnspan=2, pady=20)
    CTkButton(main_frame, text="Cancel", font=("Arial", 14), command=cancel_registration).grid(row=4, column=0, columnspan=2, pady=10)

# Performs login
def login(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()

    users = load_users()

    if username in users and users[username] == password:
        show_popup("Login successful!", "green")
        root.destroy()
        subprocess.run(["python", "mainPage.py"])  # Opens main page
    else:
        show_popup("Incorrect username or password!", "red")

# Creates the login screen
def show_login_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

    login_label = CTkLabel(main_frame, text="Login", font=("Arial", 24, "bold"))
    login_label.grid(row=0, column=0, columnspan=2, pady=30)

    username_label = CTkLabel(main_frame, text="Username:", font=("Helvetica", 14, "bold"))
    username_label.grid(row=1, column=0, padx=20, pady=15, sticky="e")
    username_entry = CTkEntry(main_frame, font=("Arial", 14), width=250)
    username_entry.grid(row=1, column=1, padx=20, pady=15, sticky="w")

    password_label = CTkLabel(main_frame, text="Password:", font=("Helvetica", 14, "bold"))
    password_label.grid(row=2, column=0, padx=20, pady=15, sticky="e")
    password_entry = CTkEntry(main_frame, font=("Arial", 14), show="*", width=250)
    password_entry.grid(row=2, column=1, padx=20, pady=15, sticky="w")

    CTkButton(main_frame, text="Login", font=("Arial", 14), command=lambda: login(username_entry, password_entry)).grid(row=3, column=0, columnspan=2, pady=20)
    CTkButton(main_frame, text="Sign Up", font=("Arial", 14), command=register).grid(row=4, column=0, columnspan=2, pady=10)

root = CTk()
root.title("Login")
root.geometry("800x500") 

main_frame = CTkFrame(root, width=400, height=350, corner_radius=20, border_width=2)
main_frame.place(relx=0.5, rely=0.5, anchor="center")
main_frame.configure(fg_color=("#f7f7f7", "#333333"))
ctk.set_default_color_theme("green")
show_login_screen()
ctk.set_appearance_mode("Dark")
root.mainloop()
