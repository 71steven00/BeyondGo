document.addEventListener("DOMContentLoaded", function() {
    const inputs = document.querySelectorAll('.otp-input');
    const hiddenInput = document.getElementById('codigo');

    if (!inputs.length || !hiddenInput) return;

    inputs.forEach((input, index) => {
        // Avanzar al siguiente input al escribir un número
        input.addEventListener('input', (e) => {
            const value = e.target.value;
            e.target.value = value.replace(/[^0-9]/g, ''); // Solo números
            
            if (e.target.value && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
            updateHiddenInput();
        });

        // Retroceder al input anterior al presionar Backspace
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && !input.value && index > 0) {
                inputs[index - 1].focus();
            }
        });
    });

    function updateHiddenInput() {
        let code = '';
        inputs.forEach(input => {
            code += input.value;
        });
        hiddenInput.value = code;
    }
});
document.addEventListener("click", function(e) {
    const toggleBtn = e.target.closest('.toggle-password');
    if (!toggleBtn) return;

    const targetId = toggleBtn.getAttribute('data-target');
    const passwordInput = document.getElementById(targetId);
    const icon = toggleBtn.querySelector('i');

    if (!passwordInput || !icon) return;

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    }
});