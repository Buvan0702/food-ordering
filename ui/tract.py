import customtkinter as ctk
import subprocess
import sys
from db_connection import DatabaseConnection
from datetime import datetime, timedelta

class OrderTrackingApp:
    def __init__(self, user_id=None):
        # Configure CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Create the main window
        self.root = ctk.CTk()
        self.root.title("Order Tracking")
        self.root.geometry("1000x1000")
        self.root.resizable(False, False)

        # Store user ID
        self.user_id = user_id

        # Order status mapping
        self.status_map = {
            0: "Order Placed",
            1: "Preparing",
            2: "Out for Delivery",
            3: "Delivered"
        }

        # Fetch orders for the user
        self.orders = self.fetch_user_orders()

        # Current order index (for multiple orders)
        self.current_order_index = 0

        # Setup UI
        self.setup_ui()

    def fetch_user_orders(self):
        """
        Fetch active orders for the current user
        """
        if not self.user_id:
            return []

        try:
            query = """
            SELECT o.order_id, o.total_amount, o.order_date, o.status, 
                   o.estimated_delivery_time, o.delivery_address,
                   r.restaurant_name,
                   oi.quantity, mi.item_name, mi.price
            FROM Orders o
            JOIN OrderItems oi ON o.order_id = oi.order_id
            JOIN MenuItems mi ON oi.menu_item_id = mi.menu_item_id
            JOIN Restaurants r ON mi.restaurant_id = r.restaurant_id
            WHERE o.user_id = %s AND o.status < 3
            ORDER BY o.order_date DESC
            """
            orders = DatabaseConnection.execute_query(
                query, 
                params=(self.user_id,), 
                fetch=True
            )
            return orders
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return []

    def setup_ui(self):
        """
        Setup the user interface for the order tracking page
        """
        # Main white background with rounded corners
        self.main_frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a white inner card
        self.card_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=15, border_width=1, border_color="#E5E7EB")
        self.card_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # Header with order navigation
        self.create_header()

        # No orders message
        if not self.orders:
            self.show_no_orders()
            self.create_bottom_navigation()
            return

        # Current order details
        self.current_order = self.orders[self.current_order_index]

        # Estimated Delivery Time
        self.create_estimated_time()

        # Order Status Tracking
        self.create_order_tracking()

        # Your Order Heading
        self.create_order_details()

        # Delivery Location
        self.create_delivery_location()

        # Bottom Navigation
        self.create_bottom_navigation()

    def create_header(self):
        """
        Create header with order navigation
        """
        header_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))

        # Header title
        self.header_label = ctk.CTkLabel(
            header_frame, 
            text="Order Tracking", 
            font=("Arial", 28, "bold"), 
            text_color="#1F2937"
        )
        self.header_label.pack(side="left")

        # Order navigation for multiple orders
        if len(self.orders) > 1:
            # Previous order button
            prev_btn = ctk.CTkButton(
                header_frame, 
                text="◀", 
                width=40, 
                font=("Arial", 16, "bold"),
                fg_color="#F3F4F6",
                text_color="#1F2937",
                hover_color="#E5E7EB",
                command=self.prev_order
            )
            prev_btn.pack(side="right", padx=(10, 5))

            # Next order button
            next_btn = ctk.CTkButton(
                header_frame, 
                text="▶", 
                width=40, 
                font=("Arial", 16, "bold"),
                fg_color="#F3F4F6",
                text_color="#1F2937",
                hover_color="#E5E7EB",
                command=self.next_order
            )
            next_btn.pack(side="right")

            # Order count label
            self.order_count_label = ctk.CTkLabel(
                header_frame, 
                text=f"Order {self.current_order_index + 1} of {len(self.orders)}", 
                font=("Arial", 14),
                text_color="#6B7280"
            )
            self.order_count_label.pack(side="right", padx=10)

    def prev_order(self):
        """Navigate to previous order"""
        if self.current_order_index > 0:
            self.current_order_index -= 1
            self.update_order_display()

    def next_order(self):
        """Navigate to next order"""
        if self.current_order_index < len(self.orders) - 1:
            self.current_order_index += 1
            self.update_order_display()

    def update_order_display(self):
        """Update the display with current order details"""
        # Update current order
        self.current_order = self.orders[self.current_order_index]

        # Update order count label if it exists
        if hasattr(self, 'order_count_label'):
            self.order_count_label.configure(
                text=f"Order {self.current_order_index + 1} of {len(self.orders)}"
            )

        # Recreate dynamic sections
        # Clear existing widgets
        widgets_to_destroy = [
            'time_frame', 'tracking_frame', 'order_heading', 
            'order_frame', 'delivery_heading', 'map_frame'
        ]
        for widget_name in widgets_to_destroy:
            if hasattr(self, widget_name):
                getattr(self, widget_name).destroy()

        # Recreate sections
        self.create_estimated_time()
        self.create_order_tracking()
        self.create_order_details()
        self.create_delivery_location()

    def show_no_orders(self):
        """
        Display message when no active orders exist
        """
        no_orders_label = ctk.CTkLabel(
            self.card_frame, 
            text="No Active Orders", 
            font=("Arial", 24, "bold"), 
            text_color="#6B7280"
        )
        no_orders_label.pack(expand=True)

    def create_estimated_time(self):
        """
        Create estimated delivery time section
        """
        # Estimated Delivery Time frame
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
        
        # Convert estimated time to readable format
        est_time = self.current_order.get('estimated_delivery_time', '')
        self.time_value = ctk.CTkLabel(
            self.time_frame, 
            text=est_time, 
            font=("Arial", 16, "bold"), 
            text_color="#EF4444",
            anchor="e"
        )
        self.time_value.pack(side="right")

    def create_order_tracking(self):
        """
        Create order tracking progress visualization
        """
        # Status steps with emojis
        status_steps = [
            {"name": "Order Placed", "emoji": "✅"},
            {"name": "Preparing", "emoji": "🍳"},
            {"name": "Out for Delivery", "emoji": "🚚"},
            {"name": "Delivered", "emoji": "🎉"}
        ]
        
        # Frame for tracking visualization
        self.tracking_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.tracking_frame.pack(fill="x", padx=30, pady=10)
        
        # Calculate widths
        step_width = 220  # Approximate width per step
        total_width = step_width * len(status_steps)
        current_status = self.current_order.get('status', 0)
        progress_width = step_width * current_status + (step_width/2 if current_status > 0 else 0)
        
        # Progress line container
        line_container = ctk.CTkFrame(self.tracking_frame, fg_color="transparent", height=50)
        line_container.pack(fill="x", pady=10)
        
        # Background progress line
        progress_bg = ctk.CTkFrame(line_container, height=4, width=total_width, fg_color="#E5E7EB")
        progress_bg.place(relx=0.5, y=25, anchor="center")
        
        # Highlighted progress line
        if progress_width > 0:
            progress_complete = ctk.CTkFrame(line_container, height=4, width=progress_width, fg_color="#22C55E")
            progress_complete.place(x=(total_width - progress_width)/2, y=25)
        
        # Status labels container
        status_container = ctk.CTkFrame(self.tracking_frame, fg_color="transparent", height=60)
        status_container.pack(fill="x")
        
        # Create status steps evenly spaced
        for i, step in enumerate(status_steps):
            # Calculate x position
            x_pos = (i / (len(status_steps) - 1)) * 0.9 + 0.05  # 5% margins on each side
            
            # Status text
            status_label = ctk.CTkLabel(
                status_container, 
                text=f"{step['name']} {step['emoji']}",
                font=("Arial", 14, "bold" if i <= current_status else "normal"),
                text_color="#1F2937" if i <= current_status else "#9CA3AF"
            )
            status_label.place(relx=x_pos, rely=0.5, anchor="center")

    def create_order_details(self):
        """
        Create order details section with food items
        """
        # Your Order Heading
        self.order_heading = ctk.CTkLabel(
            self.card_frame, 
            text="Your Order", 
            font=("Arial", 18, "bold"), 
            text_color="#1F2937",
            anchor="w"
        )
        self.order_heading.pack(anchor="w", padx=30, pady=(25, 10))

        # Order frame
        self.order_frame = ctk.CTkFrame(self.card_frame, fg_color="#F9FAFB", corner_radius=10)
        self.order_frame.pack(fill="x", padx=30, pady=5)
        
        # Image placeholder
        img_placeholder = ctk.CTkFrame(self.order_frame, fg_color="#E5E7EB", width=80, height=80, corner_radius=5)
        img_placeholder.pack(side="left", padx=20, pady=15)
        
        # "80 × 80" text in the center of the placeholder
        placeholder_text = ctk.CTkLabel(img_placeholder, text="80 × 80", font=("Arial", 10), text_color="#9CA3AF")
        placeholder_text.place(relx=0.5, rely=0.5, anchor="center")
        
        # Food details
        details_frame = ctk.CTkFrame(self.order_frame, fg_color="transparent", width=200)
        details_frame.pack(side="left", fill="y", pady=15, padx=(0, 20))
        
        # Restaurant name
        restaurant_name = ctk.CTkLabel(
            details_frame, 
            text=self.current_order.get('restaurant_name', 'Restaurant'), 
            font=("Arial", 16, "bold"), 
            text_color="#1F2937",
            anchor="w"
        )
        restaurant_name.pack(anchor="w")
        
        # Food name
        food_name = ctk.CTkLabel(
            details_frame, 
            text=self.current_order.get('item_name', 'Food Item'), 
            font=("Arial", 14), 
            text_color="#6B7280",
            anchor="w"
        )
        food_name.pack(anchor="w", pady=(5, 0))
        
        # Price and Quantity
        price_qty_frame = ctk.CTkFrame(self.order_frame, fg_color="transparent")
        price_qty_frame.pack(side="right", padx=20)
        
        price = ctk.CTkLabel(
            price_qty_frame, 
            text=f"${self.current_order.get('price', 0):.2f}", 
            font=("Arial", 14), 
            text_color="#1F2937"
        )
        price.pack(side="top")
        
        quantity = ctk.CTkLabel(
            price_qty_frame, 
            text=f"Quantity: {self.current_order.get('quantity', 0)}", 
            font=("Arial", 14), 
            text_color="#6B7280"
        )
        quantity.pack(side="top", pady=(5, 0))

    def create_delivery_location(self):
        """
        Create delivery location section
        """
        # Delivery Location Heading
        self.delivery_heading = ctk.CTkLabel(
            self.card_frame, 
            text="Delivery Location", 
            font=("Arial", 18, "bold"), 
            text_color="#1F2937",
            anchor="w"
        )
        self.delivery_heading.pack(anchor="w", padx=30, pady=(25, 10))

        # Map Placeholder
        self.map_frame = ctk.CTkFrame(self.card_frame, fg_color="#F1F2F3", height=180, corner_radius=10)
        self.map_frame.pack(fill="x", padx=30, pady=5)
        
        # Address details
        address_frame = ctk.CTkFrame(self.map_frame, fg_color="transparent")
        address_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Address text
        address_label = ctk.CTkLabel(
            address_frame, 
            text=self.current_order.get('delivery_address', 'No Address Provided'), 
            font=("Arial", 16), 
            text_color="#1F2937",
            wraplength=500,
            justify="center"
        )
        address_label.pack()

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
            {"name": "Home", "icon": "🏠", "action": self.go_to_home},
            {"name": "Orders", "icon": "📦", "action": self.stay_on_orders, "active": True},
            {"name": "Cart", "icon": "🛒", "action": self.go_to_cart},
            {"name": "Profile", "icon": "👤", "action": self.go_to_profile},
            {"name": "Settings", "icon": "⚙️", "action": self.go_to_settings}
        ]
        
        # Create navigation buttons
        for item in nav_items:
            nav_frame = ctk.CTkFrame(nav_bar, fg_color="transparent", width=80)
            nav_frame.pack(side="left", expand=True, fill="y")
            
            # Color for active/inactive items
            text_color = "#22C55E" if item.get("active", False) else "#1F2937"
            
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

            # Bind click events
            for widget in [icon_label, text_label]:
                widget.bind("<Button-1>", lambda e, action=item['action']: action())

    def go_to_home(self):
        """Navigate to home page"""
        try:
            subprocess.Popen([sys.executable, "home.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error going to home: {e}")

    def go_to_cart(self):
        """Navigate to cart page"""
        try:
            subprocess.Popen([sys.executable, "cart.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error going to cart: {e}")

    def stay_on_orders(self):
        """Do nothing, already on orders page"""
        pass

    def go_to_profile(self):
        """Navigate to profile page"""
        try:
            subprocess.Popen([sys.executable, "profile.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error going to profile: {e}")

    def go_to_settings(self):
        """Navigate to settings page"""
        try:
            subprocess.Popen([sys.executable, "settings.py", str(self.user_id)])
            self.root.destroy()
        except Exception as e:
            print(f"Error going to settings: {e}")

def main():
    # Check if user ID is passed as command-line argument
    user_id = None
    if len(sys.argv) > 1:
        try:
            user_id = int(sys.argv[1])
        except ValueError:
            print("Invalid user ID")

    # Create and run order tracking page
    app = OrderTrackingApp(user_id)
    app.root.mainloop()

if __name__ == "__main__":
    main()