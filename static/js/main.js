document.addEventListener('DOMContentLoaded', () => {
    const balanceElement = document.getElementById('balance');
    const portfolioElement = document.getElementById('portfolio');
    const chartElement = document.getElementById('chart');

    const fetchPortfolio = async () => {
        const response = await fetch('/portfolio');
        const data = await response.json();
        balanceElement.textContent = data.balance.toFixed(2);
        portfolioElement.innerHTML = '';
        for (const [symbol, quantity] of Object.entries(data.portfolio)) {
            const li = document.createElement('li');
            li.textContent = `${symbol}: ${quantity}`;
            li.addEventListener('click', () => loadChart(symbol));
            portfolioElement.appendChild(li);
        }
    };

    const loadChart = async (symbol) => {
        try {
            const response = await fetch('/load_data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symbol }),
            });
            if (response.ok) {
                const stockData = await response.json();
                const dates = stockData.index;
                const closes = stockData.data.map(row => row[3]);  // Assuming 'Close' is the 4th column

                const trace = {
                    x: dates,
                    y: closes,
                    type: 'scatter'
                };
                const layout = {
                    title: `${symbol} Historical Prices`
                };
                Plotly.newPlot(chartElement, [trace], layout);
            } else {
                const errorData = await response.json();
                alert(errorData.message);
            }
        } catch (error) {
            console.error("Error loading chart data:", error);
        }
    };

    document.getElementById('load-data-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const symbol = event.target.symbol.value;
        loadChart(symbol);
    });

    document.getElementById('buy-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const symbol = event.target.symbol.value;
    const quantity = event.target.quantity.value;
    console.log("Sending buy request:", { symbol, quantity });  // Debugging line

    const response = await fetch('/buy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol, quantity }),
    });

    const data = await response.json();
    if (data.success) {
        fetchPortfolio();
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
        } else {
            alert(data.message);
        }
    });

    fetchPortfolio();
});
