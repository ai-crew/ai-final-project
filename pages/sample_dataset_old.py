# from dash import html, dcc, callback, Input, Output
# from dash.dependencies import Input, Output
# import pandas as pd
# import dash_bootstrap_components as dbc
# from linear_regression import gradient_descent, mean_squared_error, calc_correlation_p_value, gradient_descent_returns_weights_and_biases
# import plotly.graph_objects as go
# import numpy as np

# # TODO: add links to kaggle for all datasets
# datasetList = [
#     {"label": "Car Price Data", "value": "car_price.csv"},
#     {"label": "NYSE Stock Fundamentals Data", "value": "fundamentals.csv"},
#     {"label": "NYSE Stock Prices Data", "value": "prices.csv"},
# ]

# layout = html.Div(
#     children=[
#         # Header
#         html.Div(
#             children=[
#                 html.H1("Sample Datasets"),
#                 html.P("Select a dataset to visualize"),
#             ],
#         ),
#         # Body
#         html.Div(
#             children=[
#                 html.Div(
#                     children=[
#                         html.Div("Select a Dataset",
#                                  className="menu-title"),
#                         dcc.Dropdown(
#                             id="input-filter",
#                             options=datasetList,
#                             value="car_price.csv",
#                             clearable=False,
#                         ),
#                     ]
#                 ),
#                 html.Div(
#                     style={
#                         "display": "flex",
#                         "width": "100%",
#                         "margin": "0 auto",
#                         "align-items": "center",
#                         "text-align": "center",
#                         "padding-top": "1rem",
#                     },
#                     children=[
#                         html.Span(
#                             style={"flex": "1"},
#                             children=[
#                                 html.Div(children="X variable",
#                                          className="menu-title"),
#                                 dcc.Dropdown(
#                                     id="x-var-dropdown-choice",
#                                     options=datasetList,
#                                     clearable=False,
#                                     searchable=True,
#                                 ),
#                             ],
#                         ),
#                         html.Span(
#                             style={"flex": "1"},
#                             children=[
#                                 html.Div("Y variable",
#                                          className="menu-title"),
#                                 dcc.Dropdown(
#                                     id="y-var-dropdown-choice",
#                                     options=datasetList,
#                                     clearable=False,
#                                     searchable=True,
#                                 ),
#                             ],
#                         ),
#                     ],
#                 ),
#                 html.Div(
#                     dbc.Col(
#                         [
#                             dbc.InputGroup(
#                                 [
#                                     dbc.InputGroupText("Learning Rate"),
#                                     dbc.Input(
#                                         id="learning_rate",
#                                         type="number",
#                                         value=0.002,
#                                         step=0.001,
#                                         max=0.01,
#                                     ),
#                                 ],
#                                 className="mb-3",
#                             ),
#                             dbc.InputGroup(
#                                 [
#                                     dbc.InputGroupText("Iteration Amount"),
#                                     dbc.Input(
#                                         id="iteration_amount",
#                                         type="number",
#                                         value=100,
#                                         min=1,
#                                         max=150,
#                                     ),
#                                 ],
#                                 className="mb-3",
#                             ),
#                         ],
#                         width="auto",
#                     ),
#                 ),
#             ],
#         ),
#         # Graph
#         html.Div(
#             children=[
#                 html.Div(
#                     children=dcc.Graph(
#                         id="relationship-chart",
#                         config={"displayModeBar": False},
#                         figure={
#                             "data": [
#                                 {
#                                     "x": 0,
#                                     "y": 0,
#                                     "type": "lines",
#                                     "hovertemplate": " Y = %{y:.2f} X + %{x:.2f}<extra></extra>",
#                                 },
#                             ],
#                             "layout": {
#                                 "title": {
#                                     "text": "Relationship between Selected Input and Time",
#                                     "x": 0.1,
#                                     "xanchor": "left",
#                                 },
#                                 "xaxis": {"fixedrange": True},
#                                 "yaxis": {
#                                     "fixedrange": True,
#                                 },
#                             },
#                         },
#                     ),
#                 ),
#             ],
#         ),
#         # Statistics
#         html.H3("Statistics"),
#         html.Div(
#             style={"display": "flex", "flexDirection": "column"},
#             children=[
#                 html.Div(
#                     style={"display": "flex",
#                            "justify-content": "space-between"},
#                     children=[

#                         html.Div(
#                             style={"flex": "1", "padding-right": "1rem"},
#                             children=[
#                                 html.Div(
#                                     children="Equation of the line",
#                                 ),
#                                 html.Div(
#                                     id="equation-relation",
#                                     style={
#                                         "background-color": "lightgrey",
#                                         "font-family": "monospace",
#                                         "padding": "0.5rem",
#                                         "border-radius": "5px",
#                                     },
#                                 ),
#                                 dcc.Clipboard(target_id="equation-relation"),
#                             ],
#                         ),
#                         html.Div(
#                             style={"flex": "1"},
#                             children=[
#                                 html.Div(
#                                     children="Pearson correlation coefficient",
#                                 ),
#                                 html.Div(
#                                     id="correlation-relation",
#                                     style={
#                                         "background-color": "lightgrey",
#                                         "font-family": "monospace",
#                                         "padding": "0.5rem",
#                                         "border-radius": "5px",
#                                     },
#                                 ),
#                                 dcc.Clipboard(
#                                     target_id="correlation-relation"),
#                             ],
#                         ),
#                     ],
#                 ),
#                 html.Div(
#                     style={"display": "flex",
#                            "justify-content": "space-between"},
#                     children=[
#                         html.Div(
#                             style={"flex": "1", "padding-right": "1rem"},
#                             children=[
#                                 html.Div(
#                                     children="P-value",
#                                 ),
#                                 html.Div(
#                                     id="pvalue-relation",
#                                     style={
#                                         "background-color": "lightgrey",
#                                         "font-family": "monospace",
#                                         "padding": "0.5rem",
#                                         "border-radius": "5px",
#                                     },
#                                 ),
#                                 dcc.Clipboard(target_id="pvalue-relation"),
#                             ],
#                         ),
#                         html.Div(
#                             style={"flex": "1"},
#                             children=[
#                                 html.Div(
#                                     children="Standard error of the estimated slope",
#                                 ),
#                                 html.Div(
#                                     id="standard_error-relation",
#                                     style={
#                                         "background-color": "lightgrey",
#                                         "font-family": "monospace",
#                                         "padding": "0.5rem",
#                                         "border-radius": "5px",
#                                     },
#                                 ),
#                                 dcc.Clipboard(
#                                     target_id="standard_error-relation"),
#                             ],
#                         ),
#                     ],
#                 ),
#                 html.Div(
#                     style={"display": "flex",
#                            "justify-content": "space-between"},
#                     children=[
#                         html.Div(
#                             style={"flex": "1", "padding-right": "1rem"},
#                             children=[
#                                 html.Div(
#                                     children="Standard error of estimated intercept",
#                                 ),
#                                 html.Div(
#                                     id="intercept_stderr-relation",
#                                     style={
#                                         "background-color": "lightgrey",
#                                         "font-family": "monospace",
#                                         "padding": "0.5rem",
#                                         "border-radius": "5px",
#                                     },
#                                 ),
#                                 dcc.Clipboard(
#                                     target_id="intercept_stderr-relation"),
#                             ],
#                         ),
#                         html.Div(
#                             style={"flex": "1"},
#                             children=[
#                                 html.Div(
#                                     children="Root-mean-squared error (RMSE)",
#                                 ),
#                                 html.Div(
#                                     id="estimate_rmse-relation",
#                                     style={
#                                         "background-color": "lightgrey",
#                                         "font-family": "monospace",
#                                         "padding": "0.5rem",
#                                         "border-radius": "5px",
#                                     },
#                                 ),
#                                 dcc.Clipboard(
#                                     target_id="estimate_rmse-relation"),
#                             ],
#                         ),
#                     ],
#                 ),
#             ],
#         ),
#         # end of statistics
#     ],
# )


# @callback(
#     Output("x-var-dropdown-choice", "options"),
#     [Input("input-filter", "value")],
# )
# def set_output_options(filename):
#     df = pd.read_csv("datasets/" + filename)
#     options = []
#     for col in df.columns:
#         if df[col].dtype == "int64" or df[col].dtype == "float64":
#             colOriginal = col
#             col = col.replace("_", " ").title()
#             options.append({"label": col, "value": colOriginal})
#     return options


# @callback(
#     Output("y-var-dropdown-choice", "options"),
#     [Input("input-filter", "value")],
# )
# def set_output_options(input_value):
#     df = pd.read_csv("datasets/" + input_value)

#     options = []
#     for col in df.columns:
#         # Only if the column contains numeric data
#         if df[col].dtype == "int64" or df[col].dtype == "float64":
#             if input_value == "housing.csv":
#                 # col is just the first name before _
#                 colOriginal = col
#                 colName = col.split("_")[0]
#                 options.append({"label": colName, "value": colOriginal})
#                 continue
#             else:
#                 colOriginal = col
#                 col = col.replace("_", " ").title()
#                 options.append({"label": col, "value": colOriginal})
#     return options


# # If no options have been selected for the dropdown menu, select any two options at random
# @callback(
#     Output("x-var-dropdown-choice", "value"),
#     [Input("x-var-dropdown-choice", "options")],
# )
# def set_output_value(available_options):
#     if available_options:
#         return available_options[0]["value"]
#     else:
#         return None


# @callback(
#     Output("y-var-dropdown-choice", "value"),
#     [Input("y-var-dropdown-choice", "options")],
# )
# def set_output_value(available_options):
#     if available_options:
#         return available_options[1]["value"]
#     else:
#         return None


# @callback(
#     Output("relationship-chart", "figure"),
#     [
#         Input("input-filter", "value"),
#         Input("x-var-dropdown-choice", "value"),
#         Input("y-var-dropdown-choice", "value"),
#         Input("iteration_amount", "value"),
#         Input("learning_rate", "value"),
#     ],
# )
# def set_chart(input_value, x_var, y_var, iterations, learning_rate):
#     df = pd.read_csv("datasets/" + input_value)
#     x_column = df[x_var]
#     y_column = df[y_var]
#     x_var = x_var.replace("_", " ").title()
#     y_var = y_var.replace("_", " ").title()
#     df = pd.read_csv("datasets/" + input_value)

#     # remove nan values and the corresponding y values
#     x_column = x_column[~np.isnan(x_column)]
#     y_column = y_column[~np.isnan(y_column)]

#     # Fix the columns so they are the same length
#     if len(x_column) > len(y_column):
#         x_column = x_column[: len(y_column)]
#     elif len(y_column) > len(x_column):
#         y_column = y_column[: len(x_column)]

#     _, _, _, slope, intercept = gradient_descent_returns_weights_and_biases(
#         x_column, y_column, learning_rate, iterations)

#     # Calculate the Pearson correlation coefficient and p-value
#     correlation_coefficient, p_value = calc_correlation_p_value(
#         x_column, y_column)

#     # Calculate the standard error
#     mse = mean_squared_error(y_column, slope * x_column + intercept)
#     std_err = np.sqrt(mse / (len(y_column) - 2))

#     line = slope * x_column + intercept

#     # Plot data points
#     fig = go.Figure()
#     fig.add_trace(
#         go.Scatter(x=x_column, y=y_column, mode='markers', name='data', marker=dict(color='deepskyblue')))
#     fig.add_trace(
#         go.Scatter(
#             x=x_column,
#             y=line,
#             mode="lines",
#             name="Regression Line",
#             line=dict(color="red", dash="dash"),
#         )
#     )

#     fig.update_layout(
#         title={
#             "text": "Relationship between " + x_var + " and " + y_var,
#             "x": 0.1,
#             "xanchor": "left",
#         },
#         xaxis_title=x_var,
#         yaxis_title=y_var,
#     )
#     return fig


# @callback(
#     [
#         Output("equation-relation", "children"),
#         Output("correlation-relation", "children"),
#         Output("pvalue-relation", "children"),
#         Output("standard_error-relation", "children"),
#         Output("intercept_stderr-relation", "children"),
#         Output("estimate_rmse-relation", "children"),
#     ],
#     [
#         Input("input-filter", "value"),
#         Input("x-var-dropdown-choice", "value"),
#         Input("y-var-dropdown-choice", "value"),
#         Input("iteration_amount", "value"),
#         Input("learning_rate", "value"),
#     ],
# )
# def set_equation(
#     input_value, x_var, y_var, iteration_amount, learning_rate
# ):
#     df = pd.read_csv("datasets/" + input_value)
#     x_column = df[x_var]
#     y_column = df[y_var]
#     x_var = x_var.replace("_", " ").title()
#     y_var = y_var.replace("_", " ").title()
#     df = pd.read_csv("datasets/" + input_value)

#     # remove nan values and the corresponding y values
#     import numpy as np

#     x_column = x_column[~np.isnan(x_column)]
#     y_column = y_column[~np.isnan(y_column)]
#     # Fix the columns so they are the same length
#     if len(x_column) > len(y_column):
#         x_column = x_column[: len(y_column)]
#     elif len(y_column) > len(x_column):
#         y_column = y_column[: len(x_column)]

#     if learning_rate is not None and iteration_amount is not None:
#         res_x, res_y, costs = gradient_descent(
#             x_column, y_column, learning_rate, iteration_amount
#         )
#         slope = res_x[-1]
#         intercept = res_y[-1]

#     # Calculate additional model statistics
#     y_predicted_estimate = slope * x_column + intercept
#     rmse = mean_squared_error(y_column, y_predicted_estimate)
#     correlation, pvalue = calc_correlation_p_value(x_column, y_column)
#     std_err = np.sqrt(
#         np.sum(np.square(y_predicted_estimate - y_column)) /
#         (len(y_column) - 2)
#     )
#     intercept_err = std_err * np.sqrt(
#         (1 / len(x_column))
#         + (np.mean(x_column) ** 2 / np.sum((x_column - np.mean(x_column)) ** 2))
#     )

#     # Format the output strings
#     equation_str = f"y = {slope:.2f}x + {intercept:.2f}"
#     correlation_str = f"r = {correlation:.2f}"
#     pvalue = f"p = {pvalue:.2f}"
#     std_err = f"Standard Error = {std_err:.2f}"
#     intercept_err_str = f"Intercept Error = {intercept_err:.2f}"
#     rmse_str = f"RMSE = {rmse:.2f}"

#     return [
#         html.Div(children=equation_str),
#         html.Div(children=correlation_str),
#         html.Div(children=pvalue),
#         html.Div(children=std_err),
#         html.Div(children=intercept_err_str),
#         html.Div(children=rmse_str),
#     ]
