""" Declares Vote entity"""

from pydantic import BaseModel


class Vote (BaseModel):
    """ Represents that an user wants (or not) to see a watchable """

    watchable_index: int
    content: bool
