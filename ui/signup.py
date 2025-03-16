import tkinter as tk
from tkinter import Entry, Label, Button, Frame

# Main App Window
root = tk.Tk()
root.title("Sign Up Page")
root.geometry("1000x600")
root.configure(bg="#FF9C66")  # Background color to match the UI

# Gradient Background Effect (Simulated)
canvas = tk.Canvas(root, width=1000, height=600, bg="white", highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_rectangle(0, 0, 1000, 600, fill="#FF9C66", outline="")

# --- Left Side: Signup Form ---
form_frame = Frame(root, bg="white", width=350, height=400, bd=5, relief="flat")
form_frame.place(x=120, y=100)

# Title
Label(form_frame, text="Create Your Account", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

# Full Name
Label(form_frame, text="Full Name", font=("Arial", 10), bg="white").pack(anchor="w", padx=20)
Entry(form_frame, font=("Arial", 12), width=30, relief="solid", bd=1).pack(pady=5, padx=20)

# Email
Label(form_frame, text="Email", font=("Arial", 10), bg="white").pack(anchor="w", padx=20)
Entry(form_frame, font=("Arial", 12), width=30, relief="solid", bd=1).pack(pady=5, padx=20)

# Phone Number
Label(form_frame, text="Phone Number", font=("Arial", 10), bg="white").pack(anchor="w", padx=20)
Entry(form_frame, font=("Arial", 12), width=30, relief="solid", bd=1).pack(pady=5, padx=20)

# Password
Label(form_frame, text="Password", font=("Arial", 10), bg="white").pack(anchor="w", padx=20)
Entry(form_frame, font=("Arial", 12), width=30, relief="solid", bd=1, show="*").pack(pady=5, padx=20)

# Confirm Password
Label(form_frame, text="Confirm Password", font=("Arial", 10), bg="white").pack(anchor="w", padx=20)
Entry(form_frame, font=("Arial", 12), width=30, relief="solid", bd=1, show="*").pack(pady=5, padx=20)

# Sign Up Button
signup_button = Button(form_frame, text="Sign Up", font=("Arial", 12, "bold"), bg="red", fg="white", width=25, height=2)
signup_button.pack(pady=15)

# Footer Links
footer_frame = Frame(form_frame, bg="white")
footer_frame.pack()
Label(footer_frame, text="Already have an account?", fg="black", bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
Label(footer_frame, text="Login", fg="red", bg="white", font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=10)

# --- Right Side: Mobile UI Placeholder ---
right_frame = Frame(root, bg="white", width=200, height=400, bd=5, relief="flat")
right_frame.place(x=650, y=100)

Label(right_frame, text="[Mobile UI]", font=("Arial", 12, "bold"), bg="white", fg="black").pack(expand=True)

root.mainloop()
