from atexit import register
from types import SimpleNamespace
from uuid import uuid4
from abc import ABC, abstractmethod
from streamlit_elements import dashboard, mui, elements
from streamlit import session_state as state
from contextlib import contextmanager
# from .control_board_editor import ControlBoardEditor

from .board_elements import NumericInputElement, SelectElement, SliderElement, SwitchElement


class ControlBoard:
    DRAGGABLE_CLASS = "draggable"
    dashboard_element_types = {
        'slider': SliderElement,
        # 'button': ButtonElement,
        'switch': SwitchElement,
        'numeric': NumericInputElement,
        'dropdown': SelectElement,
        # 'card': CardElement,
    }

    def __init__(self, control_board_editor):
        self.editor = control_board_editor
        self.editor.add_new_element_cb = self.register
        self._layout_changed_cb = None
        self._layout = []
        if 'layout' not in state:
            state.layout = self._layout

    def register(self, item, **params):
        if item not in self.dashboard_element_types.keys():
            raise ValueError(
                f"Unknown dashboard element type: {item}. choose from: {self.dashboard_element_types.keys()}")
        dashboad_element = self.dashboard_element_types[item](**params)
        self._layout.append(dashboad_element)
        state.pop('w', None)
        state.layout = self._layout

    def __call__(self, **props):
        # Draggable classname query selector.
        # if self.allow_dragging:
        props["draggableHandle"] = f".{ControlBoard.DRAGGABLE_CLASS}"
        if 'w' not in state:
            w = SimpleNamespace()
            print(f'displaying layout {self._layout}')
            for element in state.layout:
                print(f'adding element {element}')
                w.__dict__[element._key] = element
            state.w = w
        else:
            w = state.w

        with elements('dashboard_display'):
            with dashboard.Grid(self._layout, onLayoutChange=self.editor.layout_changed_cb, rowHeight=20, **props):
                for element in w.__dict__.values():
                    element()
