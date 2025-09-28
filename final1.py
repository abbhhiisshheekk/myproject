import tkinter as tk
from tkinter import ttk # for a cleaner look

# --- SCHEDULE DATA ---
schedule = {
    "Monday": {
        "447(A)": {
            "08:15 AM - 10:15 AM": "Comp B - Batch B (EM practical)",
            "10:30 AM - 12:30 PM": "E&TC - Batch A (EM practical)"
        },
        "228(B)": {
            "10:30 AM - 12:30 PM": "E&TC - Batch B (FCSE practical)"
        },
        "238(B)": {
            "10:30 AM - 12:30 PM": "E&TC - Batch C (DT&IL practical)"
        },
        "429": {
            "08:15 AM - 10:15 AM": "Comp B - Batch A (BXE practical)",
            "01:00 PM - 03:00 PM": "Comp A - Batch A (BXE practical)"
        },
        "302": {
            "08:15 AM - 10:15 AM": "Comp B - Batch C (CHEM practical)",
            "01:00 PM - 03:00 PM": "Comp A - Batch B (CHEM practical)"
        },
        "324": {
            "01:00 PM - 03:00 PM": "Comp A - Batch C (DT&IL practical)"
        },
        "238(A)": {
            "10:30 AM - 12:30 PM": "AIML A - Batch A (DT&IL practical)"
        },
        "305": {
            "08:15 AM - 10:15 AM": "AIML B - Batch A (CHEM practical)",
            "10:30 AM - 12:30 PM": "AIML A - Batch B (CHEM practical)"
        },
        "447(B)": {
            "08:15 AM - 10:15 AM": "AIML B - Batch C (EM practical)",
            "10:30 AM - 12:30 PM": "AIML A - Batch C (EM practical)"
        },
        "228(A)": {
            "08:15 AM - 10:15 AM": "AIML B - Batch B (FCSE practical)"
        }
        # ... MONDAY DATA ...
    },
   "Tuesday": {
        "429": {
            "08:15 AM - 10:15 AM": "Comp A - Batch C (BXE practical)",
            "10:30 AM - 12:30 PM": "Comp B - Batch C (BXE practical)",
            "01:00 PM - 03:00 PM": "E&TC - Batch A (BXE practical)"
        },
        "305": {
            "08:15 AM - 10:15 AM": "AIML A - Batch A (CHEM practical)",
            "10:30 AM - 12:30 PM": "AIML B - Batch B (CHEM practical)",
            "01:00 PM - 03:00 PM": "E&TC - Batch B (CHEM practical)"
        },
        "447(A)": {
            "08:15 AM - 10:15 AM": "AIML A - Batch B (EM practical)",
            "10:30 AM - 12:30 PM": "AIML B - Batch A (EM practical)",
            "01:00 PM - 03:00 PM": "E&TC - Batch C (EM practical)"
        },
        "15(A)": {
            "08:15 AM - 10:15 AM": "Comp A - Batch A (DT&IL practical)"
        },
        "225": {
            "08:15 AM - 10:15 AM": "Comp A - Batch B (FCSE practical)"
        },
        "302": {
            "10:30 AM - 12:30 PM": "Comp B - Batch A (CHEM practical)"
        },
        "228(B)": {
            "10:30 AM - 12:30 PM": "Comp B - Batch B (FCSE practical)"
        },
        "238(A)": {
            "08:15 AM - 10:15 AM": "AIML A - Batch C (DT&IL practical)"
        },
        "217(A)": {
            "10:30 AM - 12:30 PM": "AIML B - Batch C (FCSE practical)"
        }
        # ... TUESDAY DATA ...
    },
    "Wednesday": {},
    "Thursday": {},
    "Friday": {}
}
# --- END OF SCHEDULE DATA ---


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
        
        # Day widgets
        ttk.Label(input_frame, text="Day:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.day_entry = ttk.Entry(input_frame, width=20)
        self.day_entry.grid(row=1, column=1, padx=5, pady=5)

        # The 'Get Schedule' button
        self.search_button = ttk.Button(root, text="Get Schedule", command=self.find_schedule)
        self.search_button.pack(pady=10)

        # Output text box with a scrollbar
        output_frame = ttk.Frame(root, padding="10")
        output_frame.pack(expand=True, fill="both")
        
        self.output_text = tk.Text(output_frame, height=10, width=60, font=("Courier New", 11), relief="solid", borderwidth=1)
        self.output_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=scrollbar.set)

    def find_schedule(self):
        """This function is called when the button is clicked."""
        # 1. Get user input from the entry boxes
        room_query = self.room_entry.get().strip()
        day_query = self.day_entry.get().strip().capitalize()
        
        # 2. Clear the previous output
        self.output_text.delete("1.0", tk.END)

        # 3. GUI output
        if not room_query or not day_query:
            self.output_text.insert(tk.END, "Please enter both room and day.")
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

# --- Main part of the program ---
if __name__ == "__main__":
    main_window = tk.Tk()
    app = ScheduleApp(main_window)
    main_window.mainloop() # starts app and keeps window open