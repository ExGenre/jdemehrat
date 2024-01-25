//document.addEventListener('DOMContentLoaded', function() {
    // Získání ID události z URL
//    const urlParams = new URLSearchParams(window.location.search);
//    const eventId = urlParams.get('id');

    // Načtení detailů události z API
//    fetch(`/api/events/${eventId}`)
//    .then(response => response.json())
//    .then(eventData => {
        // Zde aktualizujte elementy na stránce s informacemi o události
//        document.getElementById('eventName').textContent = eventData.nazev;
//        document.getElementById('eventDate').textContent = eventData.datum_konani;
//        document.getElementById('eventLocation').textContent = eventData.misto;
        // Další aktualizace podle potřeby
//    })
//    .catch(error => {
//        console.error('Error:', error);
        // Zpracování chyb
//    });
//});

//document.addEventListener('DOMContentLoaded', function() {
    // Získání ID události z URL
//    const urlParams = new URLSearchParams(window.location.search);
//    const eventId = urlParams.get('id');

    // Simulace načítání dat z API pro fiktivní událost
//    if (eventId === "1") {
//        const eventData = {
//            nazev: "Testovací Událost",
//            datum_konani: "2021-01-01",
//            misto: "Virtuální Prostor"
//        };

//        document.getElementById('eventName').textContent = eventData.nazev;
//        document.getElementById('eventDate').textContent = eventData.datum_konani;
//        document.getElementById('eventLocation').textContent = eventData.misto;
//    }
//});

// Bere ID z URL
function getEventIdFromUrl() {
    const path = window.location.pathname;
    const pathParts = path.split('/');
    // Předpokládáme, že ID je poslední část cesty (například /event-detail/9/)
    return pathParts[pathParts.length - 2];
}

function loadEventDetails(eventId) {
    fetch(`/api/events/${eventId}/`) // Upravte URL podle vaší API cesty
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(eventData => {
        document.querySelector('.event-detail-card .event-image').style.backgroundImage = `url('${eventData.image_url}')`;
        document.getElementById('eventName').textContent = eventData.nazev;
        document.getElementById('eventDate').textContent = eventData.datum_konani;
        document.getElementById('eventLocation').textContent = eventData.misto;
        document.getElementById('eventDescription').textContent = eventData.popis;
        const participantsList = document.getElementById('participants-list');
        eventData.ucastnici.forEach(participant => {
            const listItem = document.createElement('li');
            listItem.textContent = participant.uzivatel.username; // Ujistěte se, že tato vlastnost existuje v datech účastníka
            participantsList.appendChild(listItem);
        });
    })

    .catch(error => {
        console.error('Chyba při načítání události:', error);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const eventId = getEventIdFromUrl();
    if (eventId) {
        loadEventDetails(eventId);
    } else {
        console.error('ID události není k dispozici');
        // Zde můžete přidat kód pro zpracování situace, kdy ID události není k dispozici
    }
});

// Přihlášení k události

//funkce POST na přihlášení


function joinEvent() {
    const eventId = getEventIdFromUrl();  // Získání ID události z URL
    fetch('/api/participations/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            udalost: eventId
        })
    })
    .then(response => {
        if (!response.ok) {
            if(response.status === 400) {
                throw new Error('Uživatel je již přihlášen k této události.');
            }
            throw new Error('Chyba při přihlašování k události');
        }
        return response.json();
    })
    .then(data => {
        console.log('Úspěšně přihlášen k události:', data);
        showStatusMessage('Úspěšně přihlášen k události!', 'success');
    })
    .catch(error => {
        console.error('Chyba:', error);
        showStatusMessage(error.message, 'error');
    });
}





document.getElementById('join-event-btn').addEventListener('click', joinEvent);


