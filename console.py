
import imgui
import config
from typing import Self


class Console:
    def __init__(self: Self) -> None:
        self.lines: list[str] = list[str]()
        pass

    def write_line(self: Self, line: str) -> None:
        self.lines.append(">: " + line)

    def gui(self: Self) -> None:
        imgui.set_next_window_size(config.WINDOW_WIDTH - 256, 256)
        imgui.set_next_window_position(0, config.WINDOW_HEIGHT - 256)
        imgui.begin("Console", flags=imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_RESIZE)
        imgui.input_text_multiline("", '\n'.join(self.lines), width=-1, height=200, flags=imgui.INPUT_TEXT_READ_ONLY)
        imgui.push_item_width(-1)
        imgui.input_text("", "test")
        imgui.pop_item_width()
        imgui.end()
