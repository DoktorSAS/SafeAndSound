import tkinter as tk
from tkinter import filedialog

class Inputs:

    def __init__(self) -> None:
        pass

    def open_file_dialog(self, **kwargs):
        """
        Opens a file selection dialog and returns the selected file path.

        Keyword Arguments:
        - filetypes: List of tuples specifying file types to display. Each tuple should contain 
                    a description and a pattern, e.g., ("Text files", "*.txt").
        - title: Title of the file dialog window.
        - initialdir: Initial directory to start the dialog in.
        - defaultextension: Default extension if the user doesn't provide one.
        - multiple: If True, allows selecting multiple files (returns list).

        Returns:
        str or list: Path to the selected file(s), or None if canceled.
        """
        
        # Create a new Tk instance and immediately withdraw it
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # Ensure the dialog appears on top of all other windows
        root.attributes("-topmost", True)
        root.update()  # Force update to make sure the window attributes are applied
    
        # Set up default values if not provided
        if 'filetypes' not in kwargs:
            kwargs['filetypes'] = [("All files", "*.*")]
        if 'title' not in kwargs:
            kwargs['title'] = "Select a file"

        # Determine if we're allowing multiple file selection
        try:
            # Determine if we're allowing multiple file selection
            if kwargs.get('multiple', False):
                file_paths = filedialog.askopenfilenames(parent=root, **kwargs)
            else:
                file_paths = filedialog.askopenfilename(parent=root, **kwargs)
        finally:
            # Make sure we clean up even if an error occurs
            root.destroy()
 
        return file_paths
