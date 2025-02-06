import os
import json

import utils.Logger
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

    def remove_credential(self, credential_id):
        """Remove a credential by its ID."""
        with open(self.file_path, 'r+') as file:
            data = json.load(file)
            new_data = [cred for cred in data if cred['id'] != int(credential_id)]
            file.seek(0)
            json.dump(new_data, file, indent=4)
            file.truncate()
        
        removed_credential = next((cred for cred in data if cred['id'] == int(credential_id)), None)
        if removed_credential:
            self.Logger.info(f"Credential for '{removed_credential['service']}' with ID {credential_id} removed.")
        else:
            self.Logger.warning(f"No credential found with ID {credential_id}.")

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

