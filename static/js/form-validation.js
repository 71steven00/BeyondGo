document.addEventListener("DOMContentLoaded", function() {

    // 1. ALERTAS DE VALIDACIÓN DEL FORMULARIO DE LOGIN (Solo se ejecuta si existe #login-form)
    const form = document.getElementById('login-form');
    
    if (form) {
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
            } else if (!emailRegex.test(emailInput.value.trim())){
                event.preventDefault();
                emailError.textContent = "El correo debe ser de un dominio válido (@gmail.com o @hotmail.com).";
                emailError.classList.remove('hidden');
                emailInput.classList.add('border-red-500');
                emailInput.classList.remove('border-slate-700');
                hasError = true;
            } else {
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
        if (emailInput) {
            emailInput.addEventListener('input', function() {
                if (emailInput.value.trim()) {
                    emailError.classList.add('hidden');
                    emailInput.classList.remove('border-red-500');
                    emailInput.classList.add('border-slate-700');
                }
            });
        }

        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                if (passwordInput.value.trim()) {
                    passwordError.classList.add('hidden');
                    passwordInput.classList.remove('border-red-500');
                    passwordInput.classList.add('border-slate-700');
                }
            });
        }
    }

    // 2. MOSTRAR / OCULTAR CONTRASEÑA (OJOS)
    const togglePasswordIcons = document.querySelectorAll('.toggle-password');
    togglePasswordIcons.forEach(function(icon) {
        icon.addEventListener('click', function() {
            const inputField = this.parentElement.querySelector('input');
            if (inputField) {
                if (inputField.type === 'password') {
                    inputField.type = 'text';
                    this.classList.remove('fa-eye');
                    this.classList.add('fa-eye-slash');
                } else {
                    inputField.type = 'password';
                    this.classList.remove('fa-eye-slash');
                    this.classList.add('fa-eye');
                }
            }
        });
    });

    // 3. ALERTAS Y RESTRICCIONES DEL FORMULARIO DE REGISTRO
    const regForm = document.getElementById('register-form');
    if (regForm) {
        const regFullname = document.getElementById('fullname');
        const regFullnameError = document.getElementById('fullname-error');

        const regEmail = document.getElementById('email');
        const regEmailError = document.getElementById('email-error');

        const regPhone = document.getElementById('phone');
        const regPhoneError = document.getElementById('phone-error');

        const regCity = document.getElementById('city');
        const regCityError = document.getElementById('city-error');

        const regBirthdate = document.getElementById('birthdate');
        const regBirthdateError = document.getElementById('birthdate-error');

        const regPassword = document.getElementById('password');
        const regPasswordError = document.getElementById('password-error');

        const regConfirmPassword = document.getElementById('confirm_password');
        const regConfirmPasswordError = document.getElementById('confirm_password-error');

        const colombianCities = [
            "bogotá", "sogamoso", "tunja", "duitama", "medellín", "cali", 
            "barranquilla", "bucaramanga", "cartagena", "pereira", "manizales", 
            "cúcuta", "ibagué", "pasto", "villavicencio", "armenia", "popayán", 
            "neiva", "santa marta", "montería", "valledupar", "sincelejo"
        ];

        // Restricción en tiempo real: Celular solo dígitos y máximo 10
        if (regPhone) {
            regPhone.addEventListener('input', function() {
                this.value = this.value.replace(/\D/g, '').slice(0, 10);
            });
        }

    
    });
    

});