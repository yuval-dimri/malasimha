# sidebar.py

from streamlit_elements import mui, elements, editor
import streamlit as st
import json


class Sidebar:
    def __init__(self, gui_manager):
        self.gui_manager = gui_manager
        self.control_types = [
            {"value": "Slider", "label": "Slider"},
            {"value": "Button", "label": "Button"},
            {"value": "Dropdown", "label": "Dropdown"},
            {"value": "Checkbox", "label": "Checkbox"},
            {"value": "TextInput", "label": "Text Input"},
        ]

    def __call__(self):
        with st.sidebar:
            with elements("sidebar"):
                # Allow Editing Switch
                mui.FormGroup(
                    mui.FormControlLabel(
                        control=mui.Switch(
                            checked=self.gui_manager.editing_allowed,
                            onChange=self.toggle_editing,
                            name="editingSwitch",
                            color="primary",
                            inputProps={"aria-label": "Toggle editing"}
                        ),
                        label="Allow Editing"
                    )
                )

                # Load Configuration Button
                uploaded_file = st.file_uploader(
                    "Load Configuration", type="json")
                if uploaded_file is not None:
                    self.load_configuration(uploaded_file)

                # Save Configuration Button
                config_str = self.gui_manager.download_configuration()
                st.download_button(label="Save Configuration", data=config_str,
                                   file_name="config.json", mime="application/json")

                # Dropdown to select control type
                selected_control = st.selectbox(
                    "Select control to add",
                    options=[control["label"]
                             for control in self.control_types],
                    index=0,
                )

                # Button to add the selected control
                st.button("Add Control", on_click=self.add_control,
                          args=(selected_control,))

                # Monaco Editor for direct JSON editing
                st.write("Edit Configuration JSON")
                edited_config = editor.Monaco(
                    height="500px",
                    language="json",
                    value=config_str,
                    options={"readOnly": False},
                    onChange=self.update_configuration
                )

    def toggle_editing(self, event, value):
        self.gui_manager.toggle_editing(value)

    def load_configuration(self, uploaded_file):
        new_config = json.load(uploaded_file)
        self.gui_manager.configuration = new_config
        self.gui_manager.save_configuration()

    def add_control(self, control_label):
        control_type = next(
            control["value"] for control in self.control_types if control["label"] == control_label)
        default_config = self.gui_manager.control_classes[control_type].default_config(
        )
        default_config.update({
            "x": 0,
            "y": 0
        })
        self.gui_manager.configuration.append(default_config)
        self.gui_manager.save_configuration()

    def update_configuration(self, edited_config):
        try:
            new_config = json.loads(edited_config)
            self.gui_manager.configuration = new_config
            self.gui_manager.save_configuration()
        except json.JSONDecodeError:
            st.error("Invalid JSON format")
