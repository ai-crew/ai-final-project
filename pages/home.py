from dash import dcc, html

# TODO: add names to group members section & brief descriptions

layout = html.Div(
    [
        html.H1("Linear Regression Visualizer"),
        html.Div(
            [
                dcc.Link(
                    html.Button(
                        [
                            html.Div("Upload your own dataset"),
                            html.I(className="fas fa-upload fa-5x"),
                        ],
                        id="upload-button",
                        n_clicks=0,
                        className="button upload-button",
                    ),
                    href="/uploadDataset",
                ),
                dcc.Link(
                    html.Button(
                        [
                            html.Div("Select sample dataset"),
                            html.I(className="fas fa-database fa-5x"),
                        ],
                        id="sample-button",
                        n_clicks=0,
                        className="button sample-button",
                    ),
                    href="/sampleDataset",
                ),
            ],
            className="button-container"
        ),
        html.Footer(
            [
                html.A(
                    [
                        html.I(className="fab fa-github fa-2x"),
                    ],
                    href="https://github.com/ai-crew/ai-final-project",
                    className="github-link"
                ),
                html.P("Group Members: TODO", className="group-members")
            ],
            className="footer"
        ),
    ],
    className="main-container"
)
