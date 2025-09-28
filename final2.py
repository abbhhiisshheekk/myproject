import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- LOAD SCHEDULE FROM JSON ---
JSON_FILE = "schedule.json"

if not os.path.exists(JSON_FILE):
    messagebox.showerror("Error", f"'{JSON_FILE}' not found. Please create the file.")
    exit()

try:
    with open(JSON_FILE, "r") as f:
        schedule = json.load(f)
except json.JSONDecodeError:
    messagebox.showerror("Error", f"'{JSON_FILE}' is not a valid JSON file.")
    exit()
# --- END OF LOADING ---

class ScheduleApp:
    # --- Define a clean, professional color palette ---
    BG_COLOR = "#F7F7F7"        # Off-white background
    TEXT_COLOR = "#333333"      # Dark grey text
    INPUT_BG_COLOR = "#FFFFFF"  # White for input fields
    PRIMARY_COLOR = "#3A7FF6"   # Professional blue for interaction
    PRIMARY_HOVER = "#5C9AFF"   # Lighter blue for hover
    BORDER_COLOR = "#DCDCDC"    # Light grey for borders

    def __init__(self, root):
        self.root = root
        self.root.title("Lab Schedule Checker")
        self.root.geometry("600x520") # Slightly taller for the new layout
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)

        # Set the application's font
        self.app_font = ("Segoe UI", 11)

        self.setup_styles()

        # --- Prepare lists for dropdowns ---
        self.day_list = list(schedule.keys()) if schedule else ["No Days Found"]
        room_set = set()
        if schedule:
            for day_data in schedule.values():
                room_set.update(day_data.keys())
        self.room_list = sorted(list(room_set)) if room_set else ["No Rooms Found"]

        # --- Create and arrange the widgets ---
        main_frame = ttk.Frame(root, padding=20, style="Main.TFrame")
        main_frame.pack(expand=True, fill="both")

        # Main Title
        title_label = ttk.Label(
            main_frame, text="Lab Schedule Checker",
            style="Title.TLabel",
            anchor="center"
        )
        title_label.pack(pady=(0, 20), fill="x")

        # --- Input Panel ---
        input_panel = ttk.Labelframe(main_frame, text=" Selection ", style="Custom.TLabelframe")
        input_panel.pack(fill="x")
        input_panel.columnconfigure(1, weight=1)

        # Room dropdown
        ttk.Label(input_panel, text="Room Number:", style="Custom.TLabel").grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")
        self.room_entry = ttk.Combobox(input_panel, values=self.room_list, state="readonly", font=self.app_font)
        self.room_entry.grid(row=0, column=1, padx=15, pady=(15, 10), sticky="ew")
        if self.room_list:
            self.room_entry.set(self.room_list[0])

        # Day dropdown
        ttk.Label(input_panel, text="Day:", style="Custom.TLabel").grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.day_entry = ttk.Combobox(input_panel, values=self.day_list, state="readonly", font=self.app_font)
        self.day_entry.grid(row=1, column=1, padx=15, pady=10, sticky="ew")
        if self.day_list:
            self.day_entry.set(self.day_list[0])
            
        # Button inside the input panel
        self.search_button = ttk.Button(input_panel, text="Get Schedule", command=self.find_schedule, style="Custom.TButton")
        self.search_button.grid(row=2, column=0, columnspan=2, padx=15, pady=(15, 20))

        # --- Visual Separator ---
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=20)

        # --- Output Panel ---
        output_panel = ttk.Labelframe(main_frame, text=" Schedule Details ", style="Custom.TLabelframe")
        output_panel.pack(expand=True, fill="both")

        self.output_text = tk.Text(
            output_panel, height=10, width=60,
            font=("Consolas", 11), relief="solid", borderwidth=1,
            bg=self.INPUT_BG_COLOR, fg=self.TEXT_COLOR,
            highlightthickness=0, bd=0, # Remove outer border as Labelframe provides it
            insertbackground=self.TEXT_COLOR,
            padx=10, pady=10 # Internal padding for the text
        )
        self.output_text.pack(side="left", fill="both", expand=True, pad_x=1, pady=1) # Minimal padding to show frame border

        scrollbar = ttk.Scrollbar(output_panel, orient="vertical", command=self.output_text.yview, style="Custom.Vertical.TScrollbar")
        scrollbar.pack(side="right", fill="y", pad_x=(0,1), pady=1)
        self.output_text.config(yscrollcommand=scrollbar.set, state="disabled")

    def setup_styles(self):
        """Configures the styles for all ttk widgets for a professional look."""
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # General Style Configurations
        style.configure(".", background=self.BG_COLOR, foreground=self.TEXT_COLOR, font=self.app_font)
        
        # Frame Styles
        style.configure("Main.TFrame", background=self.BG_COLOR)
        style.configure("Custom.TLabelframe", background=self.BG_COLOR, bordercolor=self.BORDER_COLOR, relief="solid", borderwidth=1)
        style.configure("Custom.TLabelframe.Label", background=self.BG_COLOR, foreground=self.TEXT_COLOR, font=("Segoe UI", 10))

        # Label Styles
        style.configure("Custom.TLabel", background=self.BG_COLOR)
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), background=self.BG_COLOR)

        # Button Style
        style.configure("Custom.TButton",
            font=("Segoe UI", 12, "bold"),
            background=self.PRIMARY_COLOR,
            foreground="white",
            bordercolor=self.PRIMARY_COLOR,
            relief="flat",
            padding=5)
        style.map("Custom.TButton",
            background=[('active', self.PRIMARY_HOVER), ('pressed', self.PRIMARY_COLOR)])

        # Combobox (Dropdown) Style
        style.configure("TCombobox",
            selectbackground=self.INPUT_BG_COLOR,
            fieldbackground=self.INPUT_BG_COLOR,
            background=self.INPUT_BG_COLOR,
            foreground=self.TEXT_COLOR,
            arrowcolor=self.TEXT_COLOR,
            bordercolor=self.BORDER_COLOR)
        self.root.option_add('*TCombobox*Listbox.font', self.app_font)
        self.root.option_add('*TCombobox*Listbox.background', self.INPUT_BG_COLOR)
        self.root.option_add('*TCombobox*Listbox.foreground', self.TEXT_COLOR)
        self.root.option_add('*TCombobox*Listbox.selectBackground', self.PRIMARY_COLOR)
        self.root.option_add('*TCombobox*Listbox.selectForeground', 'white')

        # Scrollbar and Separator Styles
        style.configure("Custom.Vertical.TScrollbar", troughcolor=self.BG_COLOR, background=self.BORDER_COLOR, gripcount=0)
        style.map("Custom.Vertical.TScrollbar", background=[('active', self.PRIMARY_HOVER)])
        style.configure("TSeparator", background=self.BORDER_COLOR)

    def find_schedule(self):
        room_query = self.room_entry.get().strip()
        day_query = self.day_entry.get().strip()

        self.output_text.config(state="normal") # Enable writing
        self.output_text.delete("1.0", tk.END)

        if not room_query or not day_query or "No " in room_query or "No " in day_query:
            self.output_text.insert(tk.END, "Please select a valid room and day from the controls above.")
            self.output_text.config(state="disabled") # Disable writing
            return

        day_schedule = schedule.get(day_query, {})
        room_schedule = day_schedule.get(room_query)

        if room_schedule is not None:
            if room_schedule:
                output_string = ""
                for time in sorted(room_schedule.keys()):
                    details = room_schedule[time]
                    output_string += f"{time:<12} | {details}\n" # Padded for alignment
                self.output_text.insert(tk.END, output_string.strip())
            else:
                self.output_text.insert(tk.END, f"Room {room_query} is free on {day_query}. ✅")
        else:
            self.output_text.insert(tk.END, f"No schedule data found for Room {room_query} on {day_query}.")

        self.output_text.config(state="disabled")

# --- MAIN ---
if __name__ == "__main__":
    main_window = tk.Tk()
    app = ScheduleApp(main_window)
    main_window.mainloop()