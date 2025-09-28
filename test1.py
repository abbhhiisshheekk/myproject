class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab Schedule Checker")
        self.root.geometry("550x400") # Set the window size

        # Style configuration
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12, "bold"))
        style.configure("TEntry", font=("Helvetica", 12))

        # --- Create and arrange the widgets ---
        # Frame for input fields
        input_frame = ttk.Frame(root, padding="20 10 20 10")
        input_frame.pack(fill="x")

        # Room Number widgets
        ttk.Label(input_frame, text="Room Number:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.room_entry = ttk.Entry(input_frame, width=20)
        self.room_entry.grid(row=0, column=1, padx=5, pady=5)