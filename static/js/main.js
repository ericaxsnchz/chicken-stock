document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('load-data-form').addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const symbol = formData.get('symbol');

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
    });

    document.getElementById('buy-form').addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const symbol = formData.get('symbol');
        const quantity = parseInt(formData.get('quantity'));

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

            const portfolioList = document.getElementById('portfolio');
            portfolioList.innerHTML = '';
            for (const [symbol, quantity] of Object.entries(data.portfolio)) {
                const listItem = document.createElement('li');
                listItem.textContent = `${symbol}: ${quantity}`;
                portfolioList.appendChild(listItem);
            }
        });
    });

    document.getElementById('sell-form').addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const symbol = formData.get('symbol');
        const quantity = parseInt(formData.get('quantity'));

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

            const portfolioList = document.getElementById('portfolio');
            portfolioList.innerHTML = ''; 
            for (const [symbol, quantity] of Object.entries(data.portfolio)) {
                const listItem = document.createElement('li');
                listItem.textContent = `${symbol}: ${quantity}`;
                portfolioList.appendChild(listItem);
            }
        });
    });
});
