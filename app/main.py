import json
import streamlit as st

from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event, lazy, mui
from types import SimpleNamespace

from dashboard.editor_card import editor_card
from dashboard import Dashboard, ControlBox


class Gui:
    def __init__(self):
        if 'master_config' not in st.session_state:
            self.master_config = {
                'grid_config': {},
                'control_boxes_config': {}
            }
            try:
                with open('gui_configuration.json', 'r') as json_file:
                    self.master_config = json.loads(json_file.read())
            except:
                pass
            st.session_state['master_config'] = self.master_config
        else:
            self.master_config = st.session_state['master_config']

    def main(self):
        self._side_bar()
        self._display_grid()

    def _side_bar(self):
        with st.sidebar:
            self._download_configuration_button()
            self._load_json_configuration_button()
            self.allow_grid_dragg = st.toggle('allow editing', value=False)
            self._gui_edit_card()

    def _gui_edit_card(self):
        editor_card()

    def _load_json_configuration_button(self):
        json_file = st.file_uploader(
            'upload json configuration', accept_multiple_files=False)
        if json_file is not None:
            st.session_state.master_config = json.loads(
                json_file.read())

    def _download_configuration_button(self):
        # TODO correct this ugly workaround
        file_path = 'gui_configuration.json'
        with open(file_path, 'w') as json_file:
            json.dump(self.master_config, json_file, indent=4)

        # Read the JSON file
        with open(file_path, 'r') as json_file:
            st.download_button(
                label="download gui configuration file",
                data=json_file,
                file_name="gui_config.json",
                # mime="application/json"
            )

    def _update_grid_configuration_on_change(self, config):
        grid_config = config
        self.master_config['grid_config'] = grid_config

    def _display_grid(self):
        board = Dashboard(
            change_config_cb=self._update_grid_configuration_on_change,
        )

        self.control_boxes = [
            ControlBox(board, **grid_box_config, allow_dragging=self.allow_grid_dragg) for grid_box_config in self.master_config['grid_config']
        ]

        with elements("grid_layout"):
            event.Hotkey("ctrl+u", sync(), bindInputs=True,
                         overrideDefault=True)

            with board(rowHeight=57):
                for control_box in self.control_boxes:
                    control_box()
                    self.master_config['control_boxes_config'][control_box._key] = control_box.box_config


def main():
    gui_app = Gui()
    gui_app.main()


if __name__ == "__main__":
    st.set_page_config(layout="wide", initial_sidebar_state='collapsed')

    main()
