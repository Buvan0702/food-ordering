import customtkinter as ctk
import subprocess
import os

os.environ['TCL_LIBRARY'] = r"C:\Users\buvan\AppData\Local\Programs\Python\Python39\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\buvan\AppData\Local\Programs\Python\Python39\tcl\tk8.6"

# Configure CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Sample Order Data
order_details = {
    "food_name": "Pizza",
    "price": 12.99,
    "quantity": 1,
    "estimated_time": "15:00",
    "status": 2,  # 0: Order Placed, 1: Preparing, 2: Out for Delivery, 3: Delivered
    "address": "123 Main Street, New York, NY 10001"
}

class OrderTrackingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Order Tracking")
        self.geometry("1000x1000")
        self.resizable(False, False)

        # Main white background with rounded corners
        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a white inner card
        self.card_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=15, border_width=1, border_color="#E5E7EB")
        self.card_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # Header
        self.header_label = ctk.CTkLabel(
            self.card_frame, 
            text="Order Tracking", 
            font=("Arial", 28, "bold"), 
            text_color="#1F2937"
        )
        self.header_label.pack(pady=(20, 30))

        # Estimated Delivery Time
        self.time_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.time_frame.pack(fill="x", padx=30, pady=5)
        
        self.time_label = ctk.CTkLabel(
            self.time_frame, 
            text="Estimated Delivery Time:", 
            font=("Arial", 16, "bold"), 
            text_color="#1F2937",
            anchor="w"
        )
        self.time_label.pack(side="left")
        
        self.time_value = ctk.CTkLabel(
            self.time_frame, 
            text=order_details["estimated_time"], 
            font=("Arial", 16, "bold"), 
            text_color="#EF4444",
            anchor="e"
        )
        self.time_value.pack(side="right")

        # Order Status Tracking
        self.create_order_tracking()

        # Your Order Heading
        self.order_heading = ctk.CTkLabel(
            self.card_frame, 
            text="Your Order", 
            font=("Arial", 18, "bold"), 
            text_color="#1F2937",
            anchor="w"
        )
        self.order_heading.pack(anchor="w", padx=30, pady=(25, 10))

        # Order Details
        self.create_order_details()

        # Delivery Location
        self.delivery_heading = ctk.CTkLabel(
            self.card_frame, 
            text="Delivery Location", 
            font=("Arial", 18, "bold"), 
            text_color="#1F2937",
            anchor="w"
        )
        self.delivery_heading.pack(anchor="w", padx=30, pady=(25, 10))

        # Map Placeholder
        self.create_map_placeholder()

        # Bottom Navigation
        self.create_bottom_navigation()

    def create_order_tracking(self):
        """Create the order tracking progress visualization"""
        # Status steps with emojis
        status_steps = [
            {"name": "Order Placed", "emoji": "✅"},
            {"name": "Preparing", "emoji": "🍳"},
            {"name": "Out for Delivery", "emoji": "🚚"},
            {"name": "Delivered", "emoji": "🎉"}
        ]
        
        # Frame for tracking visualization
        tracking_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        tracking_frame.pack(fill="x", padx=30, pady=10)
        
        # Calculate widths
        step_width = 220  # Approximate width per step
        total_width = step_width * len(status_steps)
        progress_width = step_width * order_details["status"] + (step_width/2 if order_details["status"] > 0 else 0)
        
        # Progress line container
        line_container = ctk.CTkFrame(tracking_frame, fg_color="transparent", height=50)
        line_container.pack(fill="x", pady=10)
        
        # Background progress line - FIXED: Set width in constructor
        progress_bg = ctk.CTkFrame(line_container, height=4, width=total_width, fg_color="#E5E7EB")
        progress_bg.place(relx=0.5, y=25, anchor="center")
        
        # Highlighted progress line - FIXED: Set width in constructor
        if progress_width > 0:
            progress_complete = ctk.CTkFrame(line_container, height=4, width=progress_width, fg_color="#22C55E")
            progress_complete.place(x=(total_width - progress_width)/2, y=25)
        
        # Status labels container
        status_container = ctk.CTkFrame(tracking_frame, fg_color="transparent", height=60)
        status_container.pack(fill="x")
        
        # Create status steps evenly spaced
        for i, step in enumerate(status_steps):
            # Calculate x position
            x_pos = (i / (len(status_steps) - 1)) * 0.9 + 0.05  # 5% margins on each side
            
            # Status text
            status_label = ctk.CTkLabel(
                status_container, 
                text=f"{step['name']} {step['emoji']}",
                font=("Arial", 14, "bold" if i <= order_details["status"] else "normal"),
                text_color="#1F2937" if i <= order_details["status"] else "#9CA3AF"
            )
            status_label.place(relx=x_pos, rely=0.5, anchor="center")

    def create_order_details(self):
        """Create order details section with food item"""
        order_frame = ctk.CTkFrame(self.card_frame, fg_color="#F9FAFB", corner_radius=10)
        order_frame.pack(fill="x", padx=30, pady=5)
        
        # Image placeholder
        img_placeholder = ctk.CTkFrame(order_frame, fg_color="#E5E7EB", width=80, height=80, corner_radius=5)
        img_placeholder.pack(side="left", padx=20, pady=15)
        
        # "80 × 80" text in the center of the placeholder
        placeholder_text = ctk.CTkLabel(img_placeholder, text="80 × 80", font=("Arial", 10), text_color="#9CA3AF")
        placeholder_text.place(relx=0.5, rely=0.5, anchor="center")
        
        # Food details
        details_frame = ctk.CTkFrame(order_frame, fg_color="transparent", width=200)
        details_frame.pack(side="left", fill="y", pady=15, padx=(0, 20))
        
        # Food name
        food_name = ctk.CTkLabel(
            details_frame, 
            text=order_details["food_name"], 
            font=("Arial", 16, "bold"), 
            text_color="#1F2937",
            anchor="w"
        )
        food_name.pack(anchor="w")
        
        # Price
        price = ctk.CTkLabel(
            details_frame, 
            text=f"${order_details['price']:.2f}", 
            font=("Arial", 14), 
            text_color="#6B7280",
            anchor="w"
        )
        price.pack(anchor="w", pady=(5, 0))
        
        # Quantity (right-aligned)
        quantity = ctk.CTkLabel(
            order_frame, 
            text=f"Quantity: {order_details['quantity']}", 
            font=("Arial", 14), 
            text_color="#1F2937"
        )
        quantity.pack(side="right", padx=20)

    def create_map_placeholder(self):
        """Create a map placeholder for delivery location"""
        map_frame = ctk.CTkFrame(self.card_frame, fg_color="#F1F2F3", height=180, corner_radius=10)
        map_frame.pack(fill="x", padx=30, pady=5)
        
        # Inner lighter section
        inner_map = ctk.CTkFrame(map_frame, fg_color="#E5E7EB", width=300, height=140, corner_radius=5)
        inner_map.place(relx=0.5, rely=0.5, anchor="center")
        
        # Map placeholder text
        map_text = ctk.CTkLabel(inner_map, text="Map Placeholder", font=("Arial", 18), text_color="#9CA3AF")
        map_text.place(relx=0.5, rely=0.5, anchor="center")

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
            {"name": "Home", "icon": "🏠", "active": False},
            {"name": "Orders", "icon": "📦", "active": True},
            {"name": "Cart", "icon": "🛒", "active": False},
            {"name": "Profile", "icon": "👤", "active": False},
            {"name": "Settings", "icon": "⚙️", "active": False}
        ]
        
        # Create navigation buttons
        for item in nav_items:
            nav_frame = ctk.CTkFrame(nav_bar, fg_color="transparent", width=80)
            nav_frame.pack(side="left", expand=True, fill="y")
            
            # Color for active/inactive items
            text_color = "#22C55E" if item["active"] else "#1F2937"
            
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

# Run the application
if __name__ == "__main__":
    app = OrderTrackingApp()
    app.mainloop()