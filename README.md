# Used-Car Price Estimator

Pick a car (brand, model, year, mileage, fuel type, transmission) and get a fair-price estimate in **USD$** learned from 3,915 real used-car listings (`used-cars.csv`).

Built with pandas + scikit-learn (`RandomForestRegressor`) + Streamlit. Session 2 class project — see `PRD.md` → `FUNCTIONAL.md` → `TECHNICAL.md` for the docs chain.

## What you get per estimate

- Estimated price (USD$) with a low–high range
- Top 3 plain-English factors behind the price (e.g. "Low mileage added value")
- 3 similar real listings to sanity-check against

## Run locally (Windows PowerShell)

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` (first load takes a few seconds — the model trains on startup, which is normal).

## Deploy to Railway

Push this repo to GitHub, then in Railway: New Project → Deploy from GitHub repo. Start command:

```
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

## Sanity checks

- 2023 BMW, 20,000 miles → high price
- 2008 Ford, 200,000 miles → low price
- Same car + 50,000 miles → price drops
