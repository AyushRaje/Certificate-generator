const cards = document.querySelectorAll('.card');
const uploadButton = document.getElementById('uploadBtn');
const clearButton = document.getElementById('clearBtn');
const csvInput = document.getElementById('csvInput');
const fileInfo = document.getElementById('fileInfo');
// Create a new button for generating, initially hidden
const generateButton = document.createElement('button');
generateButton.id = 'generateBtn';
generateButton.innerText = 'Generate';
generateButton.style.display = 'none'; // Hidden initially
document.querySelector('.container').appendChild(generateButton);


let selectedCard = null;

// Add click event listeners to each card
cards.forEach((card) => {
    card.addEventListener('click', () => {
        // If the clicked card is already selected, unselect it
        if (selectedCard === card) {
            card.classList.remove('selected');
            selectedCard = null;
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
            uploadButton.disabled = false;  // Enable upload button
            clearButton.disabled = false;   // Enable clear button
        }
    });
});

// Add event listener to the clear button to clear the selection
clearButton.addEventListener('click', () => {
    if (selectedCard !== null) {
        selectedCard.classList.remove('selected');
        selectedCard = null;
        uploadButton.disabled = true;
        clearButton.disabled = true;
        fileInfo.innerText = ''; // Clear file info
    }
});

// Show file input dialog when upload button is clicked
uploadButton.addEventListener('click', () => {
    csvInput.click();  // Simulate click on hidden file input
});

// Handle file upload and validation
function handleFileUpload() {
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
}


