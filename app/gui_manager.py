# gui_manager.py

import json
import streamlit as st
from controls import Slider, Button, Dropdown, Checkbox, TextInput
from uuid import uuid4


class GuiManager:
    def __init__(self, dashboard=None, config_file="gui_state.json"):
        self.dashboard = dashboard
        self.config_file = config_file
        self.controls = []
        self.control_classes = {
            "Slider": Slider,
            "Button": Button,
            "Dropdown": Dropdown,
            "Checkbox": Checkbox,
            "TextInput": TextInput
        }

        if 'editing_allowed' not in st.session_state:
            st.session_state.editing_allowed = False

        self.configuration = []
        self.load_configuration()

    def toggle_editing(self, value):
        st.session_state.editing_allowed = value

    def value_set_callback(self, topic, data):
        print(f'sending: {data}, on topic: {topic}')

    @property
    def editing_allowed(self):
        return st.session_state.editing_allowed

    def save_configuration(self):
        st.session_state.configuration = self.configuration
        self._save_to_file()

    def download_configuration(self):
        return json.dumps(self.configuration, indent=4)

    def on_layout_change(self, layout):
        for item in layout:
            control = next(
                (ctrl for ctrl in self.configuration if ctrl.get('_key') == item['i']), None)
            if control:
                control.update({
                    'x': item['x'],
                    'y': item['y'],
                    'w': item['w'],
                    'h': item['h']
                })
        self.save_configuration()

    def _save_to_file(self):
        with open(self.config_file, 'w') as file:
            json.dump(self.configuration, file, indent=4)

    def load_configuration(self):
        try:
            with open(self.config_file, 'r') as file:
                self.configuration = json.load(file)
        except FileNotFoundError:
            self.configuration = []

    def load_controls(self):
        self.controls.clear()  # Clear existing controls before loading new ones
        for control in self.configuration:
            control_type = control.get('type')
            ControlClass = self.control_classes.get(control_type)

            if not ControlClass:
                continue

            x = control.get('x', 0)
            y = control.get('y', 0)
            w = control.get('w', 4)
            h = control.get('h', 2)
            _key = control.get('_key', None)
            label = control.get('label')

            item_props = {k: v for k, v in control.items() if k not in [
                'type', 'x', 'y', 'w', 'h', '_key', 'label']}

            control_instance = ControlClass(
                self.dashboard, x, y, w, h, _key=_key, label=label, **item_props)
            self.controls.append(control_instance)

    def display_controls(self):
        for control_instance in self.controls:
            control_instance()
