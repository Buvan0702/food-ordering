import customtkinter as ctk
import subprocess
import sys
import re
import os
from PIL import Image
from db_connection import DatabaseConnection
from password_utility import PasswordManager
from image_handler import ImageHandler

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
        
        # Initialize image handler
        self.image_handler = ImageHandler()

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
            SELECT o.order_id, r.restaurant_id, r.restaurant_name, o.order_date, o.total_amount
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

        # Header with user avatar
        self.create_header()

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
        
    def create_header(self):
        """Create header with user avatar"""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=100)
        header_frame.pack(fill="x", padx=50, pady=(20, 10))
        
        # User avatar frame (circular)
        avatar_size = 80
        avatar_frame = ctk.CTkFrame(
            header_frame, 
            width=avatar_size, 
            height=avatar_size, 
            corner_radius=avatar_size//2,
            fg_color="#E5E7EB"
        )
        avatar_frame.pack(side="left", padx=(0, 20))
        
        # User initial or avatar
        if self.user_data:
            initials = (self.user_data.get('first_name', 'U')[0] + self.user_data.get('last_name', '')[0:1]).upper()
        else:
            initials = "U"
            
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text=initials,
            font=("Arial", 36, "bold"),
            text_color="#4B5563"
        )
        avatar_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # User name and header
        if self.user_data:
            full_name = f"{self.user_data.get('first_name', '')} {self.user_data.get('last_name', '')}".strip()
            header_text = f"{full_name}'s Profile"
        else:
            header_text = "User Profile"
            
        header_label = ctk.CTkLabel(
            header_frame, 
            text=header_text, 
            font=("Arial", 28, "bold"), 
            text_color="#1F2937"
        )
        header_label.pack(side="left", pady=(20, 0))

    def create_past_orders(self):
        """Create past orders section with cards and images"""
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
            
            # Restaurant image (small)
            img_frame = ctk.CTkFrame(
                order_card,
                fg_color="#F3F4F6",
                width=40,
                height=40,
                corner_radius=20
            )
            img_frame.place(x=20, y=20)
            
            # Try to get restaurant image for the order
            restaurant_id = order.get('restaurant_id')
            if restaurant_id:
                restaurant_image = self.image_handler.get_restaurant_image(restaurant_id, size=(40, 40))
                if restaurant_image:
                    img_label = ctk.CTkLabel(img_frame, image=restaurant_image, text="")
                    img_label.place(relx=0.5, rely=0.5, anchor="center")
                else:
                    # Fallback to first letter of restaurant name
                    rest_initial = order.get('restaurant_name', 'R')[0].upper()
                    initial_label = ctk.CTkLabel(
                        img_frame,
                        text=rest_initial,
                        font=("Arial", 16, "bold"),
                        text_color="#6B7280"
                    )
                    initial_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Restaurant name
            restaurant_label = ctk.CTkLabel(
                order_card, 
                text=order.get('restaurant_name', 'Unknown Restaurant'), 
                font=("Arial", 16, "bold"), 
                text_color="#1F2937",
                anchor="w"
            )
            restaurant_label.place(x=70, y=20)
            
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

            # Show confirmation message
            confirmation = ctk.CTkToplevel(self.root)
            confirmation.title("Order Added to Cart")
            confirmation.geometry("300x150")
            confirmation.resizable(False, False)
            confirmation.grab_set()
            
            # Message
            msg_label = ctk.CTkLabel(
                confirmation,
                text="Items added to your cart!",
                font=("Arial", 16)
            )
            msg_label.pack(pady=(30, 20))
            
            # Buttons frame
            buttons_frame = ctk.CTkFrame(confirmation, fg_color="transparent")
            buttons_frame.pack(pady=10)
            
            # Continue button
            continue_btn = ctk.CTkButton(
                buttons_frame,
                text="Continue Shopping",
                font=("Arial", 14),
                fg_color="#6B7280",
                text_color="white",
                hover_color="#4B5563",
                command=lambda: confirmation.destroy()
            )
            continue_btn.pack(side="left", padx=5)
            
            # Go to cart button
            cart_btn = ctk.CTkButton(
                buttons_frame,
                text="Go to Cart",
                font=("Arial", 14),
                fg_color="#22C55E",
                text_color="white",
                hover_color="#16A34A",
                command=lambda: self.go_to_cart_confirm(confirmation)
            )
            cart_btn.pack(side="left", padx=5)
            
        except Exception as e:
            print(f"Error reordering: {e}")
            
    def go_to_cart_confirm(self, confirmation_window):
        """Navigate to cart from the confirmation window"""
        confirmation_window.destroy()
        self.go_to_cart()

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
            {"label": "Name:", "value": full_name, "icon": "👤"},
            {"label": "Email:", "value": self.user_data.get('email', 'N/A'), "icon": "✉️"},
            {"label": "Phone:", "value": self.user_data.get('phone_number', 'N/A'), "icon": "📱"},
            {"label": "Address:", "value": self.user_data.get('address', 'N/A'), "icon": "🏠"}
        ]

        # Add each field with proper spacing
        for i, field in enumerate(fields):
            # Row frame
            row_frame = ctk.CTkFrame(profile_container, fg_color="transparent")
            row_frame.grid(row=i, column=0, sticky="ew", padx=20, pady=15)
            row_frame.grid_columnconfigure(1, weight=1)
            
            # Icon
            icon_label = ctk.CTkLabel(
                row_frame,
                text=field["icon"],
                font=("Arial", 18),
                text_color="#6B7280"
            )
            icon_label.grid(row=0, column=0, padx=(0, 10))
            
            # Label
            label = ctk.CTkLabel(
                row_frame, 
                text=field["label"], 
                font=("Arial", 14), 
                text_color="#1F2937",
                anchor="w"
            )
            label.grid(row=0, column=1, sticky="w")
            
            # Value (right-aligned)
            value = ctk.CTkLabel(
                row_frame, 
                text=field["value"], 
                font=("Arial", 14), 
                text_color="#1F2937",
                anchor="e"
            )
            value.grid(row=0, column=2, sticky="e", padx=(10, 0))

        # Configure grid to make value column expand
        profile_container.grid_columnconfigure(0, weight=1)
        
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
        edit_btn.grid(row=len(fields), column=0, padx=20, pady=20, sticky="ew")

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
                self.show_error_message("Validation Error", "First and Last name are required")
                return

            # Validate phone number
            if phone and not re.match(r'^\+?1?\d{10,14}$', phone):
                self.show_error_message("Validation Error", "Invalid phone number")
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

            # Recreate the UI with updated data
            for widget in self.main_frame.winfo_children():
                widget.destroy()
                
            # Recreate all UI components
            self.create_header()
            
            self.past_orders_label = ctk.CTkLabel(
                self.main_frame, 
                text="Past Orders", 
                font=("Arial", 20, "bold"), 
                text_color="#1F2937",
                anchor="w"
            )
            self.past_orders_label.pack(anchor="w", padx=50, pady=(20, 10))
            
            self.create_past_orders()
            
            self.profile_settings_label = ctk.CTkLabel(
                self.main_frame, 
                text="Profile & Settings", 
                font=("Arial", 20, "bold"), 
                text_color="#1F2937",
                anchor="w"
            )
            self.profile_settings_label.pack(anchor="w", padx=50, pady=(30, 10))
            
            self.create_profile_info()
            self.create_bottom_navigation()

            # Show success message
            self.show_success_message("Success", "Profile updated successfully")

        except Exception as e:
            print(f"Error saving profile changes: {e}")
            self.show_error_message("Error", "Failed to update profile")
            
    def show_error_message(self, title, message):
        """Show error message dialog"""
        error_window = ctk.CTkToplevel(self.root)
        error_window.title(title)
        error_window.geometry("400x150")
        error_window.resizable(False, False)
        error_window.grab_set()
        
        # Error icon
        icon_label = ctk.CTkLabel(
            error_window,
            text="❌",
            font=("Arial", 36),
            text_color="#EF4444"
        )
        icon_label.pack(pady=(10, 0))
        
        # Message
        msg_label = ctk.CTkLabel(
            error_window,
            text=message,
            font=("Arial", 14),
            wraplength=350
        )
        msg_label.pack(pady=10)
        
        # OK button
        ok_btn = ctk.CTkButton(
            error_window,
            text="OK",
            font=("Arial", 14),
            command=error_window.destroy
        )
        ok_btn.pack(pady=10)
        
    def show_success_message(self, title, message):
        """Show success message dialog"""
        success_window = ctk.CTkToplevel(self.root)
        success_window.title(title)
        success_window.geometry("400x150")
        success_window.resizable(False, False)
        success_window.grab_set()
        
        # Success icon
        icon_label = ctk.CTkLabel(
            success_window,
            text="✅",
            font=("Arial", 36),
            text_color="#22C55E"
        )
        icon_label.pack(pady=(10, 0))
        
        # Message
        msg_label = ctk.CTkLabel(
            success_window,
            text=message,
            font=("Arial", 14)
        )
        msg_label.pack(pady=10)
        
        # OK button
        ok_btn = ctk.CTkButton(
            success_window,
            text="OK",
            font=("Arial", 14),
            fg_color="#22C55E",
            hover_color="#16A34A",
            command=success_window.destroy
        )
        ok_btn.pack(pady=10)

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