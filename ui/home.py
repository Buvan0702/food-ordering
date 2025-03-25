import customtkinter as ctk

# Configure the theme
ctk.set_appearance_mode("light")  # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # You can change this to "green", "dark-blue", etc.

# Main Window
root = ctk.CTk()
root.title("Food Delivery UI")
root.geometry("1000x600")
root.configure(bg="white")

# Header
header_label = ctk.CTkLabel(root, text="Find Your Favorite Food", font=("Arial", 18, "bold"), fg_color="white", text_color="black")
header_label.pack(pady=10)

# Search Bar
search_bar = ctk.CTkEntry(root, font=("Arial", 14), width=600, height=35, placeholder_text="🔍 Search for restaurants or dishes...", fg_color="white", text_color="black", border_color="gray")
search_bar.pack(pady=5)

# Category Buttons
categories = ["FastFood", "Desserts", "Healthy", "Indian", "Chinese"]
category_frame = ctk.CTkFrame(root, fg_color="white")
category_frame.pack(pady=10)

for category in categories:
    btn = ctk.CTkButton(category_frame, text=category, font=("Arial", 12, "bold"), corner_radius=10, width=120, fg_color="#FFA500", text_color="white", hover_color="#FF8C00")
    btn.pack(side="left", padx=5)

# Restaurant Listings
restaurant_frame = ctk.CTkFrame(root, fg_color="white")
restaurant_frame.pack(pady=10)

restaurants = [
    ("Restaurant 1", "Pizza Place", "⭐️⭐️⭐️⭐️ (4.4)", "Estimated Delivery: 30 mins"),
    ("Restaurant 2", "Burger Haven", "⭐️⭐️⭐️⭐️⭐️ (4.5)", "Estimated Delivery: 25 mins"),
    ("Restaurant 3", "Sweet Treats", "⭐️⭐️⭐️ (3.5)", "Estimated Delivery: 20 mins")
]

for res_name, res_title, rating, delivery in restaurants:
    card = ctk.CTkFrame(restaurant_frame, width=300, height=180, corner_radius=10, fg_color="white", border_color="gray", border_width=2)
    card.pack(side="left", padx=10, pady=10)

    # Placeholder for Image
    img_label = ctk.CTkLabel(card, text=res_name, font=("Arial", 14, "bold"), width=280, height=80, fg_color="gray", text_color="white")
    img_label.pack(pady=5)

    # Restaurant Details
    ctk.CTkLabel(card, text=res_title, font=("Arial", 12, "bold"), fg_color="white", text_color="black").pack(anchor="w", padx=10, pady=3)
    ctk.CTkLabel(card, text=rating, font=("Arial", 10), fg_color="white", text_color="black").pack(anchor="w", padx=10)
    ctk.CTkLabel(card, text=delivery, font=("Arial", 10), fg_color="white", text_color="black").pack(anchor="w", padx=10)

    # View Menu Button
    view_menu_btn = ctk.CTkButton(card, text="View Menu", font=("Arial", 10, "bold"), corner_radius=5, fg_color="green", text_color="white", width=180)
    view_menu_btn.pack(pady=10)

# Bottom Navigation Bar with Emojis
nav_bar = ctk.CTkFrame(root, height=50, fg_color="white", border_width=1, border_color="gray")
nav_bar.pack(side="bottom", fill="x")

nav_items = [
    ("🏠 Home", "green"),
    ("📦 Orders", "orange"),
    ("🛒 Cart", "blue"),
    ("👤 Profile", "purple"),
    ("⚙️ Settings", "gray")
]

for item, color in nav_items:
    nav_btn = ctk.CTkButton(nav_bar, text=item, font=("Arial", 10), width=120, corner_radius=5, fg_color="white", text_color=color, hover_color="lightgray")
    nav_btn.pack(side="left", expand=True, padx=10, pady=5)

root.mainloop()
