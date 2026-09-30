document.addEventListener('DOMContentLoaded', function() {
    // 1. Desvanecer y eliminar alertas flotantes automáticas
    setTimeout(function() {
        const alertBox = document.getElementById('alert-container');
        if (alertBox) {
            alertBox.style.opacity = '0';
            setTimeout(() => alertBox.remove(), 500);
        }
    }, 4000);
    // 2. ocultar errores del formulario al escribir en los inputs

    const inputs = document.querySelectorAll('form input, form select');

    inputs.forEach(input => {
      input.addEventListener('input', function() {
        // Busca el grupo contenedor del input
        const formGroup = this.closest('.form-group');
        if (formGroup) {
          // Busca la etiqueta de error y la remueve o la oculta
          const errorMsg = formGroup.querySelector('.error-msg');
          if (errorMsg) {
            errorMsg.style.display = 'none';
          }
        }
      });
    });
  });