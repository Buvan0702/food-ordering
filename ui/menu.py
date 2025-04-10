import customtkinter as ctk
import subprocess
import sys
import os
from PIL import Image
from db_connection import DatabaseConnection
from image_handler import ImageHandler

class RestaurantMenuApp:
    def __init__(self, restaurant_id=None, user_id=None):
        # Configure CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Create the main window
        self.root = ctk.CTk()
        self.root.title("Restaurant Menu")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        # Store IDs
        self.restaurant_id = restaurant_id
        self.user_id = user_id
        
        # Initialize image handler
        self.image_handler = ImageHandler()
        
        # Fetch restaurant info
        self.restaurant_info = self.fetch_restaurant_info()
        
        # Fetch menu items
        self.menu_items = self.fetch_menu_items()

        # Setup UI
        self.setup_ui()

    def fetch_restaurant_info(self):
        """Fetch restaurant details"""
        if not self.restaurant_id:
            return None
            
        try:
            query = """
            SELECT r.*, c.category_name 
            FROM Restaurants r
            JOIN Categories c ON r.category_id = c.category_id
            WHERE r.restaurant_id = %s
            """
            results = DatabaseConnection.execute_query(
                query, 
                params=(self.restaurant_id,), 
                fetch=True
            )
            
            return results[0] if results else None
        except Exception as e:
            print(f"Error fetching restaurant info: {e}")
            return None

    def fetch_menu_items(self):
        """Fetch menu items for the restaurant"""
        if not self.restaurant_id:
            return []
            
        try:
            query = """
            SELECT * FROM MenuItems 
            WHERE restaurant_id = %s 
            ORDER BY category, item_name
            """
            results = DatabaseConnection.execute_query(
                query, 
                params=(self.restaurant_id,), 
                fetch=True
            )
            
            return results
        except Exception as e:
            print(f"Error fetching menu items: {e}")
            return []

    def setup_ui(self):
        """Setup the user interface"""
        # Main white background
        self.main_frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Restaurant header with image and details
        self.create_restaurant_header()
        
        # Menu categories and items
        self.create_menu_sections()
        
        # Bottom Navigation
        self.create_bottom_navigation()

    def create_restaurant_header(self):
        """Create restaurant header with image and details"""
        if not self.restaurant_info:
            header_label = ctk.CTkLabel(
                self.main_frame,
                text="Restaurant not found",
                font=("Arial", 24, "bold"),
                text_color="#1F2937"
            )
            header_label.pack(pady=20)
            return

        # Header container
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=200)
        header_frame.pack(fill="x", padx=40, pady=20)
        
        # Restaurant image on the left
        img_frame = ctk.CTkFrame(header_frame, fg_color="#F3F4F6", width=300, height=180, corner_radius=15)
        img_frame.pack(side="left", padx=(0, 20))
        
        # Get restaurant image
        restaurant_image = self.image_handler.get_restaurant_image(self.restaurant_id, size=(300, 180))
        
        if restaurant_image:
            # Show actual image
            img_label = ctk.CTkLabel(img_frame, image=restaurant_image, text="")
            img_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            # Fallback to text
            img_label = ctk.CTkLabel(
                img_frame,
                text=self.restaurant_info.get('restaurant_name', 'Restaurant'),
                font=("Arial", 24, "bold"),
                text_color="#9CA3AF"
            )
            img_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Restaurant details on the right
        details_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        details_frame.pack(side="left", fill="both", expand=True)
        
        # Restaurant name
        name_label = ctk.CTkLabel(
            details_frame,
            text=self.restaurant_info.get('restaurant_name', 'Restaurant'),
            font=("Arial", 28, "bold"),
            text_color="#1F2937",
            anchor="w"
        )
        name_label.pack(anchor="w", pady=(10, 5))
        
        # Category
        category_label = ctk.CTkLabel(
            details_frame,
            text=self.restaurant_info.get('category_name', 'Restaurant'),
            font=("Arial", 16),
            text_color="#6B7280",
            anchor="w"
        )
        category_label.pack(anchor="w", pady=(0, 10))
        
        # Rating with stars
        rating_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        rating_frame.pack(anchor="w", pady=(0, 5))
        
        rating = float(self.restaurant_info.get('rating', 0))
        star_count = int(rating)
        half_star = rating - star_count >= 0.5
        
        for i in range(5):
            if i < star_count:
                star = ctk.CTkLabel(rating_frame, text="★", font=("Arial", 16), text_color="#FFD700")
            elif i == star_count and half_star:
                star = ctk.CTkLabel(rating_frame, text="★", font=("Arial", 16), text_color="#FFD700")
            else:
                star = ctk.CTkLabel(rating_frame, text="★", font=("Arial", 16), text_color="#D3D3D3")
            star.pack(side="left")
        
        rating_value = ctk.CTkLabel(
            rating_frame,
            text=f" ({rating})",
            font=("Arial", 14),
            text_color="#6B7280"
        )
        rating_value.pack(side="left", padx=(5, 0))
        
        # Delivery info
        delivery_label = ctk.CTkLabel(
            details_frame,
            text=f"Delivery: {self.restaurant_info.get('delivery_time', 'N/A')} mins | {self.restaurant_info.get('address', 'No Address')}",
            font=("Arial", 14),
            text_color="#6B7280",
            anchor="w"
        )
        delivery_label.pack(anchor="w", pady=(0, 5))
        
        # Description
        if self.restaurant_info.get('description'):
            desc_label = ctk.CTkLabel(
                details_frame,
                text=self.restaurant_info.get('description', ''),
                font=("Arial", 14),
                text_color="#4B5563",
                anchor="w",
                wraplength=500
            )
            desc_label.pack(anchor="w", pady=(5, 0))

    def create_menu_sections(self):
        """Create menu categories and items with images"""
        if not self.menu_items:
            empty_label = ctk.CTkLabel(
                self.main_frame,
                text="No menu items found for this restaurant",
                font=("Arial", 16),
                text_color="#6B7280"
            )
            empty_label.pack(pady=20)
            return
        
        # Group items by category
        categories = {}
        for item in self.menu_items:
            category = item.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        
        # Menu container with scrollable frame
        self.menu_container = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="white",
            width=1100,
            height=450
        )
        self.menu_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        # Create sections for each category
        for category, items in categories.items():
            # Category heading
            category_label = ctk.CTkLabel(
                self.menu_container,
                text=category,
                font=("Arial", 20, "bold"),
                text_color="#1F2937",
                anchor="w"
            )
            category_label.pack(anchor="w", pady=(20, 10))
            
            # Create items grid
            items_frame = ctk.CTkFrame(self.menu_container, fg_color="transparent")
            items_frame.pack(fill="x", pady=(0, 20))
            
            # Create a wrapper frame for grid
            row_frame = None
            
            # Add menu items in rows of 3
            for i, item in enumerate(items):
                if i % 3 == 0:
                    row_frame = ctk.CTkFrame(items_frame, fg_color="transparent")
                    row_frame.pack(fill="x", pady=5)
                
                # Create menu item card
                self.create_menu_item_card(row_frame, item)

    def create_menu_item_card(self, parent, item):
        """Create a menu item card with image"""
        # Card frame
        card = ctk.CTkFrame(
            parent,
            width=350,
            height=180,
            corner_radius=10,
            fg_color="white",
            border_width=1,
            border_color="#E5E7EB"
        )
        card.pack(side="left", padx=10, pady=5)
        card.pack_propagate(False)
        
        # Left side: Food image
        img_frame = ctk.CTkFrame(
            card,
            width=120,
            height=120,
            corner_radius=8,
            fg_color="#F3F4F6"
        )
        img_frame.place(x=15, y=30)
        
        # Get food item image
        menu_item_id = item.get('menu_item_id')
        food_image = self.image_handler.get_menu_item_image(menu_item_id, size=(120, 120))
        
        if food_image:
            # Show actual image
            img_label = ctk.CTkLabel(img_frame, image=food_image, text="")
            img_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            # Fallback to text
            img_label = ctk.CTkLabel(
                img_frame,
                text=item.get('item_name', 'Food Item')[:10],
                font=("Arial", 12),
                text_color="#9CA3AF"
            )
            img_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Right side: Item details
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.place(x=150, y=15, width=185, height=150)
        
        # Item name
        name_label = ctk.CTkLabel(
            details_frame,
            text=item.get('item_name', 'Food Item'),
            font=("Arial", 16, "bold"),
            text_color="#1F2937",
            anchor="w",
            wraplength=180
        )
        name_label.pack(anchor="w")
        
        # Item description (truncated)
        description = item.get('description', '')
        if len(description) > 80:
            description = description[:77] + "..."
            
        desc_label = ctk.CTkLabel(
            details_frame,
            text=description,
            font=("Arial", 12),
            text_color="#6B7280",
            anchor="w",
            wraplength=180,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(5, 0))
        
        # Price and Add to Cart button in a row
        bottom_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", pady=(5, 10))
        
        # Price
        price_label = ctk.CTkLabel(
            bottom_frame,
            text=f"${float(item.get('price', 0)):.2f}",
            font=("Arial", 14, "bold"),
            text_color="#22C55E"
        )
        price_label.pack(side="left")
        
        # Add to cart button
        add_btn = ctk.CTkButton(
            bottom_frame,
            text="+",
            width=30,
            height=30,
            font=("Arial", 16, "bold"),
            fg_color="#22C55E",
            text_color="white",
            hover_color="#16A34A",
            corner_radius=15,
            command=lambda item_id=item.get('menu_item_id'): self.add_to_cart(item_id)
        )
        add_btn.pack(side="right")
        
        # Vegetarian badge if applicable
        if item.get('is_vegetarian'):
            veg_badge = ctk.CTkLabel(
                card,
                text="VEG",
                font=("Arial", 10, "bold"),
                text_color="white",
                fg_color="#22C55E",
                corner_radius=5,
                width=40,
                height=20
            )
            veg_badge.place(x=15, y=15)

    def add_to_cart(self, menu_item_id):
        """Add item to cart"""
        if not self.user_id or not menu_item_id:
            self.show_message("Login Required", "Please log in to add items to cart")
            return
            
        try:
            # Check if item already in cart
            check_query = """
            SELECT cart_item_id, quantity 
            FROM CartItems 
            WHERE user_id = %s AND menu_item_id = %s
            """
            existing_item = DatabaseConnection.execute_query(
                check_query, 
                params=(self.user_id, menu_item_id), 
                fetch=True
            )
            
            if existing_item:
                # Update quantity if already in cart
                update_query = """
                UPDATE CartItems 
                SET quantity = quantity + 1 
                WHERE cart_item_id = %s
                """
                DatabaseConnection.execute_query(
                    update_query, 
                    params=(existing_item[0]['cart_item_id'],)
                )
                message = "Item quantity updated in cart!"
            else:
                # Insert new cart item
                insert_query = """
                INSERT INTO CartItems (user_id, menu_item_id, quantity) 
                VALUES (%s, %s, 1)
                """
                DatabaseConnection.execute_query(
                    insert_query, 
                    params=(self.user_id, menu_item_id)
                )
                message = "Item added to cart!"
                
            # Show success message
            self.show_success_message(message)
            
        except Exception as e:
            print(f"Error adding to cart: {e}")
            self.show_error_message("Could not add item to cart")
            
    def show_message(self, title, message):
        """Show information message"""
        message_window = ctk.CTkToplevel(self.root)
        message_window.title(title)
        message_window.geometry("300x150")
        message_window.resizable(False, False)
        message_window.grab_set()
        
        # Message
        msg_label = ctk.CTkLabel(
            message_window,
            text=message,
            font=("Arial", 14),
            wraplength=250
        )
        msg_label.pack(pady=(30, 20))
        
        # OK button
        ok_btn = ctk.CTkButton(
            message_window,
            text="OK",
            font=("Arial", 14),
            command=message_window.destroy
        )
        ok_btn.pack(pady=10)
            
    def show_success_message(self, message):
        """Show success message with cart options"""
        success_window = ctk.CTkToplevel(self.root)
        success_window.title("Success")
        success_window.geometry("300x180")
        success_window.resizable(False, False)
        success_window.grab_set()
        
        # Success icon
        icon_label = ctk.CTkLabel(
            success_window,
            text="✅",
            font=("Arial", 36),
            text_color="#22C55E"
        )
        icon_label.pack(pady=(15, 0))
        
        # Message
        msg_label = ctk.CTkLabel(
            success_window,
            text=message,
            font=("Arial", 14)
        )
        msg_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(success_window, fg_color="transparent")
        buttons_frame.pack(pady=10)
        
        # Continue shopping button
        continue_btn = ctk.CTkButton(
            buttons_frame,
            text="Continue Shopping",
            font=("Arial", 14),
            fg_color="#6B7280",
            text_color="white",
            hover_color="#4B5563",
            command=lambda: success_window.destroy()
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
            command=lambda: self.go_to_cart(success_window)
        )
        cart_btn.pack(side="left", padx=5)
        
    def show_error_message(self, message):
        """Show error message"""
        error_window = ctk.CTkToplevel(self.root)
        error_window.title("Error")
        error_window.geometry("300x180")
        error_window.resizable(False, False)
        error_window.grab_set()
        
        # Error icon
        icon_label = ctk.CTkLabel(
            error_window,
            text="❌",
            font=("Arial", 36),
            text_color="#EF4444"
        )
        icon_label.pack(pady=(15, 0))
        
        # Message
        msg_label = ctk.CTkLabel(
            error_window,
            text=message,
            font=("Arial", 14),
            wraplength=250
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

    def go_to_cart(self, window=None):
        """Navigate to cart page"""
        try:
            if window:
                window.destroy()
                
            subprocess.Popen([sys.executable, "cart.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error going to cart: {e}")

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
            {"name": "Profile", "icon": "👤", "action": self.go_to_profile},
            {"name": "Settings", "icon": "⚙️", "action": self.go_to_settings}
        ]
        
        # Create navigation buttons
        for item in nav_items:
            nav_frame = ctk.CTkFrame(nav_bar, fg_color="transparent", width=80)
            nav_frame.pack(side="left", expand=True, fill="y")
            
            # Icon
            icon_label = ctk.CTkLabel(
                nav_frame,
                text=item["icon"],
                font=("Arial", 24),
                text_color="#1F2937"
            )
            icon_label.pack(pady=(10, 0))
            
            # Text
            text_label = ctk.CTkLabel(
                nav_frame,
                text=item["name"],
                font=("Arial", 12),
                text_color="#1F2937"
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
    # Check for restaurant_id and user_id in command-line arguments
    restaurant_id = None
    user_id = None
    
    if len(sys.argv) > 1:
        try:
            restaurant_id = int(sys.argv[1])
        except ValueError:
            print("Invalid restaurant ID")
    
    if len(sys.argv) > 2:
        try:
            user_id = int(sys.argv[2])
        except ValueError:
            print("Invalid user ID")
    
    # Create and run the menu page
    app = RestaurantMenuApp(restaurant_id, user_id)
    app.root.mainloop()

if __name__ == "__main__":
    main()