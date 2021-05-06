import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from data import countries_df, totals_df, dropdown_options, make_combined_df
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
    labels={"condition": "Condition", "count": "Count", "color": "Condition"},
)

bars.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])


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
            style={
                "display": "grid",
                "gap": 20,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[dcc.Graph(id="bubble_map", figure=bubble_map)],
                ),
                html.Div(children=[make_table(countries_df)]),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 30,
                "gridTemplateColumns": "repeat(3, 1fr)",
            },
            children=[
                html.Div(children=[dcc.Graph(id="Bar", figure=bars)]),
                html.Div(
                    style={"grid-column": "span 2"},
                    children=[
                        dcc.Dropdown(
                            id="country",
                            options=[
                                {"label": country, "value": country}
                                for country in dropdown_options
                            ],
                        ),
                        dcc.Graph(id="country_graph"),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(Output("country_graph", "figure"), [Input("country", "value")])
def update(value):
    df = make_combined_df()
    fig = px.line(
        df,
        x="Date",
        y=["confirmed", "deaths", "recovered"],
        template="plotly_dark",
        labels={"value": "Cases", "variable": "Condition", "date": "Date"},
        hover_data={"value": ":,", "variable": False},
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig["data"][0]["line"]["color"] = "#e74c3c"
    fig["data"][1]["line"]["color"] = "#8e44ad"
    fig["data"][2]["line"]["color"] = "#27ae60"
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
