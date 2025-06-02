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


import os
import json


def load_all_json_files(folder_path):
    """
    Load all JSON files from a specified folder.

    Args:
        folder_path (str): Path to the folder containing JSON files

    Returns:
        list: List of loaded JSON objects
    """
    all_data = []

    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return all_data

    # Get all json files in the folder
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

    # Load each json file
    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.append(data)
        except Exception as e:
            print(f"Error loading {file_path}: {str(e)}")

    print(f"Loaded {len(all_data)} JSON files from {folder_path}")
    return all_data