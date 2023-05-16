import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


# Define a function that takes two variables as input and returns a matplotlib plot
def absorption_coefficient_plot(f_start:int, f_end:int, d:int):
    """This function takes three variables as input and returns a matplotlib plot
    """

    fig, ax = plt.subplots()
    x = np.linspace(f_start, f_end, 10)
    alpha = 0.9 * np.log10(x*d) - 2.4
    alpha[alpha > 1] = 1
    alpha[alpha < 0] = 0
    ax.plot(x, alpha)
    ax.set_xlabel('Frequency in [Hz]')
    ax.set_ylabel('Absorption Coefficient')
    ax.set_title('Absorption coefficient of a {} mm material'.format(d))
    return fig

# Define a class from the function above
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
        fig.add_trace(go.Scatter(x=x, y=alpha, mode='lines'))
        fig.update_layout(yaxis_range=[0, 1.1])
        fig.update_layout(title='Absorption coefficient of a {} mm material'.format(self.d),
                          xaxis_title='Frequency in [Hz]',
                          yaxis_title='Absorption Coefficient')
        return fig