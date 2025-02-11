import configparser
import logging
import os

import eel
import utils.Logger

class Config:
    Logger: utils.Logger = None

    def set_logger(self, logger: utils.Logger):
        self.Logger = logger

    APP: dict = {
        "min_width_size": 720,
        "min_hight_size": 1280,
        "pubkey_fpath": "",
        "privkey_fpath": "",
        "algorithm": "RSA",
        "auth_method": "P",
        "language": "en",
        "credentials_location": "data/storage/credentials.json",
        "plaintexts_location": "data/storage/plaintexts.json",
    }

    DEV:dict = {
        "debug_mode": True,
        "log_fname": "log.txt",
        "log_fpath": "./"
    }

    def __eel__(self):
        @eel.expose
        def configuration_set(key, value):
            """Set or update a configuration value."""
            section = 'DEV' if key in self.DEV else 'APP'
            
            if self.ConfigParser.has_option(section, key):
                # Printing for debugging
                self.Logger.info(f"Setting {key} in {section} to {value}")
                
                # Set the value in ConfigParser
                self.ConfigParser.set(section, key, str(value))
                
                # Save the configuration to file
                with open(os.path.join(self.DEV['log_fpath'], 'config.ini'), 'w') as configfile:
                    self.ConfigParser.write(configfile)
                
                # Update internal dictionaries
                if key in self.APP:
                    self.APP[key] = self.__convert_type(key, value)
                    self.Logger.info(f"Updated APP: {key} to {self.APP[key]}")
                elif key in self.DEV:
                    self.DEV[key] = self.__convert_type(key, value)
                    self.Logger.info(f"Updated DEV: {key} to {self.DEV[key]}")
                
                # Verify the change
                new_value = self.ConfigParser.get(section, key)
                self.Logger.info(f"Config file now has: {key} = {new_value}")
                
                return True
            else:
                self.Logger.error(f"Key {key} not found in {section}")
                return False

        @eel.expose
        def configuration_get(key=None):
            """Get configuration values. If key is None, return all configs."""
            if key is None:
                return {s: dict(self.ConfigParser.items(s)) for s in self.ConfigParser.sections()}
            else:
                section = 'DEV' if key in self.DEV else 'APP'
                if self.ConfigParser.has_option(section, key):
                    raw_value = self.ConfigParser.get(section, key)
                    return self.__convert_type(key, raw_value)
                return None

    def __convert_type(self, key, value):
        """Helper method to convert string values to appropriate types."""
        if key in ['MIN_WIDTH_SIZE', 'MIN_HIGHT_SIZE']:
            return int(value)
        elif key == 'debug_mode':
            return bool(int(value))  # configparser reads boolean as string '1' or '0'
        return value
    
    def __init__(self, config_fpath: str):
        self.__eel__()
        # Check if the configuration file exists
        if not os.path.exists(config_fpath):
            # If the file does not exist, create it with default values
            self.ConfigParser = configparser.ConfigParser()
            self.__update__(config_fpath)
        else:
            # If the file exists, read its contents
            self.ConfigParser = configparser.ConfigParser()
            self.__read__(config_fpath)

    def __read__(self, config_fpath):
        # Read the configuration file
        self.ConfigParser.read(config_fpath)

        # Update dictionaries with values from the file
        for key in self.APP:
            self.APP[key] = self.__convert_type(key, self.ConfigParser.get('APP', key, fallback=self.APP[key]))
        for key in self.DEV:
            self.DEV[key] = self.__convert_type(key, self.ConfigParser.get('DEV', key, fallback=self.DEV[key]))

        # Ensure log_fpath does not have trailing slashes/backslashes
        self.DEV['log_fpath'] = self.DEV['log_fpath'].rstrip('/').rstrip('\\')

    def __update__(self, config_fpath: str):
        # Update ConfigParser with the current values of the dictionaries
        self.ConfigParser['APP'] = {key: str(value) for key, value in self.APP.items()}
        self.ConfigParser['DEV'] = {key: str(int(value)) if isinstance(value, bool) else value for key, value in self.DEV.items()}

        # Write the updated configuration to the file
        with open(config_fpath, 'w') as configfile:
            self.ConfigParser.write(configfile)
