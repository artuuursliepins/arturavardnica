document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const searchButton = document.getElementById("searchButton");
    const resultsSection = document.getElementById("searchResults");
    const resultsList = document.getElementById("resultsList");

    searchButton.addEventListener("click", search);
    searchInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            search();
        }
    });

    function search() {
        const query = searchInput.value.trim().toLowerCase();
        if (!query) return;

        fetch("/search?query=" + encodeURIComponent(query))
            .then(response => response.json())
            .then(results => {
                resultsList.innerHTML = "";
                if (results.length === 0) {
                    resultsList.innerHTML = "<li>❌ Nav rezultātu.</li>";
                    return;
                }

                results.forEach(result => {
                    const li = document.createElement("li");
                    li.innerHTML = `<a href="${result.url}#highlight">${result.title}</a>
                                    <p>${highlightText(result.snippet, query)}</p>`;
                    resultsList.appendChild(li);
                });

                resultsSection.classList.remove("hidden");
            })
            .catch(error => console.error("Meklēšanas kļūda:", error));
    }

    function highlightText(text, keyword) {
        const regex = new RegExp(`(${keyword})`, "gi");
        return text.replace(regex, "<span class='highlight'>$1</span>");
    }
});

