const form = document.getElementById("prediction-form");
const titleInput = document.getElementById("movie-title");
const plotInput = document.getElementById("movie-plot");
const submitButton = document.getElementById("submit-button");
const submitLabel = document.getElementById("submit-label");
const formMessage = document.getElementById("form-message");
const characterCount = document.getElementById("character-count");
const resultCard = document.getElementById("result-card");
const resultTitle = document.getElementById("result-title");
const genreList = document.getElementById("genre-list");
const resultEmpty = document.getElementById("result-empty");
const historyList = document.getElementById("history-list");
const historyMessage = document.getElementById("history-message");
const refreshHistoryButton = document.getElementById("refresh-history");
const themeToggle = document.getElementById("theme-toggle");
const themeLabel = document.getElementById("theme-label");

function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  const nextTheme = theme === "dark" ? "light" : "dark";
  themeToggle.setAttribute("aria-label", `Switch to ${nextTheme} mode`);
  themeLabel.textContent = `${nextTheme[0].toUpperCase()}${nextTheme.slice(1)} mode`;
  localStorage.setItem("frame-theme", theme);
}

const savedTheme = localStorage.getItem("frame-theme");
const initialTheme =
  savedTheme === "light" || savedTheme === "dark"
    ? savedTheme
    : window.matchMedia("(prefers-color-scheme: light)").matches
      ? "light"
      : "dark";
setTheme(initialTheme);

themeToggle.addEventListener("click", () => {
  setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
});

plotInput.addEventListener("input", () => {
  const count = plotInput.value.length;
  characterCount.textContent = `${count} ${count === 1 ? "character" : "characters"}`;
});

function showFormMessage(message) {
  formMessage.textContent = message;
  formMessage.hidden = false;
}

function getErrorMessage(payload, fallback) {
  if (typeof payload?.message === "string") {
    return payload.message;
  }
  if (typeof payload?.detail === "string") {
    return payload.detail;
  }
  if (Array.isArray(payload?.detail)) {
    return payload.detail
      .map((item) => item.msg)
      .filter((message) => typeof message === "string")
      .join(" ");
  }
  return fallback;
}

function addGenre(container, genre, className) {
  const tag = document.createElement("span");
  tag.className = className;
  tag.textContent = genre;
  container.append(tag);
}

function showPrediction(prediction) {
  const genres = Array.isArray(prediction.predicted_genres)
    ? prediction.predicted_genres
    : [];
  resultTitle.textContent = prediction.title;
  genreList.replaceChildren();
  genres.forEach((genre) => addGenre(genreList, genre, "genre-tag"));
  resultEmpty.hidden = genres.length > 0;
  resultCard.hidden = false;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  formMessage.hidden = true;

  const title = titleInput.value.trim();
  const plot = plotInput.value.trim();
  if (!title || !plot) {
    showFormMessage("Enter both a movie title and a plot summary.");
    return;
  }

  submitButton.disabled = true;
  submitLabel.textContent = "Finding genres…";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, plot }),
    });
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(getErrorMessage(payload, `Prediction failed (${response.status}).`));
    }

    showPrediction(payload);
    await loadHistory();
  } catch (error) {
    showFormMessage(
      error instanceof Error
        ? error.message
        : "Unable to reach the prediction service. Check that the backend is running.",
    );
  } finally {
    submitButton.disabled = false;
    submitLabel.textContent = "Discover genres";
  }
});

async function loadHistory() {
  historyMessage.textContent = "Loading saved predictions…";
  historyList.replaceChildren();

  try {
    const response = await fetch("/history");
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(getErrorMessage(payload, `History request failed (${response.status}).`));
    }

    const records = payload.History;
    if (!Array.isArray(records)) {
      throw new Error("The backend returned an unexpected history format.");
    }

    if (records.length === 0) {
      historyMessage.textContent = "Your predictions will appear here.";
      return;
    }

    historyMessage.textContent = "";
    records.forEach((record) => {
      const item = document.createElement("li");
      item.className = "history-item";

      const title = document.createElement("p");
      title.className = "history-item-title";
      title.textContent = record.title || "Untitled movie";
      item.append(title);

      const genres = document.createElement("div");
      genres.className = "history-genres";
      if (Array.isArray(record.predicted_genres)) {
        record.predicted_genres.forEach((genre) =>
          addGenre(genres, genre, "history-genre"),
        );
      }
      item.append(genres);
      historyList.append(item);
    });
  } catch (error) {
    historyMessage.textContent =
      error instanceof Error
        ? `Could not load history: ${error.message}`
        : "Could not load prediction history.";
  }
}

refreshHistoryButton.addEventListener("click", loadHistory);
loadHistory();
