document.addEventListener('DOMContentLoaded', () => {
    function loadData(symbol) {
        fetch('/load_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol })
        })
        .then(response => response.json())
        .then(data => {
            const dates = data.index;
            const closes = data.data.map(row => row[3]);
            const price = data.current_price;
            const trace = {
                x: dates,
                y: closes,
                type: 'scatter'
            };
            const layout = {
                title: `${symbol} Historical Prices`
            };
            Plotly.newPlot('chart', [trace], layout);

            document.getElementById('stock-price').value = `$${price.toFixed(2)}`;
        })
        .catch(error => console.error('Error:', error));
    }

    function handleBuy(event) {
        event.preventDefault();
        const symbol = document.getElementById('buy-symbol').value;
        const quantity = parseInt(document.getElementById('buy-quantity').value);
    
        fetch('/buy', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol, quantity })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
            } else {
                updateBalance(data.balance);
                updatePortfolioTable(data.portfolio);
                fetchPortfolioValue();
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function handleSell(event) {
        event.preventDefault();
        const symbol = document.getElementById('sell-symbol').value;
        const quantity = parseInt(document.getElementById('sell-quantity').value);

        fetch('/sell', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol, quantity })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
            } else {
                updateBalance(data.balance);
                updatePortfolioTable(data.portfolio);
                fetchPortfolioValue();
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function fetchPortfolioValue() {
        fetch('/portfolio_value')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Error:', data.error);
                } else {
                    updatePortfolioChart(data.portfolio_data);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    function updatePortfolioChart(portfolioData) {
        const dates = portfolioData.index;
        const values = portfolioData.data.map(value => parseFloat(value.replace(/[^\d.-]/g, '')));
        const formattedValues = values.map(value => value.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
    
        const trace = {
            x: dates,
            y: formattedValues,
            type: 'scatter',
            mode: 'lines+markers',
            line: { shape: 'linear' },
            name: 'Portfolio Value'
        };
    
        const layout = {
            title: 'Daily Portfolio Value',
            xaxis: {
                title: 'Date',
                type: 'date',
                tickformat: '%Y-%m-%d'
            },
            yaxis: {
                title: 'Portfolio Value',
                tickformat: '$,.2f'
            }
        };
    
        Plotly.newPlot('portfolio-value-chart', [trace], layout);
    }

    function updateBalance(balance) {
        document.getElementById('balance').innerText = `$${balance.toFixed(2)}`;
    }
    
    function updatePortfolioTable(portfolio) {
        const tbody = document.querySelector('#portfolioTable tbody');
        tbody.innerHTML = '';
        for (const [symbol, quantity] of Object.entries(portfolio)) {
            const row = tbody.insertRow();
            const cell1 = row.insertCell(0);
            const cell2 = row.insertCell(1);
            cell1.innerText = symbol;
            cell2.innerText = quantity;
        }
    }

    document.getElementById('buy-form').addEventListener('submit', handleBuy);
    document.getElementById('sell-form').addEventListener('submit', handleSell);
    document.getElementById('load-data-form').addEventListener('submit', (event) => {
        event.preventDefault();
        const symbol = document.querySelector('input[name="symbol"]').value;
        loadData(symbol);
    });
    fetchPortfolioValue();
});
