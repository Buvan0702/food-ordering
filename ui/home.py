import tkinter as tk
from tkinter import Frame, Entry, Button, Label

# Main Window
root = tk.Tk()
root.title("Food Delivery UI")
root.geometry("1000x600")
root.configure(bg="white")

# Header
Label(root, text="Find Your Favorite Food", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

# Search Bar
search_bar = Entry(root, font=("Arial", 12), width=80, relief="solid", bd=1)
search_bar.insert(0, "🔍 Search for restaurants or dishes...")  # Placeholder
search_bar.pack(pady=5, ipady=5)

# Category Buttons
categories = ["FastFood", "Desserts", "Healthy", "Indian", "Chinese"]
colors = ["#2ECC71", "#E67E22", "#E74C3C", "#F1C40F", "#8E44AD"]

category_frame = Frame(root, bg="white")
category_frame.pack(pady=10)

for i, category in enumerate(categories):
    Button(category_frame, text=category, font=("Arial", 10), bg=colors[i], fg="white", padx=10, pady=5, relief="flat").pack(side=tk.LEFT, padx=5)

# Restaurant Listings
restaurant_frame = Frame(root, bg="white")
restaurant_frame.pack(pady=10)

restaurants = [
    ("Restaurant 1", "Pizza Place", "⭐️⭐️⭐️⭐️ (4.4)", "Estimated Delivery: 30 mins"),
    ("Restaurant 2", "Burger Haven", "⭐️⭐️⭐️⭐️⭐️ (4.5)", "Estimated Delivery: 25 mins"),
    ("Restaurant 3", "Sweet Treats", "⭐️⭐️⭐️ (3.5)", "Estimated Delivery: 20 mins")
]

for res_name, res_title, rating, delivery in restaurants:
    card = Frame(restaurant_frame, bg="white", bd=2, relief="solid", width=300, height=200)
    card.pack(side=tk.LEFT, padx=10, pady=10)

    # Placeholder for Image
    Label(card, text=res_name, font=("Arial", 14, "bold"), bg="lightgray", width=30, height=6).pack()

    # Restaurant Details
    Label(card, text=res_title, font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=5)
    Label(card, text=rating, font=("Arial", 10), bg="white").pack(anchor="w", padx=10)
    Label(card, text=delivery, font=("Arial", 10), bg="white").pack(anchor="w", padx=10)

    # View Menu Button
    Button(card, text="View Menu", font=("Arial", 10, "bold"), bg="green", fg="white", relief="flat", width=20).pack(pady=10)

# Bottom Navigation Bar with Emojis
nav_bar = Frame(root, bg="white", height=50)
nav_bar.pack(side=tk.BOTTOM, fill=tk.X)

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
