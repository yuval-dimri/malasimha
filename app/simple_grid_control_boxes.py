import json
import streamlit as st

from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event, lazy
from types import SimpleNamespace

from dashboard import Dashboard, Card, Editor, ControlBox


def main():
    if "w" not in state:
        board = Dashboard()
        w = SimpleNamespace(
            dashboard=board,
            control_box=ControlBox(board, 0, 0, 4, 8, minW=4, minH=8),
            control_box1=ControlBox(board, 0, 0, 4, 8, minW=4, minH=8),
            control_box2=ControlBox(board, 0, 0, 4, 8, minW=4, minH=8),
        )
        state.w = w

    else:
        w = state.w

    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

        with w.dashboard(rowHeight=57):
            w.control_box()
            w.control_box1()
            w.control_box2()


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
