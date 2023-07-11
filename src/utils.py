import pandas as pd
import plotly.graph_objects as go
import pendulum
import streamlit as st


@st.cache_data(show_spinner=False)
def _convert_df(df: pd.DataFrame):
    """Converts a dataframe to a CSV file.

    Args:
        df (pd.DataFrame): Dataframe to convert

    Returns:
        bytes: CSV file
    """
    return df.to_csv().encode("utf-8")


# Define a function that creates a download button for a dataframe
def create_df_export_button(
        df: pd.DataFrame,
        title: str,
        ts: pendulum.DateTime | None,
) -> bool:
    """Creates a Streamlit button to export a dataframe to a CSV file.

    Args:
        df (pd.DataFrame): Dataframe to export
        title (str): Title of the file being exported
        ts (pendulum.DateTime): Optional datetime that will be used for file name

    Returns:
        bool: Streamlit button functioning a boolean type
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


def plotly_go_line(x, y, x_label, y_label, title):
    """Creates a plotly-go line plot.

    Args:
        x (list): List of x values
        y (list): List of y values
        x_label (str): Label for x axis
        y_label (str): Label for y axis
        title (str): Title of the plot

    Returns:
        plotly.graph_objects.Figure: Plotly line plot
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines'))
    fig.update_xaxes(showgrid=True, type="log")
    fig.update_layout(title=title,
                      xaxis_title=x_label,
                      yaxis_title=y_label,
                      yaxis_range=[0, 1],
                      width=1000,
                      height=500)
    return fig
