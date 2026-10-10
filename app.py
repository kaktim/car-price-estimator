"""Used-car price estimator: pick a car, get a fair-price estimate in USD$."""

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

CSV_PATH = "used-cars.csv"
FEATURES = ["brand", "model", "year", "mileage_miles", "fuel_type", "transmission"]
TARGET = "price_usd"


@st.cache_resource
def load_data_and_model():
    """Load the CSV and train the model once per app start."""
    df = pd.read_csv(CSV_PATH)
    categorical = ["brand", "model", "fuel_type", "transmission"]
    numeric = ["year", "mileage_miles"]
    preprocess = ColumnTransformer(
        [("cat", OneHotEncoder(handle_unknown="ignore"), categorical)],
        remainder="passthrough",
    )
    model = Pipeline(
        [
            ("prep", preprocess),
            ("rf", RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)),
        ]
    )
    model.fit(df[FEATURES], df[TARGET])
    return df, model


def predict_with_range(model, row_df):
    """Return (estimate, low, high) from the forest's tree predictions."""
    rf = model.named_steps["rf"]
    prepared = model.named_steps["prep"].transform(row_df)
    tree_preds = np.array([tree.predict(prepared) for tree in rf.estimators_])
    return (
        float(tree_preds.mean()),
        float(np.percentile(tree_preds, 10)),
        float(np.percentile(tree_preds, 90)),
    )


def top_factors(df, brand, year, mileage):
    """Top 3 plain-English reasons behind the price."""
    factors = []
    overall_year = df["year"].mean()
    overall_miles = df["mileage_miles"].mean()
    overall_price = df[TARGET].mean()
    factors.append(
        (
            "Low mileage added value."
            if mileage < overall_miles
            else "High mileage pulled it down.",
            abs(mileage - overall_miles) / max(overall_miles, 1),
        )
    )
    factors.append(
        (
            "Newer year added value."
            if year > overall_year
            else "Older year pulled it down.",
            abs(year - overall_year) / 20,
        )
    )
    brand_avg = df.loc[df["brand"] == brand, TARGET].mean()
    factors.append(
        (
            f"{brand} models hold value well."
            if brand_avg >= overall_price
            else f"{brand} models tend to price lower.",
            abs(brand_avg - overall_price) / max(overall_price, 1),
        )
    )
    factors.sort(key=lambda item: item[1], reverse=True)
    return [text for text, _ in factors[:3]]


def similar_listings(df, estimate, brand, model, n=3):
    """Closest-priced real listings: same model first, then same brand."""
    same_model = df[df["model"] == model].copy()
    same_model["gap"] = (same_model[TARGET] - estimate).abs()
    picks = same_model.nsmallest(n, "gap")
    if len(picks) < n:
        rest = df[(df["brand"] == brand) & (~df.index.isin(picks.index))].copy()
        rest["gap"] = (rest[TARGET] - estimate).abs()
        picks = pd.concat([picks, rest.nsmallest(n - len(picks), "gap")])
    return picks.head(n)


def money(value):
    return f"USD$ {value:,.0f}"


st.title("Used-Car Price Estimator")
st.write("Pick a car — get a fair-price estimate from 3,915 real listings (USD$).")

df, model = load_data_and_model()

brand = st.selectbox("Brand", sorted(df["brand"].unique()))
models = sorted(df.loc[df["brand"] == brand, "model"].unique())
car_model = st.selectbox("Model", models)
fuel = st.selectbox("Fuel type", sorted(df["fuel_type"].unique()))
transmission = st.selectbox("Transmission", sorted(df["transmission"].unique()))
year = st.number_input(
    "Year", min_value=int(df["year"].min()), max_value=int(df["year"].max()),
    value=2019, step=1,
)
mileage = st.number_input(
    "Mileage (miles)", min_value=int(df["mileage_miles"].min()),
    max_value=int(df["mileage_miles"].max()), value=80000, step=1000,
)

if st.button("Estimate price"):
    row = pd.DataFrame(
        [{
            "brand": brand, "model": car_model, "year": int(year),
            "mileage_miles": int(mileage), "fuel_type": fuel,
            "transmission": transmission,
        }]
    )
    estimate, low, high = predict_with_range(model, row)

    st.subheader(f"Estimated price: {money(estimate)}")
    st.write(f"Fair range: **{money(low)} – {money(high)}**")

    st.subheader("Why this price?")
    for factor in top_factors(df, brand, int(year), int(mileage)):
        st.write(f"- {factor}")

    st.subheader("Similar real listings")
    for _, car in similar_listings(df, estimate, brand, car_model).iterrows():
        st.write(
            f"- {car['brand']} {car['model']} ({int(car['year'])}, "
            f"{int(car['mileage_miles']):,} miles): {money(car[TARGET])}"
        )
