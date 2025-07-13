document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('videoInput');
    const statusDiv = document.getElementById('status');
    const resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
    
    if (fileInput.files.length === 0) {
        statusDiv.innerText = 'Please select a video file to upload.';
        return;
    }
    
    const formData = new FormData();
    formData.append('video', fileInput.files[0]);
    statusDiv.innerText = 'Uploading and processing video...';
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        statusDiv.innerText = 'Processing complete!';
        resultsTable.innerHTML = '';
        data.plates.forEach(plate => {
            const row = resultsTable.insertRow();
            row.insertCell(0).innerText = plate['License Plate'];
            row.insertCell(1).innerText = plate['Violation Details'];
        });
    })
    .catch(error => {
        statusDiv.innerText = 'Error processing video.';
        console.error('Error:', error);
    });
});
