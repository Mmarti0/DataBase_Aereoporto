document.getElementById('searchButton').addEventListener('click', async () => {
    const departure = document.getElementById('departure_airport').value;
    const arrival = document.getElementById('arrival_airport').value;
    const date = document.getElementById('flight_date').value;
    const time = document.getElementById('start_time').value;

    // Invio dei dati al server
    const response = await fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ departure, arrival, date, time })
    });

    const flights = await response.json();

    // Mostra i risultati
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = flights.length
        ? flights.map(f => `<p>${f.departure_time} - ${f.arrival_time}: ${f.departure_airport} -> ${f.arrival_airport}</p>`).join('')
        : '<p>Nessun volo trovato.</p>';
});
