import json
import os
import subprocess

# Define ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

# logo

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

# Display script information

def display_header():
    print(ascii_logo)
    print(f"{script_info['name']} - v{script_info['version']}")
    print(f"Author: {script_info['author']}")
    print(f"Contact: {script_info['contact']}")
    print("\n--- MENU ---")
    print("\n")
    print("Select which action you would like to perform.")
    print("\n")
 
 # Menu options
def menu():
    print("\n")
    print("1. List all files owned by a user")
    print("2. Transfer ownership of files")
    print("3. User lookup")
    print("0. Exit")
    choice = input("\nChoose an option: ")
    return choice
    
# Function to create email address
def create_email(first, last):
    email_format = config["email_format"]
    domain = config["domain"]
    return email_format.format(first=first.lower(), last=last.lower()) + "@" + domain

# Option 1: List files owned by a user
def list_files():
    print("\n")
    print("\nMenu:")
    print("\n")
    print("1. Export file list to Google Drive")
    print("2. Export file list to CSV")
    print("3. Display file list in console")
    print("0. Return to main menu")
    print("\n")
    sub_choice = input("Choose an option: ")
    
    if sub_choice == "0":
            return  # Return to main menu
    
    first_name = input("Enter the user's First Name: ")
    last_name = input("Enter the user's Last Name: ")
    email = create_email(first_name, last_name)



    # Build GAM command
    command = ["gam", "user", email, "show", "filelist"]

    if sub_choice == "1":
        # Export to Google Drive
        destination = input("Press enter to export to your drive")
        command.extend(["todrive"])
    elif sub_choice == "2":
        # Export to CSV
        output_csv = input("Enter output name: ")
        command.extend([">", output_csv])
    elif sub_choice == "3":
        # Display in console
        command

    # Execute command
    subprocess.run(command, shell=True)

# Option 2: Transfer ownership of files
def transfer_ownership():
    print("\n")
    print("\nMenu:")
    print("\n")
    print("1. Transfer ownership of a single file")
    print("2. Bulk transfer files using a CSV list")
    print("0. Return to main menu")
    print("\n")
    sub_choice = input("Choose an option: ")
    
    if sub_choice == "0":
            return  # Return to main menu
    
    first_name_current = input("Enter the First Name of the current owner: ")
    last_name_current = input("Enter the Last Name of the current owner: ")
    email_current = create_email(first_name_current, last_name_current)

    first_name_new = input("Enter the First Name of the new owner: ")
    last_name_new = input("Enter the Last Name of the new owner: ")
    email_new = create_email(first_name_new, last_name_new)

    if sub_choice == "1":
        file_id = input("Enter the File ID to transfer: ")
        # Build GAM command for single file transfer
        command = ["gam", "user", email_current, "add", "drivefileacl", file_id, "user", email_new, "role", "owner"]
        subprocess.run(command, shell=True)

    elif sub_choice == "2":
        csv_file = input("Enter the name of the CSV containging the list of files to transfer ex. filelist.csv")
        # Build GAM command for bulk file transfer
        command = ["gam", "csv", csv_file, "gam", "user", "~owner", "add", "drivefileacl", "~id", "user", "~newowner", "role", "owner"]
        subprocess.run(command, shell=True)

# Option 3: Lookup all information about a user
def lookup_user_info():
    first_name = input("Enter the user's First Name: ")
    last_name = input("Enter the user's Last Name: ")
    email = create_email(first_name, last_name)

    # Build and execute the GAM command to look up all user info
    command = ["gam", "info", "user", email]
    
    print(f"\nLooking up all information for {email}...\n")
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