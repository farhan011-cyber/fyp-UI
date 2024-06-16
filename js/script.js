document.getElementById('uploadButton').addEventListener('click', function(event) {
    event.preventDefault();

    var fileInput = document.getElementById('imageUpload');
    var file = fileInput.files[0];
    var reader = new FileReader();

    reader.onload = function(e) {
        var image = e.target.result.split(',')[1]; // Extract base64-encoded image data
        
        // Display the uploaded image
        var uploadedImage = document.getElementById('uploadedImage');
        uploadedImage.src = e.target.result;
        uploadedImage.style.display = 'block';

        // Show loading spinner while processing
        document.getElementById('loading').style.display = 'block';

        // Send image data to Flask backend
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({image: image})
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading spinner after processing
            document.getElementById('loading').style.display = 'none';

            // Display the result
            var result = document.getElementById('result');
            if (data.error) {
                result.textContent = "Error: " + data.error;
            } else {
                result.textContent = "Prediction Result: " + data.class;
            }
        })
        .catch(error => {
            // Hide loading spinner if an error occurs
            document.getElementById('loading').style.display = 'none';
            console.error('Error:', error);
        });
    };

    // Read the selected image file as data URL
    reader.readAsDataURL(file);
});
