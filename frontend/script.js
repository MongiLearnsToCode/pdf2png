document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('file-input');
    if (fileInput.files.length === 0) {
        alert('Please select a file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Upload failed');
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<a href="${url}" download="converted.zip">Download Converted Files</a>`;
    } catch (error) {
        alert('Error: ' + error.message);
    }
});
