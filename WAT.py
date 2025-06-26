#Add option to export file list 

import json
import os
import subprocess
import platform
import csv
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

# Define ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

# ASCII logo
ascii_logo = f""" 
{CYAN} 
888       888        d8888 88888888888 
888   o   888       d88888     888     
888  d8b  888      d88P888     888     
888 d888b 888     d88P 888     888     
888d88888b888    d88P  888     888     
88888P Y88888   d88P   888     888     
8888P   Y8888  d8888888888     888     
888P     Y888 d88P     888     888  {RESET}
"""

# Script metadata
script_info = {
    "name": "Workspace Administration Tool",
    "author": "Eric Ross",
    "version": "0.5",
    "contact": "https://github.com/bytewyseIT"
}

# In-memory employee list
employees = []

def fetch_employees_from_gworkspace():
    global employees
    print(f"\n{YELLOW}Fetching employees from Google Workspace...{RESET}")
    try:
        command = ["gam", "print", "users", "fields", "primaryemail,firstname,lastname"]
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            new_employees = []
            for line in lines[1:]:  # Skip header line
                if line.strip():
                    parts = line.split(',')
                    if len(parts) >= 3:
                        email = parts[0].strip()
                        firstname = parts[1].strip()
                        lastname = parts[2].strip()
                        if email and '@' in email:
                            if firstname and lastname:
                                full_name = f"{firstname} {lastname}"
                            elif firstname:
                                full_name = firstname
                            elif lastname:
                                full_name = lastname
                            else:
                                full_name = email.split('@')[0]
                            new_employees.append({
                                "name": full_name,
                                "email": email
                            })
            if new_employees:
                employees = new_employees
                print(f"{GREEN}Successfully imported {len(new_employees)} employees from Google Workspace{RESET}")
            else:
                print(f"{RED}No employees found or invalid data format{RESET}")
                print(f"{YELLOW}Debug: Raw output: {result.stdout[:200]}...{RESET}")
        else:
            print(f"{RED}Error fetching employees: {result.stderr}{RESET}")
            print(f"{YELLOW}Try running 'gam print users fields primaryemail,firstname,lastname' manually to test{RESET}")
    except Exception as e:
        print(f"{RED}Error: {str(e)}{RESET}")

class EmployeeCompleter(Completer):
    """Custom completer for employee names using prompt_toolkit."""
    def get_completions(self, document, complete_event):
        text = document.text.lower()
        for emp in employees:
            display = f"{emp['name']} <{emp['email']}>"
            if text in emp["name"].lower() or text in emp["email"].lower():
                yield Completion(display, start_position=-len(text))

def display_header():
    print(ascii_logo)
    print(f"{script_info['name']} - v{script_info['version']}")
    print(f"Author: {script_info['author']}")
    print(f"Contact: {script_info['contact']}")
    print("\n--- MENU ---")
    print("\nSelect which action you would like to perform.\n")

def menu():
    print("\n")
    print("1. List all files owned by a user")
    print("2. Transfer ownership of files")
    print("3. User lookup")
    print("4. Reset Password")
    print("5. Manage Employee Database")
    print("0. Exit")
    choice = input("\nChoose an option: ")
    return choice

def employee_management_menu():
    print(f"\n{BLUE}--- EMPLOYEE DATABASE MANAGEMENT ---{RESET}")
    print("1. Fetch employees from Google Workspace")
    print("2. Import employees from CSV file")
    print("3. Export employees to CSV file")
    print("4. Add employee manually")
    print("5. Remove employee")
    print("6. List all employees")
    print("7. Clear all employees")
    print("0. Back to main menu")
    choice = input("\nChoose an option: ")
    return choice

def import_employees_from_csv():
    global employees
    csv_file = input("Enter the path to the CSV file: ")
    try:
        new_employees = []
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get('name') or row.get('Name') or row.get('full_name') or row.get('Full Name')
                email = row.get('email') or row.get('Email') or row.get('email_address') or row.get('Email Address')
                if name and email:
                    new_employees.append({
                        "name": name.strip(),
                        "email": email.strip()
                    })
        if new_employees:
            employees = new_employees
            print(f"{GREEN}Successfully imported {len(new_employees)} employees from CSV{RESET}")
        else:
            print(f"{RED}No valid employee data found in CSV{RESET}")
    except FileNotFoundError:
        print(f"{RED}CSV file not found: {csv_file}{RESET}")
    except Exception as e:
        print(f"{RED}Error importing CSV: {str(e)}{RESET}")

def export_employees_to_csv():
    if not employees:
        print(f"{YELLOW}No employees to export{RESET}")
        return
    csv_file = input("Enter the path for the CSV file (e.g., employees.csv): ")
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'email'])
            writer.writeheader()
            writer.writerows(employees)
        print(f"{GREEN}Successfully exported {len(employees)} employees to {csv_file}{RESET}")
    except Exception as e:
        print(f"{RED}Error exporting CSV: {str(e)}{RESET}")

def add_employee_manually():
    global employees
    name = input("Enter employee name: ").strip()
    email = input("Enter employee email: ").strip()
    if name and email:
        for emp in employees:
            if emp["email"].lower() == email.lower():
                print(f"{YELLOW}Employee with this email already exists{RESET}")
                return
        new_employee = {"name": name, "email": email}
        employees.append(new_employee)
        print(f"{GREEN}Employee added successfully{RESET}")
    else:
        print(f"{RED}Name and email are required{RESET}")

def remove_employee():
    global employees
    if not employees:
        print(f"{YELLOW}No employees to remove{RESET}")
        return
    print("\nCurrent employees:")
    for i, emp in enumerate(employees, 1):
        print(f"{i}. {emp['name']} ({emp['email']})")
    try:
        choice = int(input("\nEnter the number of the employee to remove: ")) - 1
        if 0 <= choice < len(employees):
            removed_emp = employees.pop(choice)
            print(f"{GREEN}Removed {removed_emp['name']} successfully{RESET}")
        else:
            print(f"{RED}Invalid selection{RESET}")
    except ValueError:
        print(f"{RED}Please enter a valid number{RESET}")

def list_all_employees():
    if not employees:
        print(f"{YELLOW}No employees in database{RESET}")
        return
    print(f"\n{BLUE}--- CURRENT EMPLOYEES ({len(employees)}) ---{RESET}")
    for i, emp in enumerate(employees, 1):
        print(f"{i:3d}. {emp['name']} - {emp['email']}")

def clear_all_employees():
    global employees
    confirm = input("Are you sure you want to clear all employees? (yes/no): ").lower()
    if confirm == 'yes':
        employees = []
        print(f"{GREEN}All employees cleared{RESET}")
    else:
        print("Operation cancelled")

def manage_employees():
    while True:
        choice = employee_management_menu()
        if choice == "1":
            fetch_employees_from_gworkspace()
        elif choice == "2":
            import_employees_from_csv()
        elif choice == "3":
            export_employees_to_csv()
        elif choice == "4":
            add_employee_manually()
        elif choice == "5":
            remove_employee()
        elif choice == "6":
            list_all_employees()
        elif choice == "7":
            clear_all_employees()
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")

def get_employee_email(name):
    for emp in employees:
        if emp["name"].lower() == name.lower():
            return emp["email"]
    print(f"No employee found with the name: {name}")
    return None

def get_employee_name():
    completer = EmployeeCompleter()
    # No preview of available employees, just prompt
    selected = prompt("Enter the user's name: ", completer=completer)
    if '<' in selected and '>' in selected:
        name = selected.split('<')[0].strip()
        return name
    return selected

def list_files():
    name = get_employee_name()
    email = get_employee_email(name)
    if not email:
        return
    command = ["gam", "user", email, "show", "filelist"]
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"{RED}Error fetching file list: {result.stderr}{RESET}")
        return
    output = result.stdout.strip()
    if not output:
        print(f"{YELLOW}No files found for user.{RESET}")
        return
    # Parse CSV output
    from io import StringIO
    reader = csv.reader(StringIO(output))
    rows = list(reader)
    if not rows or len(rows) < 2:
        print(f"{YELLOW}No files found for user.{RESET}")
        return
    headers = rows[0]
    data = rows[1:]
    # Calculate column widths
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*([headers] + data))]
    # Print header
    header_row = " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
    print(f"\n{BLUE}{header_row}{RESET}")
    print("-+-".join("-" * w for w in col_widths))
    # Print rows
    for row in data:
        print(" | ".join(f"{cell:<{w}}" for cell, w in zip(row, col_widths)))
    # Prompt to export
    export = input(f"\nWould you like to export this file list to CSV? (y/n): ").strip().lower()
    if export == 'y':
        filename = input("Enter filename for export (e.g., user_filelist.csv): ").strip()
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(data)
            print(f"{GREEN}File list exported to {filename}{RESET}")
        except Exception as e:
            print(f"{RED}Error exporting file list: {str(e)}{RESET}")

def transfer_ownership():
    current_owner = get_employee_name()
    new_owner = get_employee_name()
    email_current = get_employee_email(current_owner)
    email_new = get_employee_email(new_owner)
    if not email_current or not email_new:
        return
    print("\nSub-options:")
    print("1. Transfer a single file")
    print("2. Bulk transfer using a CSV")
    sub_choice = input("Choose an option: ")
    if sub_choice == "1":
        file_id = input("Enter the File ID to transfer: ")
        command = ["gam", "user", email_current, "transfer", "file", file_id, "to", email_new]
    elif sub_choice == "2":
        csv_file = input("Enter the path to the CSV file: ")
        command = ["gam", "user", email_current, "transfer", "drivefile", "csv", csv_file, "to", email_new]
    else:
        print("Invalid option. Returning to main menu.")
        return
    subprocess.run(command, shell=True)

def lookup_user_info():
    name = get_employee_name()
    email = get_employee_email(name)
    if not email:
        return
    command = ["gam", "info", "user", email]
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    display_header()
    fetch_employees_from_gworkspace()  # Always fetch on startup
    while True:
        choice = menu()
        if choice == "1":
            list_files()
        elif choice == "2":
            transfer_ownership()
        elif choice == "3":
            lookup_user_info()
        elif choice == "4":
            print("Reset Password functionality not implemented yet")
        elif choice == "5":
            manage_employees()
        elif choice == "0":
            print("Exiting script...")
            break
        else:
            print("Invalid option. Please try again.")
