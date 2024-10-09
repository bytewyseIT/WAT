# Workspace Administration Tool

A tool to simplify the administration of your Google Workspace from the command line.

## Requirements
- GAM
    - Install GAM from the official repo https://github.com/GAM-team/GAM
    - Configure GAM as per the instructions in the repo
    - You will need a Google Workspace account with Super Admin / Elevated permissions to complete some of the tasks in the script
- Python

- Config.json
	- Edit this file to contain your domain & email format
## Usage
There are several menu options available on starting the script, each with specific functionalities.

### List Files Owned By A User
Generate a list of files owned by a user in your organization, with options to export the list. This function only requires the users name, and will print out a list of all files owned by the user. It provides you with 3 options for the file list: 

- **Export file list to Google Drive:** Generates the file list and uploads it directly to your Drive
- **Export file list to CSV:** Generates the file list and saves it as a CSV in your current working folder
- **Display file list in console:** Displays the file list in the console

### Transfer ownership of files
If you need to transfer ownership of files from one user to another this script will give you a few options. You will need the File ID, as well as the current owner and desired owner. 

- **Transfer ownership of a single file:** Transfers ownership of one file. Requires First/Last of current owner, First/Last of desired owner, and FileID
- **Bulk transfer files using a CSV list:** Transfers ownership of all files listed in the CSV. The CSV must contain the colum headers "owner", "id", and "newowner". The script reads from these headers to perform the actions. **The CSV must be contained in the working folder.**
    - **owner:** Current owner of the file (in email format)
    - **id:** The file ID
    - **newowner:** The desired new owner of the file (in email format)
	
View filelist.csv in the project files for an example.