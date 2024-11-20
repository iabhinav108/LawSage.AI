document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('file-input');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data here
        document.getElementById('pdf-output').style.display = 'block';
        document.getElementById('output-block-1').innerText = data.summary; // Example
        document.getElementById('output-block-2').innerText = data.details; // Example
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
