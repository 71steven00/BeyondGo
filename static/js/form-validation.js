document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('login-form');
    
    if (!form) return;

    const emailInput = document.getElementById('id_email');
    const emailError = document.getElementById('email-error');
    
    const passwordInput = document.getElementById('id_password');
    const passwordError = document.getElementById('password-error');

    form.addEventListener('submit', function(event) {
        let hasError = false;

        const emailRegex = /^[^\s@]+@(gmail\.com|hotmail\.com)$/i;

        // Validar correo
        if (!emailInput.value.trim()) {
            event.preventDefault();
            emailError.classList.remove('hidden');
            emailInput.classList.add('border-red-500');
            emailInput.classList.remove('border-slate-700');
            hasError = true;
        }else if (!emailRegex.test(emailInput.value.trim())){
            event.preventDefault();
            emailError.textContent = "El correo debe ser de un dominio válido (@gmail.com o @hotmail.com).";
            emailError.classList.remove('hidden');
            emailInput.classList.add('border-red-500');
            emailInput.classList.remove('border-slate-700');
            hasError = true;
        }else {
            emailError.classList.add('hidden');
            emailInput.classList.remove('border-red-500');
            emailInput.classList.add('border-slate-700');
        }

        // Validar contraseña
        if (!passwordInput.value.trim()) {
            event.preventDefault();
            passwordError.classList.remove('hidden');
            passwordInput.classList.add('border-red-500');
            passwordInput.classList.remove('border-slate-700');
            hasError = true;
        } else {
            passwordError.classList.add('hidden');
            passwordInput.classList.remove('border-red-500');
            passwordInput.classList.add('border-slate-700');
        }
    });

    // Limpiar alertas en tiempo real mientras el usuario escribe
    emailInput.addEventListener('input', function() {
        if (emailInput.value.trim()) {
            emailError.classList.add('hidden');
            emailInput.classList.remove('border-red-500');
            emailInput.classList.add('border-slate-700');
        }
    });

    passwordInput.addEventListener('input', function() {
        if (passwordInput.value.trim()) {
            passwordError.classList.add('hidden');
            passwordInput.classList.remove('border-red-500');
            passwordInput.classList.add('border-slate-700');
        }

    
    });

});