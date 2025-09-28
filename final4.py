import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- Define the JSON file name ---
JSON_FILE = "schedule.json"

class ScheduleApp:
    # --- Define a clean, professional color palette ---
    BG_COLOR = "#F7F7F7"
    TEXT_COLOR = "#333333"
    INPUT_BG_COLOR = "#FFFFFF"
    PRIMARY_COLOR = "#3A7FF6"
    PRIMARY_HOVER = "#5C9AFF"
    BORDER_COLOR = "#DCDCDC"

    def __init__(self, root):
        self.root = root
        self.root.title("Lab Schedule Manager")
        self.root.geometry("700x600") # Increased size for new features
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)

        self.app_font = ("Segoe UI", 11)
        self.schedule = self.load_schedule() # Load schedule into an instance variable

        self.setup_styles()

        # --- Prepare lists for dropdowns ---
        self.day_list = list(self.schedule.keys()) if self.schedule else ["No Days Found"]
        room_set = set()
        if self.schedule:
            for day_data in self.schedule.values():
                room_set.update(day_data.keys())
        self.room_list = sorted(list(room_set)) if room_set else ["No Rooms Found"]

        # --- Create and arrange the widgets ---
        main_frame = ttk.Frame(root, padding=20, style="Main.TFrame")
        main_frame.pack(expand=True, fill="both")

        title_label = ttk.Label(main_frame, text="Lab Schedule Manager", style="Title.TLabel", anchor="center")
        title_label.pack(pady=(0, 20), fill="x")

        # --- Input Panel ---
        input_panel = ttk.Labelframe(main_frame, text=" Selection ", style="Custom.TLabelframe")
        input_panel.pack(fill="x")
        input_panel.columnconfigure(1, weight=1)

        ttk.Label(input_panel, text="Room Number:", style="Custom.TLabel").grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")
        self.room_entry = ttk.Combobox(input_panel, values=self.room_list, state="readonly", font=self.app_font)
        self.room_entry.grid(row=0, column=1, padx=15, pady=(15, 10), sticky="ew")
        if self.room_list: self.room_entry.set(self.room_list[0])

        ttk.Label(input_panel, text="Day:", style="Custom.TLabel").grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.day_entry = ttk.Combobox(input_panel, values=self.day_list, state="readonly", font=self.app_font)
        self.day_entry.grid(row=1, column=1, padx=15, pady=10, sticky="ew")
        if self.day_list: self.day_entry.set(self.day_list[0])
        
        button_frame = ttk.Frame(input_panel, style="Main.TFrame")
        button_frame.grid(row=2, column=0, columnspan=2, pady=(15, 20))
        
        self.search_button = ttk.Button(button_frame, text="Get Room Schedule", command=self.find_schedule, style="Custom.TButton")
        self.search_button.pack(side="left", padx=5)
        
        self.view_day_button = ttk.Button(button_frame, text="View Full Day", command=self.view_full_day, style="Custom.TButton")
        self.view_day_button.pack(side="left", padx=5)

        # --- Visual Separator ---
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=15)

        # --- Output Panel ---
        output_panel = ttk.Labelframe(main_frame, text=" Schedule Details ", style="Custom.TLabelframe")
        output_panel.pack(expand=True, fill="both")
        output_panel.grid_rowconfigure(0, weight=1)
        output_panel.grid_columnconfigure(0, weight=1)

        self.schedule_tree = ttk.Treeview(output_panel, columns=("room", "time", "details"), show="headings")
        self.schedule_tree.heading("room", text="Room")
        self.schedule_tree.heading("time", text="Time Slot")
        self.schedule_tree.heading("details", text="Subject / Details")
        self.schedule_tree.column("room", width=100, anchor="center")
        self.schedule_tree.column("time", width=150, anchor="center")
        self.schedule_tree.column("details", width=300)

        scrollbar = ttk.Scrollbar(output_panel, orient="vertical", command=self.schedule_tree.yview)
        self.schedule_tree.configure(yscrollcommand=scrollbar.set)

        self.schedule_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=5)
        
        # Style for headers in the full day view
        self.schedule_tree.tag_configure('room_header', background='#EAEAEA', font=("Segoe UI", 10, "bold"))

        # --- Management Panel ---
        manage_frame = ttk.Frame(main_frame, style="Main.TFrame")
        manage_frame.pack(pady=(10,0), fill='x', side='bottom')

        self.add_button = ttk.Button(manage_frame, text="Add New Entry...", command=self.open_add_window)
        self.add_button.pack(side='left', padx=(0, 5))

        self.delete_button = ttk.Button(manage_frame, text="Delete Selected", command=self.delete_entry)
        self.delete_button.pack(side='left')

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure(".", background=self.BG_COLOR, foreground=self.TEXT_COLOR, font=self.app_font)
        style.configure("Main.TFrame", background=self.BG_COLOR)
        style.configure("Custom.TLabelframe", background=self.BG_COLOR, bordercolor=self.BORDER_COLOR, relief="solid", borderwidth=1)
        style.configure("Custom.TLabelframe.Label", background=self.BG_COLOR, foreground=self.TEXT_COLOR, font=("Segoe UI", 10))
        style.configure("Custom.TLabel", background=self.BG_COLOR)
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), background=self.BG_COLOR)
        style.configure("Custom.TButton", font=("Segoe UI", 12, "bold"), background=self.PRIMARY_COLOR, foreground="white", bordercolor=self.PRIMARY_COLOR, relief="flat", padding=5)
        style.map("Custom.TButton", background=[('active', self.PRIMARY_HOVER), ('pressed', self.PRIMARY_COLOR)])
        style.configure("TCombobox", selectbackground=self.INPUT_BG_COLOR, fieldbackground=self.INPUT_BG_COLOR, background=self.INPUT_BG_COLOR, foreground=self.TEXT_COLOR, arrowcolor=self.TEXT_COLOR, bordercolor=self.BORDER_COLOR)
        self.root.option_add('*TCombobox*Listbox.font', self.app_font)
        self.root.option_add('*TCombobox*Listbox.background', self.INPUT_BG_COLOR)
        self.root.option_add('*TCombobox*Listbox.foreground', self.TEXT_COLOR)
        self.root.option_add('*TCombobox*Listbox.selectBackground', self.PRIMARY_COLOR)
        self.root.option_add('*TCombobox*Listbox.selectForeground', 'white')
        style.configure("Custom.Vertical.TScrollbar", troughcolor=self.BG_COLOR, background=self.BORDER_COLOR, gripcount=0)
        style.map("Custom.Vertical.TScrollbar", background=[('active', self.PRIMARY_HOVER)])
        style.configure("TSeparator", background=self.BORDER_COLOR)
        # Style for Treeview
        style.configure("Treeview", rowheight=25, fieldbackground=self.INPUT_BG_COLOR)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=self.PRIMARY_COLOR, foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', self.PRIMARY_HOVER)])

    def load_schedule(self):
        if not os.path.exists(JSON_FILE):
            messagebox.showerror("Error", f"'{JSON_FILE}' not found. Please create an empty JSON file with {{}}.")
            exit()
        try:
            with open(JSON_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"'{JSON_FILE}' is not a valid JSON file.")
            exit()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the file: {e}")
            exit()

    def save_schedule_to_json(self):
        try:
            with open(JSON_FILE, "w") as f:
                json.dump(self.schedule, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save to file: {e}")

    def clear_treeview(self):
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)

    def find_schedule(self):
        self.clear_treeview()
        room_query = self.room_entry.get().strip()
        day_query = self.day_entry.get().strip()

        if not room_query or not day_query or "No " in room_query or "No " in day_query:
            self.schedule_tree.insert("", tk.END, values=("Error", "Please select a valid room and day.", ""))
            return

        day_schedule = self.schedule.get(day_query, {})
        room_schedule = day_schedule.get(room_query)

        if room_schedule is not None:
            if room_schedule:
                for time in sorted(room_schedule.keys()):
                    details = room_schedule[time]
                    self.schedule_tree.insert("", tk.END, values=(room_query, time, details))
            else:
                self.schedule_tree.insert("", tk.END, values=(room_query, f"Free on {day_query}", "✅"))
        else:
            self.schedule_tree.insert("", tk.END, values=(room_query, f"No data found for this day.", ""))

    def view_full_day(self):
        self.clear_treeview()
        day_query = self.day_entry.get().strip()

        if not day_query or "No " in day_query:
            self.schedule_tree.insert("", tk.END, values=("Error", "Please select a valid day.", ""))
            return

        day_schedule = self.schedule.get(day_query, {})
        if not day_schedule:
            self.schedule_tree.insert("", tk.END, values=("", f"No schedule found for {day_query}.", ""))
            return

        found_schedule = False
        for room in sorted(day_schedule.keys()):
            room_schedule = day_schedule[room]
            if room_schedule:
                found_schedule = True
                self.schedule_tree.insert("", tk.END, values=(f"--- {room} ---", "----------", "--------------------"), tags=('room_header',))
                for time in sorted(room_schedule.keys()):
                    details = room_schedule[time]
                    self.schedule_tree.insert("", tk.END, values=(room, time, details))
            else:
                self.schedule_tree.insert("", tk.END, values=(room, "All Day", "Free ✅"))
        
        if not found_schedule and day_schedule:
            self.schedule_tree.insert("", tk.END, values=("", f"All rooms are free on {day_query}.", ""))


    def open_add_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Schedule Entry")
        add_window.geometry("400x250")
        add_window.configure(bg=self.BG_COLOR)
        add_window.resizable(False, False)
        add_window.transient(self.root)
        add_window.grab_set() # Modal behavior

        form_frame = ttk.Frame(add_window, padding=20, style="Main.TFrame")
        form_frame.pack(expand=True, fill="both")
        
        ttk.Label(form_frame, text="Day:").grid(row=0, column=0, sticky="w", pady=5)
        day_val = ttk.Combobox(form_frame, values=self.day_list, state="readonly")
        day_val.grid(row=0, column=1, sticky="ew", pady=5)
        day_val.set(self.day_entry.get())

        ttk.Label(form_frame, text="Room:").grid(row=1, column=0, sticky="w", pady=5)
        room_val = ttk.Combobox(form_frame, values=self.room_list) # Not readonly to allow new rooms
        room_val.grid(row=1, column=1, sticky="ew", pady=5)
        room_val.set(self.room_entry.get())

        ttk.Label(form_frame, text="Time (e.g., 10:00-11:00):").grid(row=2, column=0, sticky="w", pady=5)
        time_val = ttk.Entry(form_frame)
        time_val.grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Label(form_frame, text="Details (e.g., Physics Lab):").grid(row=3, column=0, sticky="w", pady=5)
        details_val = ttk.Entry(form_frame)
        details_val.grid(row=3, column=1, sticky="ew", pady=5)
        
        save_btn = ttk.Button(form_frame, text="Save Entry", 
            command=lambda: self.save_new_entry(add_window,
                day_val.get(), room_val.get(), time_val.get(), details_val.get()
            ))
        save_btn.grid(row=4, columnspan=2, pady=15)

    def save_new_entry(self, window, day, room, time, details):
        if not all([day, room, time, details]):
            messagebox.showerror("Error", "All fields are required.", parent=window)
            return

        # Update the schedule dictionary
        self.schedule.setdefault(day, {}).setdefault(room, {})[time] = details
        self.save_schedule_to_json()

        # Update room list if a new room was added
        if room not in self.room_list:
            self.room_list.append(room)
            self.room_list.sort()
            self.room_entry['values'] = self.room_list
        
        messagebox.showinfo("Success", "Schedule entry saved!", parent=window)
        window.destroy()
        self.find_schedule()

    def delete_entry(self):
        selected_items = self.schedule_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select an entry in the table to delete.")
            return

        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected entry?"):
            return
            
        selected_item = selected_items[0]
        item_values = self.schedule_tree.item(selected_item)['values']
        
        # Check if it's a real entry and not a status message or header
        if len(item_values) < 3 or '---' in str(item_values[0]):
            messagebox.showerror("Invalid Selection", "Cannot delete a header or status message.")
            return

        room, time, details = item_values[0], item_values[1], item_values[2]
        day = self.day_entry.get()

        try:
            if day in self.schedule and room in self.schedule[day] and time in self.schedule[day][room]:
                del self.schedule[day][room][time]
                self.save_schedule_to_json()
                self.find_schedule()
            else:
                 messagebox.showerror("Error", "Could not find the entry to delete in the data source.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred during deletion: {e}")

# --- MAIN ---
if __name__ == "__main__":
    main_window = tk.Tk()
    app = ScheduleApp(main_window)
    main_window.mainloop()