# PRD: Used-Car Price Estimator

## Problem
Used-car buyers and small sellers guess at fair prices. Listings vary widely for similar cars, so people overpay or underprice without a data-backed reference.

## Who it's for
- Class project users (Session 2): anyone buying or selling a used car who wants a quick, honest price check.
- Beginner-friendly: no car expertise needed.

## Goals
1. User enters brand, model, year, mileage, fuel type, and transmission, and gets a fair-price estimate in US dollars (USD, $) from real listings in `used-cars.csv`.
2. Show a low–high price range, not just one number, so the estimate is honest about uncertainty.
3. Explain the estimate in plain words (e.g. low mileage added value) with a few similar real listings to sanity-check against.

## In scope
- Web page that runs locally and later on Railway with a public link.
- Inputs limited to the dataset's real columns: brand, model, year, mileage, fuel type, transmission.
- Estimate (USD) + range + top reasons + 3 similar real listings.
- Sensible behavior on unusual inputs (very old car, very high mileage still returns a low but reasonable estimate with a note).

## Out of scope
- Live market data or dealer integrations.
- Accident history, title status, color, location, or condition photos (dataset has them but v1 keeps inputs simple).
- User accounts, saved searches, or price negotiation features.

## How we'll know it works
- A 2023 BMW with 20,000 miles estimates high; a 2008 Ford with 200,000 miles estimates low.
- Adding 50,000 miles to the same car lowers the estimate.
- The range always brackets the single estimate, and the 3 similar listings are visibly close in model and price.
- App opens in a browser locally and the same code deploys to Railway.
