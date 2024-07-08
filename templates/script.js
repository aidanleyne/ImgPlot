// Drag and Drop functionality
const dropzone = document.getElementById('dropzone');
const imageContainer = document.querySelector('.image-container');
const fullscreenView = document.getElementById('fullscreen-view');
const fullscreenImage = document.getElementById('fullscreen-image');
const closeFullscreenButton = document.getElementById('close-fullscreen');
const fullscreenBackground = document.getElementById('fullscreen-background');

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = '#333';
});

dropzone.addEventListener('dragleave', () => {
    dropzone.style.borderColor = '#ccc';
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = '#ccc';

    const files = e.dataTransfer.files;
    for (const file of files) {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const img = document.createElement('img');
                img.src = event.target.result;
                img.addEventListener('click', () => {
                    fullscreenImage.src = img.src;
                    fullscreenView.style.display = 'flex';
                });
                imageContainer.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    }
});

fullscreenBackground.addEventListener('click', () => {
    fullscreenView.style.display = 'none';
});

closeFullscreenButton.addEventListener('click', () => {
    fullscreenView.style.display = 'none';
});
