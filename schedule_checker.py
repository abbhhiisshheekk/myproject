# The main schedule is stored in a nested dictionary.
# Format: schedule[Day][Room Number][Time Slot] = "Class Details"
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
    },
    "Wednesday": {
        # Add your Wednesday schedule here
    },
    "Thursday": {
        # Add your Thursday schedule here
    },
    "Friday": {
        # Add your Friday schedule here
    }
}


def get_room_schedule(day_query, room_query):
    """
    Looks up and prints the schedule for a given room on a specific day.
    """
    day = day_query.strip().capitalize()
    room = room_query.strip()  # Keep room query case-sensitive, e.g., 447(A) vs 447(a)

    if day in schedule:
        if room in schedule[day]:
            room_schedule = schedule[day][room]

            if room_schedule:
                print(f"\n--- Schedule for Room {room} on {day} ---")
                # Sort the schedule by time for cleaner output
                for time in sorted(room_schedule.keys()):
                    details = room_schedule[time]
                    print(f"{time}: {details}")
                print("------------------------------------------")
            else:
                print(f"\nRoom {room} is free on {day}.")
        else:
            print(f"\nRoom {room} has no scheduled classes on {day}.")
    else:
        print(f"\nSorry, no schedule found for {day}.")


# --- Main part of the program ---
if __name__ == "__main__":
    user_input = input(
        "Enter the room number and day (e.g., '429 Tuesday' or '305 Monday'): ")

    try:
        parts = user_input.split()
        day_input = parts[-1]
        # Handles room numbers with spaces if any
        room_input = " ".join(parts[:-1])

        get_room_schedule(day_input, room_input)

    except IndexError:
        print("Invalid input format. Please enter as: 'RoomNumber Day'.")
