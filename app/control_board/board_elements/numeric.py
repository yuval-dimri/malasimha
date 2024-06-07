
from uuid import uuid4
import streamlit as st
from streamlit_elements import elements, mui, lazy
from .dashboard_element import DashboardElement


def constrain(value, min_value, max_value):
    return max(min(float(value), float(max_value)), float(min_value))


class NumericInputElement(DashboardElement):
    def config(self, *, min_value=0, max_value=100):
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value

    def _mui_element(self):
        if f"{self._key}_value" not in st.session_state:
            st.session_state[f"{self._key}_value"] = 0

        def handle_input_change(event):
            self.value = constrain(
                event.target.value.strip() or 0, self.min_value, self.max_value)
            st.session_state[f"{self._key}_value"] = self.value
            self._value_changed_callback(self.value)

        with mui.FormControl(fullWidth=True, sx={'m': 1}):
            mui.TextField(
                value=self.value,
                key=self._key,
                onChange=handle_input_change,
                type="number",
                label=self.label,
                disabled=self.disabled,
                inputProps={
                    'min': self.min_value,
                    'max': self.max_value,
                    'aria-labelledby': self._key
                }
            )
