
class Color:

    def __init__(self, colorObject: tuple) -> None:
        """It keeps data of the color selection from tkinter color selection inside a parameter colorObject"""
        self.colorObject = colorObject
        self._colors_by_K = None

    def get_rgb(self) -> tuple:
        return self.colorObject[0]

    def get_red(self) -> float:
        return self.colorObject[0][0]

    def get_green(self) -> float:
        return self.colorObject[0][1]

    def get_blue(self) -> float:
        return self.colorObject[0][2]

    def get_hex(self) -> str:
        return self.colorObject[1]

    def convert_color_to_hex(self, red: float, green: float, blue: float) -> str:
        red = int(red)
        green = int(green)
        blue = int(blue)
        return '#%02x%02x%02x' % (red, green, blue)

    def __get_colors_by_K(self, K: int) -> list:
        splitter = 255 / K

        red = self.get_red()
        green = self.get_green()
        blue = self.get_blue()
        
        result = []
        for _ in range(K):
            result.append(self.convert_color_to_hex(abs(red), abs(green), abs(blue)))

            red -= splitter
            green -= splitter
            blue -= splitter

        return result

    def get_colors_by_K(self, K: int, force: bool = False) -> list:
        """Returns list of colors based on the number of states K"""
        if self._colors_by_K is None or force:
            self._colors_by_K = self.__get_colors_by_K(K)
        
        return self._colors_by_K