const translations = {
    en: {
        logo: "KrishiGyan",
        aboutTitle: "About KrishiGyan",
        aboutParagraph1: "KrishiGyan is an AI-powered platform designed to assist farmers in making informed decisions about crop selection. By analyzing soil type, real-time weather data, and market demand trends, we provide the best crop recommendations to maximize yield and profit.",
        aboutParagraph2: "Our mission is to revolutionize agriculture through technology, ensuring sustainable farming and food security for future generations.",
        stepsTitle: "How to Use the Tool",
        step1: "Select your <strong>Soil Type</strong> from the dropdown menu.",
        step2: "Enter your <strong>Weather Condition</strong>...",
        step3: "Provide the <strong>Humidity</strong>...",
        step4: "Click on <strong>Get Recommendation</strong>...",
        dashboardTitle:"Crop Recommendation",
        soilLabel: "Soil Type:",
        cityLabel: "City:",
        rainfallLabel: "Rainfall",
        cityPlaceholder: "Enter your city name",
        getRecommendation: "Get Recommendation",
        cropListDefault: "Select soil type and conditions to view recommended crops.",
        footer: "&copy; 2025 KrishiGyan. All rights reserved. | Designed to empower farmers with smart technology."
    },
    hi: {
        // Header
        logo: "कृषिज्ञान",
    
        // About Section
        aboutTitle: "कृषिज्ञान के बारे में",
        aboutParagraph1: "कृषिज्ञान एक एआई-संचालित प्लेटफ़ॉर्म है जो किसानों को फसल चयन के निर्णय लेने में मदद करता है। यह मिट्टी के प्रकार, वास्तविक समय के मौसम डेटा और बाज़ार की मांग का विश्लेषण करके सर्वोत्तम फसल सिफारिशें प्रदान करता है, जिससे उपज और लाभ अधिकतम हो सके।",
        aboutParagraph2: "हमारा मिशन तकनीक के माध्यम से कृषि में क्रांति लाना है, जिससे टिकाऊ खेती और आने वाली पीढ़ियों के लिए खाद्य सुरक्षा सुनिश्चित की जा सके।",
    
        // Steps Section
        stepsTitle: "उपकरण का उपयोग कैसे करें",
        step1: "<strong>मिट्टी का प्रकार</strong> ड्रॉपडाउन सूची से चुनें।",
        step2: "अपने क्षेत्र के अनुसार <strong>मौसम की स्थिति</strong> दर्ज करें।",
        step3: "बेहतर फसल चयन के लिए <strong>नमी</strong> प्रदान करें।",
        step4: "<strong>सिफारिश प्राप्त करें</strong> बटन पर क्लिक करें।",
    
        // Dashboard Section
        dashboardTitle: "फसल सिफारिश उपकरण",
        soilLabel: "मिट्टी का प्रकार:",
        cityLabel: "शहर:",
        cityPlaceholder: "अपना शहर का नाम दर्ज करें",

        rainfallLabel: "वर्षा (मिमी में):",

        getRecommendation: "सिफारिश प्राप्त करें",
    
        // Results Section
        cropListDefault: "अनुशंसित फसलें देखने के लिए मिट्टी का प्रकार और स्थिति चुनें।",
    
        // Footer
        footer: "&copy; 2025 कृषिज्ञान। सर्वाधिकार सुरक्षित। | स्मार्ट तकनीक के साथ किसानों को सशक्त बनाने के लिए डिज़ाइन किया गया।"
      }
};


function updateLanguage(lang) {
    const elements = document.querySelectorAll("[data-i18n]");
    elements.forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (translations[lang][key]) {
            el.innerHTML = translations[lang][key];
        }
    });

    // Update input labels separately if needed
    document.querySelector('label[for="soil"]').textContent = translations[lang]["soilLabel"];
    document.querySelector('label[for="city"]').textContent = translations[lang]["cityLabel"];
    document.querySelector('label[for="rainfall"]').textContent = translations[lang]["rainfallLabel"];
    document.getElementById("getRecommendation").textContent = translations[lang]["getRecommendation"];
    document.getElementById("crop-list").innerHTML = `<p>${translations[lang]["cropListDefault"]}</p>`;
    document.querySelector("footer p").innerHTML = translations[lang]["footer"];
}

// Listen for changes
document.getElementById("languageSelect").addEventListener("change", function () {
    updateLanguage(this.value);
});

// Default language
document.addEventListener("DOMContentLoaded", () => {
    updateLanguage("hi");
});
