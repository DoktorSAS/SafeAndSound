import os
import json

import utils.Logger
from utils.Enum import CredentialsType

"""
Example JSON file structure:
[
    {

        "service": "www.exemple.com",
        "email_or_username": "testuser",
        "value": "123456789"
    },
    {
        "service": "www.exemple.com",
        "email_or_username": "testuser",
        "value": "123-456-789"
    }
]
"""
class Credential:
    def __init__(self, service, username, value):
        self.service = service
        self.username = username
        self.value = value

    def to_dict(self):
        """Convert the Credential object to a dictionary."""
        return {
            'service': self.service,
            'email_or_username': self.username,
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
            with open(self.file_path, 'w') as file:
                json.dump([], file) 
            self.Logger.info(f"File '{self.file_path}' created with default value '[]'.")
        else:
            try:
                with open(self.file_path, 'r') as file:
                    json.load(file)
            except (json.JSONDecodeError, ValueError):
                with open(self.file_path, 'w') as file:
                    json.dump([], file)
                self.Logger.error(f"File '{self.file_path}' was invalid and has been reset to default value '[]'.")

    def append_credential(self, credential: Credential):
        """Append a new credential to the JSON file."""
        with open(self.file_path, 'r+') as file:
            data = json.load(file)
            credential.id = len(data)
            data.append(credential.to_dict())
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        self.Logger.info(f"Credential for '{credential.service}' added with ID {credential.id}.")

    def remove_credential(self, index):
        """Remove a credential by its index in the array."""
        with open(self.file_path, 'r+') as file:
            data = json.load(file)
            # Check if the index is valid
            if 0 <= index < len(data):
                # Remove the credential at the given index
                removed_credential = data.pop(index)
                # Move the file pointer to the beginning of the file
                file.seek(0)
                # Write the updated data back to the file
                json.dump(data, file, indent=4)
                # Truncate the file to remove any leftover data
                file.truncate()
                
                self.Logger.info(f"Credential for '{removed_credential['service']}' at index {index} removed.")
            else:
                self.Logger.warning(f"No credential found at index {index}.")

    def get_all_credentials(self):
        """Retrieve all credentials from the JSON file."""
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data

    def get_credential_by_id(self, credential_id):
        """Retrieve a credential by its ID."""
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        credential = next((cred for cred in data if cred['id'] == int(credential_id)), None)
        return credential

