class InvalidInputException(Exception):
    """Exception raised for invalid user's input.
    Will record the exact line number of the problematic
    input.
    """
    error_template = "Invalid input detected on line {}: \n{}"

    def __init__(self, message, line_number=None):
        super().__init__(message)
        self.message = message
        self.line_number = line_number

    def __str__(self):
        if self.line_number is not None:
            return self.__class__.error_template.format(
                self.line_number, super().__str__())
        else:
            return super().__str__()


class InvalidRoverOperationException(Exception):
    """Exception raised when a rover is trying to
    perform an invalid operation.
    Will record the problematic rover's name.
    """
    error_template = "Invalid operation detected for rover {}: \n{}"

    def __init__(self, message, rover_name):
        super().__init__(message)
        self.message = message
        self.rover_name = rover_name

    def __str__(self):
        return self.__class__.error_template.format(
            self.rover_name, super().__str__())
