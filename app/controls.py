# controls.py

from time import time
from dashboard import Dashboard
from streamlit_elements import mui, lazy
import streamlit as st
from uuid import uuid4


def constrain(value, min_value, max_value):
    return max(min(float(value), float(max_value)), float(min_value))


class Slider(Dashboard.Item):

    def __init__(self, board, x, y, w, h, _key=None, topic="", **item_props):
        super().__init__(board, x, y, w, h, _key=_key, topic=topic, **item_props)
        self._min_val = item_props.get('min_val', 0)
        self._max_val = item_props.get('max_val', 100)
        self._step = item_props.get('step', 1)
        self._value = self._min_val
        self.state_value_key = f'{self._key}_value'
        if self.state_value_key not in st.session_state:
            st.session_state[self.state_value_key] = self._min_val
        else:
            self._value = st.session_state[self.state_value_key]

    def _send_value(self, value):
        try:
            self._value = constrain(float(value), self._min_val, self._max_val)
        except ValueError:
            self._value = self._min_val
        # if update_state:
        st.session_state[self.state_value_key] = self._value
        self._callback({"value": self._value})

    def __call__(self):
        with self.title_bar():
            with mui.FormControl(sx={'m': 1, 'padding': 1, 'width': '80%'}):
                mui.Typography(self.label, id="input-slider",
                               gutterBottom=True)

                mui.Box(
                    sx={"display": "flex", "alignItems": "center"}
                )(
                    mui.Slider(
                        ariaLabelledby=self._key,
                        value=st.session_state.get(
                            self.state_value_key),
                        min=self._min_val,
                        max=self._max_val,
                        step=self._step,
                        onChange=lambda event, value: self._send_value(
                            value),
                        # onChangeCommitted=lambda event, value: self._send_value(
                        #     value, True),
                        sx={"width": "70%"}
                    ),
                    mui.Input(
                        value=st.session_state.get(self.state_value_key),
                        ariaLabelledby=self._key,
                        onChange=lambda event: self._send_value(
                            event.target.value
                        ),
                        sx={"width": "30%", "marginLeft": "8px"}
                    )
                )

    @ staticmethod
    def default_config():
        return {
            "type": "Slider",
            "w": 4,
            "h": 2,
            "_key": str(uuid4()),
            "label": "New Slider",
            "min_val": 0,
            "max_val": 100,
            "step": 1,
            "topic": ""
        }


class Button(Dashboard.Item):

    def __init__(self, board, x, y, w, h, _key=None, topic="", **item_props):
        super().__init__(board, x, y, w, h, _key=_key, topic=topic, **item_props)
        self._text = item_props.get('label', self.label)
        self._on_click = item_props.get('on_click', None)

    def _send_data(self, value):
        self._callback({'value': time()})

    def __call__(self):
        with self.title_bar():
            mui.Button(self._text,
                       variant='contained',
                       onClick=self._send_data,
                       sx={"width": "100%"})

    @ staticmethod
    def default_config():
        return {
            "type": "Button",
            "w": 4,
            "h": 2,
            "_key": str(uuid4()),
            "label": "New Button",
            "topic": ""
        }


class Dropdown(Dashboard.Item):

    def __init__(self, board, x, y, w, h, _key=None, topic="", **item_props):
        super().__init__(board, x, y, w, h, _key=_key, topic=topic, **item_props)
        self._options = item_props.get(
            'options', self.default_config().get('options'))

    def _send_data(self, event, data):
        self._callback({"value": data.props.value})

    def __call__(self):
        with self.title_bar():
            with mui.FormControl(fullWidth=True, sx={'m': 1}):
                with mui.FormControl(fullWidth=True, variant="outlined", size="big"):
                    mui.InputLabel(self.label)

                    with mui.Select(onChange=self._send_data,
                                    type="number",
                                    label=self.label):
                        for value, option in enumerate(self._options):
                            mui.MenuItem(option, value=value)

    @ staticmethod
    def default_config():
        return {
            "type": "Dropdown",
            "w": 4,
            "h": 2,
            "_key": str(uuid4()),
            "label": "New Dropdown",
            "options": [
                "option 1",
                "option 2",
            ],
            "topic": ""
        }


class Checkbox(Dashboard.Item):

    def __init__(self, board, x, y, w, h, _key=None, topic="", **item_props):
        super().__init__(board, x, y, w, h, _key=_key, topic=topic, **item_props)

    def _send_data(self, event):
        self._callback({"value": int(event.target.checked or 0)})

    def __call__(self):
        with self.title_bar():
            with mui.FormControl(fullWidth=True, sx={'m': 1, 'padding': 1}):
                mui.FormControlLabel(
                    control=mui.Typography(self.label),
                    label=mui.Switch(
                        label=self.label,
                        onChange=self._send_data,
                    )
                )

    @ staticmethod
    def default_config():
        return {
            "type": "Checkbox",
            "w": 4,
            "h": 2,
            "_key": str(uuid4()),
            "label": "New Checkbox",
            "topic": ""
        }


class TextInput(Dashboard.Item):

    def __init__(self, board, x, y, w, h, _key=None, topic="", **item_props):
        super().__init__(board, x, y, w, h, _key=_key, topic=topic, **item_props)
        self._min_val = item_props.get('min_val', 0)
        self._max_val = item_props.get('max_val', 100)
        self._value_key = self._key + '_value'

        if self._value_key not in st.session_state:
            st.session_state[self._value_key] = self._min_val
        else:
            self._value = st.session_state[self._value_key]

    def _send_data(self, event):
        self._value = constrain(
            float(event.target.value.strip() or 0), self._min_val, self._max_val)

        st.session_state[self._value_key] = self._value
        self._callback({"value": self._value})

    def _save_value(self, event):
        self._value = constrain(
            float(event.target.value.strip() or 0), self._min_val, self._max_val)
        st.session_state[self._value_key] = self._value

    def __call__(self):
        with self.title_bar():
            mui.TextField(
                label=self.label,
                value=st.session_state[self._value_key],
                type='number',
                onBlur=self._send_data,
                onChange=self._save_value,
                inputProps={
                    'min': self._min_val,
                    'max': self._max_val,
                    'aria-labelledby': self._key
                },
                sx={"width": "100%"}
            )

    @ staticmethod
    def default_config():
        return {
            "type": "TextInput",
            "w": 4,
            "h": 2,
            'min_val': 0,
            'max_val': 100,
            "_key": str(uuid4()),
            "label": "New Text Input",
            "topic": ""
        }
