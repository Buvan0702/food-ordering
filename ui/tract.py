import customtkinter as ctk

# Sample Order Data
order_details = {
    "food_name": "Delicious Pizza",
    "price": 12.99,
    "quantity": 1,
    "estimated_time": "15:00",
    "status": 2,  # 0: Placed, 1: Preparing, 2: Out for Delivery, 3: Delivered
    "address": "123, MG Road, Bangalore, India"
}

# Status Steps
status_steps = ["Order Placed", "Preparing", "Out for Delivery", "Delivered"]

class OrderTrackingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Order Tracking")
        self.geometry("900x550")
        
        # Set Light Theme Colors
        ctk.set_appearance_mode("light")
        self.configure(bg="white")

        # Header
        ctk.CTkLabel(self, text="📦 Order Tracking", font=("Arial", 22, "bold"), text_color="black").pack(pady=10)

        # Delivery Time & Address
        self.create_delivery_section()

        # Progress Bar
        self.create_progress_bar()

        # Order Details
        ctk.CTkLabel(self, text="Your Order", font=("Arial", 16, "bold"), text_color="black").pack(anchor="w", padx=20, pady=10)
        self.create_order_card()

        # Navigation Bar
        self.create_navbar()

    def create_delivery_section(self):
        """Creates the estimated delivery section with address."""
        frame = ctk.CTkFrame(self, fg_color="#F8F9FA", corner_radius=10)
        frame.pack(fill="x", padx=20, pady=5)

        # Delivery Time
        ctk.CTkLabel(frame, text="Estimated Delivery Time:", font=("Arial", 14, "bold"), text_color="black").pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(frame, text=order_details["estimated_time"], font=("Arial", 14, "bold"), text_color="red").pack(side="right", padx=20)

        # Delivery Address
        ctk.CTkLabel(frame, text="Delivery Address:", font=("Arial", 12, "bold"), text_color="black").pack(anchor="w", padx=10, pady=2)
        ctk.CTkLabel(frame, text=order_details["address"], font=("Arial", 12), text_color="gray").pack(anchor="w", padx=10, pady=2)

    def create_progress_bar(self):
        """Creates a real progress bar."""
        progress_frame = ctk.CTkFrame(self, fg_color="white")
        progress_frame.pack(fill="x", padx=20, pady=5)

        progress_bar = ctk.CTkProgressBar(progress_frame, width=800, height=12, fg_color="lightgray", progress_color="#3498DB")
        progress_bar.pack(pady=10)
        progress_bar.set(order_details["status"] / (len(status_steps) - 1))  # Normalize progress

        # Status Labels
        status_frame = ctk.CTkFrame(progress_frame, fg_color="white")
        status_frame.pack(fill="x", pady=5)

        for i, step in enumerate(status_steps):
            color = "black" if i <= order_details["status"] else "gray"
            ctk.CTkLabel(status_frame, text=step, font=("Arial", 10, "bold"), text_color=color).pack(side="left", expand=True)

    def create_order_card(self):
        """Creates a structured order card."""
        order_frame = ctk.CTkFrame(self, fg_color="#F8F9FA", corner_radius=10, border_width=1, border_color="gray")
        order_frame.pack(pady=5, padx=20, fill="x")

        # Order Details
        text_frame = ctk.CTkFrame(order_frame, fg_color="#F8F9FA")
        text_frame.pack(pady=10, padx=10, expand=True)

        ctk.CTkLabel(text_frame, text=order_details["food_name"], font=("Arial", 14, "bold"), text_color="black").pack(anchor="w")
        ctk.CTkLabel(text_frame, text=f"Price: ${order_details['price']:.2f}", font=("Arial", 12), text_color="black").pack(anchor="w")
        ctk.CTkLabel(text_frame, text=f"Quantity: {order_details['quantity']}", font=("Arial", 12), text_color="black").pack(anchor="w")

    def create_navbar(self):
        """Creates a bottom navigation bar."""
        nav_frame = ctk.CTkFrame(self, fg_color="white", height=50)
        nav_frame.pack(side="bottom", fill="x")

        nav_items = ["🏠 Home", "📦 Orders", "🛒 Cart", "👤 Profile", "⚙️ Settings"]
        colors = ["#2ECC71", "#E67E22", "#3498DB", "#9B59B6", "#95A5A6"]

        for item, color in zip(nav_items, colors):
            ctk.CTkButton(nav_frame, text=item, font=("Arial", 10), fg_color="white", text_color=color, width=100, height=30).pack(side="left", expand=True)


# Run the Tkinter App
if __name__ == "__main__":
    app = OrderTrackingApp()
    app.mainloop()
