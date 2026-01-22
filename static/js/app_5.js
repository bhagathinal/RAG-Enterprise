const askbtn = document.getElementById('askbtn');
const question = document.getElementById('question');
const loading = document.getElementById('loading');
const answerCard = document.getElementById('answer-card');
const answer = document.getElementById('answer');
const sources = document.getElementById('sources');
const error = document.getElementById('error');

askbtn.addEventListener('click', async () => {
    if (!question.value.trim()){
        showError('Please enter a question.');
        return;
    }

    resetUI();
    loading.classList.remove("hidden");

    try {
        const res = await fetch('/ask', {
            method:'POST',
            headers :{"Content-Type":"application/json"},
            body: JSON.stringify({question: question.value})
        });

        const data = await res.json();
        loading.classList.add("hidden");

        answer.textContent = data.answer;

        data.sources.forEach(s => {
            const li = document.createElement('li');
            li.textContent = `${s.source} (Page ${s.page})`;
            sources.appendChild(li);
        });

        answerCard.classList.remove("hidden");

    } catch (e) {
        loading.classList.add("hidden");
        showError('Server Error. Please try again.');
    }
});

        function resetUI(){
            error.classList.add("hidden");
            answerCard.classList.add("hidden");
            sources.innerHTML = "";
        }

        function showError(msg){
            error.textContent = msg;
            error.classList.remove("hidden");
        }