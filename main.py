import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import countries_df
from builders import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,700;1,400;1,700&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

bubble_map = px.scatter_geo(
    countries_df,
    size="Confirmed",
    color="Confirmed",
    hover_name="Country_Region",
    locations="Country_Region",
    locationmode="country names",
    projection="natural earth",
    hover_data={
        "Confirmed": ":,2f",
        "Deaths": ":,2f",
        "Recovered": ":,2f",
        "Country_Region": False,
    },
    size_max=50,
    template="plotly_dark",
)

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Noto Sans, sans-serif",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px", "marginBottom": 100},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})],
        ),
        html.Div(
            children=[
                html.Div(children=[dcc.Graph(id="bubble_map", figure=bubble_map)]),
                html.Div(children=[make_table(countries_df)]),
            ]
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
