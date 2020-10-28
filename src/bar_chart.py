import plotly.express as px
from pathlib import Path
import pandas as pd

path = str(Path(__file__).parents[1])

def generate_bar_chart():
    df_weekdays = pd.read_csv(path + '/Datasets/data_set_weekdays.csv')


    fig = px.bar(df_weekdays, x="weekday", y="total", color="language",
    animation_frame="year", animation_group="weekday", text="total")

    fig.update_traces(textposition='outside')
    #fig.show()
    return fig