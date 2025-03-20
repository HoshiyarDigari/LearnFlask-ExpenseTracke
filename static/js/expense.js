// DOM Elements
const descriptionInput = document.getElementById('description');
const categorySelect = document.getElementById('category');
const suggestionBox = document.getElementById('category-suggestion');
const suggestedCategory = document.getElementById('suggested-category');
const confidence = document.getElementById('confidence');
const useSuggestionButton = document.getElementById('use-suggestion');
const loadingIndicator = document.getElementById('loading-indicator');
const suggestionContent = document.getElementById('suggestion-content');

// State variables
let suggestionTimeout;
let lastRequestLength = 0;
let isFetching = false;

// Event Listeners
descriptionInput.addEventListener('input', handleDescriptionInput);
descriptionInput.addEventListener('blur', handleDescriptionBlur);
descriptionInput.addEventListener('keypress', handleKeyPress);
useSuggestionButton.addEventListener('click', handleSuggestionClick);

// Functions
function handleDescriptionInput() {
    clearTimeout(suggestionTimeout);
    const description = this.value.trim();
    const currentLength = description.length;

    // Only proceed if we have at least 4 characters
    if (currentLength < 4) {
        hideSuggestionBox();
        return;
    }

    // Only make a new request if we've added at least 2 more characters
    if (currentLength - lastRequestLength < 2) {
        return;
    }

    lastRequestLength = currentLength;

    suggestionTimeout = setTimeout(() => {
        fetchCategorySuggestion(description);
    }, 500);
}

function handleDescriptionBlur() {
    const description = this.value.trim();
    if (description.length >= 4 && !isFetching) {
        fetchCategorySuggestion(description);
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const description = this.value.trim();
        if (description.length >= 4 && !isFetching) {
            fetchCategorySuggestion(description);
        }
    }
}

function handleSuggestionClick() {
    categorySelect.value = suggestedCategory.textContent;
    hideSuggestionBox();
}

function showLoadingState() {
    isFetching = true;
    suggestionBox.style.display = 'block';
    loadingIndicator.style.display = 'flex';
    suggestionContent.style.display = 'none';
}

function hideLoadingState() {
    isFetching = false;
    loadingIndicator.style.display = 'none';
}

function showSuggestion(category, confidenceValue) {
    suggestedCategory.textContent = category;
    confidence.textContent = confidenceValue;
    suggestionContent.style.display = 'block';
}

function hideSuggestionBox() {
    suggestionBox.style.display = 'none';
    loadingIndicator.style.display = 'none';
    suggestionContent.style.display = 'none';
}

async function fetchCategorySuggestion(description) {
    if (isFetching) return;
    
    showLoadingState();
    
    try {
        const response = await fetch('/suggest_category', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `description=${encodeURIComponent(description)}`
        });
        
        const data = await response.json();
        
        if (data.suggestion) {
            showSuggestion(data.suggestion, data.confidence);
        } else {
            hideSuggestionBox();
        }
    } catch (error) {
        console.error('Error:', error);
        hideSuggestionBox();
    } finally {
        hideLoadingState();
    }
} 