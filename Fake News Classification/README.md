# Fake News Classification

This notebook explores classifying news articles as fake or real using the Kaggle fake-news dataset. It cleans article text, creates word and n-gram features, and compares Multinomial Naive Bayes with Logistic Regression.

## Why this project?

The project is a practical way to learn how a text-classification pipeline works, from inspecting and preprocessing news text to training models and trying predictions. It also demonstrates how token counts and phrases can be used as input features.

## What it does

- Loads and inspects the training data, handles missing values, and removes the `id` column.
- Preprocesses news text with NLTK and regular expressions.
- Uses `CountVectorizer` with up to 5,000 features and 1- to 3-word n-grams.
- Trains and evaluates Multinomial Naive Bayes and Logistic Regression on an 80/20 split.
- Loads the Kaggle test data for prediction.

## Data and setup

The folder contains `kaggle_fake_train.7z` and `kaggle_fake_test.7z`. Extract both archives and make the corresponding CSV files available. The notebook currently refers to a Google Drive path (`/content/drive/My Drive/Colab Notebooks/Datasets/`); change the `read_csv` paths to your extracted files, or place the files at that path in Colab.

Open `Fake News Classifier.ipynb` in Google Colab or Jupyter and run the cells in order. Install the libraries used by the notebook if they are not already available: pandas, NumPy, Matplotlib, Seaborn, NLTK, and scikit-learn. NLTK resources such as stopwords may also need to be downloaded.

## Where it can be used

This is suitable for NLP coursework, experimentation with news-text features, and a prototype for studying automated article triage. Predictions should be treated as model outputs for review, not as proof that an article is true or false.

## Pros and limitations

**Pros**

- Simple, interpretable baseline models and a clear end-to-end text workflow.
- N-gram features can capture short phrases as well as individual words.
- Includes separate training and test data for experimentation.

**Limitations**

- Bag-of-words features do not understand context, sarcasm, or factual evidence.
- The result depends on the dataset's labels, time period, and source distribution; it may not generalize to current news.
- The notebook's Google Drive paths need to be adjusted outside its original Colab setup.
- Automated fake-news labels can cause harm if used as definitive judgments without human review.
