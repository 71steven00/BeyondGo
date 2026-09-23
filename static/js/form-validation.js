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

        regForm.addEventListener('submit', function(event) {
            let hasRegError = false;
            const emailRegex = /^[^\s@]+@(gmail\.com|hotmail\.com)$/i;
            const phoneRegex = /^3\d{9}$/;

            // 1. Validar Nombre Completo
            if (!regFullname.value.trim()) {
                event.preventDefault();
                regFullnameError.textContent = "Ingresa tu nombre completo.";
                regFullnameError.classList.remove('hidden');
                regFullname.classList.add('border-red-500');
                regFullname.classList.remove('border-slate-700');
                hasRegError = true;
            } else {
                regFullnameError.classList.add('hidden');
                regFullname.classList.remove('border-red-500');
                regFullname.classList.add('border-slate-700');
            }

            // 2. Validar Correo
            if (!regEmail.value.trim()) {
                event.preventDefault();
                regEmailError.textContent = "El correo electrónico es obligatorio.";
                regEmailError.classList.remove('hidden');
                regEmail.classList.add('border-red-500');
                regEmail.classList.remove('border-slate-700');
                hasRegError = true;
            } else if (!emailRegex.test(regEmail.value.trim())) {
                event.preventDefault();
                regEmailError.textContent = "El correo debe ser de un dominio válido (@gmail.com o @hotmail.com).";
                regEmailError.classList.remove('hidden');
                regEmail.classList.add('border-red-500');
                regEmail.classList.remove('border-slate-700');
                hasRegError = true;
            } else {
                regEmailError.classList.add('hidden');
                regEmail.classList.remove('border-red-500');
                regEmail.classList.add('border-slate-700');
            }

            // 3. Validar Teléfono (10 dígitos iniciando en 3)
            if (!regPhone.value.trim()) {
                event.preventDefault();
                regPhoneError.textContent = "El teléfono es obligatorio.";
                regPhoneError.classList.remove('hidden');
                regPhone.classList.add('border-red-500');
                regPhone.classList.remove('border-slate-700');
                hasRegError = true;
            } else if (!phoneRegex.test(regPhone.value.trim())) {
                event.preventDefault();
                regPhoneError.textContent = "Ingresa un celular válido de Colombia (10 dígitos iniciando en 3).";
                regPhoneError.classList.remove('hidden');
                regPhone.classList.add('border-red-500');
                regPhone.classList.remove('border-slate-700');
                hasRegError = true;
            } else {
                regPhoneError.classList.add('hidden');
                regPhone.classList.remove('border-red-500');
                regPhone.classList.add('border-slate-700');
            }

            // 4. Validar Ciudad de Colombia
            const cityVal = regCity.value.trim().toLowerCase();
            if (!cityVal) {
                event.preventDefault();
                regCityError.textContent = "La ciudad de origen es obligatoria.";
                regCityError.classList.remove('hidden');
                regCity.classList.add('border-red-500');
                regCity.classList.remove('border-slate-700');
                hasRegError = true;
            } else if (!colombianCities.includes(cityVal)) {
                event.preventDefault();
                regCityError.textContent = "Ingresa una ciudad válida de Colombia.";
                regCityError.classList.remove('hidden');
                regCity.classList.add('border-red-500');
                regCity.classList.remove('border-slate-700');
                hasRegError = true;
            } else {
                regCityError.classList.add('hidden');
                regCity.classList.remove('border-red-500');
                regCity.classList.add('border-slate-700');
            }

            // 5. Validar Fecha de nacimiento
            if (!regBirthdate.value.trim()) {
                event.preventDefault();
                regBirthdateError.textContent = "Selecciona tu fecha de nacimiento.";
                regBirthdateError.classList.remove('hidden');
                regBirthdate.classList.add('border-red-500');
                regBirthdate.classList.remove('border-slate-700');
                hasRegError = true;
            } else {
                regBirthdateError.classList.add('hidden');
                regBirthdate.classList.remove('border-red-500');
                regBirthdate.classList.add('border-slate-700');
            }

            // 6. Validar Contraseña (Mínimo 8, Máximo 14)
            if (!regPassword.value.trim()) {
                event.preventDefault();
                regPasswordError.textContent = "La contraseña es obligatoria.";
                regPasswordError.classList.remove('hidden');
                regPassword.classList.add('border-red-500');
                regPassword.classList.remove('border-slate-700');
                hasRegError = true;
            } else if (regPassword.value.length < 8 || regPassword.value.length > 14) {
                event.preventDefault();
                regPasswordError.textContent = "La contraseña debe tener entre 8 y 14 caracteres.";
                regPasswordError.classList.remove('hidden');
                regPassword.classList.add('border-red-500');
                regPassword.classList.remove('border-slate-700');
                hasRegError = true;
            } else {
                regPasswordError.classList.add('hidden');
                regPassword.classList.remove('border-red-500');
                regPassword.classList.add('border-slate-700');
            }

            // 7. Validar Confirmar Contraseña
            if (!regConfirmPassword.value.trim()) {
                event.preventDefault();
                regConfirmPasswordError.textContent = "Debes confirmar la contraseña.";
                regConfirmPasswordError.classList.remove('hidden');
                regConfirmPassword.classList.add('border-red-500');
                regConfirmPassword.classList.remove('border-slate-700');
                hasRegError = true;
            } else if (regConfirmPassword.value !== regPassword.value) {
                event.preventDefault();
                regConfirmPasswordError.textContent = "Las contraseñas no coinciden.";
                regConfirmPasswordError.classList.remove('hidden');
                regConfirmPassword.classList.add('border-red-500');
                regConfirmPassword.classList.remove('border-slate-700');
                hasRegError = true;
            } else {
                regConfirmPasswordError.classList.add('hidden');
                regConfirmPassword.classList.remove('border-red-500');
                regConfirmPassword.classList.add('border-slate-700');
            }

            // ALERTA AL PRESIONAR "CREAR CUENTA" SI TODOS LOS CAMPOS ESTÁN CORRECTOS
            if (!hasRegError) {
                alert("¡Cuenta creada con éxito en Beyond Go!");
            }
        });

        // Limpiar alertas en tiempo real
        const inputsToClean = [
            { input: regFullname, error: regFullnameError },
            { input: regEmail, error: regEmailError },
            { input: regPhone, error: regPhoneError },
            { input: regCity, error: regCityError },
            { input: regBirthdate, error: regBirthdateError },
            { input: regPassword, error: regPasswordError },
            { input: regConfirmPassword, error: regConfirmPasswordError }
        ];

        inputsToClean.forEach(function(item) {
            if (item.input) {
                item.input.addEventListener('input', function() {
                    if (item.input.value.trim()) {
                        item.error.classList.add('hidden');
                        item.input.classList.remove('border-red-500');
                        item.input.classList.add('border-slate-700');
                    }
                });
            }
        });
    }

});