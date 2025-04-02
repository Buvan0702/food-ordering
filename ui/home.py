import customtkinter as ctk
from PIL import Image, ImageTk
import os
import subprocess
import os

os.environ['TCL_LIBRARY'] = r"C:\Users\buvan\AppData\Local\Programs\Python\Python39\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\buvan\AppData\Local\Programs\Python\Python39\tcl\tk8.6"

# Configure CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create the main window
root = ctk.CTk()
root.title("Home Page")
root.geometry("1500x1000")
root.resizable(False, False)

# Main white background frame
main_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=20)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Header - "Find Your Favorite Food"
header_label = ctk.CTkLabel(
    main_frame, 
    text="Find Your Favorite Food", 
    font=("Arial", 28, "bold"),
    text_color="#2D3748"
)
header_label.pack(pady=(30, 20))

# Search bar
search_entry = ctk.CTkEntry(
    main_frame,
    width=700,
    height=45,
    placeholder_text="Search for restaurants or dishes...",
    font=("Arial", 14),
    corner_radius=15,
    border_width=1,
    border_color="#E2E8F0"
)
search_entry.pack(pady=(10, 20))

# Category buttons frame
category_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
category_frame.pack(pady=(0, 20))

# Category buttons with different colors
categories = [
    ("FastFood", "#32CD32"),  # Green
    ("Desserts", "#FF7F50"),  # Coral/Orange
    ("Healthy", "#F85C50"),   # Red
    ("Indian", "#FFD700"),    # Yellow/Gold
    ("Chinese", "#9370DB")    # Purple
]

for category, color in categories:
    category_btn = ctk.CTkButton(
        category_frame,
        text=category,
        font=("Arial", 14, "bold"),
        fg_color=color,
        text_color="white",
        hover_color=color,
        width=120,
        height=35,
        corner_radius=20
    )
    category_btn.pack(side="left", padx=5)

# Restaurant listings frame
restaurants_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
restaurants_frame.pack(pady=10)

# Restaurant data
restaurants = [
    {
        "name": "Pizza Place",
        "rating": 4.4,
        "delivery_time": "30 mins",
        "placeholder": "Restaurant 1"
    },
    {
        "name": "Burger Haven",
        "rating": 4.5,
        "delivery_time": "25 mins",
        "placeholder": "Restaurant 2"
    },
    {
        "name": "Sweet Treats",
        "rating": 3.5,
        "delivery_time": "20 mins",
        "placeholder": "Restaurant 3"
    }
]

# Create restaurant cards
for restaurant in restaurants:
    # Card frame
    card = ctk.CTkFrame(
        restaurants_frame,
        width=350,
        height=370,
        corner_radius=15,
        fg_color="white",
        border_width=0,
        border_color="#E2E8F0"
    )
    card.pack(side="left", padx=10, pady=10)
    card.pack_propagate(False)
    
    # Image placeholder
    img_frame = ctk.CTkFrame(
        card,
        width=320,
        height=170,
        corner_radius=10,
        fg_color="#E2E2E2"
    )
    img_frame.pack(padx=15, pady=15)
    
    img_label = ctk.CTkLabel(
        img_frame,
        text=restaurant["placeholder"],
        font=("Arial", 20, "bold"),
        text_color="#A0A0A0"
    )
    img_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # Restaurant name
    name_label = ctk.CTkLabel(
        card,
        text=restaurant["name"],
        font=("Arial", 18, "bold"),
        text_color="#2D3748",
        anchor="w"
    )
    name_label.pack(padx=15, pady=(5, 0), anchor="w")
    
    # Rating with stars
    rating_frame = ctk.CTkFrame(card, fg_color="transparent")
    rating_frame.pack(padx=15, pady=(5, 0), anchor="w")
    
    star_count = int(restaurant["rating"])
    half_star = restaurant["rating"] - star_count >= 0.5
    
    for i in range(5):
        if i < star_count:
            star = ctk.CTkLabel(rating_frame, text="★", font=("Arial", 16), text_color="#FFD700")
        elif i == star_count and half_star:
            star = ctk.CTkLabel(rating_frame, text="★", font=("Arial", 16), text_color="#FFD700")
        else:
            star = ctk.CTkLabel(rating_frame, text="★", font=("Arial", 16), text_color="#D3D3D3")
        star.pack(side="left")
    
    rating_value = ctk.CTkLabel(
        rating_frame,
        text=f" ({restaurant['rating']})",
        font=("Arial", 14),
        text_color="#666666"
    )
    rating_value.pack(side="left", padx=(5, 0))
    
    # Delivery time
    delivery_label = ctk.CTkLabel(
        card,
        text=f"Estimated Delivery: {restaurant['delivery_time']}",
        font=("Arial", 14),
        text_color="#666666",
        anchor="w"
    )
    delivery_label.pack(padx=15, pady=(5, 0), anchor="w")
    
    # View Menu button
    view_menu_btn = ctk.CTkButton(
        card,
        text="View Menu",
        font=("Arial", 14, "bold"),
        fg_color="#32CD32",
        text_color="white",
        hover_color="#28A828",
        corner_radius=10,
        width=290,
        height=40
    )
    view_menu_btn.pack(padx=15, pady=(20, 15))

# Bottom navigation bar
nav_bar = ctk.CTkFrame(
    main_frame,
    fg_color="white",
    height=70,
    corner_radius=0
)
nav_bar.pack(side="bottom", fill="x", pady=(10, 0))

# Navigation items
nav_items = [
    {"name": "Home", "icon": "🏠", "color": "#32CD32"},
    {"name": "Orders", "icon": "📦", "color": "#000000"},
    {"name": "Cart", "icon": "🛒", "color": "#000000"},
    {"name": "Profile", "icon": "👤", "color": "#000000"},
    {"name": "Settings", "icon": "⚙️", "color": "#000000"}
]

# Create navigation buttons
for item in nav_items:
    nav_frame = ctk.CTkFrame(nav_bar, fg_color="transparent", width=80)
    nav_frame.pack(side="left", expand=True, fill="y")
    
    # Icon
    icon_label = ctk.CTkLabel(
        nav_frame,
        text=item["icon"],
        font=("Arial", 20),
        text_color=item["color"]
    )
    icon_label.pack(pady=(5, 0))
    
    # Text
    text_label = ctk.CTkLabel(
        nav_frame,
        text=item["name"],
        font=("Arial", 12),
        text_color=item["color"]
    )
    text_label.pack()

# Run the application
root.mainloop()