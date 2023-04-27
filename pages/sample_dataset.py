from dash import html, dcc, callback, Input, Output, State
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
from linear_regression import gradient_descent, mean_squared_error, calc_correlation_p_value, gradient_descent_returns_weights_and_biases
import plotly.graph_objects as go
import numpy as np

# TODO: add links to kaggle for all datasets
datasetList = [
    {"label": "FIFA 2022 World Cup Data", "value": "fifa.csv"},
    {"label": "Car Price Data", "value": "car_price.csv"},
    {"label": "NYSE Stock Fundamentals Data", "value": "fundamentals.csv"},
    {"label": "NYSE Stock Prices Data", "value": "prices.csv"},
]

layout = html.Div(
    children=[

        html.Div(
            children=[
                html.H1("Explore Sample Datasets",
                        style={"font-size": "2rem"}),
                html.Div(
                    html.Span(
                        "Select a dataset to explore",
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
                        html.Div("Select a Dataset",
                                 className="menu-title"),
                        dcc.Dropdown(
                            id="input-filter",
                            options=datasetList,
                            value="fifa.csv",
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
                    },
                    children=[
                        html.Span(
                            style={"flex": "1"},
                            children=[
                                html.Div("X variable",
                                         className="menu-title"),
                                dcc.Dropdown(
                                    id="x-variable-selector",
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
                                         className="menu-title"),
                                dcc.Dropdown(
                                    id="y-variable-selector",
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
                                    "label": "Customize Labels",
                                    "value": "show_label_inputs_sg",
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
                                                id="x_axis_label_sg",
                                                type="text",
                                                placeholder="Enter x-axis label",
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
                                                id="y_axis_label_sg",
                                                type="text",
                                                placeholder="Enter y-axis label",
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                    width=6,
                                    style={"display": "inline-block"},
                                ),
                            ],
                            id="show_label_inputs_sg",
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
                                    "value": "show_init_w_b_sg",
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
                            ],                     id="show_init_w_b_sg",
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
                                    max=500,
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
                                    html.H4("Statistics", style={
                                            "font-weight": "bold"}),
                                    html.Div("Equation of line", style={
                                             "font-weight": "bold"}),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                html.Div(id="equation_sg")),
                                            dbc.Col(dcc.Clipboard(
                                                target_id="equation_sg"), width=2, style={"color": "deepskyblue"})
                                        ],
                                        className="stats"
                                    ),
                                    html.Div("Weight", style={
                                             "font-weight": "bold"}),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(html.Div(id="weight_sg")),
                                            dbc.Col(dcc.Clipboard(
                                                target_id="weight_sg"), width=2, style={"color": "deepskyblue"})
                                        ],
                                        className="stats"
                                    ),
                                    html.Div("Bias", style={
                                             "font-weight": "bold"}),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(html.Div(id="bias_sg")),
                                            dbc.Col(dcc.Clipboard(
                                                target_id="bias_sg"), width=2, style={"color": "deepskyblue"})
                                        ],
                                        className="stats"
                                    ),
                                    html.Div("Final Cost", style={
                                             "font-weight": "bold"}),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(html.Div(id="cost_sg")),
                                            dbc.Col(dcc.Clipboard(
                                                target_id="cost_sg"), width=2, style={"color": "deepskyblue"})
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
                                                            "x": 0.1,
                                                            "xanchor": "left",
                                                        },
                                                        "xaxis": {"fixedrange": True},
                                                        "yaxis": {
                                                            "fixedrange": True,
                                                        },
                                                    },
                                                },
                                            ),                             className="card",
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


@ callback(
    [Output("show_label_inputs_sg", "className"),
     Output("x_axis_label_sg", "value"),
     Output("y_axis_label_sg", "value")],
    [Input("toggle_header_provided", "value"),
     Input("x-variable-selector", "value"),
     Input("y-variable-selector", "value")
     ],
)
def show_label_name_inputs(toggle_value, x_axis_label, y_axis_label):
    x_var = x_axis_label.replace("_", " ").title()
    y_var = y_axis_label.replace("_", " ").title()
    if toggle_value:
        return "padded-container", x_var, y_var
    else:
        return "hidden",  x_var, y_var


@ callback(
    [Output("show_init_w_b_sg", "className"),
     Output("init_w_sg", "value"),
     Output("init_b_sg", "value")],
    [Input("toggle_init", "value")],
    [State("init_w_sg", "value"),
     State("init_b_sg", "value")]
)
def show_init_w_b_sg(toggle_value, init_w_sg, init_b_sg):
    if toggle_value and init_w_sg and init_b_sg:
        return "padded-container", init_w_sg, init_b_sg
    else:
        return "hidden", float(0), float(0)


@ callback(
    Output("x-variable-selector", "options"),
    [Input("input-filter", "value")],
)
def set_output_options(filename):
    df = pd.read_csv("datasets/" + filename)
    options = []
    for col in df.columns:
        if df[col].dtype == "int64" or df[col].dtype == "float64":
            colOriginal = col
            col = col.replace("_", " ").title()
            options.append({"label": col, "value": colOriginal})
    return options


@ callback(
    Output("y-variable-selector", "options"),
    [Input("input-filter", "value")],
)
def set_output_options(input_value):
    df = pd.read_csv("datasets/" + input_value)

    options = []
    for col in df.columns:
        if df[col].dtype == "int64" or df[col].dtype == "float64":
            colOriginal = col
            col = col.replace("_", " ").title()
            options.append({"label": col, "value": colOriginal})
    return options


# If no options have been selected for the dropdown menu, select any two options at random
@ callback(
    Output("x-variable-selector", "value"),
    [Input("x-variable-selector", "options")],
)
def set_output_value(available_options):
    if available_options:
        return available_options[0]["value"]
    else:
        return None


@ callback(
    Output("y-variable-selector", "value"),
    [Input("y-variable-selector", "options")],
)
def set_output_value(available_options):
    if available_options:
        return available_options[1]["value"]
    else:
        return None


@ callback(
    [
        Output("regression-graph_sg", "figure"),
        Output("cost-graph_sg", "figure"),
        Output('cost_sg', 'children'),
        Output('weight_sg', 'children'),
        Output('bias_sg', 'children'),
        Output('equation_sg', 'children'),
        Output('x_axis_label_sg', 'children'),
        Output('y_axis_label_sg', 'children')

    ],
    [
        Input("input-filter", "value"),
        Input("x-variable-selector", "value"),
        Input("y-variable-selector", "value"),
        Input("iteration_amount", "value"),
        Input("learning_rate", "value"),
        Input("init_w_sg", "value"),
        Input("init_b_sg", "value")
    ],
)
def create_graphs(
    input_value, x_var, y_var, iteration_amount, learning_rate, init_w_sg, init_b_sg
):
    df = pd.read_csv("datasets/" + input_value)
    x_column = df[x_var]
    y_column = df[y_var]
    x_var = x_var.replace("_", " ").title()
    y_var = y_var.replace("_", " ").title()
    df = pd.read_csv("datasets/" + input_value)

    # remove nan values and the corresponding y values
    import numpy as np

    x_column = x_column[~np.isnan(x_column)]
    y_column = y_column[~np.isnan(y_column)]
    # Fix the columns so they are the same length
    if len(x_column) > len(y_column):
        x_column = x_column[: len(y_column)]
    elif len(y_column) > len(x_column):
        y_column = y_column[: len(x_column)]
    try:
        init_b_sg = float(init_b_sg) if init_b_sg else float(0)
        init_w_sg = float(init_w_sg) if init_w_sg else float(0)
        learning_rate = float(learning_rate) if learning_rate else float(0.001)
        iteration_amount = int(
            iteration_amount) if iteration_amount else int(100)
    except Exception as e:
        print(e)

    _, _, cost, w, b = gradient_descent_returns_weights_and_biases(
        x_column, y_column, init_w=init_w_sg, init_b=init_b_sg, alpha=learning_rate, iters=iteration_amount)

    regression_fig = go.Figure()
    # trace for points
    regression_fig.add_trace(go.Scatter(
        x=x_column, y=y_column, mode='markers',  name="data",   hovertemplate="X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>"))

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
        x=list(range(1, iteration_amount+1)), y=cost, mode='lines', name='Cost'))

    w_rounded = round(w, 3)
    b_rounded = round(b, 3)

    return [
        regression_fig,
        cost_fig,
        html.Div(children=cost[-1]),
        html.Div(children=w),
        html.Div(children=b),
        html.Div(children=[dcc.Markdown(
            f"y = **{w_rounded}**x + **{b_rounded}**")]),
        html.Div(children=x_var),
        html.Div(children=y_var)

    ]
