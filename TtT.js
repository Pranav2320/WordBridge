document.getElementById("translate-button").addEventListener("click", function(event) {
event.preventDefault();
const form = event.target.form;
const formData = new FormData(form);

fetch('/translate', {
    method: 'POST',
    body: formData,
})
    .then(response => response.json())
    .then(data => {
        document.getElementById("translated-text").value = data.translation;
    })
    .catch(error => console.error("Error:", error));
});


document.getElementById("copy-button").addEventListener("click", function() {
const snippetText = document.getElementById("translated-text").value;
navigator.clipboard.writeText(snippetText)
    .then(() => alert("Text copied to clipboard!"))
    .catch(err => console.error("Failed to copy text:", err));
});