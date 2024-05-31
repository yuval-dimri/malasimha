import streamlit as st
from streamlit_elements import elements, mui, html
from communicator.json_communicator import JSONCommunicator

# Create an instance of JSONCommunicator
json_communicator = JSONCommunicator("parameters.json")
margins_css = """
    <style>
        .main > div {
            padding-left: 0rem;
            padding-right: 0rem;
        }
    </style>
"""

st.markdown(margins_css, unsafe_allow_html=True)
# Define a function to update parameters based on user input
def update_parameters():
    with st.sidebar:
        st.subheader("Edit Parameters:")

        # Search box to filter parameters
        search_query = st.text_input("Search Parameter:")

        # Filter parameters based on search query
        if search_query:
            filtered_params = {key: value for key, value in json_communicator.params.items() if search_query.lower() in key.lower()}
        else:
            filtered_params = json_communicator.params

        # Debugging information
        st.write("Filtered Parameters:", filtered_params)

        # Display text inputs for filtered parameters
        for key, value in filtered_params.items():
            new_value = st.text_input(f"{key}:", value=str(json_communicator.get_param(key)))
            if new_value != str(json_communicator.get_param(key)):
                json_communicator.set_param(key, new_value)
                st.success(f"Updated parameter '{key}' to '{new_value}'")

# Define a generic function to create a box with a heading, three text inputs, and a slider
def create_generic_box(index, column):
    with column:
            with st.container():
                st.subheader(f"Box {index}")
                cols = st.columns(3)
                cols[0].text_input(f"Box {index} - Text 1")
                cols[1].text_input(f"Box {index} - Text 2")
                cols[2].text_input(f"Box {index} - Text 3")
                st.slider(f"Box {index} - Slider", min_value=0, max_value=100)

# Main Streamlit app
def main():
    st.title("JSON Parameters Editor")

    st.write("Welcome to the JSON Parameters Editor. You can use this interface to edit parameters dynamically.")

    # Update parameters based on user input
    update_parameters()

    st.write("## Dynamic Boxes")

    # Number of columns to arrange the boxes
    num_columns = 3
    columns = st.columns(num_columns)

    # Number of boxes to create
    num_boxes = st.number_input("Number of Boxes:", min_value=1, max_value=10, value=3)

    # Create the specified number of boxes, distributing them across the columns
    for i in range(1, num_boxes + 1):
        create_generic_box(i, columns[(i - 1) % num_columns])

if __name__ == "__main__":
    main()
