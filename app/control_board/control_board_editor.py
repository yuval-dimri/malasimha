import json

from .control_board import ControlBoard
from streamlit_elements import mui, elements


class ControlBoardEditor():
    def __init__(self, control_board_config_file):
        self.config_file = control_board_config_file
        self._layout_changed_cb = None
        self.add_new_element_cb = None
        self._layout = []

    def layout_changed_cb(self, new_layout):
        print('layout_changed_cb')
        self.layout = new_layout

    def register_control_board_element(self, element_name):
        if self.add_new_element_cb is not None:
            self.add_new_element_cb(element_name, x=2, y=3, w=1, h=1)

    def editor_card(self):
        def on_change_cb(event, data):
            # print(data.props)
            self.register_control_board_element(data.props.children)

        with elements('editor_module selector'):
            with mui.FormControl(fullWidth=True, sx={'m': 1}):
                with mui.FormControl(fullWidth=True, variant="outlined", size="big"):
                    mui.InputLabel("select input element",
                                   id='editor_input_element_select')
                    with mui.Select(key="editor_input_element_select", onChange=on_change_cb,
                                    type="number",
                                    labelId='editor_input_element_select',
                                    label='select input element',
                                    ):
                        for value, option in enumerate(ControlBoard.dashboard_element_types.keys()):
                            mui.MenuItem(option, value=value)

    def write_layout_to_file(self):
        # write the dict of control_board_config as json to the file
        with open(self.config_file, 'w') as f:
            json.dump(self._layout, f)
