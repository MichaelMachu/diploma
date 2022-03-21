
class FunctionInterface:

    # Object functions
    def get_name(self) -> str:
        """Returns name of the function."""

    def get_line_array(self) -> list:
        """Returns default line array value of the function."""

    def get(self, r: float, x: float) -> float:
        """Returns float value calculated by specified function."""

    def __str__(self) -> str:
        """Returns definition of specified function as a string."""