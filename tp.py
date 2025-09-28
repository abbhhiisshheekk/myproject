import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- LOAD SCHEDULE FROM JSON ---
JSON_FILE = "schedule.json"

if not os.path.exists(JSON_FILE):
    messagebox.showerror("Error", f"'{JSON_FILE}' not found. Please add the file.")
    exit()

with open(JSON_FILE, "r") as f:
    schedule = json.load(f)
# --- END OF LOADING ---

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab Schedule Checker")
        self.root.geometry("550x400")

        # Style configuration
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12, "bold"))
        style.configure("TEntry", font=("Helvetica", 12))

        # --- Prepare lists for dropdowns ---
        self.day_list = list(schedule.keys())

        room_set = set()
        for day_data in schedule.values():
            room_set.update(day_data.keys())
        self.room_list = sorted(room_set)

        # --- Create and arrange the widgets ---
        input_frame = ttk.Frame(root, padding="20 10 20 10")
        input_frame.pack(fill="x")

        # Room dropdown
        ttk.Label(input_frame, text="Room Number:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.room_entry = ttk.Combobox(input_frame, values=self.room_list, state="readonly")
        self.room_entry.grid(row=0, column=1, padx=5, pady=5)
        if self.room_list:
            self.room_entry.set(self.room_list[0])

        # Day dropdown
        ttk.Label(input_frame, text="Day:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.day_entry = ttk.Combobox(input_frame, values=self.day_list, state="readonly")
        self.day_entry.grid(row=1, column=1, padx=5, pady=5)
        self.day_entry.set(self.day_list[0])

        # Button
        self.search_button = ttk.Button(root, text="Get Schedule", command=self.find_schedule)
        self.search_button.pack(pady=10)

        # Output text box + scrollbar
        output_frame = ttk.Frame(root, padding="10")
        output_frame.pack(expand=True, fill="both")

        self.output_text = tk.Text(output_frame, height=10, width=60,
                                   font=("Courier New", 11), relief="solid", borderwidth=1)
        self.output_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=scrollbar.set)

    def find_schedule(self):
        room_query = self.room_entry.get().strip()
        day_query = self.day_entry.get().strip()

        self.output_text.delete("1.0", tk.END)

        if not room_query or not day_query:
            self.output_text.insert(tk.END, "Please select both room and day.")
            return

        if day_query in schedule and room_query in schedule[day_query]:
            room_schedule = schedule[day_query][room_query]
            if room_schedule:
                output_string = f"--- Schedule for Room {room_query} on {day_query} ---\n\n"
                for time in sorted(room_schedule.keys()):
                    details = room_schedule[time]
                    output_string += f"{time}: {details}\n"
                self.output_text.insert(tk.END, output_string)
            else:
                self.output_text.insert(tk.END, f"Room {room_query} is free on {day_query}.")
        else:
            self.output_text.insert(tk.END, f"No schedule found for Room {room_query} on {day_query}.")


# --- MAIN ---
if __name__ == "__main__":
    main_window = tk.Tk()
    app = ScheduleApp(main_window)
    main_window.mainloop()