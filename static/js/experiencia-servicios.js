document.addEventListener('DOMContentLoaded', () => {
    const servicios = document.querySelector('[data-service-rows]');
    if (!(servicios instanceof HTMLElement)) {
        return;
    }

    const lista = servicios.querySelector('[data-service-row-list]');
    const plantilla = document.querySelector('template[data-service-row-template]');
    const botonAgregar = servicios.querySelector('[data-add-service-row]');
    const cantidad = servicios.querySelector('input[name="cantidad_servicios_nuevos"]');

    if (
        !(lista instanceof HTMLElement) ||
        !(plantilla instanceof HTMLTemplateElement) ||
        !(botonAgregar instanceof HTMLButtonElement) ||
        !(cantidad instanceof HTMLInputElement)
    ) {
        throw new Error('No se pudieron preparar los campos de servicios.');
    }

    const actualizarBoton = () => {
        const filas = lista.querySelectorAll('[data-service-row]');
        cantidad.value = String(filas.length);
        botonAgregar.disabled = filas.length >= Number(servicios.dataset.maxRows);
        botonAgregar.classList.toggle('cursor-not-allowed', botonAgregar.disabled);
        botonAgregar.classList.toggle('opacity-50', botonAgregar.disabled);
    };

    botonAgregar.addEventListener('click', () => {
        const indice = lista.querySelectorAll('[data-service-row]').length;
        if (indice >= Number(servicios.dataset.maxRows)) {
            actualizarBoton();
            return;
        }

        const fila = plantilla.content.firstElementChild?.cloneNode(true);
        if (!(fila instanceof HTMLElement)) {
            throw new Error('No se pudo agregar el espacio para un servicio.');
        }

        const nombre = fila.querySelector('[data-service-name]');
        const nombreEtiqueta = fila.querySelector('[data-service-name-label]');
        const descripcion = fila.querySelector('[data-service-description]');
        const descripcionEtiqueta = fila.querySelector('[data-service-description-label]');
        if (
            !(nombre instanceof HTMLInputElement) ||
            !(nombreEtiqueta instanceof HTMLLabelElement) ||
            !(descripcion instanceof HTMLTextAreaElement) ||
            !(descripcionEtiqueta instanceof HTMLLabelElement)
        ) {
            throw new Error('No se pudieron preparar los campos del nuevo servicio.');
        }

        nombre.name = `servicio_nombre_${indice}`;
        nombre.id = `id_servicio_nombre_${indice}`;
        nombreEtiqueta.htmlFor = nombre.id;
        descripcion.name = `servicio_descripcion_${indice}`;
        descripcion.id = `id_servicio_descripcion_${indice}`;
        descripcionEtiqueta.htmlFor = descripcion.id;
        lista.append(fila);
        nombre.focus();
        actualizarBoton();
    });

    actualizarBoton();
});
