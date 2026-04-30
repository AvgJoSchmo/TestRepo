from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@dataclass
class Listing:
    source: str
    title: str
    price: float
    shipping: float
    url: str


@dataclass
class ProductTrend:
    id: str
    name: str
    category: str
    difficulty: int  # 1-5 stars
    image: str
    buy_min: float
    buy_max: float
    sell_min: float
    sell_max: float
    suggested_qty: int
    listings: List[Listing]

    @property
    def avg_buy(self) -> float:
        return (self.buy_min + self.buy_max) / 2

    @property
    def avg_sell(self) -> float:
        return (self.sell_min + self.sell_max) / 2

    @property
    def projected_profit_per_unit(self) -> float:
        return self.avg_sell - self.avg_buy

    @property
    def projected_total_profit(self) -> float:
        return self.projected_profit_per_unit * self.suggested_qty


# Demo data. Replace this with live crawler/API integration.
TRENDS: List[ProductTrend] = [
    ProductTrend(
        id="wireless-earbuds",
        name="Wireless Earbuds",
        category="Electronics",
        difficulty=2,
        image="https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&auto=format&fit=crop&q=60",
        buy_min=18,
        buy_max=32,
        sell_min=39,
        sell_max=59,
        suggested_qty=15,
        listings=[
            Listing("eBay", "New Bluetooth Earbuds", 21.99, 4.99, "https://www.ebay.com"),
            Listing("AliExpress", "TWS Earbuds Pack", 18.20, 2.50, "https://www.aliexpress.com"),
            Listing("Amazon", "Wireless Earbuds", 29.99, 0, "https://www.amazon.com"),
        ],
    ),
    ProductTrend(
        id="vintage-jacket",
        name="Vintage Denim Jacket",
        category="Fashion",
        difficulty=3,
        image="https://images.unsplash.com/photo-1542272604-787c3835535d?w=500&auto=format&fit=crop&q=60",
        buy_min=20,
        buy_max=45,
        sell_min=60,
        sell_max=120,
        suggested_qty=8,
        listings=[
            Listing("Poshmark", "Levi's Denim Jacket", 35.00, 7.99, "https://poshmark.com"),
            Listing("eBay", "Vintage Jacket Lot", 28.00, 8.50, "https://www.ebay.com"),
            Listing("Depop", "90s Denim Jacket", 40.00, 6.00, "https://www.depop.com"),
        ],
    ),
    ProductTrend(
        id="collectible-cards",
        name="Collectible Trading Cards",
        category="Collectibles",
        difficulty=5,
        image="https://images.unsplash.com/photo-1613771404721-1f92d799e49f?w=500&auto=format&fit=crop&q=60",
        buy_min=120,
        buy_max=260,
        sell_min=220,
        sell_max=520,
        suggested_qty=3,
        listings=[
            Listing("TCGPlayer", "Sealed Booster Box", 180.00, 0, "https://www.tcgplayer.com"),
            Listing("eBay", "Rare Card Auction", 145.00, 12.00, "https://www.ebay.com"),
            Listing("Mercari", "Card Lot", 130.00, 10.00, "https://www.mercari.com"),
        ],
    ),
]


@app.route("/")
def index():
    categories = sorted({p.category for p in TRENDS})
    return render_template("index.html", categories=categories)


@app.route("/api/trends")
def trends():
    category = request.args.get("category", "All")
    difficulty = request.args.get("difficulty", "All")

    items = TRENDS
    if category != "All":
        items = [p for p in items if p.category == category]

    if difficulty != "All":
        level = int(difficulty)
        items = [p for p in items if p.difficulty == level]

    payload = []
    for p in items:
        row = asdict(p)
        row["avg_buy"] = round(p.avg_buy, 2)
        row["avg_sell"] = round(p.avg_sell, 2)
        row["projected_profit_per_unit"] = round(p.projected_profit_per_unit, 2)
        row["projected_total_profit"] = round(p.projected_total_profit, 2)
        payload.append(row)

    return jsonify(payload)


if __name__ == "__main__":
    app.run(debug=True)
