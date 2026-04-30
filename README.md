# TestRepo - Trending Product Flipper

A Flask web app that displays daily trending products to buy and resell for profit.

## Features
- Category filters across product types.
- Difficulty labels from 1 to 5 stars.
- Product image on the left with difficulty overlay in the bottom-right corner.
- Buy and sell range text boxes on the right side of each image.
- Suggested quantity and projected profit calculations.
- Clickable marketplace listings with buy-range matching indicator.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install flask
python app.py
```

Then visit http://127.0.0.1:5000

## Notes
Current data is seeded in-memory for demonstration. To make this production-ready, replace `TRENDS` in `app.py` with a scheduled scraper/API pipeline that pulls fresh marketplace prices daily.
