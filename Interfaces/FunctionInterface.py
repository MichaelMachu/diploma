
class FunctionInterface:

    # Object functions
    def get_name(self) -> None:
        """Returns name of the function."""

    def get_line_array(self) -> None:
        """Returns default line array value of the function."""

    def get(self, r: float, x: float) -> float:
        """Returns float value calculated by specified function."""

    def __str__(self) -> str:
        """Returns definition of specified function as a string."""