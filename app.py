import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
## dash version 1.19.0 (Dash 2.0 has different import statements)

#from random import seed
from random import randint
import sorting_steps

#seed(1)

n = 50
array = [randint(0, 50*n) for _ in range(n)]
base_list = [i+1 for i in range(n)]

method_lists = {'Merge Sort': sorting_steps.merge_sort_steps,
                'Bubble Sort': sorting_steps.bubble_sort_steps}

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Comfortaa:wght@500&family=Lato&display=swap",
        "rel": "stylesheet",
    }
]

app = dash.Dash(__name__)
app.title = "Sorting Algorithm Visualization."

app.layout = html.Div(children = [
    # html.Div(
    #     children = [
    #                 html.H1(children="Sorting Algorithm Visualization",
    #                 className="header-title")
    #                 ],
    #     className = "header",
    # ), ## header
    html.Div(
        children = [
    #        html.Div(
    #            children= [html.P("Select a sorting algorithm and play. "),],
    #            className="menu-title"),
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
    ), ## select menu
    html.Div(
        children = [
            html.Div(dcc.Graph(id="sorting_illustration"), className="card")
        ],
        className="wrapper"
    ), ## Graph dash_html_components
])

@app.callback(
    Output(component_id="sorting_illustration", component_property="figure"),
    Input(component_id="sorting_method", component_property="value")
)
def update_graph_title(sort_method):
    steps = method_lists[sort_method](array)
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
        layout_yaxis_range=[0, 2600],
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
