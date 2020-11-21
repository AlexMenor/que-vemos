""" Defines DataRequestException """

class DataRequestException(Exception):
    """ Exception raised when the data cant be obtained from the provider"""
def __init__(self):
    self.message = "Something went wrong while obtaining the data"
    super().__init__(self.message)
