// Funzione per caricare gli aeroporti dal server e popolare i menù a tendina
async function loadAirports() {
    try {
        const response = await fetch('/airports');
        const airports = await response.json();

        // Trova i menù a tendina per partenza e arrivo
        const departureSelect = document.getElementById('departure_airport');
        const arrivalSelect = document.getElementById('arrival_airport');

        // Pulisci i menù a tendina
        departureSelect.innerHTML = '';
        arrivalSelect.innerHTML = '';

        // Aggiungi le opzioni basate sugli aeroporti
        airports.forEach(airport => {
            const departureOption = document.createElement('option');
            departureOption.value = airport;
            departureOption.textContent = airport;

            const arrivalOption = document.createElement('option');
            arrivalOption.value = airport;
            arrivalOption.textContent = airport;

            departureSelect.appendChild(departureOption);
            arrivalSelect.appendChild(arrivalOption);
        });
    } catch (error) {
        console.error('Errore durante il caricamento degli aeroporti:', error);
    }
}

// Chiama la funzione al caricamento della pagina
document.addEventListener('DOMContentLoaded', loadAirports);
