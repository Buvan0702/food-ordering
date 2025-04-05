import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
import subprocess
import sys
import hashlib

class DatabaseSetup:
    def __init__(self, host='localhost', user='root', password='new_password'):
        """
        Initialize database setup with connection parameters
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = 'food_system'

    def hash_password(self, password):
        """
        Hash password using SHA-256
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def create_connection(self, database=None):
        """
        Create a database connection
        """
        try:
            if database:
                connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=database
                )
            else:
                connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
                )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def setup_database(self):
        """
        Comprehensive database setup with all tables and sample data
        """
        try:
            # Create connection without specifying database
            connection = self.create_connection()
            cursor = connection.cursor()

            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")

            # Create all necessary tables
            self._create_tables(cursor)

            # Insert sample data
            self._insert_sample_data(cursor)

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

    def _create_tables(self, cursor):
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

    def _insert_sample_data(self, cursor):
        """
        Insert sample data into tables
        """
        # Insert Categories
        categories = [
            ('FastFood', 'Quick and convenient meals'),
            ('Indian', 'Traditional Indian cuisine'),
            ('Chinese', 'Chinese and Asian dishes'),
            ('Desserts', 'Sweet treats and desserts'),
            ('Healthy', 'Nutritious and health-conscious options')
        ]
        cursor.executemany(
            "INSERT IGNORE INTO Categories (category_name, description) VALUES (%s, %s)", 
            categories
        )

        # Insert Restaurants
        restaurants = [
            ('Pizza Palace', 'Best pizzas in town', 1, 4.5, 30, '123 Main St', '555-1234'),
            ('Burger Haven', 'Gourmet burgers', 1, 4.3, 25, '456 Elm St', '555-5678'),
            ('Curry King', 'Authentic Indian cuisine', 2, 4.7, 40, '789 Spice Lane', '555-9012')
        ]
        cursor.executemany(
            """INSERT IGNORE INTO Restaurants 
            (restaurant_name, description, category_id, rating, delivery_time, address, contact_number) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
            restaurants
        )

        # Insert Menu Items
        menu_items = [
            (1, 'Margherita Pizza', 'Classic tomato and mozzarella', 12.99, 'Pizza', True),
            (1, 'Pepperoni Pizza', 'Spicy pepperoni pizza', 14.99, 'Pizza', False),
            (2, 'Classic Cheeseburger', 'Beef patty with cheese', 10.99, 'Burger', False),
            (2, 'Veggie Burger', 'Plant-based burger', 11.99, 'Burger', True),
            (3, 'Chicken Tikka Masala', 'Creamy chicken curry', 15.99, 'Curry', False)
        ]
        cursor.executemany(
            """INSERT IGNORE INTO MenuItems 
            (restaurant_id, item_name, description, price, category, is_vegetarian) 
            VALUES (%s, %s, %s, %s, %s, %s)""", 
            menu_items
        )

        # Insert Users
        users = [
            ('John', 'Doe', 'john.doe@example.com', 
             self.hash_password('password123'), '1234567890', '123 Main St, Anytown, USA'),
            ('Jane', 'Smith', 'jane.smith@example.com', 
             self.hash_password('securepass'), '9876543210', '456 Elm St, Somewhere, USA')
        ]
        cursor.executemany(
            """INSERT IGNORE INTO Users 
            (first_name, last_name, email, password, phone_number, address) 
            VALUES (%s, %s, %s, %s, %s, %s)""", 
            users
        )

class FoodDeliveryApp:
    def __init__(self):
        # Automatically setup database before initializing UI
        self.setup_database()

        # Configure CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("Food Delivery App")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        # Setup main UI
        self.setup_ui()

    def setup_database(self):
        """
        Setup database automatically when application starts
        """
        db_setup = DatabaseSetup()
        db_setup.setup_database()

    def setup_ui(self):
        """
        Setup the main application user interface
        """
        # Main background frame
        main_frame = ctk.CTkFrame(self.root, fg_color="#FF8866", corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # App title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Food Delivery App", 
            font=("Arial", 36, "bold"), 
            text_color="white"
        )
        title_label.pack(pady=(100, 50))

        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(expand=True)

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

    def open_login(self):
        """
        Open login page
        """
        try:
            subprocess.Popen([sys.executable, "login.py"])
            self.root.destroy()
        except Exception as e:
            print(f"Error opening login page: {e}")

    def open_signup(self):
        """
        Open signup page
        """
        try:
            subprocess.Popen([sys.executable, "signup.py"])
            self.root.destroy()
        except Exception as e:
            print(f"Error opening signup page: {e}")

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