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
            const trace = {
                x: dates,
                y: closes,
                type: 'scatter'
            };
            const layout = {
                title: `${symbol} Historical Prices`
            };
            Plotly.newPlot('chart', [trace], layout);
        });
    }

    function handleBuy(symbol, quantity) {
        fetch('/buy', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol, quantity })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('balance').textContent = parseFloat(data.balance).toFixed(2);

            const portfolioTable = document.getElementById('portfolio');
            const existingRow = portfolioTable.querySelector(`tr[data-symbol="${symbol}"]`);
            if (existingRow) {
                existingRow.querySelector('td:last-child').textContent = data.portfolio[symbol];
            } else {
                const newRow = document.createElement('tr');
                newRow.setAttribute('data-symbol', symbol);
                newRow.innerHTML = `<td>${symbol}</td><td>${data.portfolio[symbol]}</td>`;
                portfolioTable.querySelector('tbody').appendChild(newRow);
            }

            updatePortfolioChart();
        });
    }

    function handleSell(symbol, quantity) {
        fetch('/sell', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol, quantity })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('balance').textContent = parseFloat(data.balance).toFixed(2);

            const portfolioTable = document.getElementById('portfolio');
            const existingRow = portfolioTable.querySelector(`tr[data-symbol="${symbol}"]`);
            if (existingRow) {
                const updatedQuantity = parseInt(existingRow.querySelector('td:last-child').textContent) - quantity;
                if (updatedQuantity > 0) {
                    existingRow.querySelector('td:last-child').textContent = updatedQuantity;
                } else {
                    existingRow.remove();
                }
            }

            updatePortfolioChart();
        });
    }

    function updatePortfolioChart() {
        fetch('/portfolio_value')
            .then(response => response.json())
            .then(data => {
                const dates = data.index.map(date => new Date(date));
                const values = data.data.map(row => row[1]);
    
                const trace = {
                    x: dates,
                    y: values,
                    type: 'scatter'
                };
                const layout = {
                    title: 'Daily Portfolio Value',
                    xaxis: {
                        title: 'Date',
                        type: 'date',
                        tickformat: '%Y-%m-%d'
                    },
                    yaxis: {
                        title: 'Portfolio Value'
                    }
                };
    
                Plotly.newPlot('portfolio-value-chart', [trace], layout);
            })
            .catch(error => {
                console.error('Error fetching portfolio value data:', error);
            });
    }

    document.getElementById('load-data-form').addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const symbol = formData.get('symbol');
        loadData(symbol);
    });

    document.getElementById('buy-form').addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const symbol = formData.get('symbol');
        const quantity = parseInt(formData.get('quantity'));
        handleBuy(symbol, quantity);
    });

    document.getElementById('sell-form').addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const symbol = formData.get('symbol');
        const quantity = parseInt(formData.get('quantity'));
        handleSell(symbol, quantity);
    });

    updatePortfolioChart();
        

    const stockButtons = document.querySelectorAll('.stock-btn');
    stockButtons.forEach(button => {
        button.addEventListener('click', () => {
            const symbol = button.dataset.symbol;
            document.getElementById('buy-symbol').value = symbol;
            document.getElementById('sell-symbol').value = symbol;
        });
    });
});
