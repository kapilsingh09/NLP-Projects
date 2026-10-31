# Movie Genre Classification with Multi-label Output

This notebook predicts one or more genres from a movie's plot summary. Unlike a single-label classifier, its target can contain multiple genre tags for each movie.

## Why this project?

The project demonstrates a common real-world text problem where a document can belong to several categories at once. It combines plot-text preprocessing with multi-label target encoding and one-vs-rest classification.

## What it does

- Reads movie metadata and plot summaries from tab-separated files and combines them.
- Cleans summaries, removes stopwords, and applies stemming.
- Encodes genre sets with `MultiLabelBinarizer`.
- Creates TF-IDF features (up to 10,000) and trains a one-vs-rest Logistic Regression classifier.
- Includes a `predict_genre_tags` helper for trying a new plot summary.

## Data and setup

The folder contains `movie_metadata.rar` and `plot_summaries.rar`. Extract them and ensure the resulting `movie_metadata.tsv` and `plot_summaries.tsv` files are available in the notebook's working directory. Update the file paths if you keep them elsewhere.

Open `Movie Genre Classifier with Multi-label Output.ipynb` in Jupyter or Google Colab and run its cells in order. Install the notebook dependencies if needed: pandas, NumPy, Matplotlib, Seaborn, NLTK, and scikit-learn. The notebook uses NLTK stopwords and stemming resources.

## Where it can be used

- Exploring multi-label text classification in an NLP course or personal project
- Building a prototype to suggest genre tags for a movie synopsis
- Comparing genre distributions and text-classification approaches

## FastAPI web app

The `backend` folder includes a FastAPI service and a browser frontend. Start MongoDB locally first; the backend currently connects to `mongodb://localhost:27017/`.

From the `backend` directory, install the backend's Python dependencies and start the API:

```bash
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to use the frontend. It submits movie titles and plot summaries to `POST /predict` and displays saved predictions from `GET /history`. The API documentation remains available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). The interface supports light and dark themes and stores the selected theme in the browser.

## Pros and limitations

**Pros**

- Supports multiple genre predictions rather than forcing each movie into a single category.
- TF-IDF and one-vs-rest Logistic Regression provide a useful, understandable baseline.
- Includes a helper function for inference on a new plot.

**Limitations**

- Genre tags and plot summaries can be incomplete, subjective, or imbalanced.
- A linear model with TF-IDF does not capture nuanced plot meaning or relationships between genres.
- Predictions can change with the chosen probability threshold and may need calibration.
- The notebook expects extracted TSV files in its working directory. The FastAPI frontend is a lightweight prototype rather than a production service.
