document.addEventListener('DOMContentLoaded', function () {
    let selectedCard = null;
    const cards = document.querySelectorAll('.card');
    const uploadButton = document.getElementById('uploadBtn');
    const clearButton = document.getElementById('clearBtn');
    const csvInput = document.getElementById('csvInput');
    const fileInfo = document.getElementById('fileInfo');
    const generateButton = document.getElementById('generateBtn');  // Generate button inside the form
    const selectedImageInput = document.getElementById('selectedImageInput');
    const uploadForm = document.getElementById('uploadForm');

    // Handle card selection for image cards
    cards.forEach((card) => {
        card.addEventListener('click', () => {
            // If the clicked card is already selected, unselect it
            if (selectedCard === card) {
                card.classList.remove('selected');
                selectedCard = null;
                selectedImageInput.value = ''; // Clear the hidden input
                uploadButton.disabled = true;  // Disable upload button
                clearButton.disabled = true;   // Disable clear button
            } else {
                // If a different card was selected previously, unselect it
                if (selectedCard !== null) {
                    selectedCard.classList.remove('selected');
                }

                // Select the clicked card
                selectedCard = card;
                card.classList.add('selected');
                selectedImageInput.value = card.querySelector('img').getAttribute('data-image'); // Set the hidden input value
                uploadButton.disabled = false;  // Enable upload button
                clearButton.disabled = false;   // Enable clear button
            }
        });
    });

    // Handle the Upload CSV button click
    uploadButton.addEventListener('click', function (event) {
        // Prevent the form from submitting when Upload CSV is clicked
        event.preventDefault();

        // Trigger the file input click to allow file selection
        csvInput.click();
    });

    // Handle file upload and show the "Generate" button
    csvInput.addEventListener('change', function () {
        const file = csvInput.files[0];

        if (file) {
            // Check if the file is a CSV file
            if (file.name.endsWith('.csv')) {
                fileInfo.innerText = `Selected file: ${file.name} (${file.size} bytes)`;
                generateButton.style.display = 'inline-block'; // Show the Generate button
            } else {
                fileInfo.innerText = 'Please upload a valid CSV file.';
                generateButton.style.display = 'none'; // Hide the Generate button if invalid
            }
        }
    });

    // Handle the Clear button click
    clearButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the form from submitting
        if (selectedCard) {
            selectedCard.classList.remove('selected');
            selectedCard = null;
            selectedImageInput.value = ''; // Clear hidden input value
            uploadButton.disabled = true;  // Disable upload button
            clearButton.disabled = true;   // Disable clear button
            fileInfo.innerText = '';       // Clear file info text
            csvInput.value = '';           // Clear file input
            generateButton.style.display = 'none'; // Hide Generate button
        }
    });
});
