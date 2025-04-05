import customtkinter as ctk
import subprocess
import sys
from db_connection import DatabaseConnection

class ShoppingCartApp:
    def __init__(self, user_id=None):
        # Configure CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Create the main window
        self.root = ctk.CTk()
        self.root.title("Shopping Cart")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)

        # Store user ID
        self.user_id = user_id

        # Cart items list
        self.cart_items = []

        # Main white frame with rounded corners
        self.setup_ui()

    def fetch_cart_items(self):
        """
        Fetch cart items from database for the current user
        """
        if not self.user_id:
            return []

        try:
            query = """
            SELECT ci.cart_item_id, mi.menu_item_id, mi.item_name, mi.price, ci.quantity, r.restaurant_name
            FROM CartItems ci
            JOIN MenuItems mi ON ci.menu_item_id = mi.menu_item_id
            JOIN Restaurants r ON mi.restaurant_id = r.restaurant_id
            WHERE ci.user_id = %s
            """
            cart_items = DatabaseConnection.execute_query(
                query, 
                params=(self.user_id,), 
                fetch=True
            )
            return cart_items
        except Exception as e:
            print(f"Error fetching cart items: {e}")
            return []

    def setup_ui(self):
        """
        Setup the user interface for the cart page
        """
        # Main white frame with rounded corners
        self.main_frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=20)
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

        # Fetch and create cart items
        self.cart_items = self.fetch_cart_items()
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
        total_amount = sum(item.get('price', 0) * item.get('quantity', 0) for item in self.cart_items)
        
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
            height=50,
            command=self.proceed_to_payment
        )
        self.checkout_button.pack(pady=(0, 30))

        # Bottom Navigation
        self.create_bottom_navigation()

    def create_cart_items(self):
        """Create cart item rows"""
        # Clear existing widgets
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()

        # Separator line at the top
        self.separator_top = ctk.CTkFrame(
            self.cart_items_frame, 
            height=1, 
            fg_color="#E5E7EB"
        )
        self.separator_top.pack(fill="x", pady=(0, 15))

        # Show message if cart is empty
        if not self.cart_items:
            empty_cart_label = ctk.CTkLabel(
                self.cart_items_frame,
                text="Your cart is empty",
                font=("Arial", 16),
                text_color="#6B7280"
            )
            empty_cart_label.pack(pady=20)
            return

        for item in self.cart_items:
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
            
            food_label = ctk.CTkLabel(
                img_placeholder, 
                text=item.get('restaurant_name', 'Food Item'), 
                text_color="#9CA3AF", 
                font=("Arial", 9)
            )
            food_label.place(relx=0.5, rely=0.5, anchor="center")

            # Item name and price
            name_label = ctk.CTkLabel(
                item_frame, 
                text=item.get('item_name', 'Unknown Item'), 
                font=("Arial", 16, "bold"), 
                text_color="#1F2937",
                anchor="w"
            )
            name_label.place(x=90, y=15)
            
            price_label = ctk.CTkLabel(
                item_frame, 
                text=f"${item.get('price', 0):.2f}", 
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
                corner_radius=5,
                command=lambda cart_item=item: self.update_quantity(cart_item, -1)
            )
            minus_btn.place(relx=0.95, y=25, anchor="e", x=-70)
            
            # Quantity
            qty_label = ctk.CTkLabel(
                item_frame,
                text=f"{item.get('quantity', 0)}",
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
                corner_radius=5,
                command=lambda cart_item=item: self.update_quantity(cart_item, 1)
            )
            plus_btn.place(relx=0.95, y=25, anchor="e", x=-10)

            # Separator line after each item (except the last one)
            if item != self.cart_items[-1]:
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

    def update_quantity(self, cart_item, change):
        """
        Update quantity of an item in the cart
        """
        try:
            # Update quantity in database
            update_query = """
            UPDATE CartItems 
            SET quantity = GREATEST(0, quantity + %s)
            WHERE cart_item_id = %s
            """
            DatabaseConnection.execute_query(
                update_query, 
                params=(change, cart_item.get('cart_item_id'))
            )

            # Refresh cart items
            self.cart_items = self.fetch_cart_items()
            self.create_cart_items()

            # Update total amount
            total_amount = sum(item.get('price', 0) * item.get('quantity', 0) for item in self.cart_items)
            self.total_amount_label.configure(text=f"${total_amount:.2f}")

        except Exception as e:
            print(f"Error updating cart item quantity: {e}")

    def proceed_to_payment(self):
        """
        Navigate to payment page
        """
        try:
            subprocess.Popen([sys.executable, "payment.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error proceeding to payment: {e}")

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
            {"name": "Home", "icon": "🏠", "action": self.go_to_home},
            {"name": "Orders", "icon": "📦", "action": self.go_to_orders},
            {"name": "Cart", "icon": "🛒", "action": self.stay_on_cart, "active": True},
            {"name": "Profile", "icon": "👤", "action": self.go_to_profile},
            {"name": "Settings", "icon": "⚙️", "action": self.go_to_settings}
        ]
        
        # Create navigation buttons
        for item in nav_items:
            nav_frame = ctk.CTkFrame(nav_bar, fg_color="transparent", width=80)
            nav_frame.pack(side="left", expand=True, fill="y")
            
            # Color for active/inactive items
            text_color = "#22C55E" if item.get("active", False) else "#1F2937"
            
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

            # Bind click events
            for widget in [icon_label, text_label]:
                widget.bind("<Button-1>", lambda e, action=item['action']: action())

    def go_to_home(self):
        """Navigate to home page"""
        try:
            subprocess.Popen([sys.executable, "home.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error going to home: {e}")

    def go_to_orders(self):
        """Navigate to orders page"""
        try:
            subprocess.Popen([sys.executable, "track.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error going to orders: {e}")

    def stay_on_cart(self):
        """Do nothing, already on cart page"""
        pass

    def go_to_profile(self):
        """Navigate to profile page"""
        try:
            subprocess.Popen([sys.executable, "profile.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error going to profile: {e}")

    def go_to_settings(self):
        """Navigate to settings page"""
        try:
            subprocess.Popen([sys.executable, "settings.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error going to settings: {e}")

def main():
    # Check if user ID is passed as command-line argument
    user_id = None
    if len(sys.argv) > 1:
        try:
            user_id = int(sys.argv[1])
        except ValueError:
            print("Invalid user ID")

    # Create and run cart page
    app = ShoppingCartApp(user_id)
    app.root.mainloop()

if __name__ == "__main__":
    main()