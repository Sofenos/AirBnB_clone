#!/usr/bin/python3

"""State Module"""

from models.base_model import BaseModel


class State(BaseModel):
    """
    State class

    Methods:
        __init__: Constructor of the State class
    """
    name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
