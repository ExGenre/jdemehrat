document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form[action*="login"]');
    const registerForm = document.querySelector('form[action*="register"]');

    function validateForm(event) {
        let isValid = true;
        const inputs = this.querySelectorAll('input');

        inputs.forEach(input => {
            if (!input.value) {
                isValid = false;
                input.style.borderColor = 'red';
            } else {
                input.style.borderColor = '#ddd';
            }
        });

        if (!isValid) {
            event.preventDefault();
            alert('Prosím, vyplňte všechna pole.');
        }
    }

    if (loginForm) {
        loginForm.addEventListener('submit', validateForm);
    }

    if (registerForm) {
        registerForm.addEventListener('submit', validateForm);
    }
});
