

from uuid import uuid4
import streamlit as st
from streamlit_elements import mui, lazy

from .dashboard_element import DashboardElement


class SelectElement(DashboardElement):
    def config(self, *, options):
        self.options = options

    def _mui_element(self):
        def on_change_cb(event, data):
            self._value_changed_callback(data.props)

        with mui.FormControl(fullWidth=True, sx={'m': 1}):
            with mui.FormControl(fullWidth=True, variant="outlined", size="big"):
                mui.InputLabel(self.label, id=self._key)
                with mui.Select(key=self._key, onChange=on_change_cb,
                                type="number",
                                labelId=self._key,
                                label=self.label,
                                disabled=self.disabled):
                    for value, option in enumerate(self.options):
                        mui.MenuItem(option, value=value)
