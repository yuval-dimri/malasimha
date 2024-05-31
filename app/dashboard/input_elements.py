from enum import Enum
from uuid import uuid4
import streamlit as st
from streamlit_elements import elements, mui, lazy


def constrain(value, min_value, max_value):
    return max(min(float(value), float(max_value)), float(min_value))


class GridElement():
    def __init__(self, label, callback, data_name='', disabled=False):
        self.id = str(uuid4())
        self.label = label
        self.callback = callback
        self.disabled = disabled
        self.data_name = data_name
        self.value = 0

    def disable(self):
        self.disabled = True
        self.display()

    def config(self):
        raise NotImplementedError()

    def display(self):
        self._mui_element()

    def _mui_element(self):
        raise NotImplementedError()


class SliderElement(GridElement):
    def config(self,
               *,
               min_value=0,
               max_value=100,
               step=1):
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = min_value

    def _mui_element(self):
        if f"{self.id}_value" not in st.session_state:
            st.session_state[f"{self.id}_value"] = 0

        def handle_slider_input_committed(event, value):
            self.value = constrain(
                value, self.min_value, self.max_value)
            st.session_state[f"{self.id}_value"] = value
            self.value = value
            self.callback(st.session_state[f"{self.id}_value"])

        def handle_text_input_change(event):
            self.value = constrain(event.target.value.strip() or 0,
                                   self.min_value, self.max_value)
            st.session_state[f"{self.id}_value"] = self.value
            self.callback(st.session_state[f"{self.id}_value"])

        self._mui_element_slider_and_input(
            handle_text_input_change, handle_slider_input_committed)

    def _mui_element_slider_and_input(self, text_cb, slider_cb, value=None):
        self.value = st.session_state[f"{self.id}_value"]

        def slider_change(event, value):
            st.session_state[f"{self.id}_value"] = value
            self.value = value

        slider_params = {
            'value': st.session_state[f"{self.id}_value"],
            'onChangeCommitted': slider_cb,
            # 'onChange': slider_change,
            # 'valueLabelDisplay': 'on',
            'ariaLabelledby': self.id,
            'min': self.min_value,
            'max': self.max_value,
            'step': self.step
        }

        text_input_params = {
            'value': self.value,
            'size': 'small',
            'onChange': text_cb,
            'inputProps': {
                'step': self.step,
                'min': self.min_value,
                'max': self.max_value,
                'type': 'number',
                'ariaLabelledby': self.id
            }
        }

        with mui.FormControl(sx={'m': 1, 'padding': 1, 'width': '80%'}):
            mui.Typography(self.label, id="input-slider", gutterBottom=True)
            with mui.Grid(container=True, spacing=2, alignItems="center"):
                with mui.Grid(item=True, xs=True):
                    mui.Slider(**slider_params)
                with mui.Grid(item=True):
                    mui.Input(**text_input_params)


class NumericInputElement(GridElement):
    def config(self, *, min_value=0, max_value=100):
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value

    def _mui_element(self):
        if f"{self.id}_value" not in st.session_state:
            st.session_state[f"{self.id}_value"] = 0

        def handle_input_change(event):
            self.value = constrain(
                event.target.value.strip() or 0, self.min_value, self.max_value)
            st.session_state[f"{self.id}_value"] = self.value
            self.callback(self.value)

        with mui.FormControl(fullWidth=True, sx={'m': 1}):
            mui.TextField(
                value=self.value,
                key=self.id,
                onChange=handle_input_change,
                type="number",
                label=self.label,
                disabled=self.disabled,
                inputProps={
                    'min': self.min_value,
                    'max': self.max_value,
                    'aria-labelledby': self.id
                }
            )


class ButtonElement(GridElement):
    def config(self, *, shift_key_callback):
        self.shift_key_callback = shift_key_callback

    def _mui_element(self):
        def on_click_cb(event):
            if event.shiftKey:
                self.shift_key_callback()
            else:
                self.callback()

        with mui.FormControl(sx={'m': 1}):
            mui.Button(
                self.label,
                key=self.id,
                onClick=on_click_cb,
                variant="contained",
                padding='5px',
                disabled=self.disabled
            )


class SwitchElement(GridElement):
    def config(self, **kwargs):
        # nothing special
        pass

    def _mui_element(self):
        def on_change_cb(event):
            self.value = event.target.checked
            self.callback(self.value)

        if self.id not in st.session_state:
            st.session_state[self.id] = ""

        with mui.FormControl(fullWidth=True, sx={'m': 1, 'padding': 1}):
            mui.FormControlLabel(
                control=mui.Typography(self.label),
                label=mui.Switch(key=self.id,
                                 label=self.label,
                                 onChange=on_change_cb,
                                 default=False,
                                 disabled=self.disabled
                                 )
            )


class SelectElement(GridElement):
    def config(self, *, options):
        self.options = options

    def _mui_element(self):
        def on_change_cb(event, data):
            self.value = data.props
            self.callback(data.props)

        with mui.FormControl(fullWidth=True, sx={'m': 1}):
            with mui.FormControl(fullWidth=True, variant="outlined", size="big"):
                mui.InputLabel(self.label, id=self.id)
                with mui.Select(key=self.id, onChange=on_change_cb,
                                type="number",
                                labelId=self.id,
                                label=self.label,
                                disabled=self.disabled):
                    for value, option in enumerate(self.options):
                        mui.MenuItem(option, value=value)


ControlTypes = {
    'slider': SliderElement,
    'button': ButtonElement,
    'number': NumericInputElement,
    'switch': SwitchElement,
    'select': SelectElement,
}

# def select(container, key, callback, label, disabled=False, options=None):
#     def onChangeCB(event, data):
#         callback(data.props)

#     with elements(f'{key} element'):
#         st.session_state[key] = ""

#         # with container:
#         # mui.Typography(key)
#         with mui.FormControl(fullWidth=True, fullHeight=True, variant="outlined", size="big"):
#             mui.InputLabel(label, id=key)
#             with mui.Select(key=key, onChange=onChangeCB,
#                             type="number",
#                             labelId=key,
#                             label=label,
#                             disabled=disabled):
#                 for value, option in enumerate(options):
#                     mui.MenuItem(option, value=value)


if __name__ == "__main__":
    container = st.container()

    def generic_callback(*data):
        pass
        # print(f"received: {data}")
        # st.write(data)

    with elements(""):
        form = mui.FormControl(
            fullWidth=True, margin='normal', variant='outlined')
        with form:
            slider = SliderElement('slider1', 'slider in class',
                                   generic_callback)
            slider.config(min_value=0, max_value=100, step=5)
            slider.display()

            numeric_input = NumericInputElement(
                'input1', 'test input', generic_callback)
            numeric_input.config(min_value=0, max_value=100)
            numeric_input.display()

            switch = SwitchElement('switch1', 'closed loop?', generic_callback)
            switch.display()

            select_element = SelectElement(
                'select1', 'what mode?', generic_callback)
            select_element.config(
                options=['absolute', 'relative', 'speed'])
            select_element.display()

            def shift_press_cb():
                print('button pressed with shift-key!')
            button = ButtonElement('button1', 'send data', generic_callback)
            button.config(shift_key_callback=shift_press_cb)
            button.display()

    # slider_element(container, key="slider1", callback=generic_callback,  min_value=0, max_value=100, step=5,
    #                tooltip="Adjust the volume", disabled=False)

    # slider_element(container, key="slider2", callback=generic_callback, min_value=0,
    #                max_value=200, step=10, tooltip="Adjust the brightness", disabled=True)

    # button_element(container, key="button1",
    #                callback=generic_callback, disabled=True)

    # button_element(container, key="button2",
    #                callback=generic_callback, disabled=False)

    # switch_element(container, key="switch1", callback=generic_callback,
    #                label="Enable Feature", default_value=False, disabled=True)

    # switch_element(container, key="switch2", callback=generic_callback,  label="Toggle Mode",
    #                default_value=True, disabled=False)

    # select(container, 'select object', callback=generic_callback,  label='what option', disabled=False,  options=[
    #        'option 1', 'option 2', 'option 3'])
