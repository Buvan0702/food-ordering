import tkinter as tk
from tkinter import Frame, Label, Button

# Main Window
root = tk.Tk()
root.title("Restaurant Menu")
root.geometry("1000x600")
root.configure(bg="white")

# Back Button
back_btn = Button(root, text="⬅ Back", font=("Arial", 10), bg="lightgreen", relief="flat", padx=10, pady=5)
back_btn.place(x=10, y=10)

# Restaurant Banner
banner = Frame(root, bg="lightgray", width=1000, height=100)
banner.place(x=0, y=40)
Label(banner, text="Restaurant Banner", font=("Arial", 36, "bold"), bg="lightgray").pack(expand=True)

# Menu Section Title
Label(root, text="Menu", font=("Arial", 14, "bold"), bg="white").place(x=50, y=160)

# Food Items List
food_items = [
    ("Pizza", "Margherita Pizza", "$12.99"),
    ("Burger", "Cheeseburger", "$9.99"),
    ("Salad", "Caesar Salad", "$8.99")
]

# Creating Food Item Cards
menu_frame = Frame(root, bg="white")
menu_frame.place(x=50, y=200)

x_offset = 0
for item, title, price in food_items:
    # Card Container
    card = Frame(menu_frame, bg="white", bd=2, relief="solid", width=280, height=220)
    card.place(x=x_offset, y=0)

    # Placeholder Image (Food Item)
    img_placeholder = Frame(card, bg="lightgray", width=280, height=100)
    img_placeholder.pack()
    Label(img_placeholder, text=item, font=("Arial", 28, "bold"), bg="lightgray", fg="gray").pack(expand=True)

    # Food Title
    Label(card, text=title, font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=5)

    # Price (Green)
    Label(card, text=price, font=("Arial", 12, "bold"), fg="green", bg="white").pack(anchor="e", padx=10, pady=5)

    # Add to Cart Button
    Button(card, text="Add to Cart", font=("Arial", 10, "bold"), bg="green", fg="white", relief="flat", width=20).pack(pady=10)

    x_offset += 300  # Move next item to the right

# Bottom Navigation Bar
nav_bar = Frame(root, bg="white", height=50)
nav_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Navigation Bar Items with Emojis
nav_items = [
    ("🏠 Home", "#2ECC71"),
    ("📦 Orders", "#E67E22"),
    ("🛒 Cart", "#3498DB"),
    ("👤 Profile", "#9B59B6"),
    ("⚙️ Settings", "#95A5A6")
]

for item, color in nav_items:
    Button(nav_bar, text=item, font=("Arial", 10), bg="white", fg=color, relief="flat").pack(side=tk.LEFT, expand=True, padx=20, pady=10)

root.mainloop()
