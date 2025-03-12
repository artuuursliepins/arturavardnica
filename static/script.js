document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("uploadForm").addEventListener("submit", async function (e) {
        e.preventDefault();  // ✅ Neļauj lapai pārlādēties

        let fileInput = document.getElementById("fileInput");
        if (!fileInput || fileInput.files.length === 0) {
            alert("❌ Lūdzu izvēlies failu!");  // ✅ Ja nav faila, parādīt paziņojumu
            return;
        }

        let formData = new FormData();
        formData.append("file", fileInput.files[0]);

        try {
            let response = await fetch("https://arturavardnica.onrender.com/upload", {  // ✅ Pārbaudi, vai šeit ir pareizā servera saite!
                method: "POST",
                body: formData
            });

            let data = await response.json();  // ✅ Pārvērš JSON formātā

            if (!response.ok) {
                throw new Error(data.error || "Neizdevās augšupielādēt!");  // ✅ Precīzāka kļūdu ziņošana
            }

            alert("✅ Veiksmīgi augšupielādēts: " + data.message);  // ✅ Veiksmīga augšupielāde
        } catch (error) {
            console.error("Kļūda:", error);
            alert("❌ Kļūda: " + error.message);  // ✅ Rāda detalizētāku kļūdu
        }
    });
});