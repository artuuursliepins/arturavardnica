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
