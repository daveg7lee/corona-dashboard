import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import countries_df, totals_df
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
    color_continuous_scale=px.colors.sequential.Oryel,
    hover_data={
        "Confirmed": ":,2f",
        "Deaths": ":,2f",
        "Recovered": ":,2f",
        "Country_Region": False,
    },
    size_max=50,
    title="Confirmed By Country",
    template="plotly_dark",
)
bubble_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))

bars = px.bar(
    totals_df,
    x="condition",
    y="count",
    template="plotly_dark",
    title="Total Global Cases",
    hover_data={"condition": False, "count": ":,"},
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
        html.Div(children=[html.Div(children=[dcc.Graph(id="Bar", figure=bars)])]),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
