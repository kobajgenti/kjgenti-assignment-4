function search() {
    const query = document.getElementById('query').value;
    
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }),
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data);
        createChart(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    
    results.forEach((result, index) => {
        const resultElement = document.createElement('div');
        resultElement.innerHTML = `
            <h3>Document ${index + 1}</h3>
            <p>${result.document}</p>
            <p>Similarity: ${result.similarity.toFixed(4)}</p>
        `;
        resultsDiv.appendChild(resultElement);
    });
}

function createChart(results) {
    const similarities = results.map(result => result.similarity);
    const labels = results.map((_, index) => `Doc ${index + 1}`);

    const trace = {
        x: labels,
        y: similarities,
        type: 'bar'
    };

    const layout = {
        title: 'Document Similarities',
        xaxis: { title: 'Documents' },
        yaxis: { title: 'Cosine Similarity' }
    };

    Plotly.newPlot('chart', [trace], layout);
}