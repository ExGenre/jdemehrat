// main.js

document.addEventListener('DOMContentLoaded', function() {
    // Animace pro uvítání
    var welcomeText = document.getElementById('welcome-text');
    welcomeText.style.opacity = 0;

    var fadeEffect = setInterval(function () {
        if (welcomeText.style.opacity < 1) {
            welcomeText.style.opacity = parseFloat(welcomeText.style.opacity) + 0.1;
        } else {
            clearInterval(fadeEffect);
        }
    }, 100);

    // Změna textu na tlačítku
    var findButton = document.getElementById('find-button');
    findButton.addEventListener('mouseover', function() {
        findButton.innerHTML = 'Najít spoluhráče!';
    });

    findButton.addEventListener('mouseout', function() {
        findButton.innerHTML = 'Najít spoluhráče';
    });
});
