import plotly.graph_objects as go

def generate_violin_plot(df_complex, df_random):
    violin_plot = go.Figure()

    violin_plot.add_trace(go.Violin(x=df_complex['language'],
                            y=df_complex['cyclomatic_complexity'],
                            legendgroup='Top', scalegroup='Top', name='Top',
                            line_color='blue', points=False, spanmode="hard")
                )
    violin_plot.add_trace(go.Violin(x=df_random['language'],
                            y=df_random['cyclomatic_complexity'],
                            legendgroup='Random', scalegroup='Random', name='Random',
                            line_color='orange', points=False, spanmode="hard")
                )

    violin_plot.update_traces(box_visible=True)
    violin_plot.update_yaxes(type='log')
    violin_plot.update_layout(violinmode='group', margin={'l': 40, 'b': 40, 't': 10, 'r': 10})
    violin_plot.update_xaxes(title='Languages')
    violin_plot.update_yaxes(title='Cyclomatic Complexity')

    
    return violin_plot
    
