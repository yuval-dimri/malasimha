# dashboard.py

from streamlit_elements import dashboard, mui
from contextlib import contextmanager
from uuid import uuid4
from abc import ABC, abstractmethod


class Dashboard:

    DRAGGABLE_CLASS = "draggable"

    def __init__(self, gui_manager):
        self._layout = []
        self.gui_manager = gui_manager

    def _register(self, item):
        self._layout.append(item)

    @contextmanager
    def __call__(self, **props):
        # Draggable classname query selector.
        props["draggableHandle"] = f".{Dashboard.DRAGGABLE_CLASS}"
        props["isDraggable"] = self.gui_manager.editing_allowed
        props["isResizable"] = self.gui_manager.editing_allowed
        props["compactType"] = None  # Allow free movement
        # Allow overlapping temporarily during drag
        props["preventCollision"] = False

        with dashboard.Grid(self._layout, onLayoutChange=self.gui_manager.on_layout_change, **props):
            yield

    class Item(ABC):

        def __init__(self, board, x, y, w, h, _key=None, **item_props):
            self._key = _key if _key else str(uuid4())
            self._x = x
            self._y = y
            self._w = w
            self._h = h
            self._label = item_props.pop('label', None)
            self._draggable_class = Dashboard.DRAGGABLE_CLASS
            self.item_props = item_props
            self.gui_manager = board.gui_manager  # Assign gui_manager from board
            board._register(dashboard.Item(
                self._key, x, y, w, h, **item_props))

        @contextmanager
        def title_bar(self, padding="5px 15px 5px 15px"):
            cursor_style = "move" if self.gui_manager.editing_allowed else "default"
            with mui.Stack(
                key=self._key,
                className=self._draggable_class,
                alignItems="center",
                direction="column",
                spacing=1,
                sx={
                    "padding": padding,
                    "borderBottom": 1,
                    "borderColor": "divider",
                    "overflow": "hidden",
                    "cursor": cursor_style,  # Indicate draggable area only if editing is allowed
                },
            ):
                if self._label:
                    mui.Typography(self._label, variant="h6",
                                   sx={"marginBottom": "5px"})
                yield

        @abstractmethod
        def __call__(self):
            """Show elements."""
            raise NotImplementedError

        def display(self):
            self.__call__()
