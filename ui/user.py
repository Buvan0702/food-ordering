import customtkinter as ctk
import subprocess
import os

os.environ['TCL_LIBRARY'] = r"C:\Users\buvan\AppData\Local\Programs\Python\Python39\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\buvan\AppData\Local\Programs\Python\Python39\tcl\tk8.6"

# Configure CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Sample user data
user_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "address": "123 Food St, Flavor Town",
    "payment_methods": "Credit Card, PayPal"
}

# Sample order history
past_orders = [
    {"restaurant": "Pizza Palace", "date": "2025-01-01", "amount": 25.99},
    {"restaurant": "Burger Haven", "date": "2025-02-02", "amount": 15.49},
    {"restaurant": "Sweet Treats", "date": "2025-03-03", "amount": 8.99}
]

class UserProfileApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("User Profile")
        self.geometry("1000x800")
        self.resizable(False, False)

        # Main white background with rounded corners
        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text="User Profile", 
            font=("Arial", 28, "bold"), 
            text_color="#1F2937"
        )
        self.header_label.pack(pady=(30, 20))

        # Past Orders Section
        self.past_orders_label = ctk.CTkLabel(
            self.main_frame, 
            text="Past Orders", 
            font=("Arial", 20, "bold"), 
            text_color="#1F2937",
            anchor="w"
        )
        self.past_orders_label.pack(anchor="w", padx=50, pady=(20, 10))

        # Past Orders Container
        self.create_past_orders()

        # Profile & Settings Section
        self.profile_settings_label = ctk.CTkLabel(
            self.main_frame, 
            text="Profile & Settings", 
            font=("Arial", 20, "bold"), 
            text_color="#1F2937",
            anchor="w"
        )
        self.profile_settings_label.pack(anchor="w", padx=50, pady=(30, 10))

        # Profile Info Container
        self.create_profile_info()

        # Bottom Navigation
        self.create_bottom_navigation()

    def create_past_orders(self):
        """Create past orders section with cards"""
        # Container for order cards
        orders_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        orders_container.pack(fill="x", padx=50, pady=5)

        # Create cards for each past order
        for order in past_orders:
            # Order card
            order_card = ctk.CTkFrame(
                orders_container, 
                fg_color="white", 
                width=280, 
                height=150, 
                corner_radius=10,
                border_width=1,
                border_color="#E5E7EB"
            )
            order_card.pack(side="left", padx=10, pady=5)
            
            # Restaurant name
            restaurant_label = ctk.CTkLabel(
                order_card, 
                text=order["restaurant"], 
                font=("Arial", 16, "bold"), 
                text_color="#1F2937",
                anchor="w"
            )
            restaurant_label.place(x=20, y=20)
            
            # Order date
            date_label = ctk.CTkLabel(
                order_card, 
                text=f"Order Date: {order['date']}", 
                font=("Arial", 14), 
                text_color="#6B7280",
                anchor="w"
            )
            date_label.place(x=20, y=50)
            
            # Order amount (in green)
            amount_label = ctk.CTkLabel(
                order_card, 
                text=f"${order['amount']:.2f}", 
                font=("Arial", 16, "bold"), 
                text_color="#22C55E",
                anchor="w"
            )
            amount_label.place(x=20, y=80)
            
            # Reorder button (orange)
            reorder_btn = ctk.CTkButton(
                order_card, 
                text="Reorder", 
                font=("Arial", 14, "bold"), 
                fg_color="#F97316", 
                text_color="white", 
                corner_radius=5,
                hover_color="#EA580C",
                width=240, 
                height=35
            )
            reorder_btn.place(x=20, y=110)

    def create_profile_info(self):
        """Create profile information section"""
        # Profile info container
        profile_container = ctk.CTkFrame(
            self.main_frame, 
            fg_color="white", 
            corner_radius=10,
            border_width=1,
            border_color="#E5E7EB"
        )
        profile_container.pack(fill="x", padx=50, pady=5)

        # User information fields
        fields = [
            {"label": "Name:", "value": user_data["name"]},
            {"label": "Email:", "value": user_data["email"]},
            {"label": "Address:", "value": user_data["address"]},
            {"label": "Payment Methods:", "value": user_data["payment_methods"]}
        ]

        # Add each field with proper spacing
        for i, field in enumerate(fields):
            # Label
            label = ctk.CTkLabel(
                profile_container, 
                text=field["label"], 
                font=("Arial", 14), 
                text_color="#1F2937",
                anchor="w"
            )
            label.grid(row=i, column=0, sticky="w", padx=(20, 10), pady=15)
            
            # Value (right-aligned)
            value = ctk.CTkLabel(
                profile_container, 
                text=field["value"], 
                font=("Arial", 14), 
                text_color="#1F2937",
                anchor="e"
            )
            value.grid(row=i, column=1, sticky="e", padx=(10, 20), pady=15)

        # Configure grid to make value column expand
        profile_container.grid_columnconfigure(1, weight=1)
        
        # Edit Profile Button (green)
        edit_btn = ctk.CTkButton(
            profile_container, 
            text="Edit Profile", 
            font=("Arial", 14, "bold"), 
            fg_color="#22C55E", 
            text_color="white", 
            corner_radius=5,
            hover_color="#16A34A",
            width=880, 
            height=40
        )
        edit_btn.grid(row=len(fields), column=0, columnspan=2, padx=20, pady=20, sticky="ew")

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
            {"name": "Orders", "icon": "📦", "active": False},
            {"name": "Cart", "icon": "🛒", "active": False},
            {"name": "Profile", "icon": "👤", "active": True},
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
    app = UserProfileApp()
    app.mainloop()