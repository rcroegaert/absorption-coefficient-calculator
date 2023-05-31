import streamlit as st
import numpy as np
import plotly.graph_objects as go

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


col1, col2 = st.columns(2)
col1.header("Materialen")

num_materials = col1.selectbox("Wähl die Anzahl an Materialen:", range(1, 6), 1)

col2.header("Materialdicke eingeben")
with col2.container():
    material_dict = {}
    for i in range(num_materials):
        key = f"Material {i+1}"
        value = st.number_input(f"{key} Dicke")
        material_dict[key] = value

    if st.button("OK"):
        st.write("Eingabe gespeichert!")
        # st.write("Material Thickness:")
        # for key, value in material_dict.items():
        #     st.write(f"{key}: {value}")

col2.write(material_dict)


st.header("Wichtige Parameter")
luft_c = 344
st.write('luft_c =', luft_c)
luft_dichte = 1.213
st.write('luft_dichte =', luft_dichte)

dichte = 1.213
st.write('Dichte =', dichte)
phi = 0.98
st.write('phi =', phi)
alpha_unend = 1.01
st.write('alpha_unend =', alpha_unend)
sigma = 20600
st.write('sigma =', sigma)
gamma = 1.4
st.write('gamma =', gamma)
P0 = 101325 # Pa
st.write('P0 =', P0)
viskosität_L = 85*10**(-6)
st.write('viskosität_L =', viskosität_L)
thermisch_L = viskosität_L*2
st.write('thermisch_L =', thermisch_L)
Pr = 0.71
st.write('Pr =', Pr)
viskosität = 1.839*10**(-5)
st.write('viskosität =', viskosität)

impedanz = luft_dichte * luft_c
Z2 = impedanz
Z0 = impedanz
st.write('Impedanz =', impedanz)

L1 = material_dict["Material 1"] / 1000
L2 = material_dict["Material 2"] / 1000

alphas = np.array([])

for f in f_range:
    Z1, k1 = utils.JAC(f, dichte, phi, alpha_unend, sigma, gamma, P0, viskosität_L, thermisch_L, Pr, viskosität)
    k2 = 2 * np.pi * f / luft_c

    # T1, T2, T3 definieren
    T1 = np.array([[np.cos(k1*L1), 1j*Z1*np.sin(k1*L1)],
                   [(1j/Z1)*np.sin(k1*L1), np.cos(k1*L1)]])

    T2 = np.array([[np.cos(k2*L2), 1j*Z2*np.sin(k2*L2)],
                   [(1j/Z2)*np.sin(k2*L2), np.cos(k2*L2)]])

    # Rigid Backed
    T3 = np.array([[1, 0],  
                   [0, 1]])

    # T_total berechnen
    T_total = np.dot(T1, T2)

    # Absorptionsgrad berechnen
    R = (T_total[0, 0] - T_total[1, 0]*Z0) / (T_total[0, 0] + T_total[1, 0]*Z0) # Reflexionskoeffizient
    alpha = 1 - np.abs(R) ** 2
    alphas = np.append(alphas, alpha)

# Ersetzen der Werte durch 0
alphas[(alphas > -0.000001) & (alphas < 0)] = 0
alphas[(alphas < 0.000001) & (alphas > 0)] = 0

titlestr = ('Absorptionsgrad eines {} mm Material'.format(material_dict["Material 1"]) + ' bei {} mm Luftspalt'.format(material_dict["Material 2"]))
fig = go.Figure()
fig.add_trace(go.Scatter(x=f_range, y=alphas, mode='lines'))
fig.update_layout(yaxis_range=[0, 1.1])
fig.update_xaxes(showgrid=True)
fig.update_layout(title=titlestr,
                    xaxis_title='Frequenz in [Hz]',
                    yaxis_title='Absorptionsgrad')
fig
