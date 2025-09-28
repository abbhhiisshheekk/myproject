# The main schedule is stored in a nested dictionary.
# Format: schedule[Day][Lab Name][Time Slot] = "Branch - Batch"
schedule = {
    "Monday": {
        "Chemistry Lab 1": {
            "09:00 AM - 11:00 AM": "AIML Engg - Batch A",
            "11:00 AM - 01:00 PM": "Computer Science Engg - Batch B",
            "02:00 PM - 04:00 PM": "Electronics and Telecommunication Engg - Batch C"
        },
        "Mechanics Lab 1": {
            "11:00 AM - 01:00 PM": "Electrical Engg - Batch A",
            "02:00 PM - 04:00 PM": "Computer Science Engg - Batch C"
        },
        "Electronics Lab 1": {
            "09:00 AM - 11:00 AM": "Electronics and Telecommunication Engg - Batch A",
            "02:00 PM - 04:00 PM": "AIML Engg - Batch B"
        }
    },
    "Tuesday": {
        "Chemistry Lab 1": {
            "11:00 AM - 01:00 PM": "Electrical Engg - Batch C",
        },
        "Mechanics Lab 1": {
            "09:00 AM - 11:00 AM": "AIML Engg - Batch C",
            "02:00 PM - 04:00 PM": "Electronics and Telecommunication Engg - Batch B"
        },
        "Electronics Lab 1": {
            "09:00 AM - 11:00 AM": "Computer Science Engg - Batch A",
        }
    }
    # You can add more days like "Wednesday", "Thursday", etc. here.
}

def get_lab_schedule(day_query, lab_query):
    """
    Looks up and prints the schedule for a given lab on a specific day.
    """
    # Format the input to match the keys in the dictionary (e.g., "monday" -> "Monday")
    day = day_query.capitalize()
    lab = lab_query.title() # Handles labs with multiple words like "Chemistry Lab 1"

    # Check if the requested day exists in the schedule
    if day in schedule:
        # Check if the requested lab exists for that day
        if lab in schedule[day]:
            lab_schedule = schedule[day][lab]
            
            # Check if there are any practicals scheduled for that lab
            if lab_schedule:
                print(f"\n--- Schedule for {lab} on {day} ---")
                for time, batch in lab_schedule.items():
                    print(f"{time}: Occupied by {batch}")
                print("------------------------------------------")
            else:
                print(f"\n{lab} is free on {day}.")
        else:
            print(f"\nSorry, {lab} is not a valid lab for {day}.")
    else:
        print(f"\nSorry, no schedule found for {day}.")

# --- Main part of the program ---
if __name__ == "__main__":
    # Get input from the user
    user_input = input("Enter the lab and day (e.g., 'Chemistry Lab 1 Monday'): ")
    
    try:
        # Split the input string to separate the lab name from the day
        parts = user_input.split()
        day_input = parts[-1]        # Assumes the last word is the day
        lab_input = " ".join(parts[:-1]) # The rest is the lab name
        
        # Call the function with the user's input
        get_lab_schedule(day_input, lab_input)
        
    except IndexError:
        print("Invalid input format. Please enter in the format: 'Lab Name Day'.")