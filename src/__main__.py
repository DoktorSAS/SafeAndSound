import os

import utils.Config as Config
import utils.Logger as Log
import utils.DataParser as Parser
import app.GUI as UserInterface


if __name__ == "__main__":
    Configuration = Config.Config("config.ini")
    
    Logger = Log.Logger(mode=Configuration.DEV['debug_mode'], log_file_name=f'{Configuration.DEV['log_fname']}')
    Logger.info("Safe&Sound - Password Manager started")

    def create_file_if_not_exists(path):
        """
        Checks if the specified path exists. If it does not exist,
        it creates the directory or file as needed.
        :param path: The path to check (can be a file or directory).
        """
        if os.path.exists(path):
            Logger.info(f"The path '{path}' already exists.")
        else:
            # Check if the path is a directory
            if os.path.splitext(path)[1] == '':
                # It's a directory, create it
                os.makedirs(path)
                Logger.info(f"Directory '{path}' created.")
            else:
                # It's a file, create the parent directory if it doesn't exist
                parent_dir = os.path.dirname(path)
                if not os.path.exists(parent_dir):
                    os.makedirs(parent_dir)
                    Logger.info(f"Parent directory '{parent_dir}' created.")
                # Now create the file
                with open(path, 'w') as file:
                    file.write('')  # Create an empty file
                Logger.info(f"File '{path}' created.")

    create_file_if_not_exists(Configuration.APP["data_location"])
    DataParser = Parser.DataParser(file_path=Configuration.APP["data_location"], Logger=Logger )
    # cmdline_args=['--incognito', '--no-experiments']
    
    UserInterface.GUI(Logger, Configuration, DataParser)