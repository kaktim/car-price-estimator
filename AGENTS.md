# AGENTS.md — car-price-estimator

## Project
Used-car price estimator (Session 2 class project). Stack: pandas + scikit-learn (`RandomForestRegressor`) + Streamlit. Docs chain: `PRD.md` → `FUNCTIONAL.md` → `TECHNICAL.md`; keep them consistent when behavior changes.

## Environment (Windows PowerShell)
- Activate venv first: `.venv\Scripts\Activate.ps1`
- If `python` is not recognized, use `py`.
- Install: `pip install -r requirements.txt` (once `requirements.txt` exists). No packages installed yet.
- `.venv/` and `__pycache__/` are git-ignored; never commit them.

## Data and currency
- Dataset `used-cars.csv` (3,915 rows) sits next to `app.py`; the app loads it by relative path.
- Columns: `brand,model,year,mileage_miles,fuel_type,transmission,accident_reported,clean_title,price_usd`. Model features are the first six; target is `price_usd`.
- All money is US dollars (USD$). Year range 1998–2024, mileage 100–300,000.

## Run and deploy
- Local: `streamlit run app.py` → `http://localhost:8501` (port busy? use `--server.port 8502`).
- Model retrains on every startup (a few seconds) — normal, not a bug.
- Railway start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`. Deploy failures are usually a missing lib in `requirements.txt`.
- Sanity checks: 2023 BMW / 20k miles = high; 2008 Ford / 200k miles = low; +50k miles on same car must lower the estimate.

## Fix loop
When the app errors, explain cause in one plain sentence, then fix.
