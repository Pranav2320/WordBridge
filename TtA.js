var voicelist = [];

// Callback function to get voices and populate the dropdown
function initVoices() {
voicelist = responsiveVoice.getVoices();
populateVoiceDropdown();
}

// Function to populate the voice selection dropdown
function populateVoiceDropdown() {
var voiceSelect = document.getElementById("voice-select");
voicelist.forEach(function (voice) {
var option = document.createElement("option");
option.value = voice.name;
option.text = voice.name;
voiceSelect.add(option);
});
}

// Call the initVoices function to initialize voices and populate the dropdown
initVoices();

// Add event listener for translate and pronounce button
document.getElementById("translate-and-pronounce-button").addEventListener("click", function (event) {
event.preventDefault();
const form = event.target.form;
const formData = new FormData(form);

// Get selected voice
const selectedVoice = document.getElementById("voice-select").value;

fetch('/translate', {
method: 'POST',
body: formData,
})
.then(response => response.json())
.then(data => {
    document.getElementById("translated-text").value = data.translation;
    const textToSpeak = data.translation;
    responsiveVoice.speak(textToSpeak, selectedVoice, { delay: 0 });
})
.catch(error => console.error("Error:", error));
});


document.getElementById("copy-button").addEventListener("click", function() {
const snippetText = document.getElementById("translated-text").value;
navigator.clipboard.writeText(snippetText)
.then(() => alert("Text copied to clipboard!"))
.catch(err => console.error("Failed to copy text:", err));
});

document.getElementById("download-audio-button").addEventListener("click", function() {
const textToDownload = document.getElementById("translated-text").value;

fetch('/download-audio', {
method: 'POST',
headers: {
    'Content-Type': 'application/json',
},
body: JSON.stringify({ text: textToDownload }),
})
.then(response => response.blob())
.then(blob => {
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'pronounced_audio.mp3';
document.body.appendChild(a);
a.click();
document.body.removeChild(a);
URL.revokeObjectURL(url);
})
.catch(error => console.error("Error:", error));
});