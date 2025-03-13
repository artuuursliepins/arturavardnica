document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    let formData = new FormData();
    let fileInput = document.getElementById("fileInput");

    if (fileInput.files.length === 0) {
        alert("❌ Lūdzu izvēlies failu!");
        return;
    }

    formData.append("file", fileInput.files[0]);

    try {
        let response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        let data = await response.json();
        if (data.error) {
            alert("❌ Kļūda: " + data.error);
        } else {
            document.getElementById("symbolList").innerHTML = data.html_content;
            alert("✅ Fails veiksmīgi apstrādāts!");
        }
    } catch (error) {
        alert("❌ Neizdevās savienoties ar serveri!");
    }
});

// 🔍 Meklēšanas funkcija visās lapās un tikai virsrakstos
function searchSymbols() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let searchType = document.getElementById("searchType").value;
    let items = document.querySelectorAll("#symbolList li");

    items.forEach(item => {
        let text = searchType === "titles" ? item.querySelector("a").textContent.toLowerCase() : item.textContent.toLowerCase();
        if (text.includes(input)) {
            item.style.display = "block";
            highlightText(item, input);
        } else {
            item.style.display = "none";
        }
    });
}

// 🔍 Izceļ meklētos vārdus
function highlightText(element, query) {
    let innerHTML = element.innerHTML;
    let regex = new RegExp(`(${query})`, "gi");
    element.innerHTML = innerHTML.replace(regex, "<span class='highlight'>$1</span>");
}

// 🌍 Apstrādā saites uz apakšlapām un ielādē saturu
function loadPage(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.getElementById("contentSection").innerHTML = html;
            attachSearchFeature(); // Pievieno meklēšanas funkcionalitāti arī jaunajām lapām
        })
        .catch(error => {
            console.error("❌ Kļūda ielādējot lapu:", error);
        });
}

// 🚀 Pievieno meklēšanas funkciju jaunajiem lapas elementiem
function attachSearchFeature() {
    let searchInput = document.getElementById("searchInput");
    if (searchInput) {
        searchInput.addEventListener("input", searchSymbols);
    }
}
