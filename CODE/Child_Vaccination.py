import json
import os
from datetime import datetime

DATA_FILE = 'vaccination_data.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as file:
        json.dump({"children": []}, file)

def load_data():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def book_appointment():
    data = load_data()
    child_name = input("Enter child's name: ")
    child_age = input("Enter child's age: ")
    vaccine_name = input("Enter vaccine name: ")
    appointment_date = input("Enter appointment date (YYYY-MM-DD): ")

    child = next((c for c in data['children'] if c['name'].lower() == child_name.lower()), None)
    if not child:
        child_id = len(data['children']) + 1
        child = {"id": child_id, "name": child_name, "age": child_age, "vaccinations": [], "appointments": []}
        data['children'].append(child)

    appointment = {
        "vaccine": vaccine_name,
        "appointment_date": appointment_date,
        "reminder_sent": False
    }
    child['appointments'].append(appointment)
    
    save_data(data)
    print(f"Appointment for {vaccine_name} on {appointment_date} has been booked.")

def view_updates():
    data = load_data()
    child_name = input("Enter child's name to view updates: ")

    child = next((c for c in data['children'] if c['name'].lower() == child_name.lower()), None)
    if not child:
        print("Child not found.")
        return
    
    print(f"Updates for {child_name}:")
    print(f"Age: {child['age']}")
    for vaccine in child['vaccinations']:
        print(f"- {vaccine['vaccine']}: Administered on {vaccine['date_administered']}, Next due: {vaccine['next_due']}")
    
    for appointment in child['appointments']:
        reminder_status = "Sent" if appointment['reminder_sent'] else "Pending"
        print(f"- {appointment['vaccine']} appointment on {appointment['appointment_date']} (Reminder: {reminder_status})")

def send_reminders():
    data = load_data()
    today = datetime.today().strftime('%Y-%m-%d')

    for child in data['children']:
        for appointment in child['appointments']:
            if appointment['appointment_date'] > today and not appointment['reminder_sent']:
                print(f"Reminder: Appointment for {child['name']} on {appointment['appointment_date']} for {appointment['vaccine']}")
                appointment['reminder_sent'] = True
    
    save_data(data)
    print("Reminders sent for upcoming appointments.")

def main_menu():
    while True:
        print("\nChild Vaccination Management System")
        print("1. Book an Appointment")
        print("2. View Updates")
        print("3. Send Reminders")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            book_appointment()
        elif choice == '2':
            view_updates()
        elif choice == '3':
            send_reminders()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
