from pathlib import Path
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import violin_plot
import utils
import word_cloud
import bar_chart
import scatter_repositories
import base64

path = str(Path(__file__).parents[1])

app = dash.Dash(__name__, title='MVis')
server = app.server

color_discrete_map = {'C#': 'rgb(148, 140, 249)',
                      'C++': 'rgb(243, 130, 110)',
                      'Java': 'rgb(110, 218, 180)',
                      'JavaScript': 'rgb(194, 143, 250)',
                      'Python': 'rgb(255, 187, 136)'}

colors = {
    'background': 'rgba(0,0,0,0)',
    'text': '#FFFFFF',
    'grid': '#C4C4C4'
}

df = pd.read_csv(path + '/Datasets/data_set_repositories.csv')
df_complex_methods = pd.read_csv(path + '/Datasets/data_set_top_complex_methods.csv')
df_random_methods = pd.read_csv(path + '/Datasets/data_set_random_methods.csv')
df_history_complex = pd.read_csv(path + '/Datasets/data_set_complexity_history_all_languages_top_complex.csv')

violin_plot = violin_plot.generate_violin_plot(df_complex_methods, df_random_methods, colors)
bar_chart = bar_chart.generate_bar_chart(path, color_discrete_map, colors)
scatter_repositories = scatter_repositories.generate_scatter_repositories(path, color_discrete_map, colors)

available_languages = df_complex_methods['language'].unique()



app.layout = html.Div(children=[
    html.H2(children='Métodos Complexos'),

    html.H3(children='Quais são os projetos analisados?'),

    dcc.Graph(figure=scatter_repositories),
    html.Br(),
    html.H3(children='Como é a complexidade dos métodos?'),

    dcc.Graph(figure=violin_plot),

    html.Br(),
    html.H3(children='Como estes métodos evoluem?'),
    html.Div([

        html.Div([
            html.Div([
                'Cyclomatic Complexity:',
                dcc.RadioItems(
                    id='crossfilter-xaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'},
                ),
            ], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                'Nloc:',
                dcc.RadioItems(
                    id='crossfilter-yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'width': '49%', 'display': 'inline-block'})
            
        ],
        style={'width': '35%', 'display': 'inline-block'}),

    ]),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': ''}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),
    
    html.H3(children='Week'),
    html.Br(),
    dcc.Graph(figure=bar_chart),

    html.Br(),
    html.H3(children='Word Cloud'),
    html.Div([
        dcc.Dropdown(
            id='language-dropdown-wordcloud',
            options=[
                {'label': 'C#', 'value': 'C#'},
                {'label': 'C++', 'value': 'C++'},
                {'label': 'Java', 'value': 'Java'},
                {'label': 'JavaScript', 'value': 'JavaScript'},
                {'label': 'Python', 'value': 'Python'}
            ],
            value=['C#', 'C++', 'Java', 'JavaScript', 'Python'],
            multi=True
        ),
    ], style={'width': '35%', 'display': 'inline-block'}),

    html.Br(),
    html.Img(id='graph-wordcloud', style={'height':'40%', 'width':'40%'}),

])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_complex_methods( xaxis_type, yaxis_type):

    fig = px.scatter(df_complex_methods, x='cyclomatic_complexity', y='nloc',
            hover_name='method', color='language', color_discrete_map=color_discrete_map)

    fig.update_traces(customdata=df_complex_methods['project']+df_complex_methods['path']+df_complex_methods['method'])

    fig.update_xaxes(title='Cyclomatic Complexity', type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title='Nloc', type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest', transition_duration=500,
                      legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

    fig.update_layout(plot_bgcolor=colors['background'],
                              paper_bgcolor=colors['background'], 
                              font_color=colors['text'])
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig


def create_time_series(dff, axis_type, title, data_type):

    x_axis = range(len(dff), 0,-1)
    
    if(len(x_axis) > 0):
        fig = px.scatter(dff, y=data_type, x=x_axis , labels=dict(cyclomatic_complexity='Cyclomatic Complexity', nloc='Nloc') )
    else:
        fig = px.scatter(dff, y=data_type, labels=dict(cyclomatic_complexity='Cyclomatic Complexity', nloc='Nloc'))
        
    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False, title_text='Commits')

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text= utils.get_only_name_method(title))

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    fig.update_layout(plot_bgcolor=colors['background'],
                              paper_bgcolor=colors['background'], 
                              font_color=colors['text'])
    
    fig.update_yaxes(showgrid=False)

    return fig
    
@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_complexity(hoverData, axis_type):
    key = hoverData['points'][0]['customdata']
    dff = df_history_complex[df_history_complex['project']+df_history_complex['path']+df_history_complex['method'] == key]

    title = '<b>{}</b><br>'.format(key)
    return create_time_series(dff, axis_type, title, 'cyclomatic_complexity')


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_nloc(hoverData, axis_type):
    key = hoverData['points'][0]['customdata']
    dff = df_history_complex[df_history_complex['project']+df_history_complex['path']+df_history_complex['method'] == key]

    title = '<b>{}</b><br>'.format(key)
    return create_time_series(dff, axis_type, title, 'nloc')


@app.callback(
    Output('graph-wordcloud', 'src'),
    [Input('language-dropdown-wordcloud','value')])
def update_wordcloud(selected_language):

    if(len(selected_language)):
        word_cloud.generate_word_cloud(selected_language)
    
    encoded_image = base64.b64encode(open(path + '/src/word-cloud.png', 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())


if __name__ == '__main__':
    app.run_server(debug=True)