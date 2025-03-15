document.addEventListener("DOMContentLoaded", function() {
    loadSymbolList();
});

function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
        alert("❌ Nav izvēlēts fails!");
        return;
    }
    
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    
    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadSymbolList();
    })
    .catch(error => console.error("🚨 Kļūda augšupielādē:", error));
}

function submitGPTUrl() {
    const urlInput = document.getElementById("gptUrlInput").value;
    if (!urlInput) {
        alert("❌ Lūdzu, ievadiet GPT saiti!");
        return;
    }
    fetch("/process_gpt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: urlInput })
    })
    .then(response => response.json())
    .then(data => {
        alert("🔗 Saites nosūtīšana veiksmīga!");
        loadSymbolList();
    })
    .catch(error => console.error("🚨 Kļūda GPT saites apstrādē:", error));
}

function loadSymbolList() {
    fetch("/get_symbols")
    .then(response => response.json())
    .then(data => {
        const listElement = document.getElementById("symbolList");
        listElement.innerHTML = "";
        data.forEach(item => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `<a href="${item.link}">${item.title}</a>`;
            listElement.appendChild(listItem);
        });
    })
    .catch(error => console.error("🚨 Kļūda saraksta ielādē:", error));
}

function performSearch() {
    const query = document.getElementById("searchInput").value.toLowerCase();
    const type = document.getElementById("searchType").value;
    
    fetch(`/search?query=${query}&type=${type}`)
    .then(response => response.json())
    .then(data => {
        const resultContainer = document.getElementById("searchResults");
        resultContainer.innerHTML = "";
        resultContainer.style.display = "block";
        
        if (data.length === 0) {
            resultContainer.innerHTML = "❌ Nekas netika atrasts!";
            return;
        }
        
        data.forEach(item => {
            const resultItem = document.createElement("div");
            resultItem.innerHTML = `<a href="${item.link}"><strong>${item.title}</strong></a><p>${item.snippet}</p>`;
            resultContainer.appendChild(resultItem);
        });
    })
    .catch(error => console.error("🚨 Kļūda meklēšanā:", error));
}
