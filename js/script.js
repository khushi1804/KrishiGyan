document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("getRecommendation").addEventListener("click", function () {
        // Get user input values
        const soilType = document.getElementById("soil").value;
        const weather = document.getElementById("weather").value;
        const marketDemand = document.getElementById("market").value;

        // Check if inputs are empty
        if (!soilType || !weather || !marketDemand) {
            alert("⚠️ Please fill all the fields before submitting!");
            return;
        }

        // Data to send in POST request
        const requestData = {
            soil_type: soilType,
            weather: weather,
            market_demand: marketDemand
        };

        // Call API using Fetch
        fetch("http://localhost:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())  
        .then(data => {
            console.log("Response from server:", data);
            displayResults(data);
        })
        .catch(error => {
            console.error("Error:", error);
            alert("❌ Failed to fetch recommendations. Please try again!");
        });
    });
});

// Function to display results
function displayResults(data) {
    const cropList = document.getElementById("crop-list");
    cropList.innerHTML = "<h3>🌾 Recommended Crops:</h3>";

    if (data.crops && data.crops.length > 0) {
        let cropsHtml = "<ul>";
        data.crops.forEach(crop => {
            cropsHtml += `<li>${crop}</li>`;
        });
        cropsHtml += "</ul>";
        cropList.innerHTML += cropsHtml;
    } else {
        cropList.innerHTML += "<p>No recommendations found.</p>";
    }
}
