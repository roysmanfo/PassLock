from enum import StrEnum


class Color(StrEnum):
    """
    For the cli
    """
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    YELLOW = "\033[1;33m"
    PURPLE = "\033[0;35m"
    RESET = "\033[0m"


col = Color



class Colors(StrEnum):
    """
    For the gui
    """
    PL_BLACK = "#000"
    PL_DARK = "#080808"
    PL_GRAY = "#111"
    PL_LGRAY = "#181818"
    PL_PURPLE = "#6300ff"

    PL_LIGHT = "#eee"
    PL_WHITE = "#fff"