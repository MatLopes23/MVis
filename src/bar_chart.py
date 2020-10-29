import plotly.express as px
from pathlib import Path
import pandas as pd

def generate_bar_chart(path, color_discrete_map, colors):

    df_weekdays = pd.read_csv(path + '/Datasets/data_set_weekdays.csv')

    fig = px.bar(df_weekdays, x="weekday", y="total", color="language", color_discrete_map=color_discrete_map,
    animation_frame="year", animation_group="weekday", text="total", height=600, range_y=[0, 1900],
    labels={"total": "Commits", "weekday": "Dias", "year":"Ano"})

    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000

    fig.update_layout(plot_bgcolor=colors['background'],
                              paper_bgcolor=colors['background'], 
                              font_color=colors['text'])

    return fig