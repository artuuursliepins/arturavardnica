const SERVER_URL = "https://34a0-34-106-31-252.ngrok-free.app"; // Tavs Flask servera URL

document.getElementById("uploadForm").addEventListener("submit", function (event) {
    event.preventDefault();
    
    let fileInput = document.getElementById("fileInput").files[0];
    if (!fileInput) {
        alert("⚠️ Izvēlieties failu!");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput);

    fetch(`${SERVER_URL}/upload`, { // Saista uz Flask serveri
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("🚫 Neizdevās augšupielādēt failu!");
        }
        return response.text();
    })
    .then(() => {
        alert("✅ Fails veiksmīgi augšupielādēts!");
        setTimeout(() => window.location.reload(), 1000); // Automātiska atsvaidzināšana pēc 1s
    })
    .catch(error => {
        console.error("❌ Kļūda:", error);
        alert(error.message);
    });
});
