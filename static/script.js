document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("uploadForm").addEventListener("submit", async function (e) {
        e.preventDefault();

        let fileInput = document.getElementById("fileInput");
        if (!fileInput || fileInput.files.length === 0) {
            alert("❌ Lūdzu izvēlies failu!");
            return;
        }

        let formData = new FormData();
        formData.append("file", fileInput.files[0]);

        try {
            let response = await fetch("https://arturavardnica.onrender.com/upload", {
                method: "POST",
                body: formData
            });

            let data = await response.json();

            if (!response.ok) {
                console.error("⚠️ Server Error:", data);
                alert(`❌ Servera kļūda: ${data.error || "Nezināma kļūda"}`);
                return;
            }

            alert("✅ Veiksmīgi augšupielādēts: " + data.message);
        } catch (error) {
            console.error("⚠️ Kļūda:", error);
            alert("❌ Tīkla kļūda: " + error.message);
        }
    });
});
