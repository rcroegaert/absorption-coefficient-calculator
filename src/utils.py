import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pendulum
import streamlit as st

# Define a class that works with three variavles and returns a plotly plot
class absorption_coefficient:
    """This class takes three variables as input and returns a matplotlib plot
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
        x = np.linspace(self.f_start, self.f_end, 10)
        alpha = 0.9 * np.log10(x*self.d) - 2.4
        alpha[alpha > 1] = 1
        alpha[alpha < 0] = 0
        df = pd.DataFrame({'Frequency': x, 'Absorption Coefficient': alpha})
        fig.add_trace(go.Scatter(x=x, y=alpha, mode='lines'))
        fig.update_layout(yaxis_range=[0, 1.1])
        fig.update_layout(title='Absorption coefficient of a {} mm material'.format(self.d),
                          xaxis_title='Frequency in [Hz]',
                          yaxis_title='Absorption Coefficient')
        return fig, df

@st.cache_data(show_spinner=False)
def _convert_df(df: pd.DataFrame):
    return df.to_csv().encode("utf-8")


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