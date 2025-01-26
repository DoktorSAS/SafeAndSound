
import json
import utils.Logger
import utils.Config
import utils.DataParser

import os
import subprocess

import eel
import sys

import Inputs as EELInputs

class GUI:

    MODE: str = 'default'
    Logger: utils.Logger = None
    Config: utils.Config = None
    Inputs: EELInputs = None
    AuthToken: str = None
    AuthHash: str = None
    DataParser: utils.DataParser = None
    

    def locate_chromium():
        # Define common paths for Chromium-based browsers by OS
        paths = {
            'linux': [
                '/usr/bin/chromium-browser',
                '/usr/bin/chromium',
                '/usr/bin/google-chrome',
                '/usr/bin/google-chrome-stable',
                '/usr/bin/chrome',
                '/usr/bin/brave-browser',
                '/usr/bin/vivaldi-stable'
            ],
            'darwin': [  # macOS
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '/Applications/Chromium.app/Contents/MacOS/Chromium',
                '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
                '/Applications/Vivaldi.app/Contents/MacOS/Vivaldi'
            ],
            'win32': [  # Windows
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files\Chromium\Application\chrome.exe',
                r'C:\Program Files (x86)\Chromium\Application\chrome.exe',
                r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
                r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe',
                r'C:\Users\[user]\AppData\Local\Vivaldi\Application\vivaldi.exe'  # User-dependent path
            ]
        }

        # Get the current operating system
        current_os = 'linux' if sys.platform.startswith('linux') else (
            'darwin' if sys.platform == 'darwin' else 
            'win32' if sys.platform.startswith('win') else None
        )

        if current_os not in paths:
            return None  # Unsupported OS or unrecognized

        # Check for each browser path
        for path in paths[current_os]:
            # On Windows, replace [user] with actual username if needed
            if current_os == 'win32' and '[user]' in path:
                path = path.replace('[user]', os.getlogin())
            if os.path.isfile(path):
                return path
            
            # For more robustness, try using which on Linux/macOS
            if current_os in ['linux', 'darwin']:
                proc = subprocess.Popen(['which', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if proc.wait() == 0:
                    return proc.stdout.read().decode('utf-8').strip()
        
        return None  # No Chromium-based browser found

    def __eel__(self):
        """
        function used to handle all the python function exposed for the eel use
        """

        @eel.expose
        def get_page_content(page: str = "home.html"):
            """
            Load HTML content from the 'pages' directory within the 'web' base directory.

            :param page: Name of the HTML file to load, defaults to 'home.html'.
            :return: HTML content or an error message in HTML format.
            """
            try:
                # Construct the base directory path, assuming 'web' is where your static files are
                base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../ui')
                
                # Sanitize the input to prevent directory traversal
                sanitized_page = os.path.basename(page)
                if not sanitized_page.endswith('.html'):
                    sanitized_page += '.html'
                
                full_path = os.path.join(base_path, 'pages', sanitized_page)
                
                if not os.path.exists(full_path):
                    return get_page_content("404.html")  # Fallback to 404 page if not found
                
                with open(full_path, 'r', encoding='utf-8') as file:
                    return file.read()
            
            except Exception as e:
                # Logger the error instead of exposing it to the client for security reasons
                print(f"An error occurred: {e}")
                return "<h1>Error Loading Page</h1>"

        @eel.expose
        def open_file_dialog_eel(options_json):
            try:
                options = json.loads(options_json)
                # Ensure 'multiple' is set correctly
                if 'multiple' not in options:
                    options['multiple'] = False  # Default to single file selection
                
                result = self.Inputs.open_file_dialog(**options)
                # Ensure result is a list or string as expected by your application
                if isinstance(result, tuple):  # Tkinter returns tuple for multiple files
                    result = list(result) if options['multiple'] else result[0]
                return result
            except Exception as e:
                self.Logger.error(f"File dialog error: {e}")
                return None

    def __init__(self, Logger: utils.Logger, Config: utils.Config, DataParser: utils.DataParser):
        self.Logger = Logger
        self.Config = Config
        self.DataParser = DataParser
        self.Inputs = EELInputs.Inputs()
        
        self.__eel__()

        eel.init("ui")
        eel_kwargs = dict(
            host='localhost', # can't use custom host name with no internet
            port=8080,
            size=(Config.APP['min_width_size'], Config.APP['min_hight_size']),
            block=True,
            cmdline_args=['--disable-gpu']
        )
        
        try:
            eel.start("index.html", mode='chrome', **eel_kwargs)
            Logger.info("Started EEL application.")
        except EnvironmentError as e:
            Logger.error(f"Environment error when starting EEL: {e}")
            # Your fallback logic
        except Exception as e:
            Logger.error(f"Unexpected error starting EEL: {e}")
            raise