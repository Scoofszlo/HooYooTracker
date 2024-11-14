class FileParsingError(Exception):
    """Custom exception for when there is a problem parsing the file"""

    def __init__(self) -> None:
        self.message = "Error parsing config file. Nothing will be processed"
        super().__init__(self.message)
