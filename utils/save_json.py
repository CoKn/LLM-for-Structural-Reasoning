import json
import os


def save_json(data, file_path, indent=2, ensure_path=True):
    """
    Save a Python dictionary to a JSON file.

    Args:
        data (dict): The dictionary to save
        file_path (str): Path where the JSON file will be saved
        indent (int, optional): Number of spaces for indentation. Defaults to 2.
        ensure_path (bool, optional): Create directory path if it doesn't exist. Defaults to True.

    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        if ensure_path:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)

        return True

    except Exception as e:
        print(f"Error saving JSON file: {e}")
        return False