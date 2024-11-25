import os
import pyodbc  # Use pyodbc for SQL Server connection
from datetime import datetime
import logging

class Logger:
    def __init__(self):
        # Use pyodbc connection string format for SQL Server
        self.connection_string = "DRIVER={SQL Server};SERVER=xx.xx.xx.xx;DATABASE=xxxxxxxx;UID=xxxxxxxx;PWD=xxxxxxxx;"
        self.documents_path = os.path.expanduser('~')  # Home directory path
        self.log_folder_path = os.path.join(self.documents_path, "Log_Folder")
        self.log_file_path = os.path.join(self.log_folder_path, "dbErrorLog.txt")
        self.setup_logger()

    def setup_logger(self):
        # Ensure the log folder exists
        if not os.path.exists(self.log_folder_path):
            os.makedirs(self.log_folder_path)

        # Configure logging
        logging.basicConfig(filename=self.log_file_path, level=logging.ERROR,
                            format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

    def log_to_database(self, tskID, logType, logCode, currentStatus, logRemarksUser, logMessage, logDetails):
        try:
            getDate = datetime.now()
            lastErrorStatusTimestamp = getDate if currentStatus != "NA" else datetime(1900, 1, 1, 12, 0, 0)

            log_insert_query = """
                INSERT INTO Daily_Task_Logs 
                (Log_TimeStamp, Task_ID, Log_Type, Log_Code, Error_Current_Status, Log_Remarks_User, 
                 Last_Error_Status_TimeStamp, Log_Remarks_System, Log_Details) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            # Connect to SQL Server using pyodbc
            connection = pyodbc.connect(self.connection_string)

            # Clean up the logMessage safely (without concatenation)
            logMessage = logMessage.replace("\r", "").replace("\n", "").replace("\t", "").replace("\v", "")

            # Execute the insert query using parameters
            cursor = connection.cursor()
            cursor.execute(log_insert_query, (
                getDate.strftime("%Y-%m-%d %H:%M:%S"),
                tskID,
                logType,
                logCode,
                currentStatus,
                logRemarksUser,
                lastErrorStatusTimestamp.strftime("%Y-%m-%d %H:%M:%S"),
                logMessage,
                logDetails
            ))

            connection.commit()
            connection.close()

            # Optionally call the old log handling
            self.old_log_file_input()

        except Exception as e:
            self.log_to_file(f"Failed to insert log: {str(e)}")
            logging.error(f"Error in log_to_database: {str(e)}")

    def old_log_file_input(self):
        if not os.path.exists(self.log_file_path):
            return

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        with open(self.log_file_path, 'r') as file:
            lines = file.readlines()

        failed_lines = []
        for line in lines:
            try:
                cursor.execute(line.strip())
                connection.commit()
            except Exception as e:
                failed_lines.append(line.strip())

        # Rewrite failed lines back to the log file
        if failed_lines:
            with open(self.log_file_path, 'w') as file:
                file.write("\n".join(failed_lines))

        connection.close()

    def log_to_file(self, log_message):
        try:
            with open(self.log_file_path, 'a') as log_file:
                log_file.write(f"{log_message}\n")
        except Exception as e:
            logging.error(f"Error writing to log file: {str(e)}")



# Example usage:
if __name__ == "__main__":
    logger = Logger()
    logger.log_to_database(
        tskID=123,
        logType="Error",
        logCode="ERR123",
        logDetails="Some error details",
        logMessage="Error message",
        currentStatus="Failed",
        logRemarksUser="User remarks"
    )
