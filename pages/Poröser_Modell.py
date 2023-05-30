import streamlit as st
import numpy as np

from src import utils

st.set_page_config(
    page_title="Poröser Modell",
    layout="wide"
)
# --- Initialising SessionState ---
if "load_state" not in st.session_state:
    st.session_state.load_state = False

col1, col2 = st.columns(2)
# Set the logo of the app
col2.image('img/logo-tuberlin-header2.png', width=350)

# Set the title of the app
st.title('Absorptionsgrad Rechner')

# Input Section
st.markdown('----')
# Dropdown for absorber model
model = st.selectbox('Absorbermodell wählen:', ['Poröser', 'Nicht definiert'])

# Define the dropdown menus for the frequency
col1, col2 = st.columns(2)
f_start = col1.selectbox('Anfangsfrequenz wählen [Hz]:', [0, 1, 10, 100])
f_end = col2.selectbox('Endfrequenz wählen [Hz]:', [100, 1000, 10000])
f_range = np.arange(f_start, f_end, 1)
st.markdown('----')

# Define the slider for the material thickness
d = st.number_input('1. Materialsdicke definieren [mm]:', step=1)


with st.form(key="Materialdaten Eingabe"):

    # Define the slider for the material density
    st.title("Dynamic Number Input")

    number_dict = {}
    next_key = 1

    utils.add_number_input(number_dict, next_key)

    if st.form_submit_button("Add Number Input"):
        next_key += 1
        utils.add_number_input(number_dict, next_key)

    st.write("Number Inputs:")
    for key, value in number_dict.items():
        st.write(f"{key}: {value}")
    


    st.write('Hi')
    st.form_submit_button("Eingabe fertig")