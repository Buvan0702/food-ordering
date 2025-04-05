import mysql.connector
from mysql.connector import Error
from typing import Optional, Tuple

class DatabaseConnection:
    """Utility class for managing database connections"""
    
    @staticmethod
    def get_connection():
        """
        Establish a connection to the MySQL database
        
        Returns:
            mysql.connector.connection: A database connection object
        
        Raises:
            Error: If connection fails
        """
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="food_system"
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL Platform: {e}")
            raise

    @staticmethod
    def execute_query(query: str, params: Optional[Tuple] = None, fetch: bool = False):
        """
        Execute a database query
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
            fetch (bool, optional): Whether to fetch results
        
        Returns:
            list or None: Query results if fetch is True
        """
        connection = None
        try:
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                results = cursor.fetchall()
                return results
            
            connection.commit()
            return None
        
        except Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()