import streamlit as st
import numpy as np
import pandas as pd

from src import utils, models_new, absorptioncoeff_new

st.set_page_config(
    page_title="Absorptionsgrad Rechner",
    layout="wide"
)
# --- Initialising SessionState ---
if "load_state" not in st.session_state:
    st.session_state.load_state = False

# Set the title and logo of the app
col1, col2 = st.columns(2)
col1.title('Absorptionsgrad Rechner')
col2.image('img/logo-tuberlin-header2.png', width=350)

################## Input Section ##################
# st.markdown('----')
# Dropdown for absorber model -> erstmal das auskommentieren
# model = st.selectbox('Absorbermodell wählen:', ['Poröser', 'Nicht definiert'])

# Define the dropdown menus for the frequency
st.header('Globale Parameter :globe_with_meridians:')
with st.expander('Werte ein/ausblenden...'):
    st.markdown('##### Frequenzbereich')
    col1, col2 = st.columns(2)
    f_min, f_max = col1.slider('Anfangs- und Endfrequenz [Hz]', 0, 10000, (0, 10000), step=100)
    f_range = np.arange(f_min, f_max, 1)

    col1, col2, col3 = st.columns(3)
    col1.markdown('##### Lufttemperatur')
    air_temp = col1.number_input('in [°C]', step=1, value=20)
    col2.markdown('##### Luftdruck')
    air_pressure = col2.number_input('in [Pa]', step=1, value=101325)
    col3.markdown('##### Einfallswinkel')
    theta = col3.number_input('in [°]', step=1, value=0)

st.markdown('----')

# Materialen Eingabe
st.header('Material Parameter :hammer:')
with st.expander('Werte ein/ausblenden...'):
    col1, col2, col3 = st.columns(3)
    num_materials = col1.number_input("Wähl die Anzahl an Materialen:", min_value=1, max_value=5, value=2, step=1)
    material_dict = {}

    # Create the specified number of columns for each material
    columns = st.columns(num_materials)
    # Display variables in each column and save them
    for i, column in enumerate(columns):
        column.markdown(f"##### Material # {i + 1}")
        key = f"Material {i + 1}"
        value1 = column.number_input(f"Dicke [mm]", key=f"value1_{i}", format='%0f')
        value2 = column.selectbox(f"Modell", options=['Bitte wählen Sie', 'Poröser', 'Lochplatte', 'Luft'],
                                  key=f"value2_{i}")
        # value3 = column.selectbox(f"Luftschicht?", options=['Bitte wählen Sie', 'Ja', 'Nein'], key=f"value3_{i}")
        # if value3 == 'Ja':
        # value3 = column.number_input(f"Dicke der Luftschicht [mm]", key=f"value3_{i}", format='%0f')
        # else:
        #     value4 = 0
        if value2 == 'Luft':
            material_dict[key] = [value1, value2, 0, 0, 0]
        else:
            value3 = column.number_input(f"Strömungswiderstand [Ns/m^4]", key=f"value3_{i}", format='%e')
            # value4 = column.number_input(f"viscosity", key=f"value4_{i}", format='%0f')
            # value5 = column.number_input(f"Thermische", key=f"value5_{i}", format='%0f', value=value4*2)
            material_dict[key] = [value1, value2, value3]

    if st.button("OK"):
        st.write("Eingabe gespeichert!")
        st.write('  ' * 10000)
        st.write("Material parameter überprüfen:")
        for key, value in material_dict.items():
            st.write(f"{key}: {value}")

st.markdown('----')

# Variablen definieren TODO: Weg damit später
air_density = (air_pressure) / (287.058 * (air_temp + 273.15))
air_speed = 331.3 * np.sqrt(1 + (air_temp / 273.15))
sigma = material_dict["Material 1"][2]
L1 = material_dict["Material 1"][0] / 1000
viscosity = 17.240165625*10**(-6) * (273.15+air_temp/273.15)**(3/2) / (273.15+110.4/273.15+air_temp+110.4)

phi = 0.98
alpha_inf = 1.01
gamma = 1.4
P0 = 101325  # Pa
viscosity_L = 85 * 10 ** (-6)
therm_L = viscosity_L * 2
Pr = 0.71
# viscosity = 1.839 * 10 ** (-5)
#impedance = air_density * air_c
#Z2 = impedance
#Z0 = impedance

L2 = material_dict["Material 2"][0] / 1000

# ################## Berechnung ##################

# por_abs = models.Porous_Absorber(f_range[0], air_density, phi, alpha_inf, sigma,
#                                  gamma, P0, viscosity_L, therm_L, Pr, viscosity)
# alphas = absorptioncoeff_new.AbsorptionCoeff(theta, L1, L2, f_min, f_max, [por_abs],
#                                          air_density, air_c).abs_coeff()

alphas = np.array([])
st.write(f_range[0], air_density, air_speed, sigma, L1, viscosity, theta)
for f in f_range:
    # Porous
    # T1 = models_new.Porous_Absorber(f, air_density, air_speed, sigma, L1, viscosity, theta).get_Tp()

    # Perforated
    T1 = models_new.PerforatedPlate_Absorber(f, air_density, air_speed, sigma, L2, viscosity, theta,
                                              d_hole=0.02, a=0.02).get_Tp()

    T2 = np.array([[1, 0],
                   [0, 1]])
    T = [T1, T2]
    # alphas.append(absorptioncoeff_new.AbsorptionCoeff(T, theta).abs_coeff())
    alphas = np.append(alphas, absorptioncoeff_new.AbsorptionCoeff(T, theta).abs_coeff())

################## Output Section ##################
# Plotting
st.header('Plot :bar_chart:')
titlestr = ('Absorptionsgrad eines {} mm Material'.format(
    material_dict["Material 1"][0]) + ' bei {} mm Luftspalt'.format(material_dict["Material 2"][0]))
fig1 = utils.plotly_go_line(x=f_range,
                            y=alphas,
                            x_label='Frequenz in [Hz]',
                            y_label='Absorptionsgrad',
                            title=titlestr)
fig1

# DF anzeigen
col1, col2 = st.columns(2)
col1.subheader('Daten :books:')
df = pd.DataFrame({'Frequenz [Hz]': f_range, 'Absorptionsgrad [1]': alphas})
st.dataframe(df, height=210)
col2.subheader('Herunterladen :arrow_heading_down:')
with col2:
    export = utils.create_df_export_button(
        df=df,
        title=f"Absorptionsgrad Berechnung",
        ts=None,
    )
