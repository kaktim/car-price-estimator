# FUNCTIONAL.md: Used-Car Price Estimator

Derived from `PRD.md`. No code — behavior only.

## Inputs and allowed values

All values come from the real columns in `used-cars.csv` (3,915 rows). The app only accepts combinations present in the dataset's dropdowns; free text is not allowed for brand, model, fuel, or transmission.

- **brand** (dropdown, 56 values, e.g.): Acura, Audi, BMW, Chevrolet, Ford, Honda, Hyundai, Jeep, Kia, Lexus, Mercedes-Benz, Nissan, Porsche, Subaru, Tesla, Toyota, Volkswagen, Volvo. Full list is whatever appears in the `brand` column.
- **model** (dropdown, filtered by brand): exact strings from the `model` column for the chosen brand (e.g. Toyota Camry variants, Ford F-150 variants). Model list updates when brand changes.
- **year** (number input): whole year, 1998–2024 (the dataset's min–max). Anything outside this range is rejected with a message.
- **mileage_miles** (number input): 100–300,000 miles (the dataset's min–max). Must be a non-negative whole number.
- **fuel_type** (dropdown): Diesel, E85 Flex Fuel, Gasoline, Hybrid, Plug-In Hybrid, Unknown.
- **transmission** (dropdown): exact strings from the `transmission` column (many variants, e.g. A/T, 8-Speed A/T, 6-Speed M/T, Automatic, Transmission w/Dual Shift Mode). Dropdown shows only values present in the data.

Not in v1 (per PRD): `accident_reported`, `clean_title`, color, location, photos.

## Outputs

For every valid input the app shows, in this order. All money values are in US dollars (USD, $).

1. **Estimated price** — a single US-dollar figure (USD, e.g. $14,500).
2. **Low–high range** — always brackets the estimate (e.g. $12,800–$16,200), showing uncertainty.
3. **Top 3 factors** — plain-English bullets naming what moved this price most (e.g. "Low mileage added value", "Older year pulled it down", "Brand holds value well"). Never jargon.
4. **3 similar real listings** — from `used-cars.csv`: same or similar model, closest in predicted price. Each shows brand, model, year, mileage, and actual `price_usd` (USD) so the user can sanity-check the estimate.

## Unusual inputs

- **Very old car** (e.g. year 1998–2002): still returns an estimate, biased low, with a note that few comparable listings exist so the range is wider.
- **Very high mileage** (e.g. above ~200,000 miles): still returns an estimate, pulled down, with a note that the range is wider.
- **Year or mileage outside dataset bounds** (before 1998, after 2024, negative or absurd mileage): no estimate; show "That value is outside what the app learned from" and the valid range.
- **Rare brand/model combo** (few rows in the data): still estimates, but the similar-listings section may show nearest-brand matches and says so.

## Example cars and expected behavior

1. **2023 BMW, 20,000 miles, Gasoline, 8-Speed A/T** → High estimate (upper part of the $2,000–$250,000 USD dataset range). Factors mention newness and low mileage adding value. Similar listings are recent BMWs near the estimate.
2. **2008 Ford, 200,000 miles, Gasoline, Automatic** → Low estimate (near the bottom of the range). Factors mention old year and high mileage pulling it down. Similar listings are old high-mileage Fords.
3. **Same car twice, mileage +50,000 the second time** (e.g. 2019 Toyota Camry 80,000 vs 130,000 miles, all else equal) → Second estimate is strictly lower than the first; factors call out mileage as the reason. Range shifts down with it.
