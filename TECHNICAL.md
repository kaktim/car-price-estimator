# TECHNICAL.md: Used-Car Price Estimator

Based on `PRD.md` and `FUNCTIONAL.md`. Beginner-friendly Python. No code — design only.

## Files to create

- **`app.py`** — the whole app: loads data, trains the model on startup, shows the input screen, displays estimate (USD) + range + factors + similar listings.
- **`requirements.txt`** — pinned libraries so local runs and Railway install the same thing.
- Already present: `used-cars.csv` (dataset), `PRD.md`, `FUNCTIONAL.md`, `.gitignore`, `.venv`.

## Libraries needed

- **pandas** — loads and filters `used-cars.csv`.
- **scikit-learn** — `RandomForestRegressor` learns prices from the data; also its preprocessing (`OneHotEncoder`, `ColumnTransformer`, `Pipeline`) for text columns.
- **Streamlit** — browser screen (dropdowns, number inputs, results). Version pinned in `requirements.txt`.
- Python 3.13 on Windows (project `.venv` already set up).

## Which CSV columns the model uses

- **Features (inputs to the model):** `brand`, `model`, `year`, `mileage_miles`, `fuel_type`, `transmission`.
  - Text columns (`brand`, `model`, `fuel_type`, `transmission`) are one-hot encoded; numbers (`year`, `mileage_miles`) pass through as-is.
- **Target (what it learns):** `price_usd` (US dollars).
- **Not used as features in v1:** `accident_reported`, `clean_title` (kept for display in similar listings only).
- **Similar-listings lookup** uses the raw CSV directly (same/similar model, closest predicted price), not the model.

## How the model trains when the app starts

1. App starts → `app.py` loads `used-cars.csv` with pandas (file must sit next to `app.py`).
2. Builds a scikit-learn `Pipeline`: preprocessing + `RandomForestRegressor` (a few hundred trees, fixed random seed so results are stable).
3. Trains on the full dataset in memory — takes a few seconds; the brief wait on every start is normal.
4. No saved model file in v1: retraining on each start keeps it simple and always matches the CSV.
5. Predictions: one estimate per user input. The low–high range comes from the spread of individual tree predictions (e.g. 10th–90th percentile), so it always brackets the estimate. Top-3 factors come from comparing this input against dataset averages in plain words (newer/older, lower/higher mileage, brand effect).

## Run locally on Windows

1. From the project folder, activate the venv: `.venv\Scripts\Activate.ps1`
2. Install libraries: `pip install -r requirements.txt`
3. Start the app: `streamlit run app.py`
4. Open the browser at `http://localhost:8501` (if the port is busy, run on 8502: `streamlit run app.py --server.port 8502`).
5. To stop: Ctrl+C in the terminal.

## Deploy to Railway (same app, public link)

- Push the project to a GitHub repo (code + `requirements.txt` + `app.py` + `used-cars.csv`).
- In Railway: New Project → Deploy from GitHub repo → pick the repo.
- Railway installs from `requirements.txt` automatically; the start command is:
  `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Open the Railway-generated public URL — same screen as local, now shareable.
- If the deploy fails, check the Railway build log first: usually a missing library in `requirements.txt`; add it, push again.
