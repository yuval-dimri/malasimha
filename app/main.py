# main.py

from dashboard import Dashboard
import streamlit as st
from streamlit_elements import elements
from sidebar import Sidebar
from gui_manager import GuiManager

# Initialize the GuiManager and Dashboard together
gui_manager = GuiManager(config_file='app/gui_controls.json')
dashboard = Dashboard(gui_manager)

# Update the gui_manager to include the dashboard reference
gui_manager.dashboard = dashboard

# Create an instance of the Sidebar
sidebar = Sidebar(gui_manager)

# Define the main layout and add controls


def main():
    # Set the Streamlit page layout to wide
    st.set_page_config(layout="wide", initial_sidebar_state='collapsed')

    # Display the sidebar content
    sidebar()

    # Main dashboard elements
    with elements('dashboard'):
        gui_manager.load_controls()

        with dashboard(rowHeight=70):
            gui_manager.display_controls()


# Run the main layout
if __name__ == "__main__":
    main()
