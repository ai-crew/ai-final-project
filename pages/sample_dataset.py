import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc, callback, Input, Output, State

from linear_regression import gradient_descent_returns_weights_and_biases

datasetList = [
    {"label": "Fish Market Data", "value": "fish.csv"},
    {"label": "Car Price Data", "value": "car_price.csv"},
    {"label": "NYSE Stock Fundamentals Data", "value": "fundamentals.csv"},
    {"label": "Housing Data", "value": "housing.csv"},
]

layout = html.Div(
    children=[
        html.H1("Explore Sample Datasets",
                style={"font-size": "2rem", "text-align": "center", "margin-bottom": "2rem"}),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div("Select a Dataset", style={"margin-bottom": ".5rem"}
                                 ),
                        dcc.Dropdown(
                            id="input-filter",
                            options=datasetList,
                            value="fish.csv",
                            clearable=False,
                        ),
                    ]
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "width": "100%",
                        "margin": "0 auto",
                        "align-items": "center",
                        "text-align": "center",
                        "padding-top": "1rem",
                        "margin-bottom": ".5rem"

                    },
                    children=[
                        html.Span(
                            style={"flex": "1"},
                            children=[
                                html.Div("X variable",
                                         ),
                                dcc.Dropdown(
                                    id="x-var-dropdown-choice",
                                    options=datasetList,
                                    clearable=False,
                                    searchable=True,
                                ),
                            ],
                        ),
                        html.Span(
                            style={"flex": "1"},
                            children=[
                                html.Div("Y variable",
                                         ),
                                dcc.Dropdown(
                                    id="y-var-dropdown-choice",
                                    options=datasetList,
                                    clearable=False,
                                    searchable=True,
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        dbc.Checklist(
                            options=[
                                {
                                    "label": "Specify initial weight and bias",
                                    "value": "show_init_w_b_sg",
                                }
                            ],
                            id="toggle_init_sg",
                            inline=True,
                            switch=True,
                        ),

                        html.Div(
                            children=[
                                dbc.Row(style={"margin-bottom": ".5rem"}, children=[
                                    dbc.Col(
                                        dbc.InputGroup(
                                            [
                                                dbc.InputGroupText(
                                                    "Enter initial weight"
                                                ),
                                                dbc.Input(
                                                    id="init_w_sg",
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
                                                    id="init_b_sg",
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
                            ], id="show_init_w_b_sg",
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
                                    id="learning_rate_sg",
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
                                    id="iteration_amount_sg",
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
                                id="regression-graph_sg",
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
                                            "x": 0.5,
                                            "xanchor": "center",
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
                                                html.Div(id="equation_sg")),
                                            dbc.Col(dcc.Clipboard(style={"fontSize": 20},
                                                                  target_id="equation_sg"), width=2,
                                                    style={"color": "deepskyblue"})
                                        ],
                                        className="stats"
                                    ),
                                    html.Div("Weight", style={
                                        "font-weight": "bold"}),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(html.Div(id="weight_sg")),
                                            dbc.Col(dcc.Clipboard(style={"fontSize": 20},
                                                                  target_id="weight_sg"), width=2,
                                                    style={"color": "deepskyblue"})
                                        ],
                                        className="stats"
                                    ),
                                    html.Div("Bias", style={
                                        "font-weight": "bold"}),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(html.Div(id="bias_sg")),
                                            dbc.Col(dcc.Clipboard(style={"fontSize": 20},
                                                                  target_id="bias_sg"), width=2,
                                                    style={"color": "deepskyblue"})
                                        ],
                                        className="stats"
                                    ),
                                    html.Div("Final Cost", style={
                                        "font-weight": "bold"}),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(html.Div(id="cost_sg")),
                                            dbc.Col(dcc.Clipboard(style={"fontSize": 20},
                                                                  target_id="cost_sg"), width=2,
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
                                                id="cost-graph_sg",
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
                            ], align="top", class_name="cost-graph_sg-container", style={"padding-top": "2rem"}
                        )
                    ],
                ),
            ],
        ),
    ]
)


@callback(
    [Output("show_label_inputs_sg", "className"),
     ],
    [Input("toggle_header_provided_sg", "value"),
     ],
)
def show_label_name_inputs(toggle_value):
    return "padded-container" if toggle_value else "hidden"


@callback(
    [Output("show_init_w_b_sg", "className"),
     Output("init_w_sg", "value"),
     Output("init_b_sg", "value")],
    [Input("toggle_init_sg", "value")],
    [State("init_w_sg", "value"),
     State("init_b_sg", "value")]
)
def show_init_w_b_sg(toggle_value, init_w_sg, init_b_sg):
    if toggle_value:
        return "padded-container", init_w_sg, init_b_sg
    else:
        return "hidden", float(0), float(0)


@callback(
    Output("x-var-dropdown-choice", "options"),
    [Input("input-filter", "value")],
)
def set_output_options(filename):
    df = pd.read_csv("datasets/" + filename)
    options = []
    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            colOriginal = col
            col = col.replace("_", " ").title()
            options.append({"label": col, "value": colOriginal})
    return options


@callback(
    Output("y-var-dropdown-choice", "options"),
    [Input("input-filter", "value")],
)
def set_output_options(input_value):
    df = pd.read_csv("datasets/" + input_value)
    options = []
    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            colOriginal = col
            col = col.replace("_", " ").title()
            options.append({"label": col, "value": colOriginal})
    return options


# If no options have been selected for the dropdown menu, select first two
@callback(
    Output("x-var-dropdown-choice", "value"),
    [Input("x-var-dropdown-choice", "options")],
)
def set_output_value(available_options):
    return available_options[0]["value"] if available_options else None


@callback(
    Output("y-var-dropdown-choice", "value"),
    [Input("y-var-dropdown-choice", "options")],
)
def set_output_value(available_options):
    return available_options[1]["value"] if available_options else None


@callback(
    [
        Output("regression-graph_sg", "figure"),
        Output("cost-graph_sg", "figure"),
        Output('cost_sg', 'children'),
        Output('weight_sg', 'children'),
        Output('bias_sg', 'children'),
        Output('equation_sg', 'children'),

    ],
    [
        Input("input-filter", "value"),
        Input("x-var-dropdown-choice", "value"),
        Input("y-var-dropdown-choice", "value"),
        Input("iteration_amount_sg", "value"),
        Input("learning_rate_sg", "value"),
        Input("init_w_sg", "value"),
        Input("init_b_sg", "value")
    ],
)
def create_graphs(
        input_value, x_var, y_var, iteration_amount_sg, learning_rate_sg, init_w_sg, init_b_sg
):
    df = pd.read_csv("datasets/" + input_value)
    x_column = df[x_var]
    y_column = df[y_var]
    x_var = x_var.replace("_", " ").title()
    y_var = y_var.replace("_", " ").title()

    x_column = x_column[~np.isnan(x_column)]
    y_column = y_column[~np.isnan(y_column)]
    if len(x_column) > len(y_column):
        x_column = x_column[: len(y_column)]
    elif len(y_column) > len(x_column):
        y_column = y_column[: len(x_column)]
    try:
        init_b_sg = float(init_b_sg) if init_b_sg else float(0)
        init_w_sg = float(init_w_sg) if init_w_sg else float(0)
        learning_rate_sg = (
            float(learning_rate_sg) if learning_rate_sg else 0.001
        )
        iteration_amount_sg = (
            int(iteration_amount_sg) if iteration_amount_sg else 100
        )
    except Exception as e:
        print(e)

    _, _, cost, w, b = gradient_descent_returns_weights_and_biases(
        x_column, y_column, init_w=init_w_sg, init_b=init_b_sg, alpha=learning_rate_sg, iters=iteration_amount_sg)

    regression_fig = go.Figure()
    # trace for points
    regression_fig.add_trace(go.Scatter(
        x=x_column, y=y_column, mode='markers', name="data", hovertemplate="X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>"))

    # trace for regression line at any point on the line
    start = min(x_column)
    end = max(x_column)
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
            "text": f"{x_var} vs {y_var}",
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis_title=x_var,
        yaxis_title=y_var,

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
        x=list(range(1, iteration_amount_sg + 1)), y=cost, mode='lines', name='Cost'))

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
