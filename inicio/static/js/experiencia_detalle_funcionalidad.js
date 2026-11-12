    document.addEventListener('DOMContentLoaded', () => {
        const reserva = document.querySelector('[data-booking-card]');
        if (!(reserva instanceof HTMLElement)) {
            return;
        }

        const calendario = reserva.querySelector('[data-booking-calendar]');
        if (calendario instanceof HTMLElement) {
            const tituloMes = calendario.querySelector('[data-calendar-month]');
            const diasContenedor = calendario.querySelector('[data-calendar-days]');
            const anterior = calendario.querySelector('[data-calendar-prev]');
            const siguiente = calendario.querySelector('[data-calendar-next]');
            const fechaReserva = calendario.querySelector('[data-booking-date]');
            const seleccion = calendario.querySelector('[data-calendar-selection]');

            if (
                !(tituloMes instanceof HTMLElement) ||
                !(diasContenedor instanceof HTMLElement) ||
                !(anterior instanceof HTMLButtonElement) ||
                !(siguiente instanceof HTMLButtonElement) ||
                !(fechaReserva instanceof HTMLInputElement) ||
                !(seleccion instanceof HTMLElement)
            ) {
                throw new Error('No se pudo inicializar el calendario: faltan elementos requeridos.');
            }

            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);
            let mesVisible = new Date(hoy.getFullYear(), hoy.getMonth(), 1);
            const formateadorMes = new Intl.DateTimeFormat('es-CO', { month: 'long', year: 'numeric' });
            const formateadorFecha = new Intl.DateTimeFormat('es-CO', {
                day: 'numeric',
                month: 'long',
                year: 'numeric',
            });
            let fechaSeleccionada = '';

            const claveFecha = (fecha) => {
                const anio = fecha.getFullYear();
                const mes = String(fecha.getMonth() + 1).padStart(2, '0');
                const dia = String(fecha.getDate()).padStart(2, '0');
                return `${anio}-${mes}-${dia}`;
            };

            const dibujarCalendario = () => {
                tituloMes.textContent = formateadorMes.format(mesVisible);
                diasContenedor.replaceChildren();
                anterior.disabled =
                    mesVisible.getFullYear() === hoy.getFullYear() &&
                    mesVisible.getMonth() === hoy.getMonth();
                anterior.classList.toggle('opacity-40', anterior.disabled);
                anterior.classList.toggle('cursor-not-allowed', anterior.disabled);

                const primerDiaSemana = new Date(mesVisible.getFullYear(), mesVisible.getMonth(), 1).getDay();
                const diasEnMes = new Date(mesVisible.getFullYear(), mesVisible.getMonth() + 1, 0).getDate();
                for (let espacio = 0; espacio < primerDiaSemana; espacio += 1) {
                    const celdaVacia = document.createElement('span');
                    celdaVacia.setAttribute('aria-hidden', 'true');
                    diasContenedor.append(celdaVacia);
                }

                for (let dia = 1; dia <= diasEnMes; dia += 1) {
                    const fecha = new Date(mesVisible.getFullYear(), mesVisible.getMonth(), dia);
                    const clave = claveFecha(fecha);
                    const boton = document.createElement('button');
                    const esPasada = fecha < hoy;
                    const estaSeleccionada = clave === fechaSeleccionada;
                    boton.type = 'button';
                    boton.textContent = String(dia);
                    boton.disabled = esPasada;
                    boton.setAttribute('aria-label', formateadorFecha.format(fecha));
                    boton.setAttribute('aria-pressed', String(estaSeleccionada));
                    boton.className = 'mx-auto flex h-8 w-8 items-center justify-center rounded-lg text-xs font-semibold transition focus:outline-none focus:ring-2 focus:ring-emerald-400';
                    if (estaSeleccionada) {
                        boton.classList.add('bg-emerald-600', 'text-white', 'shadow');
                    } else if (esPasada) {
                        boton.classList.add('cursor-not-allowed', 'text-slate-600');
                    } else {
                        boton.classList.add('bg-emerald-50', 'text-slate-900', 'shadow-sm', 'hover:bg-emerald-100', 'hover:text-emerald-900');
                    }
                    boton.addEventListener('click', () => {
                        fechaSeleccionada = clave;
                        fechaReserva.value = clave;
                        seleccion.textContent = `Fecha seleccionada: ${formateadorFecha.format(fecha)}.`;
                        dibujarCalendario();
                    });
                    diasContenedor.append(boton);
                }
            };

            anterior.addEventListener('click', () => {
                if (!anterior.disabled) {
                    mesVisible = new Date(mesVisible.getFullYear(), mesVisible.getMonth() - 1, 1);
                    dibujarCalendario();
                }
            });
            siguiente.addEventListener('click', () => {
                mesVisible = new Date(mesVisible.getFullYear(), mesVisible.getMonth() + 1, 1);
                dibujarCalendario();
            });
            dibujarCalendario();
        }

        const precioAdultoTexto = reserva.dataset.adultPrice ?? '';
        const precioNinoTexto = reserva.dataset.childPrice ?? '';
        const precioAdultoDigitos = precioAdultoTexto.replace(/\D/g, '');
        const precioNinoDigitos = precioNinoTexto.replace(/\D/g, '');
        const precioAdulto = precioAdultoDigitos ? Number(precioAdultoDigitos) : Number.NaN;
        const precioNino = precioNinoDigitos ? Number(precioNinoDigitos) : Number.NaN;
        const totales = Array.from(document.querySelectorAll('[data-booking-total]'));
        const botonReserva = reserva.querySelector('button[disabled]');

        if (!Number.isSafeInteger(precioAdulto) || !Number.isSafeInteger(precioNino)) {
            totales.forEach((total) => {
                total.textContent = 'Precio no disponible';
            });
            if (botonReserva instanceof HTMLButtonElement) {
                botonReserva.title = 'No se puede calcular la reserva porque falta un precio válido.';
            }
            return;
        }

        const precioCOP = (valor) => `$${new Intl.NumberFormat('es-CO', { maximumFractionDigits: 0 }).format(valor)} COP`;
        const cantidadAdultos = reserva.querySelector('[data-adult-count]');
        const cantidadNinos = reserva.querySelector('[data-child-count]');
        const cantidadAdultosResumen = reserva.querySelector('[data-adult-count-summary]');
        const cantidadNinosResumen = reserva.querySelector('[data-child-count-summary]');
        const subtotalAdultos = reserva.querySelector('[data-adult-subtotal]');
        const subtotalNinos = reserva.querySelector('[data-child-subtotal]');
        const precioAdultoUnitario = reserva.querySelector('[data-adult-unit-price]');
        const precioAdultoResumen = reserva.querySelector('[data-adult-summary-price]');
        const precioNinoUnitario = reserva.querySelector('[data-child-unit-price]');
        const botonAdultoMenos = reserva.querySelector('[data-adult-decrease]');
        const botonAdultoMas = reserva.querySelector('[data-adult-increase]');
        const botonNinoMenos = reserva.querySelector('[data-child-decrease]');
        const botonNinoMas = reserva.querySelector('[data-child-increase]');

        if (
            totales.length === 0 ||
            totales.some((total) => !(total instanceof HTMLOutputElement)) ||
            !(cantidadAdultos instanceof HTMLOutputElement) ||
            !(cantidadNinos instanceof HTMLOutputElement) ||
            !(cantidadAdultosResumen instanceof HTMLSpanElement) ||
            !(cantidadNinosResumen instanceof HTMLSpanElement) ||
            !(subtotalAdultos instanceof HTMLElement) ||
            !(subtotalNinos instanceof HTMLElement) ||
            !(precioAdultoUnitario instanceof HTMLElement) ||
            !(precioAdultoResumen instanceof HTMLElement) ||
            !(precioNinoUnitario instanceof HTMLElement) ||
            !(botonAdultoMenos instanceof HTMLButtonElement) ||
            !(botonAdultoMas instanceof HTMLButtonElement) ||
            !(botonNinoMenos instanceof HTMLButtonElement) ||
            !(botonNinoMas instanceof HTMLButtonElement)
        ) {
            throw new Error('No se pudo inicializar el resumen de reserva: faltan elementos requeridos.');
        }

        let adultos = 2;
        let ninos = 0;
        precioAdultoUnitario.textContent = precioCOP(precioAdulto);
        precioAdultoResumen.textContent = precioCOP(precioAdulto);
        precioNinoUnitario.textContent = precioCOP(precioNino);

        const actualizarResumen = () => {
            cantidadAdultos.textContent = String(adultos);
            cantidadNinos.textContent = String(ninos);
            cantidadAdultosResumen.textContent = String(adultos);
            cantidadNinosResumen.textContent = String(ninos);
            subtotalAdultos.textContent = precioCOP(adultos * precioAdulto);
            subtotalNinos.textContent = precioCOP(ninos * precioNino);
            totales.forEach((total) => {
                total.textContent = precioCOP(adultos * precioAdulto + ninos * precioNino);
            });
            botonAdultoMenos.disabled = adultos <= 1;
            botonNinoMenos.disabled = ninos <= 0;
        };

        botonAdultoMenos.addEventListener('click', () => {
            if (adultos > 1) {
                adultos -= 1;
                actualizarResumen();
            }
        });
        botonAdultoMas.addEventListener('click', () => {
            adultos += 1;
            actualizarResumen();
        });
        botonNinoMenos.addEventListener('click', () => {
            if (ninos > 0) {
                ninos -= 1;
                actualizarResumen();
            }
        });
        botonNinoMas.addEventListener('click', () => {
            ninos += 1;
            actualizarResumen();
        });
        actualizarResumen();
    });
    document.addEventListener('DOMContentLoaded', () => {
        const carrusel = document.querySelector('[data-experiencia-carousel]');
        if (!(carrusel instanceof HTMLElement)) {
            return;
        }

        const diapositivas = Array.from(carrusel.querySelectorAll('[data-carousel-slide]'));
        const anterior = carrusel.querySelector('[data-carousel-prev]');
        const siguiente = carrusel.querySelector('[data-carousel-next]');
        const contador = carrusel.querySelector('[data-carousel-counter]');

        if (diapositivas.length < 2) {
            return;
        }

        let indiceActual = 0;
        if (anterior instanceof HTMLButtonElement) {
            anterior.classList.remove('hidden');
            anterior.classList.add('flex');
        }
        if (siguiente instanceof HTMLButtonElement) {
            siguiente.classList.remove('hidden');
            siguiente.classList.add('flex');
        }
        if (contador instanceof HTMLElement) {
            contador.classList.remove('hidden');
            contador.textContent = `1 / ${diapositivas.length}`;
        }

        const mostrarDiapositiva = (indice) => {
            indiceActual = (indice + diapositivas.length) % diapositivas.length;
            diapositivas.forEach((diapositiva, posicion) => {
                const activa = posicion === indiceActual;
                diapositiva.classList.toggle('hidden', !activa);
                diapositiva.classList.toggle('flex', activa);
                diapositiva.setAttribute('aria-hidden', String(!activa));
            });
            if (contador instanceof HTMLElement) {
                contador.textContent = `${indiceActual + 1} / ${diapositivas.length}`;
            }
        };

        anterior?.addEventListener('click', () => mostrarDiapositiva(indiceActual - 1));
        siguiente?.addEventListener('click', () => mostrarDiapositiva(indiceActual + 1));
        carrusel.addEventListener('keydown', (event) => {
            if (event.key === 'ArrowLeft') {
                event.preventDefault();
                mostrarDiapositiva(indiceActual - 1);
            } else if (event.key === 'ArrowRight') {
                event.preventDefault();
                mostrarDiapositiva(indiceActual + 1);
            }
        });
    });
