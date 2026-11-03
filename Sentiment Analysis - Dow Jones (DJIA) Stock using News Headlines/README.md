# Sentiment Analysis - Dow Jones (DJIA) Stock Using News Headlines

This notebook explores whether the day's news headlines can be used to classify the associated Dow Jones Industrial Average direction. It compares Logistic Regression, Random Forest, and Multinomial Naive Bayes using text features.

## Why this project?

The project provides a way to practice text preprocessing and supervised classification on financial news headlines. It also illustrates an important distinction: a model can find patterns in historical data without establishing that headlines cause market movements or reliably predict future prices.

## What it does

- Loads and explores `Stock Headlines.csv`.
- Cleans headline text and creates count-based text features using `CountVectorizer` (up to 10,000 features with bigrams).
- Trains and evaluates Logistic Regression, Random Forest, and Multinomial Naive Bayes.
- Uses the dataset's direction label (`0` for down/same and `1` for up) as the classification target.

## How to run

Open `Stock Sentiment Analysis.ipynb` in Google Colab or Jupyter. The notebook currently loads the CSV from a Google Drive path and specifies ISO-8859-1 encoding. Update the `read_csv` path to the included `Stock Headlines.csv` file if running locally. Install pandas, NumPy, Matplotlib, Seaborn, NLTK, WordCloud, and scikit-learn as needed, and download NLTK stopwords if prompted by the notebook.

Run the cells in order to inspect the data, preprocess headlines, train the models, and review predictions and evaluation metrics.

## Where it can be used

- Learning text classification and feature extraction with financial news
- Exploring historical headline datasets for classroom or personal research
- Prototyping a research workflow that could later be tested on carefully separated, time-aware data

## Pros and limitations

**Pros**

- Compares several familiar classification algorithms on the same text problem.
- Connects text preprocessing and headline features to a clearly defined binary target.
- The supplied CSV makes the experiment reproducible without collecting news yourself.

**Limitations**

- Historical associations do not demonstrate causation and do not guarantee future performance.
- The notebook's train/test approach may not reflect real forecasting; time-aware validation and leakage checks are needed for that.
- Market movement depends on many factors beyond news text, and labels can be noisy.
- This is an educational experiment, not financial advice or a trading signal.
