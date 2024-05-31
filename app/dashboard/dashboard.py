from uuid import uuid4
from abc import ABC, abstractmethod
from streamlit_elements import dashboard, mui
from contextlib import contextmanager


class Dashboard:

    DRAGGABLE_CLASS = "draggable"

    def __init__(self, change_config_cb):
        self.handle_layout_change_cb = change_config_cb
        self._layout = []

    def _register(self, item):
        self._layout.append(item)

    @contextmanager
    def __call__(self, **props):
        # Draggable classname query selector.
        # if self.allow_dragging:
        props["draggableHandle"] = f".{Dashboard.DRAGGABLE_CLASS}"

        with dashboard.Grid(self._layout, onLayoutChange=self.handle_layout_change_cb, **props):
            yield

    class Item(ABC):

        def __init__(self, board, x, y, w, h, i=None, allow_dragging=False, **item_props):
            if i is None:
                self._key = str(uuid4())
            else:
                self._key = i
            self.allow_dragging = allow_dragging
            self._draggable_class = Dashboard.DRAGGABLE_CLASS
            self._dark_mode = True
            self.return_data = {}
            self.element_key_to_data_name = {}
            self.box_config = {}
            item_props['isDraggable'] = self.allow_dragging
            board._register(dashboard.Item(
                self._key, x, y, w, h, **item_props))

        def _switch_theme(self):
            self._dark_mode = not self._dark_mode

        @contextmanager
        def title_bar(self, padding="5px 15px 5px 15px", dark_switcher=False):
            with mui.Stack(
                className=self._draggable_class,
                alignItems="center",
                direction="row",
                spacing=1,
                sx={
                    "padding": padding,
                    "borderBottom": 1,
                    "borderColor": "divider",
                },
            ):
                yield

                if dark_switcher:
                    if self._dark_mode:
                        mui.IconButton(mui.icon.DarkMode,
                                       onClick=self._switch_theme)
                    else:
                        mui.IconButton(mui.icon.LightMode, sx={
                                       "color": "#ffc107"}, onClick=self._switch_theme)

        @abstractmethod
        def __call__(self):
            """Show elements."""
            raise NotImplementedError
