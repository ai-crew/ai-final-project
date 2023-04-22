import io
import dash
import base64
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash import Dash, html, dcc, dash_table, no_update
from linear_regression import linear_func
from linear_regression import cost_func
from linear_regression import total_cost
from linear_regression import gradient
from linear_regression import gradient_descent


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

server = app.server

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
                                    dbc.InputGroupText("Feature Value"),
                                    dbc.Input(id="feature-input", type="text"),
                                ],
                                className="mb-3",
                            ),
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText("Predicted Value"),
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
                        "Please fill in the input boxes",
                        id="input-error-toast",
                        header="Missing Input",
                        is_open=False,
                        dismissable=True,
                        icon="danger",
                        duration=4000,
                    ),
                    dbc.Toast(
                        "Input x and y coordinates to add points",
                        id="coordinates-error-toast",
                        header="Missing Coordinates",
                        is_open=False,
                        dismissable=True,
                        icon="danger",
                        duration=4000,
                    ),
                ],
                style={
                    "position": "fixed",
                    "top": "2rem",
                    "right": "2rem",
                },
            ),
            dcc.Graph(
                id="cost-graph",
                style={"display": "none"}
                ),
            dcc.Graph(
                id="regression-graph", 
                style={"display": "none"}
                ),
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


file_tab = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.Center(
                        [
                            html.P(
                                "Make sure that the table has appropriate column headers that can be extracted as features"
                            ),
                            html.P(
                                [
                                    "Try and make sure that there is no missing data in the table, click ",
                                    html.A(
                                        "here",
                                        href="https://www.analyticsvidhya.com/blog/2021/05/dealing-with-missing-values-in-python-a-complete-guide/",
                                        target="_blank",
                                    ),
                                    " for more information",
                                ],
                            ),
                        ],
                        style={"fontSize": 15},
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(
                            ["Drag and Drop or ", html.A("Select Files")]
                        ),
                        style={
                            "width": "95%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "marginBottom": "2.5%",
                            "cursor": "pointer",
                        },
                        multiple=False,
                    ),
                    html.Div(id="output-data-upload"),
                ]
            ),
        ]
    ),
    className="mt-3",
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
                    "This is a tool for visualizing linear regression, and getting a better understanding of linear regression through playing with parameters.",
                    style={"fontSize": 15, "marginLeft": 40},
                ),
            ],
            style={"marginRight": 20, "marginLeft": 20},
        ),
        html.Div(
            [
                html.H2("How to use?", style={"marginLeft": 20}),
                html.P(
                    "You can create a graph and adjust the values as you see fit, or simply upload an Excel file with your data.",
                    style={"fontSize": 15, "marginLeft": 40},
                ),
                html.Br(),
                html.Center(
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Graph", tab_id="tab-1"),
                            dbc.Tab(label="File", tab_id="tab-2"),
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

    if "xlsx" in filename:
        df = pd.read_excel(io.BytesIO(decoded))

    return df


@app.callback(Output("tab-content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return graph_tab
    elif at == "tab-2":
        return file_tab
    return html.P("Error rendering tabs...")


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


# App variables
x_vals = []
y_vals = []

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
    ],
    [
        Input("create-graph", "n_clicks"),
        Input("add-point", "n_clicks"),
        Input("restart-button", "n_clicks"),
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
    ],
)
def update_graph(
    n_clicks_create,
    n_clicks_add_point,
    n_clicks_restart,
    feature_value,
    predicted_value,
    x,
    y,
    learning_rate,
    iteration_amount,
    figure,
    cost_figure,
):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if triggered_id == "restart-button":
        empty_figure = go.Figure()  # Create an empty figure

        return (
            empty_figure,  # Reset cost_figure to the empty figure
            {"display": "none"},  # Hide the graph
            empty_figure,  # Reset figure to the empty figure
            {"display": "none"},  # Hide the graph
            "",  # Empty feature-input value
            "",  # Empty predicted-input value
            None,  # Empty x-input value
            None,  # Empty y-input value
            0.002,  # Reset learning rate to default value
            100,  # Reset iteration amount to default value
            "False",  # Set graph-visible to False
            no_update,  # No update for input-error-toast
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
        )

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
                xaxis_title="Iteration num",
                yaxis_title="Cost",
                title="Cost curve"
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
                )
            ],
            layout=go.Layout(
                xaxis_title=feature_value,
                yaxis_title=predicted_value,
                title="Regression curve",
                hovermode="closest",
                clickmode="event+select",
            ),
        )

    if triggered_id == "add-point" and x is not None and y is not None:
        x_vals.append(x)
        y_vals.append(y)
        print(x_vals)
        res_x, res_y, costs = gradient_descent(x_vals, y_vals, learning_rate, iteration_amount)
        
        figure["data"].pop(0)
        figure["data"].insert(0,
            {
                "x": res_x,
                "y": res_y,
                "mode": "lines",
                "type": "line",
                "line": {"color": "blue", "width": 2},
                "name": "Regression line",
            }
        )

        figure["data"].append({
            "x": [x],
            "y": [y],
            "mode": "markers",
            "marker": {"color": "red", "symbol": "x", "size": 10},
            "name": f"({x:.2f}, {y:2f})",
            "type": "scatter",
        })
        
        cost_figure["data"] = [
            go.Scatter(
                x = list(range(iteration_amount + 1)),
                y =  costs,
            )
        ]

    cost_figure["layout"].update(
        xaxis_title="Iteration num",
        yaxis_title="Cost",
        title="Cost curve"
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
        no_update,
        no_update,
        no_update,
        no_update,
        str(graph_visible),
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
