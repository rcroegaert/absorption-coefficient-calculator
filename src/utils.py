import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pendulum
import streamlit as st

# Define a class that works with three variables and returns a dataframe and a plot
class absorption_coefficient:
    """This class takes three variables as input and returns a plotly plot and a dataframe.
    """

    def __init__(
            self,
            f_start:int, 
            f_end:int, 
            d:int):
        self.f_start = f_start
        self.f_end = f_end
        self.d = d

    def plot(self):
        fig = go.Figure()
        x = np.arange(self.f_start, self.f_end + 10, 10)
        alpha = 0.9 * np.log10(x*self.d) - 2.4
        alpha[alpha > 1] = 1
        alpha[alpha < 0] = 0
        global df
        df = pd.DataFrame({'Frequency': x, 'Absorption Coefficient': alpha})
        fig.add_trace(go.Scatter(x=x, y=alpha, mode='lines'))
        fig.update_layout(yaxis_range=[0, 1.1])
        fig.update_xaxes(showgrid=True)
        fig.update_layout(title='Absorption coefficient of a {} mm material'.format(self.d),
                          xaxis_title='Frequency in [Hz]',
                          yaxis_title='Absorption Coefficient')
        return fig
    
    def data(self):
        return df


# Define a function that converts a dataframe to a CSV file
@st.cache_data(show_spinner=False)
def _convert_df(df: pd.DataFrame):
    return df.to_csv().encode("utf-8")

# Define a function that creates a download button for a dataframe
def create_df_export_button(
    df: pd.DataFrame,
    title: str,
    ts: pendulum.DateTime | None,
) -> bool:
    """Creates a Streamlit button to export a dataframe to a CSV file.

    Args:
        df (pd.DataFrame): Dataframe to export.
        title (str): Title of the data.
        ts (pendulum.DateTime): Optional datetime that will be used for file name.

    Returns:
        bool: Streamlit button functioning a boolean type.
    """

    if ts is None:
        ts = pendulum.now()

    ts_formatted = ts.to_datetime_string().translate(
        str.maketrans(
            {
                "/": "-",
                ":": "-",
            }
        )
    )

    file_name = f"{title}_{ts_formatted}.csv".replace(" ", "_").lower()

    return st.download_button(
        label="Export",
        data=_convert_df(df=df),
        file_name=file_name,
        mime="text/csv",
    )

# Define a function that creates an input field for a number
def create_input_field():
    """Creates a Streamlit input field to enter a number.

    Returns:
        int: Streamlit input field returning an integer.
    """
    return st.number_input(
        label="Select material Nr. 2 thickness [mm]:",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
    )

# JAC Modell
def JAC(f: float,
        dichte: float,
        phi: float, 
        alpha_unend: float,
        sigma: float,
        gamma: float,
        P0: float,
        viskosität_L: float,
        thermisch_L: float,
        Pr: float,
        viskosität: float
        ) -> float:

    K0 = gamma * P0
    omega = 2*pi*f
    G1 = sigma * phi / (alpha_unend * dichte * omega)

    G2 = 4*((alpha_unend)**2) * dichte * viskosität * omega / ((sigma*phi*viskosität_L)**2)

    G1_dot = 8*viskosität / (dichte * Pr * ((thermisch_L)**2) * omega)

    G2_dot = dichte * Pr * ((thermisch_L)**2) * omega / (16*viskosität)

    dichte_p = dichte * alpha_unend * (1- 1j*G1*sqrt(1+1j*G2)) / phi

    K_p = K0*phi**(-1) / (gamma - (gamma-1)*((1- 1j*G1_dot*sqrt(1+ 1j*G2_dot))**-1))

    kp = omega * sqrt(dichte_p/K_p)
    Zp = sqrt(dichte_p*K_p)

    return Zp, kp


def add_number_input(number_dict, next_key):
    new_value = st.number_input(f"Value {next_key}")
    number_dict[next_key] = new_value