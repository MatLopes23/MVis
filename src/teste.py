import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

root_path = '/home/mateuslopes/Documentos/Infoviz Complex Methods/'

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

df_complex_methods = pd.read_csv(root_path + 'Datasets/data_set_top_complex_methods.csv')

df_history_complex = pd.read_csv(root_path + 'Datasets/data_set_complexity_history_all_languages_top_complex.csv')

available_languages = df_complex_methods['language'].unique()

def get_only_name_method(key):
    start = key.find("::") + 2 if key.find("::") != -1 else 0
    end = key.find("(") if key.find("(") != -1 else len(key)

    return key[start:end] + '()'

app.layout = html.Div([
    html.Div([

        html.Div([
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
        style={'width': '50%', 'display': 'inline-block'}),

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
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('filter-language', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_graph(filter_language, xaxis_type, yaxis_type):

    dff = df_complex_methods[df_complex_methods.language.isin(filter_language)]

    fig = px.scatter(dff, x='cyclomatic_complexity',
            y='nloc',
            hover_name='method',
            )

    #fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])
    fig.update_traces(customdata=dff['project']+dff['path']+dff['method'])

    fig.update_xaxes(title='Cyclomatic Complexity', type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title='Nloc', type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

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
                       bgcolor='rgba(255, 255, 255, 0.5)', text= get_only_name_method(title))

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    #fig['layout']['xaxis']['autorange'] = "reversed"

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
def update_x_timeseries(hoverData, axis_type):
    key = hoverData['points'][0]['customdata']
    dff = df_history_complex[df_history_complex['project']+df_history_complex['path']+df_history_complex['method'] == key]

    title = '<b>{}</b><br>'.format(key)
    return create_time_series(dff, axis_type, title, 'nloc')


if __name__ == '__main__':
    app.run_server(debug=True)