import customtkinter as ctk
import subprocess
import sys
import re
from db_connection import DatabaseConnection
from password_utility import PasswordManager

class UserProfileApp:
    def __init__(self, user_id=None):
        # Configure CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Create the main window
        self.root = ctk.CTk()
        self.root.title("User Profile")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)

        # Store user ID
        self.user_id = user_id

        # Fetch user data
        self.user_data = self.fetch_user_data()
        self.past_orders = self.fetch_past_orders()

        # Setup UI
        self.setup_ui()

    def fetch_user_data(self):
        """
        Fetch user details from the database
        """
        if not self.user_id:
            return None
        
        try:
            query = """
            SELECT user_id, first_name, last_name, email, phone_number, address 
            FROM Users 
            WHERE user_id = %s
            """
            results = DatabaseConnection.execute_query(
                query, 
                params=(self.user_id,), 
                fetch=True
            )
            
            return results[0] if results else None
        except Exception as e:
            print(f"Error fetching user details: {e}")
            return None

    def fetch_past_orders(self):
        """
        Fetch past orders for the user
        """
        if not self.user_id:
            return []
        
        try:
            query = """
            SELECT o.order_id, r.restaurant_name, o.order_date, o.total_amount
            FROM Orders o
            JOIN Restaurants r ON o.restaurant_id = r.restaurant_id
            WHERE o.user_id = %s AND o.status = 'Delivered'
            ORDER BY o.order_date DESC
            LIMIT 5
            """
            results = DatabaseConnection.execute_query(
                query, 
                params=(self.user_id,), 
                fetch=True
            )
            
            return results
        except Exception as e:
            print(f"Error fetching past orders: {e}")
            return []

    def setup_ui(self):
        """
        Setup the user interface for the profile page
        """
        # Main white background with rounded corners
        self.main_frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text="User Profile", 
            font=("Arial", 28, "bold"), 
            text_color="#1F2937"
        )
        self.header_label.pack(pady=(30, 20))

        # Past Orders Section
        self.past_orders_label = ctk.CTkLabel(
            self.main_frame, 
            text="Past Orders", 
            font=("Arial", 20, "bold"), 
            text_color="#1F2937",
            anchor="w"
        )
        self.past_orders_label.pack(anchor="w", padx=50, pady=(20, 10))

        # Past Orders Container
        self.create_past_orders()

        # Profile & Settings Section
        self.profile_settings_label = ctk.CTkLabel(
            self.main_frame, 
            text="Profile & Settings", 
            font=("Arial", 20, "bold"), 
            text_color="#1F2937",
            anchor="w"
        )
        self.profile_settings_label.pack(anchor="w", padx=50, pady=(30, 10))

        # Profile Info Container
        self.create_profile_info()

        # Bottom Navigation
        self.create_bottom_navigation()

    def create_past_orders(self):
        """Create past orders section with cards"""
        # Container for order cards
        orders_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        orders_container.pack(fill="x", padx=50, pady=5)

        # Show message if no past orders
        if not self.past_orders:
            no_orders_label = ctk.CTkLabel(
                orders_container, 
                text="No past orders found", 
                font=("Arial", 16), 
                text_color="#6B7280"
            )
            no_orders_label.pack(pady=20)
            return

        # Create cards for each past order
        for order in self.past_orders:
            # Order card
            order_card = ctk.CTkFrame(
                orders_container, 
                fg_color="white", 
                width=280, 
                height=150, 
                corner_radius=10,
                border_width=1,
                border_color="#E5E7EB"
            )
            order_card.pack(side="left", padx=10, pady=5)
            
            # Restaurant name
            restaurant_label = ctk.CTkLabel(
                order_card, 
                text=order.get('restaurant_name', 'Unknown Restaurant'), 
                font=("Arial", 16, "bold"), 
                text_color="#1F2937",
                anchor="w"
            )
            restaurant_label.place(x=20, y=20)
            
            # Order date
            date_label = ctk.CTkLabel(
                order_card, 
                text=f"Order Date: {order.get('order_date', 'N/A')}", 
                font=("Arial", 14), 
                text_color="#6B7280",
                anchor="w"
            )
            date_label.place(x=20, y=50)
            
            # Order amount (in green)
            amount_label = ctk.CTkLabel(
                order_card, 
                text=f"${order.get('total_amount', 0):.2f}", 
                font=("Arial", 16, "bold"), 
                text_color="#22C55E",
                anchor="w"
            )
            amount_label.place(x=20, y=80)
            
            # Reorder button (orange)
            reorder_btn = ctk.CTkButton(
                order_card, 
                text="Reorder", 
                font=("Arial", 14, "bold"), 
                fg_color="#F97316", 
                text_color="white", 
                corner_radius=5,
                hover_color="#EA580C",
                width=240, 
                height=35,
                command=lambda o=order: self.reorder(o)
            )
            reorder_btn.place(x=20, y=110)

    def reorder(self, order):
        """
        Reorder functionality
        """
        try:
            # Fetch order items
            query = """
            SELECT menu_item_id, quantity 
            FROM OrderItems 
            WHERE order_id = %s
            """
            order_items = DatabaseConnection.execute_query(
                query, 
                params=(order.get('order_id'),), 
                fetch=True
            )

            # Add items to cart
            for item in order_items:
                self.add_to_cart(item['menu_item_id'], item['quantity'])

            # Navigate to cart
            subprocess.Popen([sys.executable, "cart.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error reordering: {e}")

    def add_to_cart(self, menu_item_id, quantity):
        """
        Add item to cart
        """
        try:
            # Check if item already in cart
            check_query = """
            SELECT cart_item_id 
            FROM CartItems 
            WHERE user_id = %s AND menu_item_id = %s
            """
            existing_cart_item = DatabaseConnection.execute_query(
                check_query, 
                params=(self.user_id, menu_item_id), 
                fetch=True
            )

            if existing_cart_item:
                # Update quantity if item exists
                update_query = """
                UPDATE CartItems 
                SET quantity = quantity + %s 
                WHERE user_id = %s AND menu_item_id = %s
                """
                DatabaseConnection.execute_query(
                    update_query, 
                    params=(quantity, self.user_id, menu_item_id)
                )
            else:
                # Insert new cart item
                insert_query = """
                INSERT INTO CartItems (user_id, menu_item_id, quantity) 
                VALUES (%s, %s, %s)
                """
                DatabaseConnection.execute_query(
                    insert_query, 
                    params=(self.user_id, menu_item_id, quantity)
                )
        except Exception as e:
            print(f"Error adding to cart: {e}")

    def create_profile_info(self):
        """Create profile information section"""
        # Profile info container
        profile_container = ctk.CTkFrame(
            self.main_frame, 
            fg_color="white", 
            corner_radius=10,
            border_width=1,
            border_color="#E5E7EB"
        )
        profile_container.pack(fill="x", padx=50, pady=5)

        # Prepare user data
        full_name = (f"{self.user_data.get('first_name', '')} {self.user_data.get('last_name', '')}").strip()
        
        # User information fields
        fields = [
            {"label": "Name:", "value": full_name},
            {"label": "Email:", "value": self.user_data.get('email', 'N/A')},
            {"label": "Phone:", "value": self.user_data.get('phone_number', 'N/A')},
            {"label": "Address:", "value": self.user_data.get('address', 'N/A')}
        ]

        # Add each field with proper spacing
        for i, field in enumerate(fields):
            # Label
            label = ctk.CTkLabel(
                profile_container, 
                text=field["label"], 
                font=("Arial", 14), 
                text_color="#1F2937",
                anchor="w"
            )
            label.grid(row=i, column=0, sticky="w", padx=(20, 10), pady=15)
            
            # Value (right-aligned)
            value = ctk.CTkLabel(
                profile_container, 
                text=field["value"], 
                font=("Arial", 14), 
                text_color="#1F2937",
                anchor="e"
            )
            value.grid(row=i, column=1, sticky="e", padx=(10, 20), pady=15)

        # Configure grid to make value column expand
        profile_container.grid_columnconfigure(1, weight=1)
        
        # Edit Profile Button (green)
        edit_btn = ctk.CTkButton(
            profile_container, 
            text="Edit Profile", 
            font=("Arial", 14, "bold"), 
            fg_color="#22C55E", 
            text_color="white", 
            corner_radius=5,
            hover_color="#16A34A",
            width=880, 
            height=40,
            command=self.open_edit_profile
        )
        edit_btn.grid(row=len(fields), column=0, columnspan=2, padx=20, pady=20, sticky="ew")

    def open_edit_profile(self):
        """
        Open profile editing window
        """
        # Create edit profile window
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Edit Profile")
        edit_window.geometry("600x500")
        edit_window.resizable(False, False)

        # Edit profile form
        edit_frame = ctk.CTkFrame(edit_window, fg_color="white")
        edit_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # First Name
        first_name_label = ctk.CTkLabel(edit_frame, text="First Name", font=("Arial", 14))
        first_name_label.pack(anchor="w", padx=20, pady=(20, 5))
        first_name_entry = ctk.CTkEntry(edit_frame, width=500, font=("Arial", 14))
        first_name_entry.pack(anchor="w", padx=20)
        first_name_entry.insert(0, self.user_data.get('first_name', ''))

        # Last Name
        last_name_label = ctk.CTkLabel(edit_frame, text="Last Name", font=("Arial", 14))
        last_name_label.pack(anchor="w", padx=20, pady=(20, 5))
        last_name_entry = ctk.CTkEntry(edit_frame, width=500, font=("Arial", 14))
        last_name_entry.pack(anchor="w", padx=20)
        last_name_entry.insert(0, self.user_data.get('last_name', ''))

        # Phone Number
        phone_label = ctk.CTkLabel(edit_frame, text="Phone Number", font=("Arial", 14))
        phone_label.pack(anchor="w", padx=20, pady=(20, 5))
        phone_entry = ctk.CTkEntry(edit_frame, width=500, font=("Arial", 14))
        phone_entry.pack(anchor="w", padx=20)
        phone_entry.insert(0, self.user_data.get('phone_number', ''))

        # Address
        address_label = ctk.CTkLabel(edit_frame, text="Address", font=("Arial", 14))
        address_label.pack(anchor="w", padx=20, pady=(20, 5))
        address_entry = ctk.CTkEntry(edit_frame, width=500, font=("Arial", 14))
        address_entry.pack(anchor="w", padx=20)
        address_entry.insert(0, self.user_data.get('address', ''))

        # Save Button
        save_btn = ctk.CTkButton(
            edit_frame, 
            text="Save Changes", 
            font=("Arial", 14, "bold"), 
            fg_color="#22C55E", 
            text_color="white", 
            corner_radius=5,
            hover_color="#16A34A",
            width=500, 
            height=40,
            command=lambda: self.save_profile_changes(
                first_name_entry.get(), 
                last_name_entry.get(), 
                phone_entry.get(), 
                address_entry.get(),
                edit_window
            )
        )
        save_btn.pack(anchor="w", padx=20, pady=30)

    def save_profile_changes(self, first_name, last_name, phone, address, window):
        """
        Save profile changes to database
        """
        try:
            # Validate inputs
            if not first_name or not last_name:
                ctk.CTkMessagebox.showerror("Validation Error", "First and Last name are required")
                return

            # Validate phone number
            if phone and not re.match(r'^\+?1?\d{10,14}$', phone):
                ctk.CTkMessagebox.showerror("Validation Error", "Invalid phone number")
                return

            # Update user profile in database
            update_query = """
            UPDATE Users 
            SET first_name = %s, 
                last_name = %s, 
                phone_number = %s, 
                address = %s
            WHERE user_id = %s
            """
            DatabaseConnection.execute_query(
                update_query, 
                params=(first_name, last_name, phone, address, self.user_id)
            )

            # Refresh user data
            self.user_data = self.fetch_user_data()

            # Close edit window
            window.destroy()

            # Recreate profile info section
            for widget in self.main_frame.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and widget != self.main_frame:
                    widget.destroy()

            self.create_past_orders()
            self.create_profile_info()

            # Show success message
            ctk.CTkMessagebox.showinfo("Success", "Profile updated successfully")

        except Exception as e:
            print(f"Error saving profile changes: {e}")
            ctk.CTkMessagebox.showerror("Error", "Failed to update profile")

    def create_bottom_navigation(self):
        """Create bottom navigation bar"""
        nav_bar = ctk.CTkFrame(
            self.main_frame,
            fg_color="white",
            height=70,
            corner_radius=0
        )
        nav_bar.pack(side="bottom", fill="x")
        
        # Define navigation items
        nav_items = [
            {"name": "Home", "icon": "🏠", "action": self.go_to_home},
            {"name": "Orders", "icon": "📦", "action": self.go_to_orders},
            {"name": "Cart", "icon": "🛒", "action": self.go_to_cart},
            {"name": "Profile", "icon": "👤", "action": self.stay_on_profile, "active": True},
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

    def go_to_cart(self):
        """Navigate to cart page"""
        try:
            subprocess.Popen([sys.executable, "cart.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error going to cart: {e}")

    def stay_on_profile(self):
        """Do nothing, already on profile page"""
        pass

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

    # Create and run profile page
    app = UserProfileApp(user_id)
    app.root.mainloop()

if __name__ == "__main__":
    main()