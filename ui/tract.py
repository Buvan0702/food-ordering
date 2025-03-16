import tkinter as tk
from tkinter import Frame, Label, Button

# Main Window
root = tk.Tk()
root.title("Order Tracking")
root.geometry("1000x600")
root.configure(bg="white")

# Header Section
header = Frame(root, bg="white", height=70)
header.pack(fill=tk.X)
Label(header, text="Order Tracking", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

# Estimated Delivery Time Section
delivery_frame = Frame(root, bg="white")
delivery_frame.pack(fill=tk.X, pady=10, padx=20)

Label(delivery_frame, text="Estimated Delivery Time:", font=("Arial", 12, "bold"), bg="white").pack(side=tk.LEFT)
Label(delivery_frame, text="15:00", font=("Arial", 12, "bold"), fg="red", bg="white").pack(side=tk.RIGHT)

# Order Progress Bar
progress_frame = Frame(root, bg="white", height=40)
progress_frame.pack(fill=tk.X, padx=20)

Label(progress_frame, text="Order Placed ✅", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT, padx=20)
Label(progress_frame, text="Preparing 🔍", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT, padx=20)
Label(progress_frame, text="Out for Delivery 🚴", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT, padx=20)
Label(progress_frame, text="Delivered 🎉", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT, padx=20)

# Order Section
Label(root, text="Your Order", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=20, pady=10)

order_frame = Frame(root, bg="#F5F5F5", bd=2, relief="solid", width=900, height=100)
order_frame.pack(pady=5, padx=20, fill=tk.X)

# Placeholder for food image
food_placeholder = Frame(order_frame, bg="lightgray", width=80, height=80)
food_placeholder.pack(side=tk.LEFT, padx=10, pady=10)
Label(food_placeholder, text="80×80", font=("Arial", 10), bg="lightgray").pack(expand=True)

# Food Details
food_details = Frame(order_frame, bg="#F5F5F5")
food_details.pack(side=tk.LEFT, padx=10, pady=10)

Label(food_details, text="Pizza", font=("Arial", 12, "bold"), bg="#F5F5F5").pack(anchor="w")
Label(food_details, text="$12.99", font=("Arial", 12), bg="#F5F5F5").pack(anchor="w")

# Quantity
Label(order_frame, text="Quantity: 1", font=("Arial", 12), bg="#F5F5F5").pack(side=tk.RIGHT, padx=20)

# Delivery Location Section
Label(root, text="Delivery Location", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=20, pady=10)

location_frame = Frame(root, bg="white")
location_frame.pack(fill=tk.X, padx=20)

map_placeholder = Frame(location_frame, bg="lightgray", width=600, height=100)
map_placeholder.pack(pady=5, padx=10)
Label(map_placeholder, text="Map Placeholder", font=("Arial", 12), bg="lightgray").pack(expand=True)

# Bottom Navigation Bar
nav_bar = Frame(root, bg="white", height=50)
nav_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Navigation Bar Items with Icons
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
