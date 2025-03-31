import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import hashlib
import subprocess  # To open login.py

# ------------------- Database Connection -------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="new_password",  # Replace with your MySQL password
        database="food_system"  # Replace with your database name
    )

# ------------------- Password Hashing -------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------- Sign Up Function -------------------
def signup_user():
    full_name = name_entry.get()
    email = email_entry.get()
    phone_number = phone_entry.get()
    password = password_entry.get()
    confirm_password = confirm_entry.get()

    # Check if any fields are empty
    if not full_name or not email or not phone_number or not password or not confirm_password:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    # Check if passwords match
    if password != confirm_password:
        messagebox.showwarning("Password Error", "Passwords do not match.")
        return

    # Hash the password
    hashed_password = hash_password(password)

    try:
        connection = connect_db()
        cursor = connection.cursor()

        # Insert the user data into the database
        cursor.execute(
            "INSERT INTO Users (full_name, email, phone_number, password) VALUES (%s, %s, %s, %s)",
            (full_name, email, phone_number, hashed_password)
        )

        connection.commit()
        messagebox.showinfo("Success", "User registered successfully!")
        
        # After successful registration, redirect to login page
        open_login_page()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ------------------- Open Login Page -------------------
def open_login_page():
    try:
        subprocess.Popen(["python", "login.py"])  # Open login.py after successful signup
        root.quit()  # Close the current signup window
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open login page: {e}")

# ----------------- Setup -----------------
ctk.set_appearance_mode("light")  # Light Mode
ctk.set_default_color_theme("blue")  # Blue Theme

root = ctk.CTk()
root.title("Sign Up Page")
root.geometry("1000x600")  
root.resizable(False, False)  

# ---------------- Left Side: Sign-Up Form ----------------
form_frame = ctk.CTkFrame(root, fg_color="white", width=350, height=450, corner_radius=20)
form_frame.place(x=120, y=80)

# Title
ctk.CTkLabel(form_frame, text="Create Your Account ✨", font=("Arial", 18, "bold"), text_color="black").pack(pady=10)

# Full Name
ctk.CTkLabel(form_frame, text="Full Name", font=("Arial", 12), text_color="black").pack(anchor="w", padx=30)
name_entry = ctk.CTkEntry(form_frame, font=("Arial", 12), width=250, height=35, corner_radius=10)
name_entry.pack(pady=5)

# Email
ctk.CTkLabel(form_frame, text="Email", font=("Arial", 12), text_color="black").pack(anchor="w", padx=30)
email_entry = ctk.CTkEntry(form_frame, font=("Arial", 12), width=250, height=35, corner_radius=10)
email_entry.pack(pady=5)

# Phone Number
ctk.CTkLabel(form_frame, text="Phone Number", font=("Arial", 12), text_color="black").pack(anchor="w", padx=30)
phone_entry = ctk.CTkEntry(form_frame, font=("Arial", 12), width=250, height=35, corner_radius=10)
phone_entry.pack(pady=5)

# Password
ctk.CTkLabel(form_frame, text="Password", font=("Arial", 12), text_color="black").pack(anchor="w", padx=30)
password_entry = ctk.CTkEntry(form_frame, font=("Arial", 12), width=250, height=35, corner_radius=10, show="*")
password_entry.pack(pady=5)

# Confirm Password
ctk.CTkLabel(form_frame, text="Confirm Password", font=("Arial", 12), text_color="black").pack(anchor="w", padx=30)
confirm_entry = ctk.CTkEntry(form_frame, font=("Arial", 12), width=250, height=35, corner_radius=10, show="*")
confirm_entry.pack(pady=5)

# Sign Up Button with Hover Effect
signup_button = ctk.CTkButton(form_frame, text="Sign Up", font=("Arial", 14, "bold"), fg_color="red",
                              text_color="white", width=250, height=40, corner_radius=10,
                              hover_color="#b71c1c", command=signup_user)
signup_button.pack(pady=15)

# Footer Links
footer_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
footer_frame.pack()
ctk.CTkLabel(footer_frame, text="Already have an account?", text_color="black", font=("Arial", 11)).pack(side="left", padx=15)
login_label = ctk.CTkLabel(footer_frame, text="Login", text_color="red", font=("Arial", 11, "bold"), cursor="hand2")
login_label.pack(side="right", padx=15)

# Bind Login label to open login.py
login_label.bind("<Button-1>", lambda e: open_login_page())  # Open login page when clicked

# ---------------- Right Side: Mobile UI Mockup ----------------
right_frame = ctk.CTkFrame(root, fg_color="white", width=250, height=450, corner_radius=20)
right_frame.place(x=600, y=80)

ctk.CTkLabel(right_frame, text="📱 Mobile UI Preview", font=("Arial", 14, "bold"), text_color="black").pack(expand=True)

# ---------------- Run Application ----------------
root.mainloop()
