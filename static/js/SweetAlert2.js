// static/js/alert.js

document.addEventListener('DOMContentLoaded', function() {
    // -------------------------------------------------------------
    // 1. SCRIPT DE CONTROL DEL MENÚ RESPONSIVE (Sidebar)
    // -------------------------------------------------------------
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const toggleBtn = document.getElementById('toggle-sidebar-btn');
    const closeBtn = document.getElementById('close-sidebar-btn');

    function openSidebar() {
        if (sidebar && overlay) {
            sidebar.classList.remove('-translate-x-full');
            overlay.classList.remove('hidden');
        }
    }

    function closeSidebar() {
        if (sidebar && overlay) {
            sidebar.classList.add('-translate-x-full');
            overlay.classList.add('hidden');
        }
    }

    toggleBtn?.addEventListener('click', openSidebar);
    closeBtn?.addEventListener('click', closeSidebar);
    overlay?.addEventListener('click', closeSidebar);


    // -------------------------------------------------------------
    // 2. CONFIGURACIÓN DE DATATABLES (Lupa y traducciones)
    // -------------------------------------------------------------
    if (typeof $.fn.dataTable !== 'undefined') {
        $.fn.dataTable.ext.errMode = 'none';

        if ($.fn.DataTable.isDataTable('#tabla-pasajeros-dt')) {
            $('#tabla-pasajeros-dt').DataTable().destroy();
        }

        $('#tabla-pasajeros-dt').DataTable({
            language: {
                "decimal": "",
                "emptyTable": "No hay datos disponibles en la tabla",
                "info": "Mostrando _START_ a _END_ de _TOTAL_ registros",
                "infoEmpty": "Mostrando 0 a 0 de 0 registros",
                "infoFiltered": "(filtrado de _MAX_ registros totales)",
                "lengthMenu": "Mostrar _MENU_ registros",
                "loadingRecords": "Cargando...",
                "processing": "Procesando...",
                "search": "🔍 Buscar:",
                "zeroRecords": "No se encontraron registros coincidentes",
                "paginate": {
                    "first": "Primero",
                    "last": "Último",
                    "next": "Siguiente",
                    "previous": "Anterior"
                }
            },
            pageLength: 5,
            lengthMenu: [5, 10, 25, 50],
            responsive: true
        });
    }
});