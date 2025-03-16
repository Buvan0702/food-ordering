import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # For handling images

# Sample cart items
cart_items = [
    {"name": "Delicious Pizza", "price": 12.99, "quantity": 1, "image": "pizza.png"},
    {"name": "Tasty Burger", "price": 9.99, "quantity": 1, "image": "burger.png"},
    {"name": "Chocolate Cake", "price": 5.99, "quantity": 1, "image": "cake.png"}
]

class ShoppingCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping Cart")
        self.root.geometry("900x600")
        self.root.configure(bg="white")

        # Header
        header = tk.Label(root, text="Your Shopping Cart", font=("Arial", 18, "bold"), bg="white", fg="black")
        header.pack(pady=10)

        # Cart Frame
        self.cart_frame = tk.Frame(root, bg="white")
        self.cart_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # Create Cart Items
        self.cart_widgets = []
        self.total_price = tk.DoubleVar()
        self.update_cart()

        # Bottom Total and Checkout Button
        self.bottom_frame = tk.Frame(root, bg="white")
        self.bottom_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(self.bottom_frame, text="Total:", font=("Arial", 14, "bold"), bg="white").pack(side=tk.LEFT, padx=10)
        self.total_label = tk.Label(self.bottom_frame, text=f"${self.total_price.get():.2f}", font=("Arial", 14, "bold"), bg="white", fg="black")
        self.total_label.pack(side=tk.LEFT)

        self.checkout_btn = tk.Button(self.bottom_frame, text="Proceed to Payment", font=("Arial", 12, "bold"),
                                      bg="green", fg="white", relief="flat", width=20, height=2, command=self.checkout)
        self.checkout_btn.pack(side=tk.RIGHT, padx=10)

        # Bottom Navigation Bar
        self.create_navbar()

    def update_cart(self):
        """Update cart items and total price"""
        for widget in self.cart_widgets:
            widget.destroy()

        self.cart_widgets = []
        self.total_price.set(0)

        for index, item in enumerate(cart_items):
            frame = tk.Frame(self.cart_frame, bg="white", bd=1, relief="solid")
            frame.pack(fill=tk.X, padx=10, pady=5)

            # Item Image (Placeholder)
            img = Image.open(item["image"]).resize((60, 60))
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=img, bg="white")
            img_label.image = img
            img_label.pack(side=tk.LEFT, padx=10, pady=5)

            # Item Name and Price
            text_frame = tk.Frame(frame, bg="white")
            text_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
            tk.Label(text_frame, text=item["name"], font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
            tk.Label(text_frame, text=f"${item['price']:.2f}", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w")

            # Quantity Controls
            qty_frame = tk.Frame(frame, bg="white")
            qty_frame.pack(side=tk.RIGHT, padx=10)
            tk.Button(qty_frame, text="-", font=("Arial", 10, "bold"), bg="gray", fg="white", command=lambda i=index: self.update_quantity(i, -1)).pack(side=tk.LEFT, padx=5)
            tk.Label(qty_frame, text=item["quantity"], font=("Arial", 12), bg="white").pack(side=tk.LEFT)
            tk.Button(qty_frame, text="+", font=("Arial", 10, "bold"), bg="gray", fg="white", command=lambda i=index: self.update_quantity(i, 1)).pack(side=tk.LEFT, padx=5)

            # Add to total price
            self.total_price.set(self.total_price.get() + (item["price"] * item["quantity"]))

        # Update total label
        self.total_label.config(text=f"${self.total_price.get():.2f}")

    def update_quantity(self, index, change):
        """Update the quantity of an item"""
        if cart_items[index]["quantity"] + change > 0:
            cart_items[index]["quantity"] += change
            self.update_cart()

    def checkout(self):
        """Checkout button action"""
        print("Proceeding to Payment...")

    def create_navbar(self):
        """Creates a bottom navigation bar"""
        nav_frame = tk.Frame(self.root, bg="white", height=50)
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X)

        icons = ["home.png", "orders.png", "cart.png", "profile.png", "settings.png"]
        labels = ["Home", "Orders", "Cart", "Profile", "Settings"]

        for i in range(5):
            btn_frame = tk.Frame(nav_frame, bg="white")
            btn_frame.pack(side=tk.LEFT, expand=True)

            img = Image.open(icons[i]).resize((30, 30))
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(btn_frame, image=img, bg="white")
            img_label.image = img
            img_label.pack()

            tk.Label(btn_frame, text=labels[i], font=("Arial", 10), bg="white").pack()


# Run the Tkinter App
if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingCartApp(root)
    root.mainloop()
