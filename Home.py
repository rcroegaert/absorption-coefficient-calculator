import streamlit as st

from src import utils

st.set_page_config(layout="wide")

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
st.markdown('----')

# Define the slider for the material thickness
d = st.number_input('1te Materialsdicke definieren [mm]:', step=1)

if st.button('Material hinzufügen') or st.session_state.load_state:
    st.session_state.load_state = True
    d2 = utils.create_input_field()
st.markdown('----')


# Calculate and Plot Section
st.subheader("Plot")
# Call the function with the selected variables and display the plot
fig = utils.absorption_coefficient(f_start, f_end, d).plot()
st.plotly_chart(fig)
st.subheader("Daten")
# Call the function with the selected variables and display the dataframe
df = utils.absorption_coefficient(f_start, f_end, d).data()
st.dataframe(df, height=210)


# Output Section
st.subheader("Herunterladen")
utils.create_df_export_button(
    df=df,
    title=f"Absorption Koffizient von einem {d} mm Material",
    ts=None,
)


# Run the app with:
# streamlit run Home.py --server.enableCORS=false