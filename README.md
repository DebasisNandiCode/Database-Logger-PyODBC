# Database-Logger-PyODBC

## Overview
This repository contains a Python implementation of a logging system that supports:
1. **Database Logging**: Inserts log entries into a SQL Server database.
2. **File-Based Logging**: Maintains error logs in a local file as a backup mechanism.
3. **Automatic Retry for Failed Logs**: Attempts to process and insert failed log entries from the local log file into the database.

---

## Features
- **Database Integration**:
  - Logs critical events directly into a SQL Server database using `pyodbc`.
  - Provides detailed logging fields such as timestamp, task ID, log type, status, and error details.

- **File Backup**:
  - Writes logs to a local file (`dbErrorLog.txt`) in case of database connection issues.
  - Retries inserting failed log entries from the file to the database.

- **Error Handling**:
  - Catches and logs errors encountered during database operations.
  - Ensures no logs are lost by falling back to file-based storage.

---

## Prerequisites
1. Python 3.8+.
2. Required Python packages:
   - `pyodbc`
   - `logging`
3. SQL Server database with a table named `Daily_Task_Logs` having the following schema:
   ```sql
   CREATE TABLE Daily_Task_Logs (
       Log_TimeStamp DATETIME,
       Task_ID INT,
       Log_Type NVARCHAR(50),
       Log_Code NVARCHAR(50),
       Error_Current_Status NVARCHAR(50),
       Log_Remarks_User NVARCHAR(MAX),
       Last_Error_Status_TimeStamp DATETIME,
       Log_Remarks_System NVARCHAR(MAX),
       Log_Details NVARCHAR(MAX)
   );


# Clone this repository: git clone https://github.com/<username>/Database-Logger-PyODBC.git


# Database-Logger-PyODBC/
│
├── Log_Folder/            # Folder for storing log files
│   └── dbErrorLog.txt     # File-based backup for logs
├── Logger.py              # Logger class implementation
├── main.py                # Example usage
└── README.md              # Documentation
