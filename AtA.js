var recognition;

function getSelectedLanguageCode(selectId) {
    const selectElement = document.getElementById(selectId);
    return selectElement.value;
}

function startRecording() {
    window.SpeechRecognition = window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.interimResults = true;

    const sourceLanguageCode = getSelectedLanguageCode('source-language-select');
    recognition.lang = sourceLanguageCode;

    recognition.addEventListener('result', e => {
        const transcript = Array.from(e.results)
            .map(result => result[0])
            .map(result => result.transcript)
            .join('');

        document.getElementById("text-to-translate").value = transcript;
        console.log(transcript);
    });

    recognition.start();

    document.getElementById('start-recording-button').classList.add('hidden');
    document.getElementById('stop-recording-button').classList.remove('hidden');
}

function stopRecording() {
    recognition.stop();

    document.getElementById('start-recording-button').classList.remove('hidden');
    document.getElementById('stop-recording-button').classList.add('hidden');
}

document.getElementById('start-recording-button').addEventListener('click', startRecording);
document.getElementById('stop-recording-button').addEventListener('click', stopRecording);

document.getElementById("translate-and-pronounce-button").addEventListener("click", function (event) {
    event.preventDefault();
    const form = event.target.form;
    const formData = new FormData(form);

    const targetLanguageCode = getSelectedLanguageCode('target-language-select');

    fetch('/translate', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            // Remove the 'hidden' class to show the textarea
            document.getElementById("translated-text").classList.remove('hidden');
            document.getElementById("translated-text").value = data.translation;
            const textToSpeak = data.translation;
            responsiveVoice.speak(textToSpeak, 'Hindi Female', { delay: 0 });
        })
        .catch(error => console.error("Error:", error));
});