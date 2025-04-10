import os
import customtkinter as ctk
from PIL import Image, ImageOps
import requests
from io import BytesIO

class ImageHandler:
    """Utility class for managing images in the Food Delivery App"""
    
    def __init__(self, base_directory="images/"):
        """
        Initialize the ImageHandler
        
        Args:
            base_directory (str): Base directory for image storage
        """
        self.base_directory = base_directory
        self.cache = {}  # Cache to avoid reloading the same images
        
        # Create image directories if they don't exist
        self._ensure_directories_exist()
    
    def _ensure_directories_exist(self):
        """Create necessary image directories if they don't exist"""
        directories = [
            self.base_directory,
            os.path.join(self.base_directory, "restaurants"),
            os.path.join(self.base_directory, "menu_items"),
            os.path.join(self.base_directory, "categories")
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def get_image(self, image_path, size=(100, 100)):
        """
        Load and cache an image from the given path
        
        Args:
            image_path (str): Path to the image
            size (tuple): Width and height for the image
            
        Returns:
            CTkImage or None: The loaded image or None if it failed
        """
        # Check if image exists in cache
        cache_key = f"{image_path}_{size[0]}_{size[1]}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Try to load the image
            img = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=size
            )
            # Cache the image
            self.cache[cache_key] = img
            return img
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None
    
    def get_restaurant_image(self, restaurant_id, size=(300, 200)):
        """Get a restaurant image by ID"""
        image_path = os.path.join(self.base_directory, "restaurants", f"restaurant_{restaurant_id}.png")
        
        # If image doesn't exist, download a placeholder
        if not os.path.exists(image_path):
            self._download_placeholder_image(image_path, f"Restaurant {restaurant_id}", size)
        
        return self.get_image(image_path, size)
    
    def get_menu_item_image(self, menu_item_id, size=(100, 100)):
        """Get a menu item image by ID"""
        image_path = os.path.join(self.base_directory, "menu_items", f"item_{menu_item_id}.png")
        
        # If image doesn't exist, download a placeholder
        if not os.path.exists(image_path):
            self._download_placeholder_image(image_path, f"Food {menu_item_id}", size)
        
        return self.get_image(image_path, size)
    
    def get_category_image(self, category_id, size=(80, 80)):
        """Get a category image by ID"""
        image_path = os.path.join(self.base_directory, "categories", f"category_{category_id}.png")
        
        # If image doesn't exist, download a placeholder
        if not os.path.exists(image_path):
            self._download_placeholder_image(image_path, f"Category {category_id}", size)
        
        return self.get_image(image_path, size)
    
    def _download_placeholder_image(self, save_path, text="Food", size=(100, 100)):
        """
        Download a placeholder image for a food item or restaurant
        
        Args:
            save_path (str): Path to save the image
            text (str): Text to display on the placeholder
            size (tuple): Width and height for the image
        """
        try:
            # Generate a placeholder image with text
            # This approach uses placeholder.com but you can replace with any placeholder service
            width, height = size
            url = f"https://via.placeholder.com/{width}x{height}.png/CCCCCC/666666?text={text.replace(' ', '+')}"
            
            response = requests.get(url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img.save(save_path)
                print(f"Downloaded placeholder image to {save_path}")
            else:
                self._create_local_placeholder(save_path, text, size)
        except Exception as e:
            print(f"Error downloading placeholder: {e}")
            self._create_local_placeholder(save_path, text, size)
    
    def _create_local_placeholder(self, save_path, text="Food", size=(100, 100)):
        """
        Create a local placeholder image when online service fails
        
        Args:
            save_path (str): Path to save the image
            text (str): Text to display on the placeholder
            size (tuple): Width and height for the image
        """
        try:
            # Create a blank image with text
            width, height = size
            img = Image.new('RGB', size, color=(204, 204, 204))
            
            # Save the image
            img.save(save_path)
            print(f"Created local placeholder image at {save_path}")
        except Exception as e:
            print(f"Error creating local placeholder: {e}")