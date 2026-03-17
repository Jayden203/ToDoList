document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('q');
    if (searchInput) {
        searchInput.setAttribute('placeholder', 'Search tasks by title...');
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const csrfTokenInput = document.getElementById("csrf-token");
    const csrfToken = csrfTokenInput ? csrfTokenInput.value : "";

    const toggleButtons = document.querySelectorAll(".toggle-task-btn");

    toggleButtons.forEach((button) => {
        button.addEventListener("click", async function () {
            const taskId = this.dataset.taskId;

            try {
                const response = await fetch(`/tasks/${taskId}/toggle-ajax/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "X-Requested-With": "XMLHttpRequest",
                        "Content-Type": "application/json"
                    }
                });

                const data = await response.json();

                if (data.success) {
                    const titleEl = document.getElementById(`task-title-${taskId}`);
                    const badgeEl = document.getElementById(`task-badge-${taskId}`);
                    const buttonEl = document.getElementById(`toggle-btn-${taskId}`);

                    if (data.completed) {
                        titleEl.classList.add("task-completed");

                        badgeEl.textContent = "Completed";
                        badgeEl.style.background = "#198754";
                        badgeEl.style.color = "#ffffff";

                        buttonEl.textContent = "Mark Pending";
                    } else {
                        titleEl.classList.remove("task-completed");

                        badgeEl.textContent = "Pending";
                        badgeEl.style.background = "#ffc107";
                        badgeEl.style.color = "#1e293b";

                        buttonEl.textContent = "Complete";
                    }
                } else {
                    alert("Failed to update task status.");
                }
            } catch (error) {
                console.error("Error toggling task status:", error);
                alert("Something went wrong while updating the task.");
            }
        });
    });
});

function getWeatherIcon(code) {
    const iconMap = {
        0: "☀️",
        1: "🌤️",
        2: "⛅",
        3: "☁️",
        45: "🌫️",
        48: "🌫️",
        51: "🌦️",
        53: "🌦️",
        55: "🌧️",
        61: "🌦️",
        63: "🌧️",
        65: "⛈️",
        71: "❄️",
        73: "❄️",
        75: "❄️",
        80: "🌦️",
        81: "🌧️",
        82: "⛈️",
        95: "⛈️"
    };
    return iconMap[code] || "🌍";
}

function getWeatherDescription(code) {
    const weatherMap = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Light snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm"
    };
    return weatherMap[code] || "Unknown";
}

async function loadWeather(cityName, latitude, longitude, tempId, descId, windId) {
    const tempEl = document.getElementById(tempId);
    const descEl = document.getElementById(descId);
    const windEl = document.getElementById(windId);

    if (!tempEl || !descEl || !windEl) return;

    const url =
        `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,weather_code,wind_speed_10m`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`${cityName} weather request failed`);
        }

        const data = await response.json();
        const current = data.current || {};
        const weatherCode = current.weather_code;

        const icon = getWeatherIcon(weatherCode);
        const description = getWeatherDescription(weatherCode);

        tempEl.textContent = `${current.temperature_2m ?? "--"}°C`;
        descEl.textContent = `${icon} ${description}`;
        windEl.textContent = `Wind: ${current.wind_speed_10m ?? "--"} km/h`;
    } catch (error) {
        console.error(`Error loading weather for ${cityName}:`, error);
        tempEl.textContent = "Weather unavailable";
        descEl.textContent = "";
        windEl.textContent = "";
    }
}

async function loadNavGlasgowWeather() {
    const iconEl = document.getElementById("nav-weather-icon");
    const cityEl = document.getElementById("nav-weather-city");
    const tempEl = document.getElementById("nav-weather-temp");
    const descEl = document.getElementById("nav-weather-desc");

    if (!iconEl || !cityEl || !tempEl || !descEl) return;

    const url =
        "https://api.open-meteo.com/v1/forecast?latitude=55.8642&longitude=-4.2518&current=temperature_2m,weather_code,wind_speed_10m";

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("Failed to fetch Glasgow weather");
        }

        const data = await response.json();
        const current = data.current || {};
        const weatherCode = current.weather_code;

        iconEl.textContent = getWeatherIcon(weatherCode);
        cityEl.textContent = "Glasgow";
        tempEl.textContent = `${current.temperature_2m ?? "--"}°C`;
        descEl.textContent = getWeatherDescription(weatherCode);
    } catch (error) {
        console.error("Error loading navbar Glasgow weather:", error);
        iconEl.textContent = "🌍";
        cityEl.textContent = "Glasgow";
        tempEl.textContent = "--°C";
        descEl.textContent = "Unavailable";
    }
}

async function loadQuote() {
    const quoteText = document.getElementById("quote-text");
    const quoteAuthor = document.getElementById("quote-author");

    if (!quoteText || !quoteAuthor) return;

    const fallbackQuotes = [
        { text: "Small progress is still progress.", author: "Unknown" },
        { text: "Stay focused and keep going.", author: "Unknown" },
        { text: "Discipline is choosing what you want most.", author: "Unknown" }
    ];

    try {
        const response = await fetch("https://zenquotes.io/api/random");
        if (!response.ok) {
            throw new Error("Quote request failed");
        }

        const data = await response.json();
        const quote = Array.isArray(data) ? data[0] : null;

        if (quote && quote.q) {
            quoteText.textContent = `"${quote.q}"`;
            quoteAuthor.textContent = `— ${quote.a || "Unknown"}`;
        } else {
            throw new Error("Invalid quote format");
        }
    } catch (error) {
        console.error("Error loading quote:", error);

        const fallback = fallbackQuotes[Math.floor(Math.random() * fallbackQuotes.length)];
        quoteText.textContent = `"${fallback.text}"`;
        quoteAuthor.textContent = `— ${fallback.author}`;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    loadQuote();
    loadWeather("London", 51.5072, -0.1276, "london-temp", "london-desc", "london-wind");
    loadWeather("Glasgow", 55.8642, -4.2518, "glasgow-temp", "glasgow-desc", "glasgow-wind");
    loadNavGlasgowWeather();
});