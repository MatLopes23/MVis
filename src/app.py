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

path = str(Path(__file__).parents[1])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(path + '/Datasets/data_set_repositories.csv')
df_complex_methods = pd.read_csv(path + '/Datasets/data_set_top_complex_methods.csv')
df_random_methods = pd.read_csv(path + '/Datasets/data_set_random_methods.csv')
df_history_complex = pd.read_csv(path + '/Datasets/data_set_complexity_history_all_languages_top_complex.csv')

violin_plot = violin_plot.generate_violin_plot(df_complex_methods, df_random_methods)

available_languages = df_complex_methods['language'].unique()

color_discrete_map = {'C#': 'rgb(148, 140, 249)',
                      'C++': 'rgb(243, 130, 110)',
                      'Java': 'rgb(110, 218, 180)',
                      'JavaScript': 'rgb(194, 143, 250)',
                      'Python': 'rgb(255, 187, 136)'}

app.layout = html.Div(children=[
    html.H2(children='Métodos Complexos'),

    html.H3(children='Quais são os projetos analisados?'),

    html.Label('Languages'),
    html.Div([
        dcc.Dropdown(
            id='language-dropdown',
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


    dcc.Graph(id='graph-repositories'),
    html.Br(),
    html.H3(children='Como é a complexidade dos métodos?'),

    dcc.Graph(figure=violin_plot),

    html.Br(),
    html.H3(children='Como estes métodos evoluem?'),
    html.Div([

        html.Div([
            html.Label('Languages'),

            dcc.Dropdown(
                id='filter-language',
                options=[{'label': i, 'value': i} for i in available_languages],
                value=['C#', 'C++', 'Java', 'JavaScript', 'Python'],
                multi=True
            ),
            html.Br(),
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

    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

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


])

@app.callback(
    Output('graph-repositories', 'figure'),
    [Input('language-dropdown','value')])

def update_repositories(selected_language):

    filtered_df = df[df.language.isin(selected_language)]

    if(len(filtered_df)):
        fig = px.scatter(filtered_df, x="stars", y="commits",
                        size="files", color="language", hover_name="repository", 
                        size_max=55, color_discrete_map=color_discrete_map)
        

        fig.update_layout(transition_duration=500, margin={'l': 40, 'b': 40, 't': 10, 'r': 10})
    else:
        fig = px.scatter()
    

    return fig

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('filter-language', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_complex_methods(filter_language, xaxis_type, yaxis_type):

    dff = df_complex_methods[df_complex_methods.language.isin(filter_language)]

    fig = px.scatter(dff, x='cyclomatic_complexity', y='nloc',
            hover_name='method', color='language', color_discrete_map=color_discrete_map)

    fig.update_traces(customdata=dff['project']+dff['path']+dff['method'])

    fig.update_xaxes(title='Cyclomatic Complexity', type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title='Nloc', type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest', transition_duration=500,
                      legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))


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


if __name__ == '__main__':
    app.run_server(debug=True)