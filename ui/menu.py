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
            sys.exit(1)  # Exit the application if database connection fails

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
            sys.exit(1)  # Exit the application if database setup fails

    def _create_tables(self, cursor):
        """
        Create all necessary database tables
        """
        # Existing table creation code remains the same as in previous implementation
        # (All the CREATE TABLE statements you had before)
        # [Table creation code from previous implementation]
        pass  # Replace with actual table creation code

    def _insert_sample_data(self, cursor):
        """
        Insert sample data into tables
        """
        # Existing sample data insertion code remains the same
        # (All the INSERT statements you had before)
        # [Sample data insertion code from previous implementation]
        pass  # Replace with actual sample data insertion code

class FoodDeliveryApp:
    def __init__(self):
        # Automatically setup database before initializing UI
        self._setup_database()

        # Configure CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("Food Delivery App")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        # Setup main UI
        self._setup_ui()

    def _setup_database(self):
        """
        Setup database automatically when application starts
        """
        try:
            db_setup = DatabaseSetup()
            db_setup.setup_database()
        except Exception as e:
            print(f"Fatal Error: Could not set up database - {e}")
            sys.exit(1)

    def _setup_ui(self):
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
            command=self._open_login
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
            command=self._open_signup
        )
        signup_btn.pack(pady=10)

    def _open_login(self):
        """
        Open login page
        """
        try:
            subprocess.Popen([sys.executable, "login.py"])
            self.root.destroy()
        except Exception as e:
            print(f"Error opening login page: {e}")

    def _open_signup(self):
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