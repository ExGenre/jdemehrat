// Bere ID z poslední části cesty před lomítkem
function getEventIdFromUrl() {
    const path = window.location.pathname;
    const pathParts = path.split('/');
    return pathParts[pathParts.length - 2];
}
// načtení detailů události
function loadEventDetails(eventId) {
    fetch(`/api/events/${eventId}/`) // Upravte URL podle vaší API cesty
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(eventData => {
        document.querySelector('.event-detail-card .event-image').style.backgroundImage = `url('${eventData.image}')`;
        document.getElementById('eventName').textContent = eventData.nazev;
        document.getElementById('eventDate').textContent = formatDateTime(eventData.datum_konani);
        document.getElementById('eventLocation').textContent = eventData.misto;
        document.getElementById('eventDescription').textContent = eventData.popis;
        const participantsList = document.getElementById('participants-list');
        // načtení seznamu účastníků
        eventData.ucastnici.forEach(participant => {
        const listItem = document.createElement('li');
        const image = document.createElement('img');
        image.src = participant.uzivatel.profile_pic; //participant.uzivatel.profileImageUrl; // Předpokládáme, že máte tuto URL
        image.className = 'participant-image';

        const name = document.createElement('span');
        name.textContent = participant.uzivatel.username;
        name.className = 'participant-name';

        listItem.appendChild(image);
        listItem.appendChild(name);

        // Přidání odkazu na profil
        const link = document.createElement('a');
        link.href = `/profile/${participant.uzivatel.id}`; // Předpokládejme, že máte tuto cestu
        link.appendChild(listItem);

        participantsList.appendChild(link);
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

// Změna datumu na uživatelský čitelný

// Přihlášení k události
function joinEvent() {
    const eventId = getEventIdFromUrl(); // Získání ID události z URL
    fetch('/api/participations/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            udalost: eventId,
        }),
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.detail || 'Chyba při přihlašování k události');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Úspěšně přihlášen k události:', data);
        showStatusMessage('Úspěšně přihlášen k události!', 'success');

        // Dynamicky přidat účastníka do seznamu
        const participantsList = document.getElementById('participants-list');
        const listItem = document.createElement('li');
        const image = document.createElement('img');
        // Předpokládáme, že `data` obsahuje URL profilového obrázku
        // Například: data.uzivatel.profile_pic, pokud API vrací objekt s URL profilového obrázku
        image.src = data.uzivatel.profile_pic; // Upravte podle vaší odpovědi z API
        image.className = 'participant-image';

        const name = document.createElement('span');
        name.textContent = data.uzivatel.username; // Změňte podle vaší odpovědi z API
        name.className = 'participant-name';

        listItem.appendChild(image);
        listItem.appendChild(name);
        participantsList.appendChild(listItem);
    })
    .catch(error => {
        console.error('Chyba:', error);
        showStatusMessage(error.message, 'error');
    });
}
// Listener na tlačítko pro přihlášení k události
document.getElementById('join-event-btn').addEventListener('click', joinEvent);

// Smazání události
function deleteEvent(eventId) {
    fetch(`/api/events/${eventId}/delete/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Chyba při mazání události.');
        }
        console.log('Událost byla úspěšně smazána.');
        window.location.href = '/events'; // Přesměrování na stránku events.html
    })
    .catch(error => {
        console.error('Chyba:', error);
        // Zobrazte chybovou zprávu
    });
}

// Listener na tlačítko pro smazání události
document.getElementById('delete-event-btn').addEventListener('click', () => {
    const eventId = getEventIdFromUrl();
    deleteEvent(eventId);
});

// Úprava události
document.getElementById('edit-event-btn').addEventListener('click', function() {
    const eventId = getEventIdFromUrl();
    window.location.href = '/edit_event/' + eventId; // Presměrování na stránku pro úpravu události
});