import customtkinter as ctk

# ---------------- Main Application Window ----------------
ctk.set_appearance_mode("light")  # Light Mode UI
root = ctk.CTk()
root.title("Restaurant Menu")
root.geometry("1100x700")
root.resizable(False, False)

# ---------------- Back Button ----------------
back_btn = ctk.CTkButton(root, text="⬅ Back", font=("Arial", 12, "bold"), fg_color="lightgreen",
                         text_color="black", width=80, height=30, corner_radius=15, hover_color="#27ae60")
back_btn.place(x=10, y=10)

# ---------------- Restaurant Banner ----------------
banner = ctk.CTkFrame(root, fg_color="lightgray", width=1100, height=100, corner_radius=0)
banner.place(x=0, y=40)

ctk.CTkLabel(banner, text="🍽️ Welcome to Our Restaurant", font=("Arial", 30, "bold"), text_color="black").pack(expand=True)

# ---------------- Search Bar ----------------
search_entry = ctk.CTkEntry(root, placeholder_text="🔍 Search for food...", width=300, height=35, corner_radius=10)
search_entry.place(x=750, y=160)

# ---------------- Menu Section Title ----------------
ctk.CTkLabel(root, text="🥘 Our Special Menu", font=("Arial", 18, "bold"), text_color="black").place(x=50, y=160)

# ---------------- Food Items ----------------
food_items = [
    ("🍕", "Margherita Pizza", "$12.99"),
    ("🍔", "Cheeseburger", "$9.99"),
    ("🥗", "Caesar Salad", "$8.99"),
    ("🍝", "Spaghetti Bolognese", "$13.49"),
    ("🍣", "Sushi Platter", "$18.99"),
    ("🌮", "Chicken Tacos", "$11.49"),
    ("🥪", "Club Sandwich", "$10.99"),
    ("🍩", "Chocolate Donut", "$5.99"),
    ("🍜", "Ramen Noodles", "$14.99"),
    ("🍛", "Butter Chicken", "$15.49"),
    ("🥞", "Pancakes", "$9.49"),
    ("🧁", "Cupcake", "$6.49")
]

# Scrollable Menu Frame
menu_frame = ctk.CTkScrollableFrame(root, fg_color="transparent", width=980, height=320)
menu_frame.place(x=50, y=200)

# Display Food Items in Grid
row, col = 0, 0
for emoji, title, price in food_items:
    # Food Card
    card = ctk.CTkFrame(menu_frame, fg_color="white", width=280, height=220, corner_radius=15)
    card.grid(row=row, column=col, padx=10, pady=10, sticky="n")

    # Placeholder Image (Food Item)
    img_placeholder = ctk.CTkFrame(card, fg_color="lightgray", width=280, height=100, corner_radius=15)
    img_placeholder.pack()
    ctk.CTkLabel(img_placeholder, text=emoji, font=("Arial", 35), text_color="gray").pack(expand=True)

    # Food Title
    ctk.CTkLabel(card, text=title, font=("Arial", 14, "bold"), text_color="black").pack(anchor="w", padx=15, pady=5)

    # Price
    ctk.CTkLabel(card, text=price, font=("Arial", 13, "bold"), text_color="green").pack(anchor="e", padx=15, pady=5)

    # Add to Cart Button
    add_btn = ctk.CTkButton(card, text="🛒 Add to Cart", font=("Arial", 12, "bold"), fg_color="green",
                            text_color="white", width=220, height=30, corner_radius=10, hover_color="#27ae60")
    add_btn.pack(pady=10)

    # Adjust grid placement
    col += 1
    if col > 2:  # Max 3 items per row
        col = 0
        row += 1

# ---------------- Order Summary Section ----------------
order_summary_frame = ctk.CTkFrame(root, fg_color="white", width=1100, height=120, corner_radius=15)
order_summary_frame.place(x=50, y=560)

# Order Summary Title
ctk.CTkLabel(order_summary_frame, text="🛒 Order Summary", font=("Arial", 16, "bold"), text_color="black").place(x=20, y=10)

# Order Summary Details
order_details = [
    ("🍔 Cheeseburger", "$9.99", "x1"),
    ("🍕 Margherita Pizza", "$12.99", "x2"),
]

y_pos = 40
for item, price, qty in order_details:
    ctk.CTkLabel(order_summary_frame, text=f"{item}  {qty}  -  {price}",
                 font=("Arial", 12), text_color="black").place(x=20, y=y_pos)
    y_pos += 30

# Checkout Button
checkout_btn = ctk.CTkButton(order_summary_frame, text="💳 Proceed to Checkout", font=("Arial", 12, "bold"),
                             fg_color="red", text_color="white", width=200, height=35, corner_radius=10,
                             hover_color="#c0392b")
checkout_btn.place(x=850, y=40)

# ---------------- Bottom Navigation Bar ----------------
nav_bar = ctk.CTkFrame(root, fg_color="white", height=60, corner_radius=0)
nav_bar.pack(side="bottom", fill="x")

# Navigation Bar Items
nav_items = [
    ("🏠 Home", "#2ECC71"),
    ("📦 Orders", "#E67E22"),
    ("🛒 Cart", "#3498DB"),
    ("👤 Profile", "#9B59B6"),
    ("⚙️ Settings", "#95A5A6")
]

for item, color in nav_items:
    nav_btn = ctk.CTkButton(nav_bar, text=item, font=("Arial", 12, "bold"), fg_color="white",
                            text_color=color, width=100, height=40, corner_radius=15, hover_color="#f2f2f2")
    nav_btn.pack(side="left", expand=True, padx=5, pady=5)

# ---------------- Run Application ----------------
root.mainloop()
