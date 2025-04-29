document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("results").style.display = "none";

    document.getElementById("getRecommendation").addEventListener("click", async function () {
        const soilType = document.getElementById("soil").value;
        const city = document.getElementById("city").value.trim();
        const rainfall = document.getElementById("rainfall").value;

        if (!soilType || !city || !rainfall) {
            alert("⚠️ Please fill all the fields before submitting!");
            return;
        }

        try {
            // Call your backend to get weather details securely
            const weatherResponse = await fetch(`http://127.0.0.1:5000/weather?city=${city}`);
            const weatherData = await weatherResponse.json();

            const weather = weatherData.temp_c;
            const humidity = weatherData.humidity;

            const requestData = {
                soil_type: soilType,
                weather: weather,
                humidity: humidity,
                rainfall: rainfall
            };

            fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requestData)
            })
            .then(response => response.json())
            .then(data => {
                displayResults(data);
                document.getElementById("results").style.display = "block";
            })
            .catch(error => {
                console.error("Error:", error);
                alert("❌ Failed to fetch recommendations.");
            });

        } catch (error) {
            console.error("Weather API Error:", error);
            alert("❌ Could not get weather info. Check city name.");
        }
    });
});

function displayResults(data) {
    const cropList = document.getElementById("crop-list");
    cropList.innerHTML = "<h3>🌾 Recommended Crops:</h3>";

    if (data.prediction) {
        cropList.innerHTML += `<div class="crop-card"><span class="crop-name">${data.prediction}</span></div>`;
    } else {
        cropList.innerHTML += "<p class='no-result'>🚫 No recommendations found.</p>";
    }
}
