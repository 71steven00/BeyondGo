// GESTION ESTABLECIMIENTOS- Detecta el cambio en el input tipo file de la imagen para mostrar su nombre en tiempo real CUANDO SE CREA UN NUEVO ESTABLECIMIENTO
  document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.querySelector('input[type="file"][name="url_img"]');
    const fileNameLabel = document.getElementById('file-name-label');

    if (fileInput && fileNameLabel) {
      fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
          // Actualiza el texto con el nombre del archivo seleccionado por el usuario
          fileNameLabel.textContent = "Archivo seleccionado: " + e.target.files[0].name;
          fileNameLabel.classList.add('text-emerald-600', 'font-bold');
        }
      });
    }
  });