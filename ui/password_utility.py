import hashlib
import re
import secrets

class PasswordManager:
    """Utility class for password management"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using SHA-256
        
        Args:
            password (str): Plain text password
        
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate password strength
        
        Criteria:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        - Contains at least one special character
        
        Args:
            password (str): Password to validate
        
        Returns:
            bool: Whether password meets strength requirements
        """
        # Check minimum length
        if len(password) < 8:
            return False
        
        # Check for at least one uppercase, one lowercase, one digit, and one special character
        patterns = [
            r'[A-Z]',  # Uppercase
            r'[a-z]',  # Lowercase
            r'\d',     # Digit
            r'[!@#$%^&*(),.?":{}|<>]'  # Special character
        ]
        
        return all(re.search(pattern, password) for pattern in patterns)
    
    @staticmethod
    def generate_reset_token(length: int = 32) -> str:
        """
        Generate a secure random reset token
        
        Args:
            length (int, optional): Length of the token. Defaults to 32.
        
        Returns:
            str: Secure random token
        """
        return secrets.token_hex(length // 2)