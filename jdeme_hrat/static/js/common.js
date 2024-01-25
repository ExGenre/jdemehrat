
// Funkce pro přepínání viditelnosti sidebaru
function toggleSidebar() {
    var sidebar = document.querySelector('.sidebar');
    if (sidebar.style.display === 'block') {
        sidebar.style.display = 'none';
    } else {
        sidebar.style.display = 'block';
    }
}
// Funkce pro získání hodnoty cookie podle jména
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

// Funkce pro zobrazení modálního okna pro vytvoření události
document.getElementById('showCreateEventModal').addEventListener('click', () => {
    document.getElementById('createEventModal').classList.remove('hidden');
});

// Funkce pro skrytí modálního okna pro vytvoření události
document.getElementById('closeCreateEventModal').addEventListener('click', () => {
    document.getElementById('createEventModal').classList.add('hidden');
});

// Funkce pro načtení seznamu událostí z API a jejich zobrazení na stránce
function loadEvents() {
    fetch('/api/events/') // Nastavte URL pro váš API endpoint
    .then(response => response.json())
    .then(events => {
        const eventsContainer = document.getElementById('eventsContainer');
        eventsContainer.innerHTML = ''; // Vymažeme stávající obsah
        events.forEach(event => {
            // Vytvoření a přidání dlaždice události do kontejneru
            const eventTile = document.createElement('div');
            eventTile.className = 'bg-white p-4 rounded-lg shadow-md event-card';
            eventTile.innerHTML = `
                <div class="bg-cover bg-center h-32" style="background-image: url('${event.image_url}');"></div>
                <h3 class="text-lg font-semibold mt-2">${event.nazev}</h3>
                <p class="text-gray-600">${event.datum_konani} v ${event.misto}</p>
            `;
            eventTile.addEventListener('click', () => {
            window.location.href = '/event-detail/' + event.id + '/'; // Cesta k detailu události
            });
            eventsContainer.prepend(eventTile); // Přidáme dlaždici na začátek, aby nejnovější byly nahoře
        });
    })
    .catch(error => {
        console.error('Nastala chyba při načítání událostí:', error);
    });
}

// Event listener pro odeslání formuláře a vytvoření události
document.getElementById('createEventForm').addEventListener('submit', function(event) {
    event.preventDefault();
    let formData = new FormData(event.target);

    fetch('/api/events/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        loadEvents(); // Načtení všech událostí včetně nové
        document.getElementById('createEventModal').classList.add('hidden'); // Skrytí modálního okna
        showStatusMessage('Událost založena!', 'success'); // Zobrazit úspěšnou zprávu
    })
    .catch(error => {
        console.error('Error:', error);
        showStatusMessage('Chyba při vytváření události.', 'error'); // Zobrazit chybovou zprávu
    });
});

// Funkce pro zobrazení statusové zprávy
function showStatusMessage(message, type) {
    let messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageElement.style.cssText = 'position: fixed; top: 20px; left: 50%; transform: translateX(-50%); color: white; padding: 10px; border-radius: 5px; z-index: 1000;';

    // Nastavení barvy podle typu zprávy
    if (type === 'success') {
        messageElement.style.backgroundColor = '#28a745'; // Zelená pro úspěch
    } else if (type === 'error') {
        messageElement.style.backgroundColor = '#dc3545'; // Červená pro chybu
    }

    // Přidání elementu do těla dokumentu
    document.body.appendChild(messageElement);

    // Odstranění zprávy po 3 sekundách
    setTimeout(function() {
        document.body.removeChild(messageElement);
    }, 3000);
}

// Příklad fiktivní události
const dummyEvent = {
    id: "1",
    nazev: "Testovací Událost",
    datum_konani: "2021-01-01",
    misto: "Virtuální Prostor",
    image_url: "https://example.com/event.jpg"
};

// Přidání této události do DOM při načtení stránky
document.addEventListener('DOMContentLoaded', function() {
    const eventsContainer = document.getElementById('eventsContainer');

    const eventTile = document.createElement('div');
    eventTile.className = 'bg-white p-4 rounded-lg shadow-md clickable-event';
    eventTile.innerHTML = `
        <div class="bg-cover bg-center h-32" style="background-image: url('${dummyEvent.image_url}');"></div>
        <h3 class="text-lg font-semibold mt-2">${dummyEvent.nazev}</h3>
        <p class="text-gray-600">${dummyEvent.datum_konani} v ${dummyEvent.misto}</p>
    `;
    eventTile.addEventListener('click', () => {
        window.location.href = '/pythonProject/event-detail.html?id=' + dummyEvent.id; // Cesta k detailu události
    });
    eventsContainer.append(eventTile);
});
