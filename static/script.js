document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();  // ✅ NEĻAUJ LAPAI PĀRLĀDĒTIES

    let formData = new FormData();
    let fileInput = document.getElementById("fileInput");
    
    if (fileInput.files.length === 0) {
        alert("❌ Lūdzu izvēlies failu!");  // ✅ JA NAV FAILA, PARĀDĪT PAZIŅOJUMU
        return;
    }

    formData.append("file", fileInput.files[0]);

    try {
        let response = await fetch("https://arturavardnica.onrender.com/upload", {  // ✅ PĀRLIECINIES, KA ŠEIT IR PAREIZA SAITE UZ TAVU SERVERI!
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Neizdevās augšupielādēt!");

        let data = await response.json();
        alert(data.message);  // ✅ PARĀDĪT VEIKSMES PAZIŅOJUMU
    } catch (error) {
        alert("❌ Failed to fetch: " + error.message);  // ✅ JA KĻŪDA, PARĀDĪT PAZIŅOJUMU
    }
});
