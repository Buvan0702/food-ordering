import tkinter as tk
from tkinter import Entry, Label, Button, Frame

# Main App Window
root = tk.Tk()
root.title("Login Page")
root.geometry("1000x600")
root.configure(bg="#FF9C66")  # Background color similar to your UI

# --- Left Side Mobile Mockup ---
left_frame = Frame(root, bg="white", width=300, height=450, bd=5, relief="flat")
left_frame.place(x=100, y=75)

# Mobile Frame Border
phone_frame = Frame(left_frame, bg="black", width=230, height=400, bd=10, relief="ridge")
phone_frame.pack(pady=20)

# Product Selection (Simulating UI Inside Phone)
product_frame = Frame(phone_frame, bg="white", width=200, height=150)
product_frame.pack(pady=20)

Label(product_frame, text="Product 1", font=("Arial", 12, "bold"), bg="white").pack()
Button(product_frame, text="+", bg="orange", fg="white", font=("Arial", 12), width=4).pack(side=tk.LEFT, padx=5)
Button(product_frame, text="-", bg="orange", fg="white", font=("Arial", 12), width=4).pack(side=tk.RIGHT, padx=5)

# --- Right Side Login Form ---
form_frame = Frame(root, bg="white", width=350, height=350, bd=5, relief="flat")
form_frame.place(x=550, y=125)

# Title
Label(form_frame, text="Welcome Back!", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

# Email Entry
Label(form_frame, text="Email", font=("Arial", 10), bg="white").pack(anchor="w", padx=20)
email_entry = Entry(form_frame, font=("Arial", 12), width=30, relief="solid", bd=1)
email_entry.pack(pady=5, padx=20)

# Password Entry
Label(form_frame, text="Password", font=("Arial", 10), bg="white").pack(anchor="w", padx=20)
password_entry = Entry(form_frame, font=("Arial", 12), width=30, relief="solid", bd=1, show="*")
password_entry.pack(pady=5, padx=20)

# Login Button
login_button = Button(form_frame, text="Login", font=("Arial", 12, "bold"), bg="orange", fg="white", width=25, height=2)
login_button.pack(pady=15)

# Footer Links
footer_frame = Frame(form_frame, bg="white")
footer_frame.pack()
Label(footer_frame, text="Forgot Password?", fg="orange", bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
Label(footer_frame, text="Register Now", fg="orange", bg="white", font=("Arial", 10)).pack(side=tk.RIGHT, padx=10)

root.mainloop()
