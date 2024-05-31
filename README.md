# Robot Controller

Welcome to the Robot Controller repository! This project provides a versatile and powerful interface for controlling robots using Python and the Streamlit package. It supports multiple communication protocols, making it suitable for a variety of robotic applications.

## Features

- **Streamlit Interface**: A user-friendly web interface built with Streamlit for real-time robot control and monitoring.
- **Multi-Protocol Communication**: Support for MAVLink, ROS topics and services, JSON, and more.
- **Extensibility**: Easily add new features and protocols to extend the functionality.
- **Open Source**: Free to use, modify, and distribute.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Streamlit
- MAVLink
- ROS (Robot Operating System)
- Additional Python packages (specified in `requirements.txt`)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/robot-controller.git
    cd robot-controller
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:

    ```sh
    streamlit run app.py
    ```

### Usage

Once the Streamlit app is running, you can access the web interface in your browser. Use the controls to send commands to your robot and monitor its status. The communicator library handles the translation of these commands into the appropriate protocol.

### Communicator Library

The communicator library enables seamless communication with robots using different protocols. It abstracts the complexities of each protocol and provides a simple interface for sending and receiving data.

Supported protocols:
- **MAVLink**: For controlling drones and other MAVLink-compatible devices.
- **ROS**: For interacting with ROS-based robots via topics and services.
- **JSON**: For sending data in a lightweight and readable format.

### Example

Here is a simple example of how to use the communicator library:

```python
from communicator import Communicator

# Initialize the communicator with MAVLink protocol
comm = Communicator(protocol='mavlink')

# Send a command
comm.send_command('TAKEOFF', altitude=10)

# Receive data
data = comm.receive_data()
print(data)
