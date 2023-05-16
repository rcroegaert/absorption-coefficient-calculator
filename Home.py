import streamlit as st

from src import utils


# Set the title of the app
st.title('Absorption Coefficient Calculator')

# Input Section
# Define the dropdown menus for the variables
col1, col2 = st.columns(2)
f_start = col1.selectbox('Select start frequency [Hz]:', [0, 1, 10, 100])
f_end = col2.selectbox('Select end frequency [Hz]:', [100, 1000, 10000])
d = st.number_input('Select material thickness [mm]:', step=1)

# Calculate and Plot Section
st.subheader("Plot")
# Call the function with the selected variables and display the plot
fig = utils.absorption_coefficient(f_start, f_end, d).plot()
st.plotly_chart(fig)
st.subheader("Data")
# Call the function with the selected variables and display the dataframe
df = utils.absorption_coefficient(f_start, f_end, d).data()
st.dataframe(df)

# Output Section
st.subheader("Download")
utils.create_df_export_button(
    df=df,
    title=f"Absorption Coefficient of a {d} mm material",
    ts=None,
)


# Run the app with:
# streamlit run Home.py --server.enableCORS=false