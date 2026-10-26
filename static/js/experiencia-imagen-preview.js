document.addEventListener('DOMContentLoaded', () => {
    const input = document.querySelector('[data-experience-image-input]');
    const preview = document.querySelector('[data-experience-image-preview]');
    const placeholder = document.querySelector('[data-experience-image-placeholder]');

    if (!input || !preview || !placeholder) return;

    let previewUrl;

    input.addEventListener('change', () => {
        const file = input.files?.[0];
        if (!file) return;

        if (previewUrl) URL.revokeObjectURL(previewUrl);
        previewUrl = URL.createObjectURL(file);
        preview.src = previewUrl;
        preview.classList.remove('hidden');
        placeholder.classList.add('hidden');
    });
});
