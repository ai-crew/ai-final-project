from dash import dcc
from dash import html

layout = html.Div(
    [
        html.H1("Linear Regression Visualizer"),
        html.Div(
            [
                dcc.Link(
                    html.Button(
                        [
                            html.Div("Upload your own dataset", style={
                                     'font-size': '24px', 'font-weight': 'bold'}),  # Make the text larger and bold
                            html.I(className="fas fa-upload fa-5x", style={
                                   'color': 'deepskyblue', 'stroke': 'black', 'stroke-width': '1px', 'padding': '15px'}),  # Make the icon larger
                        ],
                        id="upload-button",
                        n_clicks=0,
                        style={
                            'border': '2px solid deepskyblue',
                            'border-radius': '5px',
                            'padding': '30px',
                            'background-color': 'white',
                            'text-align': 'center',
                            'margin': '1rem',
                        },
                    ),
                    href="/uploadDataset",
                ),
                dcc.Link(
                    html.Button(
                        [
                            html.Div("Select sample dataset", style={
                                     'font-size': '24px', 'font-weight': 'bold'}),  # Make the text larger and bold
                            html.I(className="fas fa-database fa-5x", style={
                                   'color': 'deepskyblue', 'stroke': 'black', 'stroke-width': '1px', 'padding': '15px'}),  # Make the icon larger
                        ],
                        id="sample-button",
                        n_clicks=0,
                        style={
                            'border': '2px solid deepskyblue',
                            'border-radius': '5px',
                            'padding': '30px',
                            'background-color': 'white',
                            'text-align': 'center',
                            'margin': '1rem',
                        },
                    ),
                    href="/sampleDataset",
                ),
            ],
            style={
                'display': 'flex',
            }
        ),
    ],
    style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'height': '100%',
        'flex-direction': 'column',
        'min-height': '80vh',
        'position': 'relative',
        'padding-bottom': '2rem',
        'box-sizing': 'border-box',
    }
)

layout.children.append(
    html.Footer(
        [
            html.A(
                [
                    html.I(className="fab fa-github fa-2x",
                           style={'color': 'black'}),
                ],
                href="https://github.com/ai-crew/ai-final-project",
                style={'text-decoration': 'none', 'padding': '1rem'}
            ),
            html.P("Group Members: Abdullah Yousuf, Ege Seyithanoglu, Ihsan Ahmed, Hussein Mohamed, and Elizabeth Aufzien",
                   style={'font-size': '12px', 'margin': '0', 'padding': '1rem'}),
        ],
        style={
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center',
            'width': '100%',
            'position': 'absolute',
            'bottom': '0',
        },
    )
)
