import customtkinter as ctk
import subprocess
import sys
import re
from typing import List, Dict
import os
from PIL import Image

# Database and utility imports
from db_connection import DatabaseConnection
from image_handler import ImageHandler

class HomePage:
    def __init__(self, user_id=None):
        # Configure CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Create the main window
        self.root = ctk.CTk()
        self.root.title("Home Page")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        # Store user ID and user details
        self.user_id = user_id
        self.user_details = self.fetch_user_details()
        
        # Initialize image handler
        self.image_handler = ImageHandler()
        
        # Ensure image directories exist
        self.ensure_image_directories()

        # Setup main components
        self.setup_ui()
        
    def ensure_image_directories(self):
        """Ensure that image directories exist"""
        image_dirs = [
            "images",
            "images/restaurants",
            "images/menu_items",
            "images/categories"
        ]
        
        for directory in image_dirs:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")

    def fetch_user_details(self):
        """
        Fetch user details from the database
        """
        if not self.user_id:
            return None
        
        try:
            query = """
            SELECT user_id, first_name, last_name, email, phone_number 
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

    def setup_ui(self):
        # Main white background frame
        self.main_frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header with user greeting
        self.setup_header()

        # Search bar
        self.setup_search_bar()

        # Category buttons
        self.setup_category_buttons()

        # Restaurant listings
        self.setup_restaurant_listings()

        # Bottom navigation bar
        self.setup_navigation_bar()

    def setup_header(self):
        # Header text with user greeting
        header_text = "Find Your Favorite Food"
        if self.user_details:
            header_text = f"Welcome, {self.user_details['first_name']}! Find Your Favorite Food"
        
        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text=header_text, 
            font=("Arial", 28, "bold"),
            text_color="#2D3748"
        )
        self.header_label.pack(pady=(30, 20))

    def setup_search_bar(self):
        search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        search_frame.pack(pady=(10, 20))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=700,
            height=45,
            placeholder_text="Search for restaurants or dishes...",
            font=("Arial", 14),
            corner_radius=15,
            border_width=1,
            border_color="#E2E8F0"
        )
        self.search_entry.pack(side="left")
        
        # Search button
        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            font=("Arial", 14),
            width=100,
            height=45,
            corner_radius=15,
            fg_color="#FF8866",
            hover_color="#FF6644",
            command=self.perform_search
        )
        search_button.pack(side="left", padx=(10, 0))
        
        # Add search functionality for Enter key
        self.search_entry.bind("<Return>", lambda event: self.perform_search())

    def perform_search(self):
        """
        Perform search based on user input
        """
        search_term = self.search_entry.get().strip()
        if search_term:
            try:
                # Search for restaurants or dishes
                query = """
                SELECT r.*, c.category_name 
                FROM Restaurants r
                JOIN Categories c ON r.category_id = c.category_id
                WHERE r.restaurant_name LIKE %s 
                OR r.description LIKE %s 
                OR c.category_name LIKE %s
                """
                search_param = f"%{search_term}%"
                results = DatabaseConnection.execute_query(
                    query, 
                    params=(search_param, search_param, search_param), 
                    fetch=True
                )
                
                # Update restaurant listings
                self.display_restaurants(results)
            except Exception as e:
                print(f"Search error: {e}")
                # Show error message to user
                self.show_error("Search Error", "Could not perform search.")

    def setup_category_buttons(self):
        # Category buttons frame
        self.category_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.category_frame.pack(pady=(0, 20))

        # Fetch categories from database
        try:
            query = "SELECT category_id, category_name FROM Categories"
            categories = DatabaseConnection.execute_query(query, fetch=True)
            
            if not categories:
                print("No categories found in database")
                return
                
            print(f"Found {len(categories)} categories")
            
            # Color palette for categories
            category_colors = [
                "#32CD32",   # Green
                "#FF7F50",   # Coral/Orange
                "#F85C50",   # Red
                "#FFD700",   # Yellow/Gold
                "#9370DB"    # Purple
            ]

            for i, category in enumerate(categories):
                # Get category image
                category_id = category['category_id']
                category_image = self.image_handler.get_category_image(category_id, size=(24, 24))
                
                color = category_colors[i % len(category_colors)]
                category_btn = ctk.CTkButton(
                    self.category_frame,
                    text=category['category_name'],
                    font=("Arial", 14, "bold"),
                    fg_color=color,
                    text_color="white",
                    hover_color=color,
                    width=120,
                    height=35,
                    corner_radius=20,
                    image=category_image,  # Add category icon
                    compound="left",  # Show icon to the left of text
                    command=lambda cat_id=category_id: self.filter_restaurants(cat_id)
                )
                category_btn.pack(side="left", padx=5)
                print(f"Added category button: {category['category_name']}")
        except Exception as e:
            print(f"Error fetching categories: {e}")
            self.show_error("Database Error", f"Could not fetch categories: {e}")

    def filter_restaurants(self, category_id):
        """
        Filter restaurants by category
        """
        try:
            print(f"Filtering restaurants by category ID: {category_id}")
            query = """
            SELECT r.*, c.category_name 
            FROM Restaurants r
            JOIN Categories c ON r.category_id = c.category_id
            WHERE r.category_id = %s
            """
            results = DatabaseConnection.execute_query(
                query, 
                params=(category_id,), 
                fetch=True
            )
            
            print(f"Found {len(results)} restaurants for category {category_id}")
            
            # Update restaurant listings
            self.display_restaurants(results)
        except Exception as e:
            print(f"Error filtering restaurants: {e}")
            self.show_error("Filter Error", f"Could not filter restaurants: {e}")

    def setup_restaurant_listings(self):
        """Setup the restaurant listings section with scrollable frame"""
        # Restaurant section title
        restaurants_title = ctk.CTkLabel(
            self.main_frame,
            text="Popular Restaurants",
            font=("Arial", 20, "bold"),
            text_color="#2D3748",
            anchor="w"
        )
        restaurants_title.pack(anchor="w", padx=20, pady=(10, 5))
        
        # Create a scrollable frame container for restaurants
        self.restaurants_container = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
            width=1150,
            height=400
        )
        self.restaurants_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create a frame inside scrollable container for the restaurant cards
        self.restaurants_frame = ctk.CTkFrame(self.restaurants_container, fg_color="transparent")
        self.restaurants_frame.pack(fill="both", expand=True)

        # Fetch restaurants from database
        try:
            print("Fetching restaurants from database...")
            query = """
            SELECT r.*, c.category_name 
            FROM Restaurants r
            JOIN Categories c ON r.category_id = c.category_id
            ORDER BY r.rating DESC
            LIMIT 10
            """
            restaurants = DatabaseConnection.execute_query(query, fetch=True)
            
            if restaurants:
                print(f"Found {len(restaurants)} restaurants")
                # Display restaurants
                self.display_restaurants(restaurants)
            else:
                print("No restaurants found in database")
                no_restaurants_label = ctk.CTkLabel(
                    self.restaurants_frame,
                    text="No restaurants found. Please add restaurants to the database.",
                    font=("Arial", 16),
                    text_color="#6B7280"
                )
                no_restaurants_label.pack(pady=50)
                
        except Exception as e:
            print(f"Error fetching restaurants: {e}")
            self.show_error("Database Error", f"Could not fetch restaurants: {e}")

    def display_restaurants(self, restaurants):
        """
        Display restaurant cards in a grid layout
        """
        # Clear existing restaurants
        for widget in self.restaurants_frame.winfo_children():
            widget.destroy()

        # Display message if no restaurants found
        if not restaurants:
            no_results_label = ctk.CTkLabel(
                self.restaurants_frame,
                text="No restaurants found.",
                font=("Arial", 18),
                text_color="#666666"
            )
            no_results_label.pack(pady=50)
            return

        # Create a frame for each row (3 cards per row)
        row_frame = None
        
        for i, restaurant in enumerate(restaurants):
            # Create a new row every 3 restaurants
            if i % 3 == 0:
                row_frame = ctk.CTkFrame(self.restaurants_frame, fg_color="transparent")
                row_frame.pack(fill="x", pady=10)
            
            # Create restaurant card
            self.create_restaurant_card(row_frame, restaurant)

    def create_restaurant_card(self, parent_frame, restaurant):
        """
        Create a single restaurant card with image
        """
        # Card frame
        card = ctk.CTkFrame(
            parent_frame,
            width=360,
            height=350,
            corner_radius=15,
            fg_color="white",
            border_width=1,
            border_color="#E2E8F0"
        )
        card.pack(side="left", padx=10, pady=10)
        
        # Add card content without using pack_propagate(False)
        # to avoid layout issues
        
        # Image frame
        img_frame = ctk.CTkFrame(
            card,
            width=320,
            height=170,
            corner_radius=10,
            fg_color="#E2E2E2"
        )
        img_frame.place(x=20, y=20)
        
        # Get restaurant image
        restaurant_id = restaurant.get('restaurant_id')
        restaurant_image = self.image_handler.get_restaurant_image(restaurant_id, size=(320, 170))
        
        if restaurant_image:
            # Show actual image
            img_label = ctk.CTkLabel(
                img_frame,
                image=restaurant_image,
                text=""
            )
            img_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            # Fallback to text
            img_label = ctk.CTkLabel(
                img_frame,
                text=restaurant.get('restaurant_name', 'Restaurant'),
                font=("Arial", 20, "bold"),
                text_color="#A0A0A0"
            )
            img_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Restaurant name
        name_label = ctk.CTkLabel(
            card,
            text=restaurant.get('restaurant_name', 'Unknown Restaurant'),
            font=("Arial", 18, "bold"),
            text_color="#2D3748",
            anchor="w"
        )
        name_label.place(x=20, y=200)
        
        # Rating with stars
        rating_frame = ctk.CTkFrame(card, fg_color="transparent", width=200, height=20)
        rating_frame.place(x=20, y=230)
        
        # Convert rating to float and handle potential None/empty values
        try:
            rating = float(restaurant.get('rating', 0))
        except (ValueError, TypeError):
            rating = 0.0
            
        star_count = int(rating)
        half_star = rating - star_count >= 0.5
        
        star_x = 0
        for i in range(5):
            if i < star_count:
                star = ctk.CTkLabel(rating_frame, text="★", font=("Arial", 16), text_color="#FFD700")
            elif i == star_count and half_star:
                star = ctk.CTkLabel(rating_frame, text="★", font=("Arial", 16), text_color="#FFD700")
            else:
                star = ctk.CTkLabel(rating_frame, text="★", font=("Arial", 16), text_color="#D3D3D3")
            star.place(x=star_x, y=0)
            star_x += 20
        
        rating_value = ctk.CTkLabel(
            rating_frame,
            text=f" ({rating})",
            font=("Arial", 14),
            text_color="#666666"
        )
        rating_value.place(x=110, y=0)
        
        # Delivery time
        delivery_label = ctk.CTkLabel(
            card,
            text=f"Delivery: {restaurant.get('delivery_time', 'N/A')} mins",
            font=("Arial", 14),
            text_color="#666666",
            anchor="w"
        )
        delivery_label.place(x=20, y=260)
        
        # Category
        category_label = ctk.CTkLabel(
            card,
            text=f"Category: {restaurant.get('category_name', 'Various')}",
            font=("Arial", 14),
            text_color="#666666",
            anchor="w"
        )
        category_label.place(x=20, y=285)
        
        # View Menu button
        view_menu_btn = ctk.CTkButton(
            card,
            text="View Menu",
            font=("Arial", 14, "bold"),
            fg_color="#32CD32",
            text_color="white",
            hover_color="#28A828",
            corner_radius=10,
            width=320,
            height=40,
            command=lambda r=restaurant: self.open_restaurant_menu(r)
        )
        view_menu_btn.place(x=20, y=320-50)

    def open_restaurant_menu(self, restaurant):
        """
        Open restaurant menu
        """
        try:
            # Pass restaurant ID and user ID to menu page
            restaurant_id = restaurant.get('restaurant_id')
            if restaurant_id:
                # Use the restaurant_menu.py file
                if self.user_id:
                    subprocess.Popen([sys.executable, "menu.py", str(restaurant_id), str(self.user_id)])
                else:
                    subprocess.Popen([sys.executable, "menu.py", str(restaurant_id)])
                self.root.destroy()
            else:
                self.show_error("Error", "No restaurant ID found")
        except Exception as e:
            print(f"Error opening menu: {e}")
            self.show_error("Error", f"Unable to open restaurant menu: {e}")

    def setup_navigation_bar(self):
        """
        Setup bottom navigation bar with clickable items
        """
        # Bottom navigation bar
        self.nav_bar = ctk.CTkFrame(
            self.main_frame,
            fg_color="white",
            height=70,
            corner_radius=0
        )
        self.nav_bar.pack(side="bottom", fill="x", pady=(10, 0))

        # Navigation items with their respective page/action
        nav_items = [
            {"name": "Home", "icon": "🏠", "color": "#32CD32", "action": self.stay_on_home},
            {"name": "Orders", "icon": "📦", "color": "#000000", "action": self.open_orders},
            {"name": "Cart", "icon": "🛒", "color": "#000000", "action": self.open_cart},
            {"name": "Profile", "icon": "👤", "color": "#000000", "action": self.open_profile},
            {"name": "Settings", "icon": "⚙️", "color": "#000000", "action": self.open_settings}
        ]

        # Create navigation buttons
        for item in nav_items:
            nav_frame = ctk.CTkFrame(self.nav_bar, fg_color="transparent", width=80)
            nav_frame.pack(side="left", expand=True, fill="y")
            
            # Icon
            icon_label = ctk.CTkLabel(
                nav_frame,
                text=item["icon"],
                font=("Arial", 24),
                text_color=item["color"]
            )
            icon_label.pack(pady=(10, 0))
            
            # Text
            text_label = ctk.CTkLabel(
                nav_frame,
                text=item["name"],
                font=("Arial", 12),
                text_color=item["color"]
            )
            text_label.pack()

            # Make the frame clickable
            nav_frame.bind("<Button-1>", lambda e, action=item['action']: action())
            icon_label.bind("<Button-1>", lambda e, action=item['action']: action())
            text_label.bind("<Button-1>", lambda e, action=item['action']: action())

    def stay_on_home(self):
        """Do nothing, already on home page"""
        pass

    def open_orders(self):
        """Open orders page"""
        try:
            if not self.user_id:
                self.show_login_required("Please log in to view your orders")
                return
                
            subprocess.Popen([sys.executable, "track.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error opening orders: {e}")
            self.show_error("Error", f"Unable to open orders page: {e}")

    def open_cart(self):
        """Open cart page"""
        try:
            if not self.user_id:
                self.show_login_required("Please log in to view your cart")
                return
                
            subprocess.Popen([sys.executable, "cart.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error opening cart: {e}")
            self.show_error("Error", f"Unable to open cart page: {e}")

    def open_profile(self):
        """Open profile page"""
        try:
            if not self.user_id:
                self.show_login_required("Please log in to view your profile")
                return
                
            subprocess.Popen([sys.executable, "profile.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error opening profile: {e}")
            self.show_error("Error", f"Unable to open profile page: {e}")

    def open_settings(self):
        """Open settings page"""
        try:
            if self.user_id:
                subprocess.Popen([sys.executable, "settings.py", str(self.user_id)])
            else:
                subprocess.Popen([sys.executable, "settings.py"])
            self.root.destroy()
        except Exception as e:
            print(f"Error opening settings: {e}")
            self.show_error("Error", f"Unable to open settings page: {e}")
            
    def show_error(self, title, message):
        """Show error message dialog"""
        error_window = ctk.CTkToplevel(self.root)
        error_window.title(title)
        error_window.geometry("400x200")
        error_window.resizable(False, False)
        error_window.grab_set()
        
        # Error icon
        icon_label = ctk.CTkLabel(
            error_window,
            text="❌",
            font=("Arial", 48),
            text_color="#EF4444"
        )
        icon_label.pack(pady=(20, 10))
        
        # Error message
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
            command=error_window.destroy
        )
        ok_btn.pack(pady=10)
        
    def show_login_required(self, message):
        """Show login required dialog with login button"""
        login_window = ctk.CTkToplevel(self.root)
        login_window.title("Login Required")
        login_window.geometry("400x250")
        login_window.resizable(False, False)
        login_window.grab_set()
        
        # Info icon
        icon_label = ctk.CTkLabel(
            login_window,
            text="ℹ️",
            font=("Arial", 48),
            text_color="#3B82F6"
        )
        icon_label.pack(pady=(20, 10))
        
        # Message
        msg_label = ctk.CTkLabel(
            login_window,
            text=message,
            font=("Arial", 14),
            wraplength=350
        )
        msg_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(login_window, fg_color="transparent")
        buttons_frame.pack(pady=10)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Continue Browsing",
            font=("Arial", 14),
            fg_color="#6B7280",
            hover_color="#4B5563",
            width=150,
            command=login_window.destroy
        )
        cancel_btn.pack(side="left", padx=10)
        
        # Login button
        login_btn = ctk.CTkButton(
            buttons_frame,
            text="Go to Login",
            font=("Arial", 14),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            width=150,
            command=lambda: self.go_to_login(login_window)
        )
        login_btn.pack(side="left", padx=10)
        
    def go_to_login(self, window=None):
        """Navigate to login page"""
        if window:
            window.destroy()
            
        try:
            subprocess.Popen([sys.executable, "login.py"])
            self.root.destroy()
        except Exception as e:
            print(f"Error going to login: {e}")
            self.show_error("Error", f"Unable to open login page: {e}")

    def run(self):
        """Run the home page application"""
        self.root.mainloop()

def main():
    # Check if user ID is passed as command-line argument
    user_id = None
    if len(sys.argv) > 1 and sys.argv[1].strip():
        try:
            user_id = int(sys.argv[1])
        except ValueError:
            print("Invalid user ID")

    # Create and run home page
    app = HomePage(user_id)
    app.run()

if __name__ == "__main__":
    main()