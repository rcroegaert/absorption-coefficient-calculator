import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from src import utils, models

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
# Dropdown for absorber model -> erstmal das auskommentieren
# model = st.selectbox('Absorbermodell wählen:', ['Poröser', 'Nicht definiert'])

# Define the dropdown menus for the frequency
st.header('Globale Parameter :globe_with_meridians:')
with st.expander('Werte ein/ausblenden...'):
    st.markdown('##### Frequenzbereich')
    col1, col2 = st.columns(2)
    f_start, f_end = col1.slider('Anfangs- und Endfrequenz [Hz]', 0, 10000, (0, 10000), step=100)
    f_range = np.arange(f_start, f_end, 1)

    col1, col2, col3 = st.columns(3)
    col1.markdown('##### Lufttemperatur')
    luft_temp = col1.number_input('in [°C]', step=1, value=20)
    col2.markdown('##### Luftdruck')
    luft_druck = col2.number_input('in [Pa]', step=1, value=101325)
    col3.markdown('##### Einfallswinkel')
    winkel = col3.number_input('in [°]', step=1, value=0)

st.markdown('----')

# Materialen Eingabe
st.header('Material Parameter :hammer:')
with st.expander('Werte ein/ausblenden...'):
    col1, col2, col3 = st.columns(3)
    # num_materials = col1.selectbox("Wähl die Anzahl an Materialen:", range(1, 6))
    num_materials = col1.number_input("Wähl die Anzahl an Materialen:", min_value=1, max_value=5, value=1, step=1)
    material_dict = {}


    # Create the specified number of columns for each material
    columns = st.columns(num_materials)
    # Display variables in each column and save them
    for i, column in enumerate(columns):
        column.markdown(f"##### Material # {i+1}")
        key = f"Material {i + 1}"
        value1 = column.number_input(f"Dicke [mm]", key=f"value1_{i}", format='%0f')
        value2 = column.selectbox(f"Modell", options=['Bitte wählen Sie', 'Poröser', 'Lochplatte'], key=f"value2_{i}")
        value3 = column.selectbox(f"Luftschicht?", options=['Bitte wählen Sie', 'Ja', 'Nein'], key=f"value3_{i}")
        if value3 == 'Ja':
            value4 = column.number_input(f"Dicke der Luftschicht [mm]", key=f"value4_{i}", format='%0f')
        else:
            value4 = 0
        value5 = column.number_input(f"Strömungswiderstand [Ns/m^4]", key=f"value5_{i}", format='%e')
        # value4 = column.number_input(f"alpha_unendlich {i+1}", key=f"value_{i}", format='%0f')
        value6 = column.number_input(f"Viskosität", key=f"value6_{i}", format='%0f')
        value7 = column.number_input(f"Thermische", key=f"value7_{i}", format='%0f', value=value6*2)
        material_dict[key] = [value1, value2, value4, value5, value6, value7]

    if st.button("OK"):
        st.write("Eingabe gespeichert!")
        st.write('  ' * 10000)
        st.write("Material parameter überprüfen:")
        for key, value in material_dict.items():
            st.write(f"{key}: {value}")

st.markdown('----')


luft_c = 344
# st.write('luft_c =', luft_c)
luft_dichte = 1.213
# st.write('luft_dichte =', luft_dichte)
dichte = 1.213
# st.write('Dichte =', dichte)
phi = 0.98
# st.write('phi =', phi)
alpha_unend = 1.01
# st.write('alpha_unend =', alpha_unend)
sigma = 20600
# st.write('sigma =', sigma)
gamma = 1.4
# st.write('gamma =', gamma)
P0 = 101325 # Pa
# st.write('P0 =', P0)
viskosität_L = 85*10**(-6)
# st.write('viskosität_L =', viskosität_L)
thermisch_L = viskosität_L*2
# st.write('thermisch_L =', thermisch_L)
Pr = 0.71
# st.write('Pr =', Pr)
viskosität = 1.839*10**(-5)
# st.write('viskosität =', viskosität)

impedanz = luft_dichte * luft_c
Z2 = impedanz
Z0 = impedanz
# st.write('Impedanz =', impedanz)

L1 = material_dict["Material 1"][0] / 1000
L2 = material_dict["Material 1"][4] / 1000

alphas = np.array([])

for f in f_range:
    # Berechnung der Impedanz und Wellenzahl mit Poröser Modell
    Z1, k1 = models.JAC(f, dichte, phi, alpha_unend, sigma, gamma, P0, viskosität_L, thermisch_L, Pr, viskosität)
    k2 = 2 * np.pi * f / luft_c

    # Berechnung der TMM-Matrix
    T_total = utils.tmm(k1,L1,Z1,k2,L2,Z2)

    # Absorptionsgrad berechnen -> gehört das in tmm-fkt?
    R = (T_total[0, 0] - T_total[1, 0]*Z0) / (T_total[0, 0] + T_total[1, 0]*Z0) # Reflexionskoeffizient
    alpha = 1 - np.abs(R) ** 2
    alphas = np.append(alphas, alpha)

# Plotting
st.header('Plot :bar_chart:')
titlestr = ('Absorptionsgrad eines {} mm Material'.format(material_dict["Material 1"][0]) + ' bei {} mm Luftspalt'.format(material_dict["Material 1"][2]))
fig1 = utils.plotly_go_line(x=f_range,
                     y=alphas,
                     x_label='Frequenz in [Hz]',
                     y_label='Absorptionsgrad',
                     title=titlestr)
fig1


# DF anzeigen
col1,col2 = st.columns(2)
col1.subheader('Daten :books:')
df = pd.DataFrame({'Frequenz': f_range, 'Absorptionsgrad': alphas})
st.dataframe(df, height=210)
col2.subheader('Herunterladen :arrow_heading_down:')
with col2:
    export = utils.create_df_export_button(
        df=df,
        title=f"Absorptionsgrad Berechnung",
        ts=None,
    )