    document.addEventListener('DOMContentLoaded', () => {
        const fecha = document.getElementById('fecha-experiencia');
        const fechaVisible = document.getElementById('fecha-experiencia-visible');
        const botonCalendario = document.getElementById('abrir-calendario');

        const botonMostrarTodas = document.getElementById('mostrar-todas-experiencias');
        if (botonMostrarTodas instanceof HTMLButtonElement) {
            const experienciasAdicionales = document.querySelectorAll('[data-experiencia-adicional]');
            const textoBoton = botonMostrarTodas.querySelector('span');
            const iconoBoton = botonMostrarTodas.querySelector('i');

            botonMostrarTodas.addEventListener('click', () => {
                const expandir = botonMostrarTodas.getAttribute('aria-expanded') !== 'true';
                experienciasAdicionales.forEach((experiencia) => {
                    experiencia.classList.toggle('hidden', !expandir);
                });
                botonMostrarTodas.setAttribute('aria-expanded', String(expandir));
                if (textoBoton instanceof HTMLElement) {
                    textoBoton.textContent = expandir ? 'Mostrar menos' : 'Ver todas las experiencias';
                }
                iconoBoton?.classList.toggle('rotate-180', expandir);
            });
        }

        if (fecha instanceof HTMLInputElement && fechaVisible instanceof HTMLElement && botonCalendario instanceof HTMLButtonElement) {
            botonCalendario.addEventListener('click', () => {
                if (typeof fecha.showPicker === 'function') {
                    fecha.showPicker();
                    return;
                }

                fecha.focus();
                fecha.click();
            });

            fecha.addEventListener('change', () => {
                if (!fecha.value) {
                    fechaVisible.textContent = 'dd/mm/aaaa';
                    return;
                }

                const [year, month, day] = fecha.value.split('-');
                fechaVisible.textContent = `${day}/${month}/${year}`;
            });
        }

        const filtros = [
            {
                select: document.getElementById('filtro-tipo'),
                trigger: document.getElementById('filtro-tipo-boton'),
                menu: document.getElementById('filtro-tipo-menu'),
            },
            {
                select: document.getElementById('filtro-precio'),
                trigger: document.getElementById('filtro-precio-boton'),
                menu: document.getElementById('filtro-precio-menu'),
            },
        ];

        const cerrarMenus = (excepto = null) => {
            filtros.forEach((filtro) => {
                if (filtro === excepto || !(filtro.menu instanceof HTMLElement) || !(filtro.trigger instanceof HTMLButtonElement)) {
                    return;
                }

                filtro.menu.classList.add('hidden');
                filtro.trigger.setAttribute('aria-expanded', 'false');
                filtro.trigger.querySelector('.fa-chevron-down')?.classList.remove('rotate-180');
            });
        };

        filtros.forEach((filtro) => {
            const { select, trigger, menu } = filtro;
            if (!(select instanceof HTMLSelectElement) || !(trigger instanceof HTMLButtonElement) || !(menu instanceof HTMLElement)) {
                return;
            }

            const opciones = Array.from(menu.querySelectorAll('button[role="option"]'));
            const actualizarSeleccion = (opcion) => {
                const valor = opcion.dataset.value;
                const etiqueta = opcion.dataset.label;
                if (valor === undefined || etiqueta === undefined) {
                    return;
                }

                select.value = valor;
                const textoBoton = trigger.querySelector('span');
                if (!(textoBoton instanceof HTMLElement)) {
                    return;
                }
                textoBoton.textContent = etiqueta;
                opciones.forEach((elemento) => {
                    const seleccionada = elemento === opcion;
                    elemento.setAttribute('aria-selected', String(seleccionada));
                    elemento.classList.toggle('bg-emerald-50', seleccionada);
                    elemento.classList.toggle('font-semibold', seleccionada);
                    elemento.classList.toggle('text-emerald-800', seleccionada);
                    elemento.classList.toggle('text-slate-700', !seleccionada);
                    elemento.querySelector('.fa-check')?.classList.toggle('invisible', !seleccionada);
                });
                select.dispatchEvent(new Event('change', { bubbles: true }));
                cerrarMenus();
                trigger.focus();
            };

            trigger.addEventListener('click', () => {
                const abrir = menu.classList.contains('hidden');
                cerrarMenus(filtro);
                menu.classList.toggle('hidden', !abrir);
                trigger.setAttribute('aria-expanded', String(abrir));
                trigger.querySelector('.fa-chevron-down')?.classList.toggle('rotate-180', abrir);
            });

            opciones.forEach((opcion, indice) => {
                opcion.addEventListener('click', () => actualizarSeleccion(opcion));
                opcion.addEventListener('keydown', (event) => {
                    if (event.key === 'Escape') {
                        cerrarMenus();
                        trigger.focus();
                    } else if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
                        event.preventDefault();
                        const paso = event.key === 'ArrowDown' ? 1 : -1;
                        opciones[(indice + paso + opciones.length) % opciones.length]?.focus();
                    } else if (event.key === 'Home') {
                        event.preventDefault();
                        opciones[0]?.focus();
                    } else if (event.key === 'End') {
                        event.preventDefault();
                        opciones[opciones.length - 1]?.focus();
                    }
                });
            });

            trigger.addEventListener('keydown', (event) => {
                if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
                    event.preventDefault();
                    menu.classList.remove('hidden');
                    trigger.setAttribute('aria-expanded', 'true');
                    const seleccionada = opciones.find((opcion) => opcion.getAttribute('aria-selected') === 'true');
                    const indiceSeleccionado = seleccionada ? opciones.indexOf(seleccionada) : -1;
                    const indiceFoco = event.key === 'ArrowDown'
                        ? (indiceSeleccionado + 1) % opciones.length
                        : (indiceSeleccionado <= 0 ? opciones.length - 1 : indiceSeleccionado - 1);
                    opciones[indiceFoco]?.focus();
                }
            });
        });

        document.addEventListener('click', (event) => {
            if (event.target instanceof Node && !filtros.some(({ trigger, menu }) => trigger?.contains(event.target) || menu?.contains(event.target))) {
                cerrarMenus();
            }
        });
    });
