const resultsEl = document.getElementById('results');
const categoryFilter = document.getElementById('categoryFilter');
const difficultyFilter = document.getElementById('difficultyFilter');

const stars = (n) => '★'.repeat(n) + '☆'.repeat(5 - n);

function listingRow(listing, buyMin, buyMax) {
  const withinRange = listing.price >= buyMin && listing.price <= buyMax;
  return `<li>
    <a href="${listing.url}" target="_blank" rel="noopener noreferrer">${listing.source}</a>
    — ${listing.title} | $${listing.price.toFixed(2)} + $${listing.shipping.toFixed(2)} shipping
    ${withinRange ? '<strong>(Matches buy range)</strong>' : ''}
  </li>`;
}

function card(item) {
  return `
    <article class="card">
      <div class="card-top">
        <div class="image-wrap">
          <img src="${item.image}" alt="${item.name}" />
          <div class="difficulty" title="Difficulty">${stars(item.difficulty)}</div>
        </div>
        <div class="price-panel">
          <h2>${item.name} <small>(${item.category})</small></h2>
          <div class="price-box"><strong>Buy Range:</strong> $${item.buy_min} - $${item.buy_max}</div>
          <div class="price-box"><strong>Sell Range:</strong> $${item.sell_min} - $${item.sell_max}</div>
          <div class="price-box"><strong>Suggested Qty:</strong> ${item.suggested_qty}</div>
          <div class="price-box"><strong>Projected Profit / Unit:</strong> $${item.projected_profit_per_unit}</div>
          <div class="price-box"><strong>Projected Total Profit:</strong> $${item.projected_total_profit}</div>
        </div>
      </div>
      <div class="listings">
        <h3>Clickable matching marketplaces</h3>
        <ul>${item.listings.map((x) => listingRow(x, item.buy_min, item.buy_max)).join('')}</ul>
      </div>
    </article>
  `;
}

async function load() {
  const query = new URLSearchParams({
    category: categoryFilter.value,
    difficulty: difficultyFilter.value,
  });
  const res = await fetch(`/api/trends?${query}`);
  const data = await res.json();

  if (!data.length) {
    resultsEl.innerHTML = '<p>No products match this filter.</p>';
    return;
  }

  resultsEl.innerHTML = data.map(card).join('');
}

categoryFilter.addEventListener('change', load);
difficultyFilter.addEventListener('change', load);
load();
