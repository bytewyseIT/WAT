import json
import os
import subprocess
import platform
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

# Load config file
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

config = load_config()
employees = config["employees"]

class EmployeeCompleter(Completer):
    """Custom completer for employee names using prompt_toolkit."""
    def get_completions(self, document, complete_event):
        text = document.text.lower()
        for emp in employees:
            if emp["name"].lower().startswith(text):
                yield Completion(emp["name"], start_position=-len(text))

# Display script information
def display_header():
    print(ascii_logo)
    print(f"{script_info['name']} - v{script_info['version']}")
    print(f"Author: {script_info['author']}")
    print(f"Contact: {script_info['contact']}")
    print("\n--- MENU ---")
    print("\nSelect which action you would like to perform.\n")

# Main menu options
def menu():
    print("\n")
    print("1. List all files owned by a user")
    print("2. Transfer ownership of files")
    print("3. User lookup")
    print("4. Reset Password")
    print("0. Exit")
    choice = input("\nChoose an option: ")
    return choice

# Get employee email by name
def get_employee_email(name):
    for emp in employees:
        if emp["name"].lower() == name.lower():
            return emp["email"]
    print(f"No employee found with the name: {name}")
    return None

# Prompt user with tab completion
def get_employee_name():
    completer = EmployeeCompleter()
    return prompt("Enter the user's name: ", completer=completer)

# Option 1: List files owned by a user
def list_files():
    name = get_employee_name()
    email = get_employee_email(name)
    if not email:
        return  # Return to main menu if no valid email found

    command = ["gam", "user", email, "show", "filelist"]
    subprocess.run(command, shell=True)

# Option 2: Transfer ownership of files
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

# Option 3: Lookup all information about a user
def lookup_user_info():
    name = get_employee_name()
    email = get_employee_email(name)
    if not email:
        return

    command = ["gam", "info", "user", email]
    subprocess.run(command, shell=True)

# Main program loop
if __name__ == "__main__":
    display_header()
    while True:
        choice = menu()
        if choice == "1":
            list_files()
        elif choice == "2":
            transfer_ownership()
        elif choice == "3":
            lookup_user_info()
        elif choice == "0":
            print("Exiting script...")
            break
        else:
            print("Invalid option. Please try again.")
