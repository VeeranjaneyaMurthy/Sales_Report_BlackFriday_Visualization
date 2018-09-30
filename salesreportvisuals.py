import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly

app = dash.Dash()

app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True


#reading csv file

df = pd.read_csv("BlackFriday.csv")

# Layout


app.layout = html.Div([
    html.H1('Sales Report Black Friday'),
    dt.DataTable(
        rows=df.to_dict('records'),

        # optional - sets the order of columns
        columns=sorted(df.columns),

        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='datatable'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph'
    ),
], className="container")

# Callbacks and functions


@app.callback(
    Output('datatable', 'selected_row_indices'),
    [Input('graph', 'clickData')],
    [State('datatable', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=5, cols=1,
        subplot_titles=('Age', 'Product_Category_1', 'Product_Category_2','Product_Category_3','Purchase'),
        shared_xaxes=True)
    marker = {'color': ['#0074D9']*len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace({
        'x': dff['Product_ID'],
        'y': dff['Age'],
        'type': 'bar',
        'marker': marker
    }, 1, 1)
    fig.append_trace({
        'x': dff['Product_ID'],
        'y': dff['Product_Category_1'],
        'type': 'bar',
        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'x': dff['Product_ID'],
        'y': dff['Product_Category_2'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)
    fig.append_trace({
        'x': dff['Product_ID'],
        'y': dff['Product_Category_3'],
        'type': 'bar',
        'marker': marker
    }, 4, 1)
    fig.append_trace({
        'x': dff['Product_ID'],
        'y': dff['Purchase'],
        'type': 'scatter',
        'marker': marker
    }, 5, 1)

    
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 800
    fig['layout']['margin'] = {
        'l': 40,
        'r': 10,
        't': 60,
        'b': 200
    }
    fig['layout']['yaxis3']['type'] = 'log'
    return fig

# Boostrap CSS.
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

#main function to run local server
if __name__ == '__main__':
    app.run_server(debug=True)
