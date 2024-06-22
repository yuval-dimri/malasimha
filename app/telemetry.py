import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


class Telemetry:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = pd.read_csv(self.csv_file)
        self.selected_column = self.data.columns[0]

    def update_data(self):
        self.data = pd.read_csv(self.csv_file)

    def render(self):
        self.update_data()

        with st.expander("Live Telemetry Data", expanded=True):
            self.selected_column = st.selectbox(
                "Select Column", self.data.columns)
            st.line_chart(self.data[self.selected_column])


