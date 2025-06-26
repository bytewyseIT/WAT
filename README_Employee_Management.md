# Employee Database Management

The Workspace Administration Tool now includes comprehensive employee database management features that allow you to dynamically populate and maintain your employee list.

## Features

### 1. Fetch from Google Workspace
- Automatically imports all users from your Google Workspace domain
- Uses GAM (Google Apps Manager) to fetch user data
- Requires GAM to be properly configured and authenticated

### 2. CSV Import/Export
- Import employee data from CSV files
- Export current employee list to CSV
- Supports multiple column name formats (name/Name/full_name/Full Name, email/Email/email_address/Email Address)

### 3. Manual Management
- Add employees one by one
- Remove specific employees
- List all current employees
- Clear entire employee database

## Usage

### Main Menu
Select option **5. Manage Employee Database** from the main menu to access employee management features.

### Employee Management Submenu

#### 1. Fetch employees from Google Workspace
- Automatically populates the config with all users from your domain
- Requires GAM to be installed and configured
- Command used: `gam print users fields primaryemail,firstname,lastname`
- Constructs full names from first and last name fields for better identification

#### 2. Import employees from CSV file
- Import from a CSV file with employee data
- Supported column names:
  - Name columns: `name`, `Name`, `full_name`, `Full Name`
  - Email columns: `email`, `Email`, `email_address`, `Email Address`
- See `employees_template.csv` for reference format

#### 3. Export employees to CSV file
- Export current employee list to a CSV file
- Useful for backup or external processing

#### 4. Add employee manually
- Add individual employees by entering name and email
- Prevents duplicate email addresses

#### 5. Remove employee
- Remove specific employees from the database
- Shows numbered list for easy selection

#### 6. List all employees
- Display all current employees with numbering
- Shows total count

#### 7. Clear all employees
- Remove all employees from the database
- Requires confirmation

## CSV Format

The tool supports flexible CSV formats. Here's the recommended structure:

```csv
name,email
John Doe,john.doe@nuagelogistics.com
Jane Smith,jane.smith@nuagelogistics.com
```

## Requirements

- **GAM**: For fetching from Google Workspace (option 1)
- **CSV files**: For import/export functionality
- **Proper permissions**: GAM needs appropriate Google Workspace API permissions

## Configuration

The employee data is stored in `config.json` in the following format:

```json
{
  "domain": "nuagelogistics.com",
  "employees": [
    {
      "name": "John Doe",
      "email": "john.doe@nuagelogistics.com"
    }
  ]
}
```

## Error Handling

- File not found errors for CSV imports
- GAM command execution errors
- Duplicate email detection
- Invalid input validation
- Graceful handling of empty employee lists

## Tips

1. **Backup**: Export your employee list regularly as a backup
2. **GAM Setup**: Ensure GAM is properly configured before using Google Workspace import
3. **CSV Format**: Use the template file as a reference for proper CSV formatting
4. **Validation**: The tool validates email formats and prevents duplicates
5. **Reload**: The config is automatically reloaded after any changes 