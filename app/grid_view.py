import streamlit as st
from streamlit_elements import elements, dashboard, mui
from app.dashboard.input_elements import SliderElement, ButtonElement, NumericInputElement, SwitchElement, SelectElement


class GridView:
    def __init__(self):
        # Initialize the layout and store cell functions
        self.layout = []
        self.cell_functions = []

    def display_grid(self):
        # Display the grid within the elements context
        with elements("dashboard"):
            with dashboard.Grid(self.layout):
                for id, cell_func in enumerate(self.cell_functions):
                    cell_func()
                    # Directly creating MUI elements here might not work as expected.
                    # Consider passing containers or adjusting the layout strategy.

    def create_new_cell(self, cell_function, x_pos, y_pos, width=2, height=2):
        # Adjusted to reflect potential limitations in direct positioning.
        cell_id = f"cell_{len(self.cell_functions)}"
        self.layout.append(dashboard.Item(
            f"{cell_id}th_item", x_pos, y_pos, width, height, isResizable=False))
        self.cell_functions.append(cell_function)

    def handle_layout_change(self, updated_layout):
        # Update the layout when it changes
        self.layout = updated_layout
        print("Updated layout:", updated_layout)


def generic_callback(*data):
    print(f"received: {data}")


slider = SliderElement('slider1', 'slider in class',
                       generic_callback)
slider.config(min_value=0, max_value=100, step=5)

numeric_input = NumericInputElement(
    'input1', 'test input', generic_callback)
numeric_input.config(min_value=0, max_value=100)

switch = SwitchElement('switch1', 'closed loop?', generic_callback)

select_element = SelectElement('select1', 'what mode?', generic_callback)
select_element.config(
    options=['absolute', 'relative', 'speed'])


def shift_press_cb():
    print('button pressed with shift-key!')


button = ButtonElement('button1', 'send data', generic_callback)
button.config(shift_key_callback=shift_press_cb)


def form():
    with elements(""):
        form = mui.FormControl(
            fullWidth=True, margin='normal', variant='outlined')
        with form:
            slider.display()
            numeric_input.display()
            switch.display()
            button.display()


def handle_layout_change(updated_layout):
    # You can save the layout in a file, or do anything you want with it.
    # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
    print(updated_layout)


def main():
    with elements("dashboard"):
        layout = [
            # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
            dashboard.Item("item_1", 0, 0, 2, 2),
            dashboard.Item("item_2", 2, 0, 2, 2),
            dashboard.Item("item_3", 0, 2, 2, 2),
        ]

        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            with mui.Paper("item 1", key="item_1",):
                form()


# Example usage
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
