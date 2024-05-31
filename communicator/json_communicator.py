import json
import threading
import time
import os


class JSONCommunicator:
    def __init__(self, filename):
        self.filename = filename
        self.params = {}
        self.callbacks = {}
        self.file_last_modified = os.path.getmtime(
            filename)  # Get initial modification time

        # Load parameters from JSON file
        self.load_params()

        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_file)
        self.monitor_thread.daemon = True  # Daemonize the thread
        self.monitor_thread.start()

    def load_params(self):
        changed_params = {}
        try:
            with open(self.filename, 'r') as file:
                loaded_params = json.load(file)
                if isinstance(loaded_params, dict):
                    for key, value in loaded_params.items():
                        if key not in self.params or self.params[key] != value:
                            changed_params[key] = value
                    self.params = loaded_params
        except (FileNotFoundError, json.JSONDecodeError):
            # Create the file or set empty dictionary if it doesn't exist or JSON is invalid
            # self.save_params({})
            print("fix json file")
        return changed_params

    def save_params(self, params):
        with open(self.filename, 'w') as file:
            json.dump(params, file, indent=4)

    def set_param(self, key, value):
        if key in self.params:
            if self.params[key] != value:
                self.params[key] = value
                self.trigger_event(key, value)
                # Save parameters only when they are modified
                self.save_params(self.params)
        else:
            self.params[key] = value
            self.trigger_event(key, value)
            # Save parameters only when they are modified
            self.save_params(self.params)

    def get_param(self, key):
        return self.params.get(key, None)

    def register_callback(self, key, callback):
        if key in self.callbacks:
            self.callbacks[key].append(callback)
        else:
            self.callbacks[key] = [callback]

    def trigger_event(self, key, value):
        if key in self.callbacks:
            for callback in self.callbacks[key]:
                threading.Thread(target=callback, args=(key, value)).start()

    def monitor_file(self):
        while True:
            try:
                modified_time = os.path.getmtime(self.filename)
                if modified_time != self.file_last_modified:
                    self.file_last_modified = modified_time
                    changed_params = self.load_params()  # Reload params if file is modified
                    self.handle_param_changes(changed_params)
            except FileNotFoundError:
                pass  # File may be deleted or moved
            time.sleep(0.05)  # Check for modifications every second

    def handle_param_changes(self, changed_params):
        for key, value in changed_params.items():
            if key in self.callbacks:
                self.trigger_event(key, value)

# Example usage:


def callback_function1(key, value):
    print(f"Parameter '{key}' changed to {value}")


def callback_function2(key, value):
    print(f"Another callback: Parameter '{key}' changed to {value}")


json_communicator = JSONCommunicator("parameters.json")

# Registering callback functions for specific parameters
json_communicator.register_callback("param1", callback_function1)
json_communicator.register_callback("param2", callback_function2)
