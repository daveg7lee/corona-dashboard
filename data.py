import pandas as pd

conditions = ["confirmed", "deaths", "recovered"]

daily_df = pd.read_csv("data/daily_report.csv")

totals_df = (
    daily_df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
)
totals_df = totals_df.rename(columns={"index": "condition"})

countries_df = daily_df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
countries_df = countries_df.groupby("Country_Region").sum().reset_index()


def make_df(condition, country=None):
    df = pd.read_csv(f"data/time_{condition}.csv")
    if country is not None:
        df = df.loc[df["Country/Region"] == country]
    df = (
        df.drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
        .sum()
        .reset_index(name=condition)
    )
    df = df.rename(columns={"index": "Date"})
    return df


def make_combined_df(country=None):
    combined_df = None
    for condition in conditions:
        condition_df = make_df(condition, country)
        if combined_df is None:
            combined_df = condition_df
        else:
            combined_df = combined_df.merge(condition_df)
    return combined_df


print(make_combined_df("Korea, South"))
