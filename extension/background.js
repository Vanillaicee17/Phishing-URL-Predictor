// background.js

async function sendUrlToBackend(url) {
    console.log(url)
    try {
        if (!isValidUrl(url)) {
            throw new Error("Invalid URL");
        }
        const response = await fetch("http://localhost:8000/recieve_url", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url }),
            mode: 'cors'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data && data.prediction !== undefined) {
            chrome.runtime.sendMessage({ type: "prediction", prediction: data.prediction });
        } else {
            throw new Error("Unexpected response format");
        }
    } catch (error) {
        console.log("Error sending URL:", error);
        chrome.runtime.sendMessage({ type: "error", message: error.message });
    }
}

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

async function checkActiveTab() {
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (tab && tab.url) {
            sendUrlToBackend(tab.url);
        }
    } catch (error) {
        console.log("Error checking active tab:", error);
    }
}

// Use Chrome alarms API instead of setInterval
chrome.alarms.create("checkTab", { periodInMinutes: 0.08 }); // Every 5 seconds

chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === "checkTab") {
        checkActiveTab();
    }
});

// Send the URL immediately when the tab is changed
chrome.tabs.onActivated.addListener(checkActiveTab);

// Send the URL when the extension icon is clicked
chrome.action.onClicked.addListener(checkActiveTab);
