import io
import dash
import base64
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash import Dash, html, dcc, dash_table, no_update
from linear_regression import gradient_descent

# from linear_regression import linear_func
# from linear_regression import cost_func
# from linear_regression import total_cost
# from linear_regression import gradient

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

server = app.server

# App variables
x_vals = []
y_vals = []
facade = pd.DataFrame({"X": x_vals, "Y": y_vals})

graph_tab = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                html.Center(
                    [
                        html.P(
                            "Start by creating a graph with the appropriate labels",
                            style={"fontSize": 15},
                        ),
                        html.P(
                            "You can then start inputting points by entering x and y coordinates",
                            style={"fontSize": 15},
                        ),
                    ]
                ),
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText("Feature Label"),
                                    dbc.Input(id="feature-input", type="text"),
                                ],
                                className="mb-3",
                            ),
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText("Predicted Label"),
                                    dbc.Input(id="predicted-input", type="text"),
                                ],
                                className="mb-3",
                            ),
                            dbc.Button(
                                "Create Graph",
                                id="create-graph",
                                color="primary",
                                className="mb-3",
                            ),
                        ],
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText("X Value"),
                                    dbc.Input(id="x-input", type="number"),
                                ],
                                className="mb-3",
                            ),
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText("Y Value"),
                                    dbc.Input(id="y-input", type="number"),
                                ],
                                className="mb-3",
                            ),
                            dbc.Checklist(
                                options=[
                                    {
                                        "label": "Allow Duplicates",
                                        "value": "allow_duplicates",
                                    }
                                ],
                                id="allow-duplicates",
                                inline=True,
                                switch=True,
                                className="mb-3",
                            ),
                            dbc.Button(
                                "Add Point",
                                id="add-point",
                                color="primary",
                                className="mb-3",
                            ),
                        ],
                        width="auto",
                    ),
                    dbc.Col(
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
                            dbc.Button(
                                "Update Parameters",
                                id="param_update",
                                color="primary",
                                className="mb-3",
                            ),
                        ],
                        width="auto",
                    ),
                ],
                justify="center",
            ),
            html.Div(
                [
                    dbc.Toast(
                        "Please fill in the graph labels",
                        id="input-error-toast",
                        header="Missing Input",
                        is_open=False,
                        dismissable=True,
                        icon="warning",
                        duration=4000,
                    ),
                    dbc.Toast(
                        "Input x and y coordinates to add points",
                        id="coordinates-error-toast",
                        header="Missing Coordinates",
                        is_open=False,
                        dismissable=True,
                        icon="warning",
                        duration=4000,
                    ),
                    dbc.Toast(
                        "Toggle the checkbox to allow duplicate data points",
                        id="duplicates-error-toast",
                        header="Duplicate Error",
                        is_open=False,
                        dismissable=True,
                        icon="warning",
                        duration=4000,
                    ),
                ],
                style={
                    "position": "fixed",
                    "top": "2rem",
                    "right": "2rem",
                },
            ),
            dcc.Graph(id="regression-graph", style={"display": "none"}),
            dcc.Graph(id="cost-graph", style={"display": "none"}),
            html.Div(id="graph-visible", style={"display": "none"}, children="False"),
            dbc.Button(
                "Start Over",
                id="restart-button",
                color="danger",
                className="mt-3",
            ),
        ]
    ),
    className="mt-3",
)

""" @app.callback(
        Output('data-table', 'data'),
        Input('add-row-button', 'n_clicks'),
        prevent_initial_call=True
)
def add_row(n_clicks):
    #df.at[0, 'Y'] = n_clicks
    x_vals.append('')
    y_vals.append('')
    return facade.to_dict('records') """

@app.callback(
        Output('data-table', 'data', allow_duplicate=True),
        #Input('data-table', 'data'),
        Input("add-point", "n_clicks"),
        Input("x-input", "value"),
        Input("y-input", "value"),
        prevent_initial_call=True,
)
def update_data(n_clicks, x_val, y_val):
    global x_vals
    global y_vals
    if dash.callback_context.triggered_id == 'add-point':
        facade = pd.DataFrame({"X": x_vals, "Y": y_vals})
        return facade.to_dict('records')
    return no_update
   

""" @app.callback(
       Output('data-table', 'data', allow_duplicate=True),
       Input('data-table', 'data'),
       prevent_initial_call=True
)
def update_graphs(data):
    # Edit the current index
    x_vals[active_cell['row']] = 100
    facade = pd.DataFrame({"X": x_vals, "Y": y_vals})
    return facade.to_dict('records') """


# Bulk input tab
bulk_input_tab = dbc.Card (
    dbc.CardBody (
        [
            html.Div(
                html.Center(
                    [
                        html.H1(
                            "View Data",
                            style={"fontSize": 15},
                        )
                    ]
                ),
            ),
            dash_table.DataTable(facade.to_dict('records'),  [{"name": i, "id": i, "type": "numeric"} for i in facade.columns], editable=False, id="data-table", row_deletable=True),
            dbc.Button(
                "Add Row",
                id="add-row-button",
                color="danger",
                className="mt-3",
            ),
        ]
    )
)

app.layout = html.Div(
    [
        html.Center([html.H1("Linear Regression Tool")], style={"marginTop": 20}),
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.H2("What is this tool?", style={"marginLeft": 20}),
                html.P(
                    "This is a tool for visualizing linear regression, and getting a better understanding"
                    + "of linear regression through playing with parameters.",
                    style={"fontSize": 15, "marginLeft": 40},
                ),
            ],
            style={"marginRight": 20, "marginLeft": 20},
        ),
        html.Div(
            [
                html.H2("How to use?", style={"marginLeft": 20}),
                html.P(
                    "You can create a graph and adjust the values as you see fit",
                    style={"fontSize": 15, "marginLeft": 40},
                ),
                html.Br(),
                html.Center(
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Graph", children=graph_tab, tab_id="tab-1"),
                            dbc.Tab(label="View Data", children=bulk_input_tab, tab_id="tab-bulk-input")
                        ],
                        id="tabs",
                        active_tab="tab-1",
                        style={"width": "95%"},
                    ),
                ),
                html.Br(),
                html.Center(
                    html.Div(id="tab-content", style={"width": "95%"}),
                ),
            ],
            style={"marginRight": 20, "marginLeft": 20},
        ),
        html.Hr(),
        html.Div(
            [
                dbc.Toast(
                    "Please upload a .xlsx file",
                    id="error-toast",
                    header="Invalid File Type",
                    is_open=False,
                    dismissable=True,
                    icon="danger",
                    duration=4000,
                )
            ],
            style={"position": "fixed", "top": "2rem", "right": "2rem"},
        ),
        dcc.Store(id="active-tab-store", data="tab-1"),
    ],
)


def parse_contents(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = None
    if "xlsx" in filename:
        df = pd.read_excel(io.BytesIO(decoded))
    return df


@app.callback(
    Output("coordinates-error-toast", "is_open"),
    [Input("add-point", "n_clicks")],
    [State("x-input", "value"), State("y-input", "value")],
)
def show_coordinates_error(n_clicks, x_value, y_value):
    if n_clicks and (x_value is None or y_value is None):
        return True
    return False


@app.callback(
    Output("clicked-coordinates", "children"),
    Input("regression-graph", "clickData"),
)
def display_click_data(click_data):
    if click_data:
        x = click_data["points"][0]["x"]
        y = click_data["points"][0]["y"]
        return f"Clicked coordinates: x={x}, y={y}"
    return "No coordinates clicked yet."



@app.callback(
    [
        Output("cost-graph", "figure"),
        Output("cost-graph", "style"),
        Output("regression-graph", "figure"),
        Output("regression-graph", "style"),
        Output("feature-input", "value"),
        Output("predicted-input", "value"),
        Output("x-input", "value"),
        Output("y-input", "value"),
        Output("learning_rate", "value"),
        Output("iteration_amount", "value"),
        Output("graph-visible", "children"),
        Output("input-error-toast", "is_open"),
        Output("duplicates-error-toast", "is_open"),
    ],
    [
        Input("create-graph", "n_clicks"),
        Input("add-point", "n_clicks"),
        Input("param_update", "n_clicks"),
        Input("restart-button", "n_clicks"),
        Input("data-table", "data"),
    ],
    [
        State("feature-input", "value"),
        State("predicted-input", "value"),
        State("x-input", "value"),
        State("y-input", "value"),
        State("learning_rate", "value"),
        State("iteration_amount", "value"),
        State("regression-graph", "figure"),
        State("cost-graph", "figure"),
        State("allow-duplicates", "value"),
    ],
)
def update_graph(
    n_clicks_create,
    n_clicks_add_point,
    n_clicks_param_update,
    n_clicks_restart,
    data_table_data,
    feature_value,
    predicted_value,
    x,
    y,
    learning_rate,
    iteration_amount,
    figure,
    cost_figure,
    allow_duplicates,
):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    global x_vals
    global y_vals

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if triggered_id == "restart-button":
        empty_figure = go.Figure()
        return (
            empty_figure,
            {"display": "none"},
            empty_figure,
            {"display": "none"},
            "",
            "",
            None,
            None,
            0.002,
            100,
            "False",
            no_update,
            no_update,
        )

    if feature_value is None or predicted_value is None:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
        )

    graph_visible = False
    if (
        n_clicks_create is not None
        and feature_value is not None
        and predicted_value is not None
    ):
        graph_visible = True

    if graph_visible is False:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            {"display": "none"},
            no_update,
        )

    if cost_figure is None:
        cost_figure = go.Figure(
            data=[
                go.Scatter(
                    x=list(range(iteration_amount + 1)),
                    y=[0],
                    showlegend=False,
                )
            ],
            layout=go.Layout(
                xaxis_title="Iterations", yaxis_title="Cost", title="Cost Curve"
            ),
        )

    if figure is None:
        figure = go.Figure(
            data=[
                go.Scatter(
                    x=[0],
                    y=[0],
                    mode="lines",
                    line=dict(width=0),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[0],
                    y=[0],
                    mode="markers",
                    marker=dict(size=0, opacity=0),
                    showlegend=False,
                ),
            ],
            layout=go.Layout(
                xaxis_title=feature_value,
                yaxis_title=predicted_value,
                title="Regression Curve",
                hovermode="closest",
                clickmode="event+select",
            ),
        )

    if (
        triggered_id == "param_update"
        and learning_rate is not None
        and iteration_amount is not None
    ):
        res_x, res_y, costs = gradient_descent(
            x_vals, y_vals, learning_rate, iteration_amount
        )
        cost_figure["data"] = [
            go.Scatter(
                x=list(range(iteration_amount + 1)),
                y=costs,
            )
        ]

    allow_duplicates = (
        allow_duplicates is not None and "allow_duplicates" in allow_duplicates
    )

    if triggered_id == "add-point" or triggered_id == "data-table" and x is not None and y is not None:
        if not allow_duplicates and x in x_vals and y in y_vals:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
            )
        if triggered_id == "add-point":
            x_vals.append(x)
            y_vals.append(y)
        if triggered_id == "data-table":
            x_vals = [1, 2, 3]
            y_vals = [2, 4, 6]
        #global df
        #f = df
        # print(x_vals)
        res_x, res_y, costs = gradient_descent(
            x_vals, y_vals, learning_rate, iteration_amount
        )

        figure["data"].pop(0)
        figure["data"].insert(
            0,
            {
                "x": res_x,
                "y": res_y,
                "mode": "lines",
                "type": "line",
                "line": {"color": "blue", "width": 2},
                "name": "Regression line",
            },
        )

        if triggered_id == "add-point":
            figure["data"].append(
                {
                    "x": [x],
                    "y": [y],
                    "mode": "markers",
                    "marker": {"color": "red", "symbol": ".", "size": 10},
                    "name": f"({x:.2f}, {y:.2f})",
                    "type": "scatter",
                }
            )
        elif triggered_id == "bulk-edit-table":
            #add stuff here
            pass

        cost_figure["data"] = [
            go.Scatter(
                x=list(range(iteration_amount + 1)),
                y=costs,
            )
        ]

    cost_figure["layout"].update(
        xaxis_title="Iteration num", yaxis_title="Cost", title="Cost curve"
    )

    figure["layout"].update(
        xaxis_title=feature_value,
        yaxis_title=predicted_value,
        hovermode="closest",
    )

    return (
        cost_figure,
        {"display": "block" if graph_visible else "none"},
        figure,
        {"display": "block" if graph_visible else "none"},
        no_update,
        no_update,
        '', # new value of X value input
        '', # new value of Y value input
        no_update,
        no_update,
        str(graph_visible),
        no_update,
        no_update,
    )


@app.callback(
    Output("output-data-upload", "children"),
    Output("error-toast", "is_open"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
)
def update_output(contents, filename):
    if contents:
        if not filename.endswith(".xlsx"):
            return no_update, True

        try:
            df = parse_contents(contents, filename)
            df.columns = df.columns.str.replace(r"[ ()]", "_")

            return (
                html.Div(
                    [
                        html.H5(
                            ["Uploaded File: " + filename],
                            style={"marginBottom": "2.5%"},
                        ),
                        html.Div(
                            [
                                dcc.Loading(
                                    children=dash_table.DataTable(
                                        data=df.to_dict("records"),
                                        columns=[
                                            {"name": i, "id": i} for i in df.columns
                                        ],
                                        style_cell={"textAlign": "left"},
                                        style_header={
                                            "backgroundColor": "rgb(230, 230, 230)",
                                            "fontWeight": "bold",
                                        },
                                        style_data={
                                            "whiteSpace": "normal",
                                            "height": "auto",
                                        },
                                    )
                                )
                            ],
                            style={
                                "marginLeft": "5%",
                                "marginRight": "5%",
                            },
                        ),
                        html.Hr(),
                    ],
                    style={"marginTop": 20},
                ),
                False,
            )
        except Exception as e:
            return (
                html.Div(["There was an error processing the file: {}".format(e)]),
                False,
            )
    return no_update, no_update


if __name__ == "__main__":
    app.run_server(debug=True)
