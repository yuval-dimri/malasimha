# controls.py

from dashboard import Dashboard
from streamlit_elements import mui
from uuid import uuid4


class Slider(Dashboard.Item):

    def __init__(self, board, x, y, w, h, _key=None, **item_props):
        super().__init__(board, x, y, w, h, _key=_key, **item_props)
        self._min_val = item_props.get('min_val', 0)
        self._max_val = item_props.get('max_val', 100)
        self._step = item_props.get('step', 1)
        self._default_val = item_props.get('default_val', 50)

    def __call__(self):
        with self.title_bar():
            mui.Slider(
                min=self._min_val,
                max=self._max_val,
                step=self._step,
                defaultValue=self._default_val,
                sx={"width": "100%"}
            )

    @staticmethod
    def default_config():
        return {
            "type": "Slider",
            "w": 4,
            "h": 2,
            "_key": str(uuid4()),
            "label": "New Slider",
            "min_val": 0,
            "max_val": 100,
            "step": 1,
            "default_val": 50
        }


class Button(Dashboard.Item):

    def __init__(self, board, x, y, w, h, _key=None, **item_props):
        super().__init__(board, x, y, w, h, _key=_key, **item_props)
        self._text = item_props.get('text', 'Click Me')
        self._on_click = item_props.get('on_click', None)

    def __call__(self):
        with self.title_bar():
            mui.Button(self._text, onClick=self._on_click,
                       sx={"width": "100%"})

    @staticmethod
    def default_config():
        return {
            "type": "Button",
            "w": 4,
            "h": 2,
            "_key": str(uuid4()),
            "label": "New Button",
            "text": "Click Me",
            "on_click": None
        }


class Dropdown(Dashboard.Item):

    def __init__(self, board, x, y, w, h, _key=None, **item_props):
        super().__init__(board, x, y, w, h, _key=_key, **item_props)
        self._options = item_props.get('options', [
            {"value": "option1", "label": "Option 1"},
            {"value": "option2", "label": "Option 2"}
        ])
        self._default_value = item_props.get('default_value', "option1")

    def __call__(self):
        with self.title_bar():
            mui.Select(
                defaultValue=self._default_value,
                options=self._options,
                sx={"width": "100%"}
            )

    @staticmethod
    def default_config():
        return {
            "type": "Dropdown",
            "w": 4,
            "h": 2,
            "_key": str(uuid4()),
            "label": "New Dropdown",
            "options": [
                {"value": "option1", "label": "Option 1"},
                {"value": "option2", "label": "Option 2"}
            ],
            "default_value": "option1"
        }


class Checkbox(Dashboard.Item):

    def __init__(self, board, x, y, w, h, _key=None, **item_props):
        super().__init__(board, x, y, w, h, _key=_key, **item_props)
        self._default_checked = item_props.get('default_checked', False)

    def __call__(self):
        with self.title_bar():
            mui.Checkbox(
                defaultChecked=self._default_checked,
                sx={"width": "100%"}
            )

    @staticmethod
    def default_config():
        return {
            "type": "Checkbox",
            "w": 4,
            "h": 2,
            "_key": str(uuid4()),
            "label": "New Checkbox",
            "default_checked": False
        }


class TextInput(Dashboard.Item):

    def __init__(self, board, x, y, w, h, _key=None, **item_props):
        super().__init__(board, x, y, w, h, _key=_key, **item_props)
        self._default_value = item_props.get('default_value', '')

    def __call__(self):
        with self.title_bar():
            mui.TextField(
                defaultValue=self._default_value,
                sx={"width": "100%"}
            )

    @staticmethod
    def default_config():
        return {
            "type": "TextInput",
            "w": 4,
            "h": 2,
            "_key": str(uuid4()),
            "label": "New Text Input",
            "default_value": ""
        }
