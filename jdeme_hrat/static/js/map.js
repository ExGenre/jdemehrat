function initMap() {

    const input = document.getElementById("pac-input");
    const autocomplete = new google.maps.places.Autocomplete(input);
    const czechRepublic = {lat: 49.8175, lng: 15.4730}; // Zeměpisné souřadnice ČR

    const map = new google.maps.Map(document.getElementById("map"), {
        center: czechRepublic,
        zoom: 7, // Můžete upravit úroveň přiblížení podle potřeby
        styles: customMapStyles
    });

    let marker = new google.maps.Marker({
        map: map,
        position: czechRepublic,
    });

    // Posluchač pro autodoplňování
    autocomplete.addListener("place_changed", () => {
        marker.setVisible(false);
        const place = autocomplete.getPlace();
        if (!place.geometry || !place.geometry.location) {
            console.log("Returned place contains no geometry");
            return;
        }
        if (marker) {
            marker.setMap(null);
        }
        marker = new google.maps.Marker({
            position: place.geometry.location,
            map: map,
        });

        map.setCenter(place.geometry.location);
        map.setZoom(17);

        var latitude = place.geometry.location.lat();
        var longitude = place.geometry.location.lng();

        // Nastavení hodnot skrytých polí ve formuláři
        document.getElementById('lat').value = latitude;
        document.getElementById('lng').value = longitude;
    });

    // Posluchač pro kliknutí na mapu
    map.addListener('click', function(e) {
        if (marker) {
            marker.setMap(null);
        }
        marker = new google.maps.Marker({
            position: e.latLng,
            map: map,
        });

        // Předpokládejme, že máte skryté inputy pro lat a lng
        document.getElementById('lat').value = e.latLng.lat();
        document.getElementById('lng').value = e.latLng.lng();
    });
}

var customMapStyles = [
    {
        featureType: "poi.business",
        stylers: [{ visibility: "off" }]
    },
    {
        featureType: "poi.park",
        elementType: "labels.text",
        stylers: [{ visibility: "off" }]
    },
    {
        featureType: "poi.school",
        stylers: [{ visibility: "off" }]
    },
    {
        featureType: "poi.medical",
        stylers: [{ visibility: "off" }]
    }
];

function showModal() {
    document.getElementById("createEventModal").style.display = "block";
    google.maps.event.trigger(map, "resize"); // Zajistí správné zobrazení mapy po zobrazení modálního okna
}

function closeModal() {
    document.getElementById("createEventModal").style.display = "none";
}

function loadGoogleMapsAPI() {
    var script = document.createElement('script');
    script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyAbNGHpydoL8XiZvbXjanW4mcVT7CO9DyA&libraries=places&callback=initMap";
    document.head.appendChild(script);
}

document.addEventListener('DOMContentLoaded', function() {
    loadGoogleMapsAPI();
});
