# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""

    def __init__(self, message="An error has occurred. A pandas_etl.py exception was raised."):
        self.message = message
        super().__init__(self.message)


class UnsupportedDataSource(Error):
    pass


class UnsupportedDataDestination(Error):
    pass

