class InvalidGameType(Exception):
    """Custom exception if game type string is inserted"""

    def __init__(self, game=None) -> None:
        if game:
            self.message = f"Unsupported game type string supplied: '{game}'"
        else:
            self.message = "Unsupported game type string supplied"
        super().__init__(self.message)
