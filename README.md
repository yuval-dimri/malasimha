# Malasimha

Welcome to the Malasimha repository! "Malasimha" is Hebrew for "what to put inside," reflecting the drag-and-drop interface for building custom robotic control solutions. This project provides a versatile and powerful interface for controlling robots using Python and the Streamlit package. It supports multiple communication protocols, making it suitable for a variety of robotic applications.


## Features

- **Streamlit Interface**: A user-friendly web interface built with Streamlit for real-time robot control and monitoring.
- **Multi-Protocol Communication**: Support for MAVLink, ROS topics and services, JSON, and more.
- **Extensibility**: Easily add new features and protocols to extend the functionality.
- **Open Source**: Free to use, modify, and distribute.

## Getting Started

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yuval-dimri/malasimha.git
    cd malasimha
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:

    ```sh
    streamlit run main.py
    ```

### Usage

Once the Streamlit app is running, you can access the web interface in your browser. Use the controls to send commands to your robot and monitor its status. The communicator library handles the translation of these commands into the appropriate protocol.

### Communicator Library

The communicator library enables seamless communication with robots using different protocols. It abstracts the complexities of each protocol and provides a simple interface for sending and receiving data.

Supported protocols:
- **MAVLink**: For controlling drones and other MAVLink-compatible devices.
- **ROS**: For interacting with ROS-based robots via topics and services.
- **JSON**: For sending data in a lightweight and readable format.

