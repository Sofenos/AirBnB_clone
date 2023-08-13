#!/usr/bin/python3

"""This module initializes the application's file storage"""

from models.engine.file_storage import FileStorage

# Create a unique FileStorage instance for the app
storage = FileStorage()

# Call the reload() method to populate
storage.reload()
