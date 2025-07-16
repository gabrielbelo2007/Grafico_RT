const impactedTodayElement = document.getElementById('impacted-today');
const impactedTotalElement = document.getElementById('impacted-total');
const peakHourElement = document.getElementById('peak-hour'); // Novo elemento
const topZoneElement = document.getElementById('top-zone');     // Novo elemento

// URL da API do backend
const apiUrl = '<insira aqui a url do seu backend>/api/data';

async function fetchData() {
    console.log("Buscando dados atualizados...");
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        impactedTodayElement.textContent = data.impactedToday.toLocaleString('pt-BR');
        impactedTotalElement.textContent = data.impactedTotal.toLocaleString('pt-BR');
        peakHourElement.textContent = data.peakHour;
        topZoneElement.textContent = data.topZoneByPeople;

    } catch (error) {
        console.error("Erro ao buscar dados:", error);
        impactedTodayElement.textContent = "Erro";
        impactedTotalElement.textContent = "Erro";
        peakHourElement.textContent = "Erro";
        topZoneElement.textContent = "Erro";
    }
}

fetchData();

// intervalo de atualização dos dados (a fim de não sobrecarregar o servidor)
setInterval(fetchData, 1 * 60 * 1000);