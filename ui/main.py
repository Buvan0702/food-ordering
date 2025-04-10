import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
import subprocess
import sys
import hashlib
import os
from PIL import Image
from image_handler import ImageHandler

class FoodDeliveryDatabaseSetup:
    def __init__(self):
        # Database connection parameters
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'new_password'
        }

    def create_connection(self, database=None):
        """
        Create a database connection
        """
        try:
            if database:
                connection = mysql.connector.connect(
                    host=self.db_config['host'],
                    user=self.db_config['user'],
                    password=self.db_config['password'],
                    database=database
                )
            else:
                connection = mysql.connector.connect(
                    host=self.db_config['host'],
                    user=self.db_config['user'],
                    password=self.db_config['password']
                )
            print("Database connection successful!")
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def hash_password(self, password):
        """
        Hash password using SHA-256
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def setup_complete_database(self):
        """
        Comprehensive database setup with sample data
        """
        try:
            # Create connection without specifying database
            connection = self.create_connection()
            cursor = connection.cursor()

            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS food_system")
            cursor.execute("USE food_system")

            # Create all necessary tables
            self.create_tables(cursor)

            # Insert sample data
            self.insert_sample_categories(cursor)
            self.insert_sample_restaurants(cursor)
            self.insert_sample_menu_items(cursor)
            self.insert_sample_users(cursor)
            self.insert_sample_orders(cursor)

            # Commit changes
            connection.commit()

            # Close connection
            cursor.close()
            connection.close()

            print("Database setup completed successfully!")
            return True

        except Error as e:
            print(f"Error setting up database: {e}")
            return False

    def create_tables(self, cursor):
        """
        Create all necessary database tables
        """
        # Users Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            phone_number VARCHAR(20),
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Categories Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            category_id INT AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(50) NOT NULL UNIQUE,
            description TEXT
        )
        """)

        # Restaurants Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Restaurants (
            restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
            restaurant_name VARCHAR(100) NOT NULL,
            description TEXT,
            category_id INT,
            rating DECIMAL(3,2) DEFAULT 0,
            delivery_time INT,
            address VARCHAR(255),
            contact_number VARCHAR(20),
            FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        )
        """)

        # Menu Items Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS MenuItems (
            menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
            restaurant_id INT,
            item_name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            category VARCHAR(50),
            is_vegetarian BOOLEAN DEFAULT FALSE,
            is_available BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
        )
        """)

        # Orders Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            restaurant_id INT,
            total_amount DECIMAL(10, 2) NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status ENUM('Placed', 'Preparing', 'Out for Delivery', 'Delivered') DEFAULT 'Placed',
            estimated_delivery_time TIMESTAMP,
            delivery_address TEXT,
            special_instructions TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
        )
        """)

        # Order Items Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS OrderItems (
            order_item_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            menu_item_id INT,
            quantity INT NOT NULL,
            item_price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id)
        )
        """)

        # Cart Items Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS CartItems (
            cart_item_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            menu_item_id INT,
            quantity INT DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id),
            UNIQUE KEY unique_cart_item (user_id, menu_item_id)
        )
        """)

        # User Preferences Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserPreferences (
            user_id INT PRIMARY KEY,
            dark_mode BOOLEAN DEFAULT FALSE,
            notification_enabled BOOLEAN DEFAULT TRUE,
            dietary_preferences ENUM('None', 'Vegetarian', 'Vegan', 'Gluten-Free', 'Keto') DEFAULT 'None',
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
        """)

    def insert_sample_categories(self, cursor):
        """
        Insert sample food categories
        """
        categories = [
            ('FastFood', 'Quick and convenient meals'),
            ('Indian', 'Traditional Indian cuisine'),
            ('Chinese', 'Chinese and Asian dishes'),
            ('Desserts', 'Sweet treats and desserts'),
            ('Healthy', 'Nutritious and health-conscious options'),
            ('Pizza', 'Various types of pizzas'),
            ('Burger', 'Gourmet burger options')
        ]
        
        cursor.executemany(
            "INSERT IGNORE INTO Categories (category_name, description) VALUES (%s, %s)", 
            categories
        )

    def insert_sample_restaurants(self, cursor):
        """
        Insert sample restaurants
        """
        restaurants = [
            # Name, description, category_id, rating, delivery_time, address, contact
            ('Pizza Palace', 'Best pizzas in town', 1, 4.5, 30, '123 Main St', '555-1234'),
            ('Burger Haven', 'Gourmet burgers', 1, 4.3, 25, '456 Elm St', '555-5678'),
            ('Curry King', 'Authentic Indian cuisine', 2, 4.7, 40, '789 Spice Lane', '555-9012'),
            ('Wok Express', 'Chinese fast food', 3, 4.2, 35, '321 Dragon St', '555-3456'),
            ('Sweet Treats', 'Delicious desserts', 4, 4.6, 20, '654 Sugar Road', '555-7890'),
            ('Green Leaf Cafe', 'Healthy organic meals', 5, 4.4, 30, '987 Health Ave', '555-2345')
        ]
        
        cursor.executemany(
            """INSERT IGNORE INTO Restaurants 
            (restaurant_name, description, category_id, rating, delivery_time, address, contact_number) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
            restaurants
        )

    def insert_sample_menu_items(self, cursor):
        """
        Insert sample menu items for restaurants
        """
        menu_items = [
            # restaurant_id, name, description, price, category, is_vegetarian
            # Pizza Palace items
            (1, 'Margherita Pizza', 'Classic tomato and mozzarella', 12.99, 'Pizza', True),
            (1, 'Pepperoni Pizza', 'Spicy pepperoni pizza', 14.99, 'Pizza', False),
            (1, 'Vegetarian Supreme', 'Loaded with fresh vegetables', 13.99, 'Pizza', True),

            # Burger Haven items
            (2, 'Classic Cheeseburger', 'Beef patty with cheese', 10.99, 'Burger', False),
            (2, 'Veggie Burger', 'Plant-based burger', 11.99, 'Burger', True),
            (2, 'Chicken Burger', 'Grilled chicken burger', 12.99, 'Burger', False),

            # Curry King items
            (3, 'Chicken Tikka Masala', 'Creamy chicken curry', 15.99, 'Curry', False),
            (3, 'Vegetable Biryani', 'Mixed vegetable rice', 12.99, 'Rice', True),
            (3, 'Paneer Butter Masala', 'Cottage cheese in creamy sauce', 13.99, 'Vegetarian', True),

            # Wok Express items
            (4, 'Kung Pao Chicken', 'Spicy chicken with peanuts', 14.99, 'Main Course', False),
            (4, 'Vegetable Fried Rice', 'Mixed vegetable rice', 10.99, 'Rice', True),
            (4, 'Spring Rolls', 'Crispy vegetable rolls', 6.99, 'Appetizer', True),

            # Sweet Treats items
            (5, 'Chocolate Cake', 'Rich chocolate cake', 8.99, 'Dessert', True),
            (5, 'Apple Pie', 'Classic apple pie', 7.99, 'Dessert', True),
            (5, 'Cheesecake', 'New York style cheesecake', 9.99, 'Dessert', True),

            # Green Leaf Cafe items
            (6, 'Quinoa Salad', 'Healthy quinoa mix', 11.99, 'Salad', True),
            (6, 'Grilled Chicken Salad', 'Protein-packed salad', 13.99, 'Salad', False),
            (6, 'Smoothie Bowl', 'Nutritious fruit bowl', 9.99, 'Breakfast', True)
        ]
        
        cursor.executemany(
            """INSERT IGNORE INTO MenuItems 
            (restaurant_id, item_name, description, price, category, is_vegetarian) 
            VALUES (%s, %s, %s, %s, %s, %s)""", 
            menu_items
        )

    def insert_sample_users(self, cursor):
        """
        Insert sample users with hashed passwords
        """
        users = [
            # first_name, last_name, email, hashed_password, phone, address
            ('John', 'Doe', 'john.doe@example.com', 
             self.hash_password('password123'), '1234567890', '123 Main St, Anytown, USA'),
            ('Jane', 'Smith', 'jane.smith@example.com', 
             self.hash_password('securepass'), '9876543210', '456 Elm St, Somewhere, USA'),
            ('Alice', 'Johnson', 'alice.j@example.com', 
             self.hash_password('hello123'), '5555555555', '789 Oak Rd, Elsewhere, USA')
        ]
        
        cursor.executemany(
            """INSERT IGNORE INTO Users 
            (first_name, last_name, email, password, phone_number, address) 
            VALUES (%s, %s, %s, %s, %s, %s)""", 
            users
        )

    def insert_sample_orders(self, cursor):
        """
        Insert sample orders
        """
        orders = [
            # user_id, restaurant_id, total_amount, status, delivery_address
            (1, 1, 27.98, 'Delivered', '123 Main St, Anytown, USA'),
            (2, 3, 29.97, 'Out for Delivery', '456 Elm St, Somewhere, USA'),
            (3, 5, 18.98, 'Preparing', '789 Oak Rd, Elsewhere, USA')
        ]
        
        cursor.executemany(
            """INSERT IGNORE INTO Orders 
            (user_id, restaurant_id, total_amount, status, delivery_address, estimated_delivery_time) 
            VALUES (%s, %s, %s, %s, %s, DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 45 MINUTE))""", 
            orders
        )

        # Get the last inserted order IDs
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_order_id = cursor.fetchone()[0]

        # Insert order items
        order_items = [
            # order_id, menu_item_id, quantity, item_price
            (last_order_id - 2, 1, 2, 12.99),  # First order: 2 Margherita Pizzas
            (last_order_id - 1, 7, 1, 15.99),  # Second order: 1 Chicken Tikka Masala
            (last_order_id, 13, 2, 8.99)       # Third order: 2 Chocolate Cakes
        ]
        
        cursor.executemany(
            """INSERT IGNORE INTO OrderItems 
            (order_id, menu_item_id, quantity, item_price) 
            VALUES (%s, %s, %s, %s)""", 
            order_items
        )

class FoodDeliveryApp:
    def __init__(self):
        # Configure CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("Food Delivery App")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        # Initialize image handler
        self.image_handler = ImageHandler()
        
        # Ensure image directories exist
        self.ensure_image_directories()

        # Setup main UI
        self.setup_ui()

    def ensure_image_directories(self):
        """
        Ensure that image directories exist
        """
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

    def setup_ui(self):
        """
        Setup the main application user interface
        """
        # Main background frame
        main_frame = ctk.CTkFrame(self.root, fg_color="#FF8866", corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # App logo/image at the top
        try:
            # Try to load a logo if it exists
            logo_image = ctk.CTkImage(
                light_image=Image.open("images/app_logo.png"),
                dark_image=Image.open("images/app_logo.png"),
                size=(100, 100)
            )
            logo_label = ctk.CTkLabel(
                main_frame,
                image=logo_image,
                text=""
            )
            logo_label.pack(pady=(50, 0))
        except:
            # If logo doesn't exist, just use an emoji
            logo_label = ctk.CTkLabel(
                main_frame,
                text="🍔",
                font=("Arial", 72),
                text_color="white"
            )
            logo_label.pack(pady=(50, 0))

        # App title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Food Delivery App", 
            font=("Arial", 36, "bold"), 
            text_color="white"
        )
        title_label.pack(pady=(20, 50))

        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(expand=True)
        
        # Run database setup automatically
        try:
            db_setup = FoodDeliveryDatabaseSetup()
            success = db_setup.setup_complete_database()
            if success:
                print("Database setup completed successfully!")
            else:
                print("Failed to setup database. Check console for details.")
        except Exception as e:
            print(f"Database setup error: {e}")

        # Login Button
        login_btn = ctk.CTkButton(
            buttons_frame, 
            text="Login", 
            font=("Arial", 18, "bold"),
            fg_color="#FFFFFF", 
            text_color="#FF8866",
            hover_color="#F0F0F0",
            width=300, 
            height=60,
            command=self.open_login
        )
        login_btn.pack(pady=10)

        # Signup Button
        signup_btn = ctk.CTkButton(
            buttons_frame, 
            text="Sign Up", 
            font=("Arial", 18, "bold"),
            fg_color="#FFFFFF", 
            text_color="#FF8866",
            hover_color="#F0F0F0",
            width=300, 
            height=60,
            command=self.open_signup
        )
        signup_btn.pack(pady=10)
        
        # Continue as Guest Button
        guest_btn = ctk.CTkButton(
            buttons_frame, 
            text="Continue as Guest", 
            font=("Arial", 16),
            fg_color="transparent", 
            text_color="#FFFFFF",
            hover_color="rgba(255, 255, 255, 0.2)",
            border_width=2,
            border_color="#FFFFFF",
            width=300, 
            height=40,
            command=self.continue_as_guest
        )
        guest_btn.pack(pady=(20, 10))

    def setup_database(self):
        """
        Setup the database with all tables and sample data
        """
        try:
            # Create database setup instance
            db_setup = FoodDeliveryDatabaseSetup()
            
            # Show confirmation dialog
            confirmation = ctk.CTkToplevel(self.root)
            confirmation.title("Confirm Database Setup")
            confirmation.geometry("400x200")
            confirmation.resizable(False, False)
            confirmation.grab_set()
            
            # Warning message
            warning_label = ctk.CTkLabel(
                confirmation,
                text="This will create/reset the entire database. Are you sure?",
                font=("Arial", 14),
                wraplength=350
            )
            warning_label.pack(pady=(30, 20))
            
            # Buttons frame
            buttons_frame = ctk.CTkFrame(confirmation, fg_color="transparent")
            buttons_frame.pack(pady=10)
            
            # No button
            no_btn = ctk.CTkButton(
                buttons_frame,
                text="No",
                font=("Arial", 14),
                fg_color="#6B7280",
                hover_color="#4B5563",
                width=150,
                command=confirmation.destroy
            )
            no_btn.pack(side="left", padx=10)
            
            # Yes button
            yes_btn = ctk.CTkButton(
                buttons_frame,
                text="Yes",
                font=("Arial", 14),
                fg_color="#EF4444",
                hover_color="#DC2626",
                width=150,
                command=lambda: self.run_database_setup(confirmation, db_setup)
            )
            yes_btn.pack(side="left", padx=10)
            
        except Exception as e:
            self.show_error("Error", str(e))
            
    def run_database_setup(self, confirmation, db_setup):
        """Run the database setup process"""
        confirmation.destroy()
        
        # Show progress dialog
        progress_dialog = ctk.CTkToplevel(self.root)
        progress_dialog.title("Database Setup")
        progress_dialog.geometry("300x150")
        progress_dialog.grab_set()

        # Progress label
        progress_label = ctk.CTkLabel(
            progress_dialog, 
            text="Setting up database...", 
            font=("Arial", 16)
        )
        progress_label.pack(pady=20)

        # Progress bar
        progress_bar = ctk.CTkProgressBar(progress_dialog)
        progress_bar.pack(pady=10)
        progress_bar.set(0)
        progress_bar.start()

        # Attempt database setup
        try:
            # Call setup method
            success = db_setup.setup_complete_database()

            # Stop progress
            progress_bar.stop()
            progress_dialog.destroy()

            # Show result
            if success:
                self.show_success("Success", "Database setup completed successfully!")
            else:
                self.show_error("Error", "Failed to setup database. Check console for details.")

        except Exception as e:
            # Stop progress
            progress_bar.stop()
            progress_dialog.destroy()

            # Show error
            self.show_error("Database Error", f"An error occurred: {str(e)}")
            
    def show_error(self, title, message):
        """Show error message dialog"""
        error = ctk.CTkToplevel(self.root)
        error.title(title)
        error.geometry("400x200")
        error.resizable(False, False)
        error.grab_set()
        
        # Error icon
        icon_label = ctk.CTkLabel(
            error,
            text="❌",
            font=("Arial", 48),
            text_color="#EF4444"
        )
        icon_label.pack(pady=(20, 10))
        
        # Error message
        msg_label = ctk.CTkLabel(
            error,
            text=message,
            font=("Arial", 14),
            wraplength=350
        )
        msg_label.pack(pady=10)
        
        # OK button
        ok_btn = ctk.CTkButton(
            error,
            text="OK",
            command=error.destroy
        )
        ok_btn.pack(pady=10)
        
    def show_success(self, title, message):
        """Show success message dialog"""
        success = ctk.CTkToplevel(self.root)
        success.title(title)
        success.geometry("400x200")
        success.resizable(False, False)
        success.grab_set()
        
        # Success icon
        icon_label = ctk.CTkLabel(
            success,
            text="✅",
            font=("Arial", 48),
            text_color="#22C55E"
        )
        icon_label.pack(pady=(20, 10))
        
        # Success message
        msg_label = ctk.CTkLabel(
            success,
            text=message,
            font=("Arial", 14)
        )
        msg_label.pack(pady=10)
        
        # OK button
        ok_btn = ctk.CTkButton(
            success,
            text="OK",
            fg_color="#22C55E",
            hover_color="#16A34A",
            command=success.destroy
        )
        ok_btn.pack(pady=10)

    def open_login(self):
        """
        Open login page
        """
        try:
            subprocess.Popen([sys.executable, "login.py"])
            self.root.destroy()
        except Exception as e:
            self.show_error("Error", f"Unable to open login page: {e}")

    def open_signup(self):
        """
        Open signup page
        """
        try:
            subprocess.Popen([sys.executable, "signup.py"])
            self.root.destroy()
        except Exception as e:
            self.show_error("Error", f"Unable to open signup page: {e}")
            
    def continue_as_guest(self):
        """
        Continue as guest (no login required)
        """
        try:
            subprocess.Popen([sys.executable, "home.py"])  # No user_id passed
            self.root.destroy()
        except Exception as e:
            self.show_error("Error", f"Unable to continue as guest: {e}")

    def run(self):
        """
        Run the main application
        """
        self.root.mainloop()

def main():
    # Create and run the main application
    app = FoodDeliveryApp()
    app.run()

if __name__ == "__main__":
    main()