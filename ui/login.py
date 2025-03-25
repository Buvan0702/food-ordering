import customtkinter as ctk

# ---------------- Main Application Window ----------------
ctk.set_appearance_mode("light")  # Light Mode
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
                             hover_color="#b75e00")
login_button.pack(pady=15)

# Footer Links
footer_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
footer_frame.pack()
ctk.CTkLabel(footer_frame, text="Forgot Password?", text_color="orange", font=("Arial", 11)).pack(side="left", padx=15)
ctk.CTkLabel(footer_frame, text="Register Now", text_color="orange", font=("Arial", 11)).pack(side="right", padx=15)

# ---------------- Run Application ----------------
root.mainloop()
