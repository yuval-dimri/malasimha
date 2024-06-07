
from uuid import uuid4
import streamlit as st
from streamlit_elements import elements, mui, lazy

from .dashboard_element import DashboardElement


def constrain(value, min_value, max_value):
    return max(min(float(value), float(max_value)), float(min_value))


class SliderElement(DashboardElement):
    def config(self,
               *,
               min_value=0,
               max_value=100,
               step=1):
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = min_value

    def __call__(self):
        if f"{self._key}_value" not in st.session_state:
            st.session_state[f"{self._key}_value"] = 0

        def handle_slider_input_committed(event, value):
            self.value = constrain(
                value, self.min_value, self.max_value)
            st.session_state[f"{self._key}_value"] = value
            self.value = value

            self._value_changed_callback(
                st.session_state[f"{self._key}_value"])

        def handle_text_input_change(event):
            self.value = constrain(event.target.value.strip() or 0,
                                   self.min_value, self.max_value)
            st.session_state[f"{self._key}_value"] = self.value
            self._value_changed_callback(
                st.session_state[f"{self._key}_value"])

        self._mui_element_slider_and_input(
            handle_text_input_change, handle_slider_input_committed)

    def _mui_element_slider_and_input(self, text_cb, slider_cb, value=None):
        self.value = st.session_state[f"{self._key}_value"]

        def slider_change(event, value):
            st.session_state[f"{self._key}_value"] = value
            self.value = value

        slider_params = {
            'value': st.session_state[f"{self._key}_value"],
            'onChangeCommitted': slider_cb,
            # 'onChange': slider_change,
            # 'valueLabelDisplay': 'on',
            'ariaLabelledby': self._key,
            'min': self.min_value,
            'max': self.max_value,
            'step': self.step
        }

        text_input_params = {
            'value': self.value,
            'size': 'small',
            'onChange': text_cb,
            'inputProps': {
                'step': self.step,
                'min': self.min_value,
                'max': self.max_value,
                'type': 'number',
                'ariaLabelledby': self._key
            }
        }

        with mui.FormControl(sx={'m': 1, 'padding': 1, 'width': '80%'}):
            mui.Typography(self.label, id="input-slider", gutterBottom=True)
            with mui.Grid(container=True, spacing=2, alignItems="center"):
                with mui.Grid(item=True, xs=True):
                    mui.Slider(**slider_params)
                with mui.Grid(item=True):
                    mui.Input(**text_input_params)
