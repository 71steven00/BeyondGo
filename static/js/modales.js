document.addEventListener("DOMContentLoaded", function () {
    const selectRol = document.getElementById("id_rol");
    const inputCertificado = document.getElementById("id_certificado_turismo");

    if (selectRol && inputCertificado) {
      // Encontramos el contenedor padre que envuelve al input del certificado
      const contenedorCertificado = inputCertificado.closest("div");

      function actualizarVisibilidadCertificado() {
        if (selectRol.value === "GUIA") {
          contenedorCertificado.style.display = "block";
        } else {
          contenedorCertificado.style.display = "none";
          inputCertificado.value = ""; // Limpia el archivo si cambia de rol por error
        }
      }

      // Ejecutar al cargar (ideal para cuando editas un guía existente)
      actualizarVisibilidadCertificado();

      // Escuchar cambios en el selector de roles en tiempo real
      selectRol.addEventListener("change", actualizarVisibilidadCertificado);
    }
  });