import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
from pages import home, sample_dataset, upload_dataset
import flask
from dash.dependencies import Input, Output

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
)

server = app.server

app.title = "Linear Regression Visualizer"

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content',
             style={'margin': '5rem'}, children=[]),
]
)


@app.server.route('/download_csv/')
def download_csv():
    try:
        return flask.send_from_directory(
            directory='datasets',
            path='sample.csv',
            mimetype='text/csv',
            download_name='sample.csv',
            as_attachment=True,
        )
    except Exception as e:
        print(str(e))
        return flask.abort(404)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/sampleDataset':
        return sample_dataset.layout
    elif pathname == '/uploadDataset':
        return upload_dataset.layout
    else:
        return "404"


if __name__ == '__main__':
    app.run_server(debug=False)
