document.addEventListener('DOMContentLoaded', function() {
    const chartElement = document.getElementById('chart');
    const portfolioElement = document.getElementById('portfolio');
    const balanceElement = document.getElementById('balance');

    let chart;

    async function fetchPortfolio() {
        const response = await fetch('/portfolio');
        const data = await response.json();
        updatePortfolio(data);
    }

    async function fetchBalance() {
        const response = await fetch('/balance');
        const data = await response.json();
        balanceElement.textContent = data.balance.toFixed(2);
    }

    function updatePortfolio(data) {
        portfolioElement.innerHTML = '';
        for (const [symbol, quantity] of Object.entries(data)) {
            const item = document.createElement('li');
            item.textContent = `${symbol}: ${quantity}`;
            portfolioElement.appendChild(item);
        }
    }

    async function loadChart(symbol) {
        const response = await fetch('/load_data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol }),
        });
        const data = await response.json();
        const dates = data.index;
        const closes = data.data.map(row => row[3]);

        const trace = {
            x: dates,
            y: closes,
            type: 'scatter'
        };
        const layout = {
            title: `${symbol} Historical Prices`
        };

        Plotly.newPlot(chartElement, [trace], layout);
    }

    document.getElementById('load-data-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const symbol = event.target.symbol.value;
        await loadChart(symbol);
    });

    document.getElementById('buy-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const symbol = event.target.symbol.value;
        const quantity = event.target.quantity.value;

        const response = await fetch('/buy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol, quantity }),
        });

        const data = await response.json();
        if (data.success) {
            fetchPortfolio();
            fetchBalance();
        } else {
            alert(data.message);
        }
    });

    document.getElementById('sell-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const symbol = event.target.symbol.value;
        const quantity = event.target.quantity.value;

        const response = await fetch('/sell', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol, quantity }),
        });

        const data = await response.json();
        if (data.success) {
            fetchPortfolio();
            fetchBalance();
        } else {
            alert(data.message);
        }
    });

    loadChart('AAPL');
    fetchPortfolio();
    fetchBalance();
});
