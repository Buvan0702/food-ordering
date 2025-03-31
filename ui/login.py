import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import hashlib
import subprocess  # To open signup.py and home.py

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

# ------------------- Login Function -------------------
def login_user():
    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        messagebox.showwarning("Input Error", "Please enter both email and password.")
        return

    hashed_password = hash_password(password)

    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT first_name, last_name FROM Users WHERE email = %s AND password = %s",
            (email, hashed_password)
        )
        user = cursor.fetchone()

        if user:
            first_name, last_name = user
            messagebox.showinfo("Success", f"Welcome {first_name} {last_name}!")
            root.destroy()  # Close the login window upon successful login
            open_home_page()  # Open the home page after login
        else:
            messagebox.showerror("Login Failed", "Invalid Email or Password.")
    
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ------------------- Open Home Page -------------------
def open_home_page():
    try:
        subprocess.Popen(["python", "home.py"])  # Open home.py after successful login
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open home page: {e}")

# ------------------- Open Sign Up Page -------------------
def open_signup_page():
    try:
        subprocess.Popen(["python", "signup.py"])  # Open signup.py when Sign Up is clicked
        root.quit()  # Close the login window
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open signup page: {e}")

# ---------------- Initialize CustomTkinter ----------------
ctk.set_appearance_mode("light")  # Light Mode
ctk.set_default_color_theme("blue")

# ---------------- Main Application Window ----------------
root = ctk.CTk()
root.title("Login Page")
root.geometry("1000x600")
root.resizable(False, False)

# ---------------- Left Side Mobile Mockup ----------------
left_frame = ctk.CTkFrame(root, fg_color="white", width=300, height=450, corner_radius=20)
left_frame.place(x=100, y=75)

# Mobile Frame Border
phone_frame = ctk.CTkFrame(left_frame, fg_color="black", width=230, height=400, corner_radius=20)
phone_frame.pack(pady=20)

# Product Selection UI Inside Phone
product_frame = ctk.CTkFrame(phone_frame, fg_color="white", width=200, height=150, corner_radius=10)
product_frame.pack(pady=20)

ctk.CTkLabel(product_frame, text="🛒 Product 1", font=("Arial", 14, "bold"), text_color="black").pack(pady=5)
ctk.CTkButton(product_frame, text="+", font=("Arial", 14), fg_color="orange", text_color="white",
              width=40, height=30, corner_radius=10).pack(side="left", padx=10)
ctk.CTkButton(product_frame, text="-", font=("Arial", 14), fg_color="orange", text_color="white",
              width=40, height=30, corner_radius=10).pack(side="right", padx=10)

# ---------------- Right Side Login Form ----------------
form_frame = ctk.CTkFrame(root, fg_color="white", width=350, height=350, corner_radius=20)
form_frame.place(x=550, y=125)

# Title
ctk.CTkLabel(form_frame, text="Welcome Back! 👋", font=("Arial", 20, "bold"), text_color="black").pack(pady=10)

# Email Entry
ctk.CTkLabel(form_frame, text="Email", font=("Arial", 12), text_color="black").pack(anchor="w", padx=30)
email_entry = ctk.CTkEntry(form_frame, font=("Arial", 12), width=250, height=35, corner_radius=10)
email_entry.pack(pady=5)

# Password Entry
ctk.CTkLabel(form_frame, text="Password", font=("Arial", 12), text_color="black").pack(anchor="w", padx=30)
password_entry = ctk.CTkEntry(form_frame, font=("Arial", 12), width=250, height=35, corner_radius=10, show="*")
password_entry.pack(pady=5)

# Login Button with Hover Effect
login_button = ctk.CTkButton(form_frame, text="Login", font=("Arial", 14, "bold"), fg_color="orange",
                             text_color="white", width=250, height=40, corner_radius=10,
                             hover_color="#b75e00", command=login_user)
login_button.pack(pady=15)

# Footer Links
footer_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
footer_frame.pack()
ctk.CTkLabel(footer_frame, text="Forgot Password?", text_color="orange", font=("Arial", 11)).pack(side="left", padx=15)
signup_label = ctk.CTkLabel(footer_frame, text="Register Now", text_color="orange", font=("Arial", 11), cursor="hand2")
signup_label.pack(side="right", padx=15)

# Bind Register Now label to open signup.py
signup_label.bind("<Button-1>", lambda e: open_signup_page())  # Open the sign-up page when clicked

# ---------------- Run Application ----------------
root.mainloop()
