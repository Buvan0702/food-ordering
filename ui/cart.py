import customtkinter as ctk
from PIL import Image, ImageTk
import os

# Sample cart items
cart_items = [
    {"name": "Delicious Pizza", "price": 12.99, "quantity": 1, "image": "pizza.png"},
    {"name": "Tasty Burger", "price": 9.99, "quantity": 1, "image": "burger.png"},
    {"name": "Chocolate Cake", "price": 5.99, "quantity": 1, "image": "cake.png"}
]

class ShoppingCartApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Shopping Cart")
        self.geometry("900x600")
        self.configure(bg="white")

        # Header
        header = ctk.CTkLabel(self, text="🛒 Your Shopping Cart", font=("Arial", 20, "bold"), fg_color="white", text_color="black")
        header.pack(pady=10)

        # Cart Frame
        self.cart_frame = ctk.CTkFrame(self, fg_color="white")
        self.cart_frame.pack(pady=5, padx=10, fill="both", expand=True)

        # Create Cart Items
        self.cart_widgets = []
        self.total_price = ctk.DoubleVar()
        self.update_cart()

        # Bottom Total and Checkout Button
        self.bottom_frame = ctk.CTkFrame(self, fg_color="white")
        self.bottom_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(self.bottom_frame, text="Total:", font=("Arial", 14, "bold"), fg_color="white", text_color="black").pack(side="left", padx=10)
        self.total_label = ctk.CTkLabel(self.bottom_frame, text=f"${self.total_price.get():.2f}", font=("Arial", 14, "bold"), fg_color="white", text_color="black")
        self.total_label.pack(side="left")

        self.checkout_btn = ctk.CTkButton(self.bottom_frame, text="Proceed to Payment", font=("Arial", 12, "bold"),
                                          fg_color="green", text_color="white", width=200, height=40, command=self.checkout)
        self.checkout_btn.pack(side="right", padx=10)

        # Bottom Navigation Bar
        self.create_navbar()

    def load_image(self, path, size=(60, 60)):
        """Load an image, or use a default placeholder if missing"""
        if not os.path.exists(path):
            path = "default.png"  # Fallback image
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

    def update_cart(self):
        """Update cart items and total price"""
        for widget in self.cart_widgets:
            widget.destroy()

        self.cart_widgets = []
        self.total_price.set(0)

        for index, item in enumerate(cart_items):
            frame = ctk.CTkFrame(self.cart_frame, fg_color="white", border_color="gray", border_width=1)
            frame.pack(fill="x", padx=10, pady=5)

            # Item Image
            img = self.load_image(item["image"])
            img_label = ctk.CTkLabel(frame, image=img, text="")
            img_label.image = img
            img_label.pack(side="left", padx=10, pady=5)

            # Item Name and Price
            text_frame = ctk.CTkFrame(frame, fg_color="white")
            text_frame.pack(side="left", padx=10, fill="x", expand=True)
            ctk.CTkLabel(text_frame, text=item["name"], font=("Arial", 12, "bold"), fg_color="white", text_color="black").pack(anchor="w")
            ctk.CTkLabel(text_frame, text=f"${item['price']:.2f}", font=("Arial", 10), fg_color="white", text_color="gray").pack(anchor="w")

            # Quantity Controls
            qty_frame = ctk.CTkFrame(frame, fg_color="white")
            qty_frame.pack(side="right", padx=10)

            ctk.CTkButton(qty_frame, text="-", font=("Arial", 10, "bold"), fg_color="gray", text_color="white", width=30,
                          command=lambda i=index: self.update_quantity(i, -1)).pack(side="left", padx=5)

            ctk.CTkLabel(qty_frame, text=item["quantity"], font=("Arial", 12), fg_color="white", text_color="black").pack(side="left")

            ctk.CTkButton(qty_frame, text="+", font=("Arial", 10, "bold"), fg_color="gray", text_color="white", width=30,
                          command=lambda i=index: self.update_quantity(i, 1)).pack(side="left", padx=5)

            # Add to total price
            self.total_price.set(self.total_price.get() + (item["price"] * item["quantity"]))

        # Update total label
        self.total_label.configure(text=f"${self.total_price.get():.2f}")

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
        nav_frame = ctk.CTkFrame(self, fg_color="white", height=50)
        nav_frame.pack(side="bottom", fill="x")

        icons = ["home.png", "orders.png", "cart.png", "profile.png", "settings.png"]
        labels = ["Home", "Orders", "Cart", "Profile", "Settings"]

        for i in range(5):
            btn_frame = ctk.CTkFrame(nav_frame, fg_color="white")
            btn_frame.pack(side="left", expand=True)

            img = self.load_image(icons[i], size=(30, 30))
            img_label = ctk.CTkLabel(btn_frame, image=img, text="")
            img_label.image = img
            img_label.pack()

            ctk.CTkLabel(btn_frame, text=labels[i], font=("Arial", 10), fg_color="white", text_color="black").pack()


# Run the Tkinter App
if __name__ == "__main__":
    app = ShoppingCartApp()
    app.mainloop()
