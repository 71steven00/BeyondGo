document.addEventListener('DOMContentLoaded', () => {
    const input = document.querySelector('[data-experience-images-input]');
    const preview = document.querySelector('[data-experience-images-preview]');
    const error = document.querySelector('[data-experience-images-error]');

    if (!(input instanceof HTMLInputElement) || !(preview instanceof HTMLElement) || !(error instanceof HTMLElement)) return;

    let previewUrls = [];

    input.addEventListener('change', () => {
        previewUrls.forEach((url) => URL.revokeObjectURL(url));
        previewUrls = [];
        preview.querySelectorAll('[data-new-image-preview]').forEach((element) => element.remove());
        error.classList.add('hidden');
        error.textContent = '';

        const files = Array.from(input.files || []);
        const maxFiles = Number.parseInt(input.dataset.maxFiles || '10', 10);
        if (files.length > maxFiles) {
            error.textContent = `Puedes agregar como máximo ${maxFiles} imágenes más.`;
            error.classList.remove('hidden');
            input.value = '';
            return;
        }

        files.forEach((file) => {
            const url = URL.createObjectURL(file);
            previewUrls.push(url);

            const wrapper = document.createElement('div');
            wrapper.dataset.newImagePreview = 'true';
            wrapper.className = 'aspect-square overflow-hidden rounded-lg border border-emerald-300';

            const image = document.createElement('img');
            image.src = url;
            image.alt = `Vista previa: ${file.name}`;
            image.className = 'h-full w-full object-cover';

            wrapper.append(image);
            preview.append(wrapper);
        });
    });
});
