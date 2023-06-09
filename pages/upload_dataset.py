from dash import no_update
from dash import html, dcc, callback, Input, Output, State, exceptions, callback_context
import pandas as pd
import base64
import io
import plotly.graph_objs as go
from linear_regression import gradient_descent_returns_weights_and_biases
import dash_bootstrap_components as dbc
import numpy as np
import uuid

layout = html.Div(

    children=[

        html.Div(
            children=[
                html.H1("Upload Your Own Dataset To Explore (2-variables)",
                        style={"font-size": "2rem"}),
                html.Div(
                    html.Span(
                        "Your csv should have two columns. The first one will be for the x-variable, and the second one is for the y-variable",
                        style={"font-size": "1rem"}
                    )
                ),
                html.Br(),
            ],
            style={"text-align": "center"},
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Button(
                            className="button-container",
                            children=[
                                html.A(
                                    "Download Sample CSV",
                                    className="download-link",
                                    id="download-link",
                                    download="sample.csv",
                                    href="download_csv/",
                                ),
                                html.I(
                                    className="fas fa-download fa icon",
                                ),
                            ],
                        ),
                        html.Div("Upload .csv/.xslx file"),
                        dcc.Upload(
                            id="upload-data-component",
                            multiple=False,
                            children=html.Div(
                                [
                                    "Drag and Drop or ",
                                    html.A(
                                        "Select a File",
                                        style={"text-decoration": "underline"},
                                    ),
                                ],
                                className="upload-file-container",
                            ),
                        ),
                        html.Div(id="file-status-info"),
                        html.Br(),
                    ],
                    className="padded-container",
                ),
                html.Div(
                    children=[
                        html.Button(
                            className="button-container",
                            children=[
                                html.A(
                                    "Add Point",
                                    className="download-link",
                                ),
                                html.I(
                                    className="fas fa-plus fa icon",
                                ),
                            ],
                            id="add-point-modal-open-btn"
                        ),
                        dbc.Modal([
                            dbc.ModalHeader([
                                dbc.ModalTitle("Add Points"),
                            ]),
                            dbc.ModalBody([
                                html.P("Add points to the dataset"),
                                html.Div(id="modal-error-not-enough-points"),

                                html.Div(id="input-fields-container", children=[
                                    html.Div([
                                        dbc.InputGroup(
                                            children=[
                                                dbc.InputGroupText("X"),
                                                dbc.Input(id={"type": "point-input-x", "index": 0},
                                                          type="number", style={"width": "50%"}),

                                            ], className="mb-3",

                                        ),
                                        dbc.InputGroup(
                                            children=[
                                                dbc.InputGroupText("Y"),
                                                dbc.Input(id={"type": "point-input-y", "index": 0},
                                                          type="number", style={"width": "50%"}),

                                            ], className="mb-3",

                                        ),

                                    ], style={"display": "flex", "justify-content": "space-around",
                                              "margin-bottom": "10px"}),

                                ], style={"overflow-y": "auto", "max-height": "400px"}),
                                html.Div([
                                    html.I(className="fas fa-plus-square"),
                                    html.Span(" Add more points", style={
                                        "cursor": "pointer", "margin-left": "10px"})
                                ], id="add-more-points",
                                    style={"display": "flex", "align-items": "center", "cursor": "pointer",
                                           "margin-top": "10px"}),
                            ]),
                            dbc.ModalFooter([
                                dbc.Button("Add", id="add-point-btn",
                                           className="ms-auto", n_clicks=0),

                            ])
                        ], id="modal", is_open=False)
                    ],
                    className="padded-container mb-3",
                ),

                html.Div(
                    children=[
                        dbc.Checklist(
                            options=[
                                {
                                    "label": "Add custom labels to axes (toggle ON if dataset doesn't have labels in header)",
                                    "value": "show_label_inputs",
                                }
                            ],
                            id="toggle_header_provided",
                            inline=True,
                            switch=True,
                        ),
                        html.Br(),
                    ],
                    className="padded-container",
                ),

                html.Div(
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.InputGroup(
                                        [
                                            dbc.InputGroupText("x-axis label"),
                                            dbc.Input(
                                                id="x-axis-label",
                                                type="text",
                                                placeholder="X",
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                    width=6,
                                    style={"display": "inline-block"},
                                ),
                                dbc.Col(
                                    dbc.InputGroup(
                                        [
                                            dbc.InputGroupText("y-axis label"),
                                            dbc.Input(
                                                id="y-axis-label",
                                                type="text",
                                                placeholder="Y",
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                    width=6,
                                    style={"display": "inline-block"},
                                ),
                            ],
                            id="show_label_inputs",
                        ),
                    ],
                    style={
                        "padding-right": "25px",
                        "padding-left": "25px",
                    },
                ),

                html.Div(
                    children=[
                        dbc.Checklist(
                            options=[
                                {
                                    "label": "Specify initial weight and bias",
                                    "value": "show_init_w_b",
                                }
                            ],
                            id="toggle_init",
                            inline=True,
                            switch=True,
                        ),

                        html.Div(
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText(
                                                        "Enter initial weight"
                                                    ),
                                                    dbc.Input(
                                                        id="init_w",
                                                        type="text",
                                                        placeholder="0",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            width=6,
                                        ),
                                        dbc.Col(
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText(
                                                        "Enter initial bias"
                                                    ),
                                                    dbc.Input(
                                                        id="init_b",
                                                        type="text",
                                                        placeholder="0",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    className="padded-container",
                                ),
                            ], id="show_init_w_b",
                        ),
                        html.Br(),

                    ],

                    style={

                        "padding-right": "25px",
                        "padding-left": "25px",
                    }
                ),
                html.Div(
                    [
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Learning Rate"),
                                dbc.Input(
                                    id="learning_rate",
                                    type="number",
                                    value=0.002,
                                    step=0.001,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Iteration Amount"),
                                dbc.Input(
                                    id="iteration_amount",
                                    type="number",
                                    value=100,
                                    min=1,
                                    max=1000,
                                ),
                            ],
                            className="mb-3",
                        ),
                    ],
                    className="padded-container",
                ),
            ],
        ),

        html.Div(
            className="padded-container",
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="regression-graph",
                                config={"displayModeBar": True},
                                figure={
                                    "data": [
                                        {
                                            "x": 0,
                                            "y": 0,
                                            "type": "lines",
                                            "hovertemplate": " %{y:.2f}"
                                                             "<extra></extra>",
                                        },
                                    ],
                                    "layout": {
                                        "title": {
                                            "text": "Relationship between X and Y",
                                            "x": 0.1,
                                            "xanchor": "left",
                                        },
                                        "xaxis": {"fixedrange": True},
                                        "yaxis": {
                                            "fixedrange": True,
                                        },
                                    },
                                },
                            ),
                            className="card",
                            width=12,
                        ),

                    ],
                ),
                html.Br(),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(children=[
                            dbc.Row(
                                id='stats-container',
                                children=[
                                    html.H4("Results"),
                                    html.Div("Equation of line", style={
                                        "font-weight": "bold"}),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                html.Div(id="equation")),
                                            dbc.Col(dcc.Clipboard(style={"fontSize": 20},
                                                                  target_id="equation"), width=2,
                                                    style={"color": "deepskyblue"})
                                        ],
                                        className="stats"
                                    ),
                                    html.Div("Weight", style={
                                        "font-weight": "bold"}),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                html.Div(id="weight")),
                                            dbc.Col(dcc.Clipboard(style={"fontSize": 20},
                                                                  target_id="weight"), width=2,
                                                    style={"color": "deepskyblue"})
                                        ],
                                        className="stats"
                                    ),
                                    html.Div("Bias", style={
                                        "font-weight": "bold"}),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                html.Div(id="bias")),
                                            dbc.Col(dcc.Clipboard(style={"fontSize": 20},
                                                                  target_id="bias"), width=2,
                                                    style={"color": "deepskyblue"})
                                        ],
                                        className="stats"
                                    ),
                                    html.Div("Final Cost", style={
                                        "font-weight": "bold"}),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                html.Div(id="cost")),
                                            dbc.Col(dcc.Clipboard(style={"fontSize": 20},
                                                                  target_id="cost"), width=2,
                                                    style={"color": "deepskyblue"})
                                        ],
                                        className="stats"
                                    ),
                                ],
                                align="top",
                                className="flex-stats-container",
                            )

                        ],
                            style={"padding-top": "2rem"}),
                        dbc.Col(
                            children=[
                                html.Div(
                                    children=[
                                        html.Div(
                                            children=dcc.Graph(
                                                id="cost-graph",
                                                config={
                                                    "displayModeBar": True},
                                                figure={
                                                    "data": [
                                                        {
                                                            "x": 0,
                                                            "y": 0,
                                                            "type": "lines",
                                                            "hovertemplate": " %{y:.2f}"
                                                                             "<extra></extra>",
                                                        },
                                                    ],
                                                    "layout": {
                                                        "title": {
                                                            "text": "Cost over iterations",
                                                            "x": 0.5,
                                                            "xanchor": "center",
                                                        },
                                                        "xaxis": {"fixedrange": True},
                                                        "yaxis": {
                                                            "fixedrange": True,
                                                        },
                                                    },
                                                },
                                            ), className="card",
                                        ),
                                    ],
                                ),
                            ], align="top", class_name="cost-graph-container", style={"padding-top": "2rem"}
                        )
                    ],
                ),
            ],
        ),

    ]
)


@callback(
    [Output("input-fields-container", "children"),
     Output("modal", "is_open"),
     Output("modal-error-not-enough-points", "children")],
    [Input("add-more-points", "n_clicks"),
     Input("add-point-modal-open-btn", "n_clicks"),
     Input("add-point-btn", "n_clicks"),
     Input("x-axis-label", "value"),
     Input("y-axis-label", "value"),
     ],
    [State("input-fields-container", "children"),
     State("modal", "is_open"),
     State("input-fields-container", "children")
     ],
)
def toggle_modal_and_add_input_fields(add_more_points_n_clicks, add_point_n_clicks, add_point_btn_n_clicks,
                                      x_axis_label, y_axis_label, children, is_open, input_fields):
    ctx = callback_context
    triggered_id, triggered_prop = ctx.triggered[0]['prop_id'].split('.')

    if triggered_id == 'add-more-points':
        if add_more_points_n_clicks:
            new_index = str(uuid.uuid4())
            new_input = html.Div(children=[
                dbc.InputGroup(
                    children=[
                        dbc.InputGroupText("X"),
                        dbc.Input(id={"type": "point-input-x", "index": new_index},
                                  type="number", style={"width": "50%"}),

                    ], className="mb-3",

                ),
                dbc.InputGroup(
                    children=[
                        dbc.InputGroupText("Y"),
                        dbc.Input(id={"type": "point-input-y", "index": new_index},
                                  type="number", style={"width": "50%"}),

                    ], className="mb-3",

                ),

            ], style={"display": "flex", "justify-content": "space-around", "margin-bottom": "10px"})
            children.append(new_input)
        return children, no_update, html.Div()

    elif triggered_id == 'add-point-modal-open-btn':
        if add_point_n_clicks:
            return no_update, not is_open, html.Div()
        return no_update, is_open, False
    elif triggered_id == triggered_id == 'add-point-btn':
        return no_update, not is_open, html.Div()

    else:
        raise exceptions.PreventUpdate


@callback(
    [Output("show_label_inputs", "className"),
     Output("x-axis-label", "value"),
     Output("y-axis-label", "value")],
    [Input("toggle_header_provided", "value")],
    [State("x-axis-label", "value"),
     State("y-axis-label", "value")]
)
def show_label_name_inputs(toggle_value, x_axis_label, y_axis_label):
    if not toggle_value:
        exceptions.PreventUpdate()
    if toggle_value:
        return "padded-container", x_axis_label, y_axis_label
    else:
        return "hidden", "X", "Y"


@callback(
    [Output("show_init_w_b", "className"),
     Output("init_w", "value"),
     Output("init_b", "value")],
    [Input("toggle_init", "value")],
    [State("init_w", "value"),
     State("init_b", "value")]
)
def show_init_w_b(toggle_value, init_w, init_b):
    if toggle_value:
        return "padded-container", float(init_w), float(init_b)
    else:
        return "hidden", float(0), float(0)


def parse_contents(contents, filename, date):
    if filename is None or contents is None:
        return None
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None)
            return df
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
            return df
    except Exception as e:
        print("Error:", e)
        return None


@callback(Output('file-status-info', 'children'),
          Input('upload-data-component', 'contents'),
          State('upload-data-component', 'filename'),
          State('upload-data-component', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        dataframes = [
            parse_contents(list_of_contents, list_of_names, list_of_dates)]

        if not dataframes or dataframes[0] is None:
            return html.Div("Error. Please check that file type and/or format is valid.", style={'color': 'red'})
        df = dataframes[0]

        if df.shape[1] != 2:
            return html.Div(
                "Invalid file format for 2D regression. Please upload a valid .csv or .xslx file (see sample.csv)",
                style={'color': 'red'})
        else:
            return html.Div(children=[
                html.Div("File uploaded successfully",
                         style={'color': 'green'}),
                html.Div(f"Filename: {list_of_names}")
            ])
    else:
        return html.Div("No data", style={'color': 'grey'})


@callback(
    [Output("regression-graph", "figure"),
     Output("cost-graph", "figure"),
     Output('cost', 'children'),
     Output('weight', 'children'),
     Output('bias', 'children'),
     Output('equation', 'children')

     ],
    Input('upload-data-component', 'contents'),
    State('upload-data-component', 'filename'),
    State('upload-data-component', 'last_modified'),
    Input("x-axis-label", "value"),
    Input("y-axis-label", "value"),
    Input("learning_rate", "value"),
    Input("iteration_amount", "value"),
    Input("init_w", "value"),
    Input("init_b", "value"),
    Input("add-point-btn", "n_clicks"),
    State("input-fields-container", "children"))
def update_chart(list_of_contents, list_of_names, list_of_dates, x_axis_label, y_axis_label, learning_rate,
                 iteration_amount, init_w, init_b, submit_points, input_fields_children):
    regression_fig = go.Figure()
    cost_fig = go.Figure()

    regression_fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": "Please upload a file to see linear regression visualization.",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 14
                }
            }
        ]
    )

    cost_fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": "Please upload a file to see cost function.",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 14
                }
            }
        ]
    )

    if submit_points < 1 and list_of_contents is None:
        raise exceptions.PreventUpdate

    df_uploaded = pd.DataFrame(columns=[x_axis_label, y_axis_label])
    df_added_points = pd.DataFrame(columns=[x_axis_label, y_axis_label])

    dataframes = parse_contents(
        list_of_contents, list_of_names, list_of_dates)

    if dataframes is not None:
        if len(dataframes) > 0 and dataframes.shape[1] == 2:
            dataframes.columns = [x_axis_label, y_axis_label]
            df_uploaded = dataframes
    if submit_points is not None:
        for input_field in input_fields_children:
            try:
                # NOTE: check this if you change object properties again
                x = input_field['props']['children'][0]['props']['children'][1]['props']['value']
                y = input_field['props']['children'][1]['props']['children'][1]['props']['value']
                df_added_points = pd.concat([df_added_points, pd.DataFrame(
                    [[x, y]], columns=[x_axis_label, y_axis_label])])
            except Exception as e:
                print("Error in points stuff:", e)
                continue
    df = pd.concat([df_uploaded, df_added_points])

    if len(df.columns) != 2:
        return [
            regression_fig,
            cost_fig,
            html.Div(children=0),
            html.Div(children=0),
            html.Div(children=0),
            html.Div(children=0)
        ]
    else:
        # continue with regression and cost calculations
        init_b = float(init_b) if init_b else float(0)
        init_w = float(init_w) if init_w else float(0)
        learning_rate = float(
            learning_rate) if learning_rate else float(0.001)
        iteration_amount = int(
            iteration_amount) if iteration_amount else int(100)

        x_values = df[x_axis_label].to_numpy()
        y_values = df[y_axis_label].to_numpy()

        if len(x_values) == 0 or len(y_values) == 0:
            raise exceptions.PreventUpdate

        _, _, cost, w, b = gradient_descent_returns_weights_and_biases(
            x_values, y_values, init_w=init_w, init_b=init_b, alpha=learning_rate, iters=iteration_amount)

        x_axis_label = x_axis_label if x_axis_label else "X"
        y_axis_label = y_axis_label if y_axis_label else "Y"

        regression_fig = go.Figure()
        regression_fig.add_trace(go.Scatter(
            x=df[x_axis_label], y=df[y_axis_label], mode='markers', name="data",
            hovertemplate="X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>"))

        start = min(df[x_axis_label])
        end = max(df[x_axis_label])
        range_df = pd.DataFrame(np.arange(start, end, 0.01))
        regression_fig.add_trace(go.Scatter(
            x=range_df[0],
            y=w * range_df[0] + b,
            mode='lines',
            name='regression line',
            line=dict(color='red', dash='dash'),
            hovertemplate="X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>"
        ))

        regression_fig.update_layout(
            title={
                "text": f"{x_axis_label} vs {y_axis_label}",
                "x": 0.5,
                "xanchor": "center",
            },
            xaxis_title=x_axis_label,
            yaxis_title=y_axis_label,

        )

        cost_fig = go.Figure()
        cost_fig.update_layout(
            title={
                "text": "Cost vs. iterations",
                "x": 0.5,
                "xanchor": "center",
            },
            xaxis={"fixedrange": True},
            yaxis={
                "fixedrange": True,
            },
            xaxis_title="Iterations",
            yaxis_title="Cost",

        )

        cost_fig.add_trace(go.Scatter(
            x=list(range(1, iteration_amount + 1)), y=cost, mode='lines', name='Cost'))

        w_rounded = round(w, 3)
        b_rounded = round(b, 3)
        cost = cost[-1] or 0
        cost_rounded = round(cost, 3)

        return [
            regression_fig,
            cost_fig,
            html.Div(children=cost_rounded),
            html.Div(children=w_rounded),
            html.Div(children=b_rounded),
            html.Div(children=[dcc.Markdown(
                f"y = **{w_rounded}**x + **{b_rounded}**")])
        ]
