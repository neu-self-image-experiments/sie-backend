class InvalidFaceImage(Exception):
    """
    Custom exception for invalid face
    """

    def __init__(self, value):
        self.value = value

    # __str__ display function
    def __str__(self):
        return repr(self.value)
