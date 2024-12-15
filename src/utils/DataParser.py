import os
import json

import utils.Logger

class Credential:
    def __init__(self, id, service, username, value):
        self.id = id
        self.service = service
        self.username = username
        self.value = value

    def to_dict(self):
        """Convert the Credential object to a dictionary."""
        return {
            'id': self.id,
            'service': self.service,
            'username': self.username,
            'value': self.value
        }

class DataParser:

    Logger: utils.Logger = None

    def __init__(self, Logger: utils.Logger, file_path):
        self.Logger = Logger
        self.file_path = file_path
        self.ensure_file_integrity()

    def ensure_file_integrity(self):
        """Ensure the JSON file exists and is a proper JSON file."""
        if not os.path.exists(self.file_path):
            # Create the file with default value if it doesn't exist
            with open(self.file_path, 'w') as file:
                json.dump([], file)  # Initialize with an empty list
            self.Logger.info(f"File '{self.file_path}' created with default value '[]'.")
        else:
            # Check if the file is empty or not a valid JSON
            try:
                with open(self.file_path, 'r') as file:
                    json.load(file)  # Try to load the JSON to check its integrity
            except (json.JSONDecodeError, ValueError):
                # If the file is not a valid JSON, reset it
                with open(self.file_path, 'w') as file:
                    json.dump([], file)  # Initialize with an empty list
                self.Logger.error(f"File '{self.file_path}' was invalid and has been reset to default value '[]'.")

    def append_credential(self, credential):
        """Append a new credential to the JSON file."""
        with open(self.file_path, 'r+') as file:
            # Load existing data
            data = json.load(file)
            # Assign an id based on the current length of the data
            credential.id = len(data)
            # Append the new credential
            data.append(credential.to_dict())
            # Move the cursor to the beginning of the file
            file.seek(0)
            # Write the updated data back to the file
            json.dump(data, file, indent=4)
            # Truncate the file to the new size
            file.truncate()
        self.Logger.info(f"Credential for '{credential.service}' added with ID {credential.id}.")

    def remove_credential(self, service):
        """Remove a credential by service name."""
        with open(self.file_path, 'r+') as file:
            # Load existing data
            data = json.load(file)
            # Filter out the credential with the specified service
            new_data = [cred for cred in data if cred['service'] != service]
            # Move the cursor to the beginning of the file
            file.seek(0)
            # Write the updated data back to the file
            json.dump(new_data, file, indent=4)
            # Truncate the file to the new size
            file.truncate()
        self.Logger.info(f"Credential for '{service}' removed.")

