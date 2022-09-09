from random import seed
from random import randint

import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

import sorting_steps

seed(1)
ARRARY_LEN = 60 # A random array of ARRARY_LEN integers to be sorted
array = [randint(0, 50 * ARRARY_LEN) for _ in range(ARRARY_LEN)]
base_list = [i+1 for i in range(ARRARY_LEN)] # Bar diagram base coordiante

method_lists = {'Merge Sort': sorting_steps.merge_sort_steps,
                'Bubble Sort': sorting_steps.bubble_sort_steps}

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Comfortaa:wght@500&family=Lato&display=swap",
        "rel": "stylesheet",
    }
]

app = Dash(__name__)
server = app.server
app.title = "Sorting Algorithm Visualization."

#===============================================================================
# Layout of the website.
#===============================================================================
app.layout = html.Div(children = [
    html.Div(
        children = [
            dcc.Dropdown(
                id="sorting_method",
                options=[
                    {"label": "Merge Sort", "value": "Merge Sort"},
                    {"label": "Bubble Sort", "value": "Bubble Sort"},
                ],
                placeholder = "Select a sorting algorithm",
                value = "Merge Sort",
                className="dropdown",
            ),
            html.Div(
                children=[html.P(" * If an animation is running, stop the animation \
                first before play a different algorithm.")],
                className="remark",
            ),
        ],
        className = "menu"
    ), # Select menu
    html.Div(
        children = [
            html.Div(dcc.Graph(id="sorting_illustration"), className="card")
        ],
        className="wrapper"
    ), # Graph dash_html_components
])

#===============================================================================
# Code for the callback function, which generates the animation.
#
# See https://dash.plotly.com/basic-callbacks for basic Dash callbacks
# Some examples of animation using plotly: https://plotly.com/python/animations/
#===============================================================================

@app.callback(
    Output(component_id="sorting_illustration", component_property="figure"),
    Input(component_id="sorting_method", component_property="value")
)
def generate_animated_figure(sort_method):
    steps = method_lists[sort_method](array) # run sorting_steps.sort_method(array)
    fig = go.Figure(
        data=[go.Bar(x=base_list, y = array[:], width=0.7),],
        layout=go.Layout(
            updatemenus=[
                dict(type="buttons",
                    buttons=[dict(label="Play",
                                 method="animate",
                                 args=[None,
                                       {"frame": {"duration": 1},
                                        "transition": {"duration": 0.5},
                                        "mode": "immediate",
                                       },
                                      ],
                                 ),
                             dict(label="Stop",
                                         method="animate",
                                         args=['null',
                                               {
                                                "mode": "immediate",
                                               },
                                              ],
                                         ),
                            ],
                ),
            ],
            height=500),
        frames=[go.Frame(data=go.Bar(x=base_list, y=step)) for step in steps],
        layout_yaxis_range=[0, 3100],
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=False)
