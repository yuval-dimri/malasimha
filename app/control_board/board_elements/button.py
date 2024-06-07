
from uuid import uuid4
import streamlit as st
from streamlit_elements import elements, mui, lazy
# from input_element import InputElement


# class ButtonElement(InputElement):
#     def config(self, *, shift_key_callback):
#         self.shift_key_callback = shift_key_callback

#     def _mui_element(self):
#         def on_click_cb(event):
#             if event.shiftKey:
#                 self.shift_key_callback()
#             else:
#                 self.callback()

#         with mui.FormControl(sx={'m': 1}):
#             mui.Button(
#                 self.label,
#                 key=self.id,
#                 onClick=on_click_cb,
#                 variant="contained",
#                 padding='5px',
#                 disabled=self.disabled
#             )
