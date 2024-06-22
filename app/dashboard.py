from streamlit_elements import dashboard, mui
from contextlib import contextmanager
from uuid import uuid4
from abc import ABC, abstractmethod
import streamlit as st


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

        def __init__(self, board, x, y, w, h, _key=None, topic="", label='set label', **item_props):
            self._key = _key if _key else str(uuid4())
            self.label = label
            self._x = x
            self._y = y
            self._w = w
            self._h = h
            self._topic = topic
            self._draggable_class = Dashboard.DRAGGABLE_CLASS
            self._dark_mode = True
            board._register(dashboard.Item(
                self._key, x, y, w, h, **item_props))
            self.gui_manager = board.gui_manager

        def _switch_theme(self):
            self._dark_mode = not self._dark_mode

        def _callback(self, data):
            # Convert the data to a dictionary and perform the callback.
            if len(self._topic) < 1:
                st.error(f'please provide a topic name for "{self.label}"')
            self.gui_manager.value_set_callback(self._topic, data)
            st.session_state.ros_topic = {"topic": self._topic, "data": data}

        @ contextmanager
        def title_bar(self, padding="5px 15px 5px 15px", dark_switcher=True):
            with mui.Stack(
                key=self._key,
                className=self._draggable_class,
                alignItems="center",
                # direction="row",
                spacing=1,
                sx={
                    "padding": padding,
                    # "borderBottom": 1,
                    "borderColor": "divider",
                    # "overflow": "hidden",
                    "cursor": "move" if self.gui_manager.editing_allowed else "default",
                },
            ):

                # mui.Typography(self.label, variant="h6")
                yield

                # if dark_switcher and self.gui_manager.editing_allowed:
                #     mui.IconButton(
                #         mui.icon.Edit, onClick=self._switch_theme
                #     )

        @ abstractmethod
        def __call__(self):
            """Show elements."""
            raise NotImplementedError
