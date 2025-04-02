import customtkinter as ctk
import subprocess
import os

os.environ['TCL_LIBRARY'] = r"C:\Users\buvan\AppData\Local\Programs\Python\Python39\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\buvan\AppData\Local\Programs\Python\Python39\tcl\tk8.6"

# Configure CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Sample cart items
cart_items = [
    {"name": "Delicious Pizza", "price": 12.99, "quantity": 1},
    {"name": "Tasty Burger", "price": 9.99, "quantity": 1},
    {"name": "Chocolate Cake", "price": 5.99, "quantity": 1}
]

class ShoppingCartApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Shopping Cart")
        self.geometry("1000x800")
        self.resizable(False, False)

        # Main white frame with rounded corners
        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text="Your Shopping Cart", 
            font=("Arial", 24, "bold"), 
            text_color="#1F2937"
        )
        self.header_label.pack(pady=(30, 20))

        # Cart items frame
        self.cart_items_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="white", 
            width=800
        )
        self.cart_items_frame.pack(fill="both", expand=True, padx=50, pady=0)

        # Create cart items
        self.create_cart_items()

        # Total section
        self.total_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="white", 
            height=60
        )
        self.total_frame.pack(fill="x", padx=50, pady=(10, 20))

        # Total label
        self.total_label = ctk.CTkLabel(
            self.total_frame, 
            text="Total:", 
            font=("Arial", 18, "bold"), 
            text_color="#1F2937"
        )
        self.total_label.place(x=0, y=15)

        # Calculate total
        total_amount = sum(item["price"] * item["quantity"] for item in cart_items)
        
        # Total amount
        self.total_amount_label = ctk.CTkLabel(
            self.total_frame, 
            text=f"${total_amount:.2f}", 
            font=("Arial", 18, "bold"), 
            text_color="#1F2937"
        )
        self.total_amount_label.place(relx=0.95, y=15, anchor="e")

        # Proceed to Payment button
        self.checkout_button = ctk.CTkButton(
            self.main_frame,
            text="Proceed to Payment",
            font=("Arial", 16, "bold"),
            fg_color="#22C55E",
            text_color="white",
            hover_color="#16A34A",
            corner_radius=5,
            width=700,
            height=50
        )
        self.checkout_button.pack(pady=(0, 30))

        # Bottom Navigation
        self.create_bottom_navigation()

    def create_cart_items(self):
        """Create cart item rows"""
        # Separator line at the top
        self.separator_top = ctk.CTkFrame(
            self.cart_items_frame, 
            height=1, 
            fg_color="#E5E7EB"
        )
        self.separator_top.pack(fill="x", pady=(0, 15))

        for item in cart_items:
            # Item frame
            item_frame = ctk.CTkFrame(
                self.cart_items_frame,
                fg_color="white",
                height=80
            )
            item_frame.pack(fill="x", pady=10)
            item_frame.pack_propagate(False)
            
            # Image placeholder
            img_placeholder = ctk.CTkFrame(
                item_frame,
                fg_color="#E5E7EB",
                width=70,
                height=70,
                corner_radius=5
            )
            img_placeholder.place(x=0, y=5)
            
            food_label = ctk.CTkLabel(img_placeholder, text="Food Item", text_color="#9CA3AF", font=("Arial", 9))
            food_label.place(relx=0.5, rely=0.5, anchor="center")

            # Item name and price
            name_label = ctk.CTkLabel(
                item_frame, 
                text=item["name"], 
                font=("Arial", 16, "bold"), 
                text_color="#1F2937",
                anchor="w"
            )
            name_label.place(x=90, y=15)
            
            price_label = ctk.CTkLabel(
                item_frame, 
                text=f"${item['price']:.2f}", 
                font=("Arial", 14), 
                text_color="#6B7280",
                anchor="w"
            )
            price_label.place(x=90, y=45)
            
            # Quantity buttons
            # Minus button
            minus_btn = ctk.CTkButton(
                item_frame,
                text="-",
                font=("Arial", 16, "bold"),
                fg_color="#E5E7EB",
                text_color="#4B5563",
                hover_color="#D1D5DB",
                width=35,
                height=35,
                corner_radius=5
            )
            minus_btn.place(relx=0.95, y=25, anchor="e", x=-70)
            
            # Quantity
            qty_label = ctk.CTkLabel(
                item_frame,
                text=f"{item['quantity']}",
                font=("Arial", 15),
                text_color="#1F2937"
            )
            qty_label.place(relx=0.95, y=25, anchor="e", x=-40)
            
            # Plus button
            plus_btn = ctk.CTkButton(
                item_frame,
                text="+",
                font=("Arial", 16, "bold"),
                fg_color="#E5E7EB",
                text_color="#4B5563",
                hover_color="#D1D5DB",
                width=35,
                height=35,
                corner_radius=5
            )
            plus_btn.place(relx=0.95, y=25, anchor="e", x=-10)

            # Separator line after each item (except the last one)
            if item != cart_items[-1]:
                separator = ctk.CTkFrame(
                    self.cart_items_frame, 
                    height=1, 
                    fg_color="#E5E7EB"
                )
                separator.pack(fill="x", pady=(15, 0))

        # Separator line at the bottom
        self.separator_bottom = ctk.CTkFrame(
            self.cart_items_frame, 
            height=1, 
            fg_color="#E5E7EB"
        )
        self.separator_bottom.pack(fill="x", pady=(15, 0))

    def create_bottom_navigation(self):
        """Create bottom navigation bar"""
        nav_bar = ctk.CTkFrame(
            self.main_frame,
            fg_color="white",
            height=80,
            corner_radius=0
        )
        nav_bar.pack(side="bottom", fill="x")
        
        # Define navigation items
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
            
            # Color for active/inactive items
            text_color = "#22C55E" if item["active"] else "#1F2937"
            
            # Icon
            icon_label = ctk.CTkLabel(
                nav_frame,
                text=item["icon"],
                font=("Arial", 24),
                text_color=text_color
            )
            icon_label.pack(pady=(10, 0))
            
            # Text
            text_label = ctk.CTkLabel(
                nav_frame,
                text=item["name"],
                font=("Arial", 12),
                text_color=text_color
            )
            text_label.pack()

# Run the application
if __name__ == "__main__":
    app = ShoppingCartApp()
    app.mainloop()