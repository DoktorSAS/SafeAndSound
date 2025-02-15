
import json
import shutil
import utils.Logger
import utils.Config
import utils.DataParser
from utils.Enum import CredentialsType, CryptoType

import os
import base64

import eel

import utils.Inputs as EELInputs

class GUI:
    MODE: str = 'default'
    Logger: utils.Logger = None
    Config: utils.Config = None
    Inputs: EELInputs = None
    PlainTexts: utils.DataParser = None
    Credentials: utils.DataParser = None
    Key: str = None # password, passcode or image

    def __eel__(self):
        """
        function used to handle all the python function exposed for the eel use
        """
        @eel.expose
        def set_key(key: str):
            self.Logger.info(f"Setting key to {key[:10]}...{key[-10:]}")
            self.Key = key
        
        @eel.expose
        def set_key_base64(key: str) -> bool:
            try:
                self.Logger.info(f"Setting key to {key[:10]}...{key[-10:]}")
                self.Key = key
                return True
            except Exception as e:
                self.Logger.error(f"Key update error: {e}")
                return False

        @eel.expose
        def add_credential(type: int, encryption: str, service: str, username: str, value: str):
            type_str: str = "Credentials" if type == CredentialsType.CREDENTIALS.value else "PlainTexts"
            self.Logger.info(f"Adding credential to {type_str} with service {service} and username {username}")
            import utils.Ciphers as Ciphers
            cryptotype: CryptoType = CryptoType.string_to_enum(encryption)
            if cryptotype != CryptoType.NONE.value:
                #service = str(Ciphers.encrypt(service, cryptotype))
                username = str(Ciphers.encrypt(username, cryptotype, self.Key))
                value = str(Ciphers.encrypt(value, cryptotype, self.Key))
            self.Logger.info(f'Encrypted service: {service}')
            if type == CredentialsType.CREDENTIALS.value:
                self.Credentials.append_credential(utils.DataParser.Credential(service, username, value))
            else:
                self.PlainTexts.append_credential(utils.DataParser.Credential(service, username, value))

        @eel.expose
        def remove_credential(type: int, id: int):
            self.Logger.info(f"Removing credential with id {id} from {type}")
            if type == CredentialsType.CREDENTIALS.value:
                self.Credentials.remove_credential(id)
            else:
                self.PlainTexts.remove_credential(id)

        @eel.expose
        def get_credentials_data(type: int):
            credentials = ""
            if type == CredentialsType.CREDENTIALS.value:
                credentials = self.Credentials.get_all_credentials()
            else:
                credentials = self.PlainTexts.get_all_credentials()

            algorithm : str = self.Config.APP["algorithm"].upper()
            import utils.Ciphers as Ciphers
            cryptotype: CryptoType = CryptoType.string_to_enum(algorithm)
            if algorithm != CryptoType.NONE.value:
                for credential in credentials:
                    #credential['service'] = Ciphers.decrypt(credential['service'], cryptotype)
                    credential['email_or_username'] = Ciphers.decrypt(credential['email_or_username'], cryptotype, self.Key)
                    credential['value'] = Ciphers.decrypt(credential['value'], cryptotype, self.Key)
            return credentials
        
        @eel.expose
        def get_page_content(page: str = "home.html"):
            """
            Load HTML content from the 'pages' directory within the 'web' base directory.

            :param page: Name of the HTML file to load, defaults to 'home.html'.
            :return: HTML content or an error message in HTML format.
            """
            try:
                # Construct the base directory path, assuming 'web' is where your static files are
                base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui')
                
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
                self.Logger.error(f"An error occurred: {e}")
                return "<h1>Error Loading Page</h1>"

        @eel.expose
        def open_file_dialog(options_json):
            try:
                options = json.loads(options_json)
                # Ensure 'multiple' is set correctly
                if 'multiple' not in options:
                    options['multiple'] = False  # Default to single file selection
                
                fpath = self.Inputs.open_file_dialog(**options)
                # Ensure result is a list or string as expected by your application
                if isinstance(fpath, tuple):  # Tkinter returns tuple for multiple files
                    fpath = list(fpath) if options['multiple'] else fpath[0]
                
                if fpath:
                    with open(fpath, 'rb') as file:
                        self.Key = base64.b64encode(file.read()).decode('utf-8')
                
                return fpath if fpath else None
            except Exception as e:
                self.Logger.error(f"File dialog error: {e}")
                return None

    def __init__(self, Logger: utils.Logger, Config: utils.Config, Credentials: utils.DataParser, PlainTexts: utils.DataParser):
        self.Logger = Logger
        self.Config = Config
        self.PlainTexts = PlainTexts
        self.Credentials = Credentials
        self.Inputs = EELInputs.Inputs()
        
        self.__eel__()

        user_data_dir = "c:\\temp\\Safe&Sound"
        if os.path.exists(user_data_dir):
            for filename in os.listdir(user_data_dir):
                file_path = os.path.join(user_data_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    self.Logger.error(f'Failed to delete {file_path}. Reason: {e}')

        eel.init("ui")

        def check_internet():
            try:
                import requests
                response = requests.get("https://www.google.com", timeout=5)
                return True
            except requests.ConnectionError:
                return False

        host = "localhost"
        if check_internet():
            host = "safeandsound"

        eel_kwargs = dict(
            host=host, # can't use custom host name with no internet
            port=8080,
            size=(Config.APP['min_width_size'], Config.APP['min_hight_size']),
            block=True,
            cmdline_args=[ '--user-data-dir=c:\\temp\\Safe&Sound',
                            '--disable-gpu',
                            '--disable-extensions',
                            '--disable-plugins',
                            '--disable-translate',
                            '--disable-features=TranslateUI',
                            '--disable-features=Translate',
                            '--disable-features=TranslateLanguageDetection',
                            '--disable-features=NetworkService',
                            '--disable-features=CrossSiteDocumentBlockingIfIsolating',
                            '--disable-features=CrossSiteDocumentBlockingAlways',
                            '--disable-features=ImprovedCookieControls',
                            '--disable-features=GlobalMediaControls',
                            '--disable-features=IdleDetection',
                            '--disable-password-manager',
                            '--disable-autofill-keyboard-accessory',
                            '--disable-autofill-fallback-to-insecure-mode',
                            '--disable-save-password-bubble',
                            '--disable-password-generation',
                            '--disable-forms-re Strict-mode-for-autofill',
                            '--disable-password-leak-detection',
                            '--disable-sync',
                            '--disable-password-manager-internal',
                            '--disable-password-manager-reauthentication',
                            '--disable-password-manager-warning',
                            '--password-manager-internal-disabled',
                            '-safe-mode'
                        ]
        )
        
        try:
            eel.start("index.html", mode='default', **eel_kwargs, app_mode=True)
            Logger.info("Started EEL application.")
        except EnvironmentError as e:
            Logger.error(f"Environment error when starting EEL: {e}")
            # Your fallback logic
        except Exception as e:
            Logger.error(f"Unexpected error starting EEL: {e}")
            raise