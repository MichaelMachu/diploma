from Interfaces.GraphicalUserInterface import GraphicalUserInterface

class WindowHandler:

    def __init__(self) -> None:
        self.__index = 0
        self.__views = {}

    def __increment(self) -> None:
        self.__index += 1

    def register(self, view: GraphicalUserInterface) -> None:
        self.__views[self.__index] = view
        view.id = self.__index
        self.__increment()

    def exists(self, view: GraphicalUserInterface) -> bool:
        if view is None:
            return False
        return view.id in self.__views

    def destroy(self, view: GraphicalUserInterface) -> None:
        if view.id == -1:
            return
        view.mainWindow.destroy()
        self.__views.pop(view.id)

    def get_index(self) -> int:
        return self.__index