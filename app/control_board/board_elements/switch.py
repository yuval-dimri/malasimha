

from uuid import uuid4
import streamlit as st
from streamlit_elements import elements, mui, lazy

from .dashboard_element import DashboardElement


class SwitchElement(DashboardElement):
    def config(self, **kwargs):
        # nothing special
        pass

    def __call__(self):
        def on_change_cb(event):
            self._value_changed_callback(event.target.checked)

        if self._key not in st.session_state:
            st.session_state[self._key] = ""

        with mui.FormControl(fullWidth=True, sx={'m': 1, 'padding': 1}):
            mui.FormControlLabel(
                control=mui.Typography(self.label),
                label=mui.Switch(key=self._key,
                                 label=self.label,
                                 onChange=on_change_cb,
                                 default=False,
                                 disabled=self.disabled
                                 )
            )
