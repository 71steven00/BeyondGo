 // =========================================================================
      // PASO D: CONTROL JAVASCRIPT DEL DESPLEGABLE DE FILTROS
      // Permite abrir/cerrar el menú flotante al hacer clic en el botón de Filtros
      // y cerrarlo automáticamente si el usuario hace clic fuera de él.
      // =========================================================================
      (function() {
        const btnToggleFiltros = document.getElementById('btn-toggle-filtros');
        const menuFiltros = document.getElementById('menu-filtros');
        const contenedorFiltros = document.getElementById('contenedor-filtros');

        if (btnToggleFiltros && menuFiltros) {
          // Abrir/cerrar menú al hacer clic en el botón
          btnToggleFiltros.addEventListener('click', function(e) {
            e.stopPropagation();
            menuFiltros.classList.toggle('hidden');
          });

          // Evitar que los clics dentro del formulario del menú lo cierren
          menuFiltros.addEventListener('click', function(e) {
            e.stopPropagation();
          });

          // Cerrar menú al hacer clic en cualquier otra parte del documento
          document.addEventListener('click', function(e) {
            if (!contenedorFiltros.contains(e.target)) {
              menuFiltros.classList.add('hidden');
            }
          });
        }
      })();