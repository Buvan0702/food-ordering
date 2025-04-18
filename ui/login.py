import customtkinter as ctk
from tkinter import messagebox
import subprocess

# Import our custom utility classes
from db_connection import DatabaseConnection
from password_utility import PasswordManager

# ------------------- Login Function -------------------
def login_user():
    email = email_entry.get().strip()
    password = password_entry.get()

    # Input validation
    if not email or not password:
        messagebox.showwarning("Input Error", "Please enter both email and password.")
        return
    
    # Validate email format
    if not is_valid_email(email):
        messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
        return

    # Hash the password
    hashed_password = PasswordManager.hash_password(password)

    try:
        # Use the database connection utility to execute login query
        query = """
        SELECT user_id, first_name, last_name 
        FROM Users 
        WHERE email = %s AND password = %s
        """
        results = DatabaseConnection.execute_query(
            query, 
            params=(email, hashed_password), 
            fetch=True
        )

        if results:
            # Login successful
            user = results[0]
            messagebox.showinfo("Success", f"Welcome {user['first_name']} {user['last_name']}!")
            root.destroy()  # Close the login window
            open_home_page(user['user_id'])  # Pass user ID to home page
        else:
            messagebox.showerror("Login Failed", "Invalid Email or Password.")
    
    except Exception as err:
        messagebox.showerror("Login Error", f"An error occurred: {str(err)}")

# ------------------- Email Validation -------------------
def is_valid_email(email):
    """
    Validate email format using a simple regex pattern
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# ------------------- Open Home Page -------------------
def open_home_page(user_id=None):
    try:
        # Pass user ID to home page if available
        if user_id:
            subprocess.Popen(["python", "home.py", str(user_id)])
        else:
            subprocess.Popen(["python", "home.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open home page: {e}")

# ------------------- Open Sign Up Page -------------------
def open_signup_page():
    try:
        subprocess.Popen(["python", "signup.py"])
        root.quit()
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open signup page: {e}")

# ---------------- Initialize CustomTkinter ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ---------------- Main Application Window ----------------
root = ctk.CTk()
root.title("Login Page")
root.geometry("1000x600")
root.resizable(False, False)

# ---------------- Background ----------------
# Create a frame that covers the entire window with coral/orange background
bg_frame = ctk.CTkFrame(root, fg_color="#FF8866", width=1000, height=600, corner_radius=20)
bg_frame.place(x=0, y=0)

# ---------------- Left Side Mobile Mockup ----------------
# Phone frame
phone_frame = ctk.CTkFrame(bg_frame, fg_color="#2B2B43", width=270, height=500, corner_radius=40)
phone_frame.place(x=150, y=50)

# Phone inner screen
phone_screen = ctk.CTkFrame(phone_frame, fg_color="white", width=240, height=470, corner_radius=30)
phone_screen.place(x=15, y=15)

# Phone notch
notch = ctk.CTkFrame(phone_screen, fg_color="#2B2B43", width=80, height=25, corner_radius=10)
notch.place(x=80, y=0)

# Product 1 (Bottle)
product1_frame = ctk.CTkFrame(phone_screen, fg_color="#FFA500", width=200, height=130, corner_radius=10)
product1_frame.place(x=20, y=40)

# Bottle icon
bottle_label = ctk.CTkLabel(product1_frame, text="🍾", font=("Arial", 50), text_color="#2B2B43")
bottle_label.place(relx=0.5, rely=0.4, anchor="center")

# Product 1 buttons
plus_btn1 = ctk.CTkButton(phone_screen, text="+", font=("Arial", 16, "bold"), fg_color="#FFA500", 
                          text_color="white", width=30, height=30, corner_radius=15)
plus_btn1.place(x=80, y=180)

minus_btn1 = ctk.CTkButton(phone_screen, text="-", font=("Arial", 16, "bold"), fg_color="#FFA500", 
                           text_color="white", width=30, height=30, corner_radius=15)
minus_btn1.place(x=130, y=180)

# Product 2 (Egg)
product2_frame = ctk.CTkFrame(phone_screen, fg_color="#FFA500", width=200, height=130, corner_radius=10)
product2_frame.place(x=20, y=230)

# Egg icon
egg_label = ctk.CTkLabel(product2_frame, text="🍳", font=("Arial", 50), text_color="white")
egg_label.place(relx=0.5, rely=0.4, anchor="center")

# Product 2 buttons
plus_btn2 = ctk.CTkButton(phone_screen, text="+", font=("Arial", 16, "bold"), fg_color="#FFA500", 
                          text_color="white", width=30, height=30, corner_radius=15)
plus_btn2.place(x=80, y=370)

minus_btn2 = ctk.CTkButton(phone_screen, text="-", font=("Arial", 16, "bold"), fg_color="#FFA500", 
                           text_color="white", width=30, height=30, corner_radius=15)
minus_btn2.place(x=130, y=370)

# Person silhouette
person_label = ctk.CTkLabel(bg_frame, text="👩", font=("Arial", 100), text_color="#2B2B43")
person_label.place(x=470, y=250)

# ---------------- Right Side Login Form ----------------
login_frame = ctk.CTkFrame(bg_frame, fg_color="white", width=400, height=400, corner_radius=20)
login_frame.place(x=550, y=100)

# Welcome text
welcome_label = ctk.CTkLabel(login_frame, text="Welcome Back!", font=("Arial", 24, "bold"), text_color="#2B2B43")
welcome_label.place(relx=0.5, rely=0.15, anchor="center")

# Email label and entry
email_label = ctk.CTkLabel(login_frame, text="Email", font=("Arial", 14), text_color="#2B2B43")
email_label.place(x=50, y=100)

email_entry = ctk.CTkEntry(login_frame, width=300, height=40, corner_radius=5, border_width=1, border_color="#E0E0E0")
email_entry.place(x=50, y=130)

# Password label and entry
password_label = ctk.CTkLabel(login_frame, text="Password", font=("Arial", 14), text_color="#2B2B43")
password_label.place(x=50, y=180)

password_entry = ctk.CTkEntry(login_frame, width=300, height=40, corner_radius=5, border_width=1, border_color="#E0E0E0", show="*")
password_entry.place(x=50, y=210)

# Login button
login_button = ctk.CTkButton(login_frame, text="Login", font=("Arial", 16, "bold"), fg_color="#FF7722", 
                             text_color="white", width=300, height=40, corner_radius=5, 
                             hover_color="#E56600", command=login_user)
login_button.place(x=50, y=280)

# Forgot password link
forgot_pwd = ctk.CTkLabel(login_frame, text="Forgot Password?", font=("Arial", 12), 
                          text_color="#FF7722", cursor="hand2")
forgot_pwd.place(x=50, y=340)

# Register now link
register = ctk.CTkLabel(login_frame, text="Register Now", font=("Arial", 12), 
                        text_color="#FF7722", cursor="hand2")
register.place(x=280, y=340)

# Bind the register label to open signup page
register.bind("<Button-1>", lambda e: open_signup_page())

# Additional import for email validation
import re

# ---------------- Run Application ----------------
root.mainloop()