import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime
from cryptography import *
import main


class logmanager:
    unread_suspicious_count = 0

    def __init__(self, log_dir="logs", log_file="mealmanagement.log"):
        self.log_dir = log_dir
        self.log_file_path = os.path.join(log_dir, log_file)
        self.unread_suspicious_count = 0 # Track of suspicious activity
        
        # Ensure the directory exists.
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Create a logger
        self.logger = logging.getLogger('meal_logger')
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.INFO)

            # Create a TimedRotatingFileHandler
            handler = TimedRotatingFileHandler(self.log_file_path, when='midnight', interval=1, backupCount=30)
            handler.setLevel(logging.INFO)

            # Create a formatter and set it for the handler
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            # Add the handler to the logger
            self.logger.addHandler(handler)

    # Function to log activities
    def log_activity(self, username, description, additional_info=None, suspicious='No'):
        # Construct the log message based on provided information
        log_entry = f"{username} - {description} - {additional_info or ''} - Suspicious: {suspicious}"

        if suspicious == 'Yes':
            self.logger.warning(log_entry)
            logmanager.unread_suspicious_count += 1
        else:
            self.logger.info(log_entry)

    def show_notifications(self):
        if logmanager.unread_suspicious_count > 0:
            print(f"\n*** You have {logmanager.unread_suspicious_count} unread suspicious activity logs. ***\n")
        else:
            print("\nNo unread suspicious acitivities.")

        
    def see_logs(self, date=None):

        file_path = self.log_file_path
        if date:
            file_path = f'{self.log_file_path}.{date}'

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                total_lines = len(lines)
                pages = (total_lines + 19) // 20

                page = 0
                while True:
                    main.clear()
                    start_index = page * 20
                    end_index = min((page + 1) * 20, total_lines)
                    current_page_lines = lines[start_index:end_index]

                    print(f"\n--- Page {page + 1} / {pages} ---\n")
                    for line in current_page_lines:
                        print(line.strip())

                    print("\n1. Next page")
                    print("2. Previous page")
                    print("3. Go back")
                    choice = input("Choose an option (1/2/3): ").strip()

                    if choice == "1":
                        if page < pages - 1:
                            page += 1
                    elif choice == "2":
                        if page > 0:
                            page -= 1
                    elif choice == "3":
                        logmanager.unread_suspicious_count = 0
                        break
                    else:
                        print("Invalid input")
                    
        except FileNotFoundError:
            print(f"The file {file_path} does not exist.")
            
