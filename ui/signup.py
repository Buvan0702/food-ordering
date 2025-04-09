import customtkinter as ctk
from tkinter import messagebox
import re
import subprocess

# Import our custom utility classes
from db_connection import DatabaseConnection
from password_utility import PasswordManager

# ------------------- Validation Functions -------------------
def validate_full_name(name):
    """
    Validate full name:
    - Must contain at least two words
    - Only letters and spaces allowed
    """
    if not name:
        return False
    
    # Split the name and check if it has at least two parts
    name_parts = name.split()
    if len(name_parts) < 2:
        return False
    
    # Check that name contains only letters and spaces
    return all(part.isalpha() for part in name_parts)

def validate_email(email):
    """
    Validate email format
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_phone_number(phone):
    """
    Validate phone number:
    - Only digits allowed
    - Between 10-15 digits
    """
    # Remove any spaces or dashes
    cleaned_phone = re.sub(r'[\s-]', '', phone)
    return cleaned_phone.isdigit() and 10 <= len(cleaned_phone) <= 15

# ------------------- Sign Up Function -------------------
def signup_user():
    full_name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone_number = phone_entry.get().strip()
    password = password_entry.get()
    confirm_password = confirm_entry.get()

    # Comprehensive input validation
    if not full_name or not email or not phone_number or not password or not confirm_password:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    # Validate full name
    if not validate_full_name(full_name):
        messagebox.showwarning("Name Error", "Please enter a valid full name (at least two words, letters only).")
        return

    # Validate email
    if not validate_email(email):
        messagebox.showwarning("Email Error", "Please enter a valid email address.")
        return

    # Validate phone number
    if not validate_phone_number(phone_number):
        messagebox.showwarning("Phone Error", "Please enter a valid phone number.")
        return

    # Validate password strength
    if not PasswordManager.validate_password(password):
        messagebox.showwarning("Password Error", 
            "Password must be at least 8 characters long and contain:\n"
            "- At least one uppercase letter\n"
            "- At least one lowercase letter\n"
            "- At least one digit\n"
            "- At least one special character"
        )
        return

    # Check if passwords match
    if password != confirm_password:
        messagebox.showwarning("Password Error", "Passwords do not match.")
        return

    # Hash the password
    hashed_password = PasswordManager.hash_password(password)

    try:
        # Check if email already exists
        check_query = "SELECT user_id FROM Users WHERE email = %s"
        existing_user = DatabaseConnection.execute_query(
            check_query, 
            params=(email,), 
            fetch=True
        )

        if existing_user:
            messagebox.showwarning("Registration Error", "Email already exists. Please use a different email.")
            return
        
        # Insert the user data into the database
        address=None
        insert_query = """
        INSERT INTO Users (first_name, last_name, email, phone_number, password,address) 
        VALUES (%s, %s, %s, %s, %s,%s)
        """
        # Split full name into first and last name
        name_parts = full_name.split(maxsplit=1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        DatabaseConnection.execute_query(
            insert_query, 
            params=(first_name, last_name, email, phone_number, hashed_password)
        )

        messagebox.showinfo("Success", "User registered successfully!")
        
        # After successful registration, redirect to login page
        open_login_page()

    except Exception as err:
        messagebox.showerror("Registration Error", f"An error occurred: {str(err)}")

# ------------------- Open Login Page -------------------
def open_login_page():
    try:
        subprocess.Popen(["python", "login.py"])
        root.quit()
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open login page: {e}")

# Rest of the UI code remains the same as in the original script
# (Keeping all the CustomTkinter UI setup from the previous script)

# ---------------- Initialize CustomTkinter ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ---------------- Main Application Window ----------------
root = ctk.CTk()
root.title("Sign Up Page")
root.geometry("1000x600")
root.resizable(False, False)

# ---------------- Background ----------------
# Create a frame that covers the entire window with coral/orange background
bg_frame = ctk.CTkFrame(root, fg_color="#FF8866", width=1000, height=600, corner_radius=0)
bg_frame.place(x=0, y=0)

# ---------------- Left Side Mobile Mockup ----------------
# Phone frame
phone_frame = ctk.CTkFrame(bg_frame, fg_color="#2B2B43", width=270, height=520, corner_radius=40)
phone_frame.place(x=150, y=40)

# Phone inner screen
phone_screen = ctk.CTkFrame(phone_frame, fg_color="white", width=240, height=480, corner_radius=30)
phone_screen.place(x=15, y=20)

# Phone notch
notch = ctk.CTkFrame(phone_screen, fg_color="#2B2B43", width=80, height=25, corner_radius=10)
notch.place(x=80, y=0)

# Product 1 (Bottle) - using an icon similar to login page
product1_frame = ctk.CTkFrame(phone_screen, fg_color="#FFA500", width=200, height=130, corner_radius=10)
product1_frame.place(x=20, y=40)

# Using a bottle icon (similar to login page)
bottle_label = ctk.CTkLabel(product1_frame, text="🍶", font=("Arial", 50), text_color="#2B2B43")
bottle_label.place(relx=0.5, rely=0.4, anchor="center")

# Product 1 buttons
plus_btn1 = ctk.CTkButton(phone_screen, text="+", font=("Arial", 16, "bold"), fg_color="#FFA500", 
                          text_color="white", width=30, height=30, corner_radius=15)
plus_btn1.place(x=130, y=180)

minus_btn1 = ctk.CTkButton(phone_screen, text="-", font=("Arial", 16, "bold"), fg_color="#FFA500", 
                           text_color="white", width=30, height=30, corner_radius=15)
minus_btn1.place(x=80, y=180)

# Product 2 (Egg) - using an icon similar to login page
product2_frame = ctk.CTkFrame(phone_screen, fg_color="#FFA500", width=200, height=130, corner_radius=10)
product2_frame.place(x=20, y=230)

# Using a magnifying glass icon like in the login image
egg_label = ctk.CTkLabel(product2_frame, text="🔍", font=("Arial", 50), text_color="white")
egg_label.place(relx=0.5, rely=0.4, anchor="center")

# Product 2 buttons
plus_btn2 = ctk.CTkButton(phone_screen, text="+", font=("Arial", 16, "bold"), fg_color="#FFA500", 
                          text_color="white", width=30, height=30, corner_radius=15)
plus_btn2.place(x=130, y=370)

minus_btn2 = ctk.CTkButton(phone_screen, text="-", font=("Arial", 16, "bold"), fg_color="#FFA500", 
                           text_color="white", width=30, height=30, corner_radius=15)
minus_btn2.place(x=80, y=370)

# Person silhouette - using a similar avatar as in the login page
person_label = ctk.CTkLabel(bg_frame, text="👩", font=("Arial", 80), text_color="#2B2B43")
person_label.place(x=500, y=250)

# ---------------- Right Side Sign Up Form ----------------
form_frame = ctk.CTkFrame(bg_frame, fg_color="white", width=400, height=600, corner_radius=20)
form_frame.place(x=550, y=40)

# Title
title_label = ctk.CTkLabel(form_frame, text="Create Account", font=("Arial", 24, "bold"), text_color="#2B2B43")
title_label.place(relx=0.5, rely=0.08, anchor="center")

# Full Name
name_label = ctk.CTkLabel(form_frame, text="Full Name", font=("Arial", 14), text_color="#2B2B43")
name_label.place(x=50, y=80)

name_entry = ctk.CTkEntry(form_frame, width=300, height=40, corner_radius=5, border_width=1, border_color="#E0E0E0")
name_entry.place(x=50, y=110)

# Email
email_label = ctk.CTkLabel(form_frame, text="Email", font=("Arial", 14), text_color="#2B2B43")
email_label.place(x=50, y=160)

email_entry = ctk.CTkEntry(form_frame, width=300, height=40, corner_radius=5, border_width=1, border_color="#E0E0E0")
email_entry.place(x=50, y=190)

# Phone Number
phone_label = ctk.CTkLabel(form_frame, text="Phone Number", font=("Arial", 14), text_color="#2B2B43")
phone_label.place(x=50, y=240)

phone_entry = ctk.CTkEntry(form_frame, width=300, height=40, corner_radius=5, border_width=1, border_color="#E0E0E0")
phone_entry.place(x=50, y=270)

# Password
password_label = ctk.CTkLabel(form_frame, text="Password", font=("Arial", 14), text_color="#2B2B43")
password_label.place(x=50, y=320)

password_entry = ctk.CTkEntry(form_frame, width=300, height=40, corner_radius=5, border_width=1, border_color="#E0E0E0", show="*")
password_entry.place(x=50, y=350)

# Confirm Password
confirm_label = ctk.CTkLabel(form_frame, text="Confirm Password", font=("Arial", 14), text_color="#2B2B43")
confirm_label.place(x=50, y=400)

confirm_entry = ctk.CTkEntry(form_frame, width=300, height=40, corner_radius=5, border_width=1, border_color="#E0E0E0", show="*")
confirm_entry.place(x=50, y=430)

# Sign Up Button - similar to the orange login button in the reference image
signup_button = ctk.CTkButton(form_frame, text="Sign Up", font=("Arial", 16, "bold"), fg_color="#FF7722", 
                             text_color="white", width=300, height=40, corner_radius=5, 
                             hover_color="#E56600", command=signup_user)
signup_button.place(x=50, y=480)

# Already have an account / Login link - styled like the login page
already_account_label = ctk.CTkLabel(form_frame, text="Already have an account?", font=("Arial", 12), text_color="#555555")
already_account_label.place(x=50, y=540)

login_link = ctk.CTkLabel(form_frame, text="Login Now", font=("Arial", 12), text_color="#FF7722", cursor="hand2")
login_link.place(x=300, y=540)

# Bind the login link
login_link.bind("<Button-1>", lambda e: open_login_page())

# ---------------- Run Application ----------------
root.mainloop()