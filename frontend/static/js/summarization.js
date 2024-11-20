document.getElementById('simplify-summary-btn')?.addEventListener('click', () => {
    const summaryText = document.querySelector('#summary-text').textContent;

    if (!summaryText) {
        alert("No summary text available for simplification.");
        return;
    }

    // Send the summary text to the server to get the simplified version
    fetch('/simplify-summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ summary_text: summaryText }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.simplified_summary) {
            // Insert the simplified summary into the DOM without reloading the page
            const simplifiedSummaryBox = document.getElementById('simplified-summary');
            simplifiedSummaryBox.innerHTML = `
                <h3>Simplified Summary</h3>
                <p>${data.simplified_summary}</p>
            `;
        } else {
            alert("Could not generate a simplified summary.");
        }
    })
    .catch((error) => {
        console.error(error);
        alert("An error occurred while simplifying the summary.");
    });
});