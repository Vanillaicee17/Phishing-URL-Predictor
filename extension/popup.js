// popup.js

document.addEventListener('DOMContentLoaded', function () {
    chrome.runtime.sendMessage({ type: "getInitialPrediction" });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "prediction") {
        const predictionElement = document.getElementById("prediction");
        if (message.prediction === 0) {
            predictionElement.innerText = "Safe";
            predictionElement.style.color = "green";
        } else {
            predictionElement.innerText = "Potential Phishing";
            predictionElement.style.color = "red";
        }
    }

});
