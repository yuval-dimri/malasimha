
from streamlit_elements import elements, dashboard, mui


def editor_card():
    with elements("editor card"):
        with mui.Card(key='key_for_editor_card', sx={"display": "flex", "flexDirection": "column", "borderRadius": 1, "overflow": "hidden"}, elevation=1):
            mui.CardHeader(
                title=f'editor',
                subheader="what's inside?",
                # avatar=mui.Avatar("R", sx={"bgcolor": "red"}),
                action=mui.IconButton(mui.icon.MoreVert),
                sx={
                    'padding': 0,
                    'padding-left': '5px',
                }
            )

            with mui.CardContent(sx={"flex": 1, 'padding': '0'}):
                id = 'input_element_selector_id'
                input_element_options = [
                    'slider', 'button', 'textarea', 'select dropdown']

                def on_change_cb(event, data):
                    print(data.props)

                with mui.FormControl(fullWidth=True, sx={'m': 1}):
                    with mui.FormControl(fullWidth=True, variant="outlined", size="big"):
                        mui.InputLabel('Choose your element', id=id)
                        with mui.Select(key=id, onChange=on_change_cb,
                                        type="number",
                                        labelId=id,
                                        label='Choose your element',
                                        disabled=False):
                            for value, option in enumerate(input_element_options):
                                mui.MenuItem(option, value=value)

            # def cb():
            #     print('pressed')
            # with mui.CardActions(disableSpacing=True):
            #     with mui.FormControl(fullWidth=True):
            #         mui.Button(
            #             'publish',
            #             alignItems='center',
            #             key=f'p_config',
            #             onClick=self._publish_callback,
            #             variant="contained",
            #             padding='5px',
            #             # disabled=self.
            #         )
