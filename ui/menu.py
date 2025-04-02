import customtkinter as ctk
import subprocess
import os

os.environ['TCL_LIBRARY'] = r"C:\Users\buvan\AppData\Local\Programs\Python\Python39\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\buvan\AppData\Local\Programs\Python\Python39\tcl\tk8.6"

# ---------------- Main Application Window ----------------
ctk.set_appearance_mode("light")  # Light Mode UI
root = ctk.CTk()
root.title("Restaurant Menu")
root.geometry("1000x600")
root.resizable(False, False)

# Main white background with rounded corners
main_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=20)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# ---------------- Back Button ----------------
back_btn = ctk.CTkButton(main_frame, text="Back", font=("Arial", 14, "bold"), fg_color="#22C55E",
                       text_color="white", width=80, height=35, corner_radius=10, hover_color="#16A34A")
back_btn.place(x=20, y=20)

# ---------------- Restaurant Banner ----------------
banner = ctk.CTkFrame(main_frame, fg_color="#E5E7EB", width=960, height=120, corner_radius=10)
banner.place(x=20, y=70)

banner_label = ctk.CTkLabel(banner, text="Restaurant Banner", font=("Arial", 36, "bold"), text_color="#9CA3AF")
banner_label.place(relx=0.5, rely=0.5, anchor="center")

# ---------------- Menu Title ----------------
menu_title = ctk.CTkLabel(main_frame, text="Menu", font=("Arial", 24, "bold"), text_color="#1F2937")
menu_title.place(x=20, y=210)

# ---------------- Menu Items ScrollableFrame ----------------
menu_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent", width=940, height=300)
menu_frame.place(x=20, y=250)

# Menu item data
menu_items = [
    {"name": "Margherita Pizza", "price": "$12.99", "image_placeholder": "Pizza"},
    {"name": "Cheeseburger", "price": "$9.99", "image_placeholder": "Burger"},
    {"name": "Caesar Salad", "price": "$8.99", "image_placeholder": "Salad"},
    {"name": "Spaghetti Bolognese", "price": "$13.99", "image_placeholder": "Pasta"},
    {"name": "Chicken Tacos", "price": "$10.99", "image_placeholder": "Taco"},
    {"name": "Club Sandwich", "price": "$8.49", "image_placeholder": "Sandwich"},
    {"name": "Beef Stir Fry", "price": "$14.99", "image_placeholder": "Stir Fry"},
    {"name": "Chocolate Cake", "price": "$6.99", "image_placeholder": "Cake"},
    {"name": "Greek Gyro", "price": "$11.99", "image_placeholder": "Gyro"}
]

# Create menu item cards
row, col = 0, 0
for item in menu_items:
    # Card frame
    card = ctk.CTkFrame(menu_frame, fg_color="white", corner_radius=15, border_width=1, border_color="#E5E7EB")
    card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    
    # Image placeholder
    img_frame = ctk.CTkFrame(card, fg_color="#E5E7EB", width=280, height=170, corner_radius=10)
    img_frame.pack(padx=10, pady=10)
    
    img_label = ctk.CTkLabel(
        img_frame, 
        text=item["image_placeholder"], 
        font=("Arial", 24, "bold"), 
        text_color="#9CA3AF"
    )
    img_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # Item details frame for name and price
    details_frame = ctk.CTkFrame(card, fg_color="transparent", width=280)
    details_frame.pack(fill="x", padx=10)
    
    # Food item name
    name_label = ctk.CTkLabel(
        details_frame, 
        text=item["name"], 
        font=("Arial", 16, "bold"), 
        text_color="#1F2937",
        anchor="w"
    )
    name_label.pack(side="left", pady=5)
    
    # Price with green color
    price_label = ctk.CTkLabel(
        details_frame, 
        text=item["price"], 
        font=("Arial", 16, "bold"), 
        text_color="#22C55E",
        anchor="e"
    )
    price_label.pack(side="right", pady=5)
    
    # Add to Cart button
    add_cart_btn = ctk.CTkButton(
        card, 
        text="Add to Cart", 
        font=("Arial", 14, "bold"), 
        fg_color="#22C55E", 
        text_color="white", 
        corner_radius=10, 
        hover_color="#16A34A",
        width=260,
        height=40
    )
    add_cart_btn.pack(padx=10, pady=10)
    
    # Update grid position
    col += 1
    if col >= 3:  # 3 items per row
        col = 0
        row += 1

# Configure grid weights to make cards expandable
for i in range(3):  # 3 columns
    menu_frame.grid_columnconfigure(i, weight=1)

# ---------------- Bottom Navigation Bar ----------------
nav_bar = ctk.CTkFrame(main_frame, fg_color="white", height=70, corner_radius=0)
nav_bar.pack(side="bottom", fill="x")

# Navigation items
nav_items = [
    {"name": "Home", "icon": "🏠", "active": False},
    {"name": "Orders", "icon": "📦", "active": False},
    {"name": "Cart", "icon": "🛒", "active": True},
    {"name": "Profile", "icon": "👤", "active": False},
    {"name": "Settings", "icon": "⚙️", "active": False}
]

# Create navigation buttons
for item in nav_items:
    nav_frame = ctk.CTkFrame(nav_bar, fg_color="transparent", width=80)
    nav_frame.pack(side="left", expand=True, fill="y")
    
    # Use active color for the current page, black for others
    text_color = "#22C55E" if item["active"] else "black"
    
    # Icon
    icon_label = ctk.CTkLabel(
        nav_frame,
        text=item["icon"],
        font=("Arial", 24),
        text_color=text_color
    )
    icon_label.pack(pady=(5, 0))
    
    # Text
    text_label = ctk.CTkLabel(
        nav_frame,
        text=item["name"],
        font=("Arial", 12),
        text_color=text_color
    )
    text_label.pack()

# Run the application
root.mainloop()