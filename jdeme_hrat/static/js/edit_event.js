function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Uložení CSRF tokenu do proměnné
const csrftoken = getCookie('csrftoken');


document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('editEventForm').addEventListener('submit', function(event) {
        event.preventDefault();  // Zabránit klasickému odeslání formuláře
        const eventId = getEventIdFromUrl();

        let formData = new FormData(event.target);  // Vytvoření FormData objektu z formuláře

        fetch(`/api/events/${eventId}/`, {  // Předpokládá se, že máte endpoint pro editaci události
            method: 'PUT',  // Použití metody PUT pro úpravu
            headers: {
                'X-CSRFToken': csrftoken,  // CSRF token pro Django
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Úspěšně upravena událost:', data);
            window.location.href = '/event-detail/' + eventId; // Přesměrování na stránku detailu události
        })
        .catch(error => {
            console.error('Chyba při úpravě události:', error);
        });
    });
});

function getEventIdFromUrl() {
    const path = window.location.pathname;
    const pathParts = path.split('/');
    return pathParts[pathParts.length - 2];
}


document.addEventListener('DOMContentLoaded', function() {
    const eventId = getEventIdFromUrl(); // Funkce pro získání ID události z URL
    fetch(`/api/events/${eventId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('nazev').value = data.nazev;
            document.getElementById('popis').value = data.popis;
            document.getElementById('hra').value = data.hra;
            document.getElementById('misto').value = data.misto;
            document.getElementById('ucast_limit').value = data.ucast_limit;
            //document.getElementById('datum_konani').value = data.datum_konani;
            //document.getElementById('image').value = data.image;

        });
});

function getEventIdFromUrl() {
    const path = window.location.pathname;
    const pathParts = path.split('/');
    return pathParts[pathParts.length - 2]; // Předpokládáme, že ID je předposlední část cesty
}

// Funkce pro zobrazení modálního okna pro editaci události
document.getElementById('showeditEventForm').addEventListener('click', () => {
    document.getElementById('editEventForm').classList.remove('hidden');
});

// Funkce pro skrytí modálního okna pro editaci události
document.getElementById('closeeditEventForm').addEventListener('click', () => {
    document.getElementById('editEventForm').classList.add('hidden');
});