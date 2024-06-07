
from streamlit_elements import elements, dashboard, mui
from app.control_board.board_elements import dashboard_elements
from app.control_board.control_board import ControlBoard


class Editor:
    def __init__(self, dashboard: ControlBoard):
        self.dashboard = dashboard
        self.dashboard.set_layout_change_cb(self.dashboard_grid_edited_cb)

    def dashboard_grid_edited_cb(self, dashboard_changes):
        print(dashboard_changes)

    def create_new_dashboard_element(self, element_type):
        self.dashboard.register(item=dashboard_elements[element_type])

    def choose_element(self):
        options = dashboard_elements.keys()
        with elements("choose_element"):
            selection = dashboard_elements["selection"]
