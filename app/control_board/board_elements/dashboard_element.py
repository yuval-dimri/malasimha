from abc import ABC, abstractmethod
from contextlib import contextmanager
from uuid import uuid4
from streamlit_elements import mui


class DashboardElement(ABC):
    DRAGGABLE_CLASS = "draggable"

    def __init__(self, x, y, w, h, i=None, label='make sure to set the label', allow_dragging=True, **item_props):
        if i is None:
            self._key = str(uuid4())
        else:
            self._key = i

        self.label = label
        self.disabled = False  # TODO - set disabled somehow
        self.allow_dragging = allow_dragging
        self._draggable_class = self.DRAGGABLE_CLASS
        self._dark_mode = True
        self.return_data = {}
        self.element_key_to_data_name = {}
        self.box_config = {}
        item_props['isDraggable'] = self.allow_dragging

    def _switch_theme(self):
        self._dark_mode = not self._dark_mode

    def _value_changed_callback(self, data):
        print(f'do something with {data}')

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
