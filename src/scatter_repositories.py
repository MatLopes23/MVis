import pandas as pd
import plotly.express as px

def generate_scatter_repositories(path, color_discrete_map, colors):
    df = pd.read_csv(path + '/Datasets/data_set_repositories.csv')
    fig = px.scatter(df, x="stars", y="commits",
                        size="files", color="language", hover_name="repository", 
                        size_max=55, color_discrete_map=color_discrete_map)
        

    fig.update_layout(transition_duration=500, margin={'l': 40, 'b': 40, 't': 10, 'r': 10})
    fig.update_layout(plot_bgcolor=colors['background'],
                              paper_bgcolor=colors['background'], 
                              font_color=colors['text'])
                              
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig