import customtkinter as ctk
import subprocess
import sys
import re
from typing import List, Dict

# Database and utility imports
from db_connection import DatabaseConnection
from password_utility import PasswordManager

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

        # Setup main components
        self.setup_ui()

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
        self.search_entry = ctk.CTkEntry(
            self.main_frame,
            width=700,
            height=45,
            placeholder_text="Search for restaurants or dishes...",
            font=("Arial", 14),
            corner_radius=15,
            border_width=1,
            border_color="#E2E8F0"
        )
        self.search_entry.pack(pady=(10, 20))
        
        # Add search functionality
        self.search_entry.bind("<Return>", self.perform_search)

    def perform_search(self, event=None):
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
                ctk.CTkMessagebox.showerror("Search Error", "Could not perform search.")

    def setup_category_buttons(self):
        # Category buttons frame
        self.category_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.category_frame.pack(pady=(0, 20))

        # Fetch categories from database
        try:
            query = "SELECT category_id, category_name FROM Categories"
            categories = DatabaseConnection.execute_query(query, fetch=True)
            
            # Color palette for categories
            category_colors = [
                "#32CD32",   # Green
                "#FF7F50",   # Coral/Orange
                "#F85C50",   # Red
                "#FFD700",   # Yellow/Gold
                "#9370DB"    # Purple
            ]

            for i, category in enumerate(categories):
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
                    command=lambda cat_id=category['category_id']: self.filter_restaurants(cat_id)
                )
                category_btn.pack(side="left", padx=5)
        except Exception as e:
            print(f"Error fetching categories: {e}")

    def filter_restaurants(self, category_id):
        """
        Filter restaurants by category
        """
        try:
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
            
            # Update restaurant listings
            self.display_restaurants(results)
        except Exception as e:
            print(f"Error filtering restaurants: {e}")

    def setup_restaurant_listings(self):
        # Restaurant listings frame
        self.restaurants_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.restaurants_frame.pack(pady=10)

        # Fetch restaurants from database
        try:
            query = """
            SELECT r.*, c.category_name 
            FROM Restaurants r
            JOIN Categories c ON r.category_id = c.category_id
            ORDER BY r.rating DESC
            LIMIT 10
            """
            restaurants = DatabaseConnection.execute_query(query, fetch=True)
            
            # Display restaurants
            self.display_restaurants(restaurants)
        except Exception as e:
            print(f"Error fetching restaurants: {e}")

    def display_restaurants(self, restaurants):
        """
        Display restaurant cards
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
            no_results_label.pack(pady=20)
            return

        for restaurant in restaurants:
            self.create_restaurant_card(restaurant)

    def create_restaurant_card(self, restaurant):
        """
        Create a single restaurant card
        """
        # Card frame
        card = ctk.CTkFrame(
            self.restaurants_frame,
            width=350,
            height=370,
            corner_radius=15,
            fg_color="white",
            border_width=0,
            border_color="#E2E8F0"
        )
        card.pack(side="left", padx=10, pady=10)
        card.pack_propagate(False)
        
        # Image placeholder (in real app, would use actual restaurant image)
        img_frame = ctk.CTkFrame(
            card,
            width=320,
            height=170,
            corner_radius=10,
            fg_color="#E2E2E2"
        )
        img_frame.pack(padx=15, pady=15)
        
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
        name_label.pack(padx=15, pady=(5, 0), anchor="w")
        
        # Rating with stars
        rating_frame = ctk.CTkFrame(card, fg_color="transparent")
        rating_frame.pack(padx=15, pady=(5, 0), anchor="w")
        
        rating = restaurant.get('rating', 0)
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
            text_color="#666666"
        )
        rating_value.pack(side="left", padx=(5, 0))
        
        # Delivery time
        delivery_label = ctk.CTkLabel(
            card,
            text=f"Estimated Delivery: {restaurant.get('delivery_time', 'N/A')} mins",
            font=("Arial", 14),
            text_color="#666666",
            anchor="w"
        )
        delivery_label.pack(padx=15, pady=(5, 0), anchor="w")
        
        # View Menu button
        view_menu_btn = ctk.CTkButton(
            card,
            text="View Menu",
            font=("Arial", 14, "bold"),
            fg_color="#32CD32",
            text_color="white",
            hover_color="#28A828",
            corner_radius=10,
            width=290,
            height=40,
            command=lambda r=restaurant: self.open_restaurant_menu(r)
        )
        view_menu_btn.pack(padx=15, pady=(20, 15))

    def open_restaurant_menu(self, restaurant):
        """
        Open restaurant menu
        """
        try:
            # Pass restaurant ID to menu page
            restaurant_id = restaurant.get('restaurant_id')
            if restaurant_id:
                subprocess.Popen([sys.executable, "menu.py", str(restaurant_id)])
            else:
                print("No restaurant ID found")
        except Exception as e:
            print(f"Error opening menu: {e}")

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
            
            # Create a button-like frame for each nav item
            nav_button = ctk.CTkFrame(nav_frame, fg_color="transparent")
            nav_button.pack(expand=True)
            
            # Icon
            icon_label = ctk.CTkLabel(
                nav_button,
                text=item["icon"],
                font=("Arial", 20),
                text_color=item["color"]
            )
            icon_label.pack(pady=(5, 0))
            
            # Text
            text_label = ctk.CTkLabel(
                nav_button,
                text=item["name"],
                font=("Arial", 12),
                text_color=item["color"]
            )
            text_label.pack()
            
            # Bind click events
            nav_button.bind("<Button-1>", lambda e, action=item['action']: action())
            icon_label.bind("<Button-1>", lambda e, action=item['action']: action())
            text_label.bind("<Button-1>", lambda e, action=item['action']: action())

    def stay_on_home(self):
        """Do nothing, already on home page"""
        pass

    def open_orders(self):
        """Open orders page"""
        try:
            subprocess.Popen([sys.executable, "track.py", str(self.user_id)])
        except Exception as e:
            print(f"Error opening orders: {e}")

    def open_cart(self):
        """Open cart page"""
        try:
            subprocess.Popen([sys.executable, "cart.py", str(self.user_id)])
        except Exception as e:
            print(f"Error opening cart: {e}")

    def open_profile(self):
        """Open profile page"""
        try:
            subprocess.Popen([sys.executable, "profile.py", str(self.user_id)])
        except Exception as e:
            print(f"Error opening profile: {e}")

    def open_settings(self):
        """Open settings page"""
        try:
            subprocess.Popen([sys.executable, "settings.py", str(self.user_id)])
        except Exception as e:
            print(f"Error opening settings: {e}")

    def run(self):
        """Run the home page application"""
        self.root