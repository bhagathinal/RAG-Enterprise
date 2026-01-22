// --------------------------------------------------
// Grab references to all required UI elements
// --------------------------------------------------

// Ask button
const askbtn = document.getElementById('askbtn');

// Textarea where user types the question
const question = document.getElementById('question');

// Loading indicator shown while backend processes the query
const loading = document.getElementById('loading');

// Container that displays the final answer
const answerCard = document.getElementById('answer-card');

// Paragraph where the answer text will be inserted
const answer = document.getElementById('answer');

// List that displays document sources
const sources = document.getElementById('sources');

// Error message container
const error = document.getElementById('error');


// --------------------------------------------------
// Handle Ask button click
// --------------------------------------------------
askbtn.addEventListener('click', async () => {

    // Validate input: prevent empty questions
    if (!question.value.trim()) {
        showError('Please enter a question.');
        return;
    }

    // Reset UI state before new request
    resetUI();

    // Show loading indicator
    loading.classList.remove("hidden");

    try {
        // Send the question to Flask backend
        const res = await fetch('/ask', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: question.value })
        });

        // Parse JSON response from backend
        const data = await res.json();

        // Hide loading indicator
        loading.classList.add("hidden");

        // Insert generated answer text into UI
        answer.textContent = data.answer;

        // Loop through sources returned by backend
        // and display them in the UI
        data.sources.forEach(s => {
            const li = document.createElement('li');
            li.textContent = `${s.source} (Page ${s.page})`;
            sources.appendChild(li);
        });

        // Show the answer card
        answerCard.classList.remove("hidden");

    } catch (e) {
        // Hide loading indicator if error occurs
        loading.classList.add("hidden");

        // Display user-friendly error message
        showError('Server Error. Please try again.');
    }
});


// --------------------------------------------------
// Helper function to reset UI state
// --------------------------------------------------
function resetUI() {
    error.classList.add("hidden");
    answerCard.classList.add("hidden");
    sources.innerHTML = "";
}


// --------------------------------------------------
// Helper function to display error messages
// --------------------------------------------------
function showError(msg) {
    error.textContent = msg;
    error.classList.remove("hidden");
}
