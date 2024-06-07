from types import SimpleNamespace
from .dashboard_element import DashboardElement
import streamlit as st
from streamlit_elements import elements, dashboard, mui


class CardElement(DashboardElement):
    def _publish_callback(self):
        for input_element in self.session_input_elements.__dict__.values():
            self.return_data[input_element.data_name] = input_element.value

        print(f'{self.return_data=}')
        # input_element.value

    def __call__(self, box_config=DEFAULT_CONFIG):
        self.box_config = box_config
        with mui.Card(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 1, "overflow": "hidden"}, elevation=1):
            with self.title_bar():
                mui.Typography(f'{box_config.get("title")}')

                mui.CardHeader(
                    title=f'{box_config.get("title")}',
                    subheader=f'{box_config.get("subtitle")}',
                    # avatar=mui.Avatar("R", sx={"bgcolor": "red"}),
                    # action=mui.IconButton(mui.icon.MoreVert),
                    className=self._draggable_class,
                    sx={
                        'padding': 0,
                        'padding-left': '5px',
                    }
                )

            with mui.CardContent(sx={"flex": 1, 'padding': '0'}):
                input_elements = box_config.get('input_elements')

                if self._key not in st.session_state:
                    self.session_input_elements = SimpleNamespace()
                    for idx, input_element_config in enumerate(input_elements):
                        element_key = f'{self._key}_element_{idx}'

                        element_class = ControlTypes.get(
                            input_element_config.get('type'))

                        if element_class is not None:
                            input_element = element_class(input_element_config.get(
                                'label'), lambda *x: x)  # TODO: pass some callback
                        else:
                            mui.Typography(
                                f'could not find element class for {input_element_config.get("type")}')
                            continue

                        setattr(self.session_input_elements,
                                element_key, input_element)

                        input_element.data_name = input_element_config.get(
                            'data_name')

                        config_params = input_element_config.get('params')

                        if config_params is not None:
                            input_element.config(**config_params)

                    st.session_state[self._key] = self.session_input_elements
                else:
                    self.session_input_elements = st.session_state[self._key]

                for element_key, input_element in self.session_input_elements.__dict__.items():
                    input_element.display()
                    # mui.Typography("")

            def cb():
                print('pressed')
            with mui.CardActions(disableSpacing=True):
                with mui.FormControl(fullWidth=True):
                    mui.Button(
                        'publish',
                        alignItems='center',
                        key=f'publish button{self._key}',
                        onClick=self._publish_callback,
                        variant="contained",
                        padding='5px',
                        # disabled=self.
                    )
            # mui.IconButton(mui.icon.IosShare, fontSize='Large')
            # mui.IconButton(mui.icon.Share)
