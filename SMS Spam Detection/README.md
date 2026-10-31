# SMS Spam Detection

This project classifies a text message as spam or ham (not spam). It includes a notebook for data exploration and model experiments, serialized model and TF-IDF vectorizer files, and two lightweight web-app entry points.

## Why this project?

SMS filtering is a compact example for learning how to turn raw messages into machine-learning features and use a trained text model to make predictions. The included app scripts show how a notebook model can be connected to a basic user interface.

## What it does

- Explores the SMS dataset and preprocesses message text using tokenization, stopword removal, and stemming.
- Experiments with text vectorization and classifiers, including Naive Bayes and other scikit-learn models.
- Provides `model.pkl` and `vectorizer.pkl` for the supplied prediction apps.
- Provides a Streamlit app (`streamlit_app.py`) and a Flask app (`app.py`).

## Run the notebook

Open `sms_spam_detection.ipynb` in Jupyter or Google Colab. The notebook reads `spam.csv` from `/content/`; change that path if the file is in another location. Install pandas, NumPy, Matplotlib, Seaborn, NLTK, WordCloud, and scikit-learn if needed.

## Run a web app

Run commands from this project folder so the scripts can find `model.pkl` and `vectorizer.pkl`. Install the dependencies for the app you choose (`streamlit`, or `flask`), as well as NLTK and scikit-learn.

For the Streamlit interface:

```bash
streamlit run streamlit_app.py
```

For the Flask interface:

```bash
python app.py
```

Then open the local address printed by the app and submit a message for classification. The Flask script downloads the NLTK `punkt` and `stopwords` resources at startup if they are missing.

## Run with Docker

Build the image from this project directory:

```bash
docker build -t sms-spam-detection .
```

Start the Streamlit app:

```bash
docker run --rm -p 8501:8501 sms-spam-detection
```

Open [http://localhost:8501](http://localhost:8501) in your browser. The image includes the Streamlit app, model files, Python dependencies, and required NLTK data; the notebook and training dataset are not copied into the image.

## Where it can be used

This is useful for learning text preprocessing and building a local spam-filter prototype. It is not a ready-to-deploy message filtering service; review predictions before taking action on a message.

## Pros and limitations

**Pros**

- Includes both a training notebook and runnable UI examples.
- Shows the complete preprocessing, vectorization, and prediction flow.
- Can be tried locally without setting up a hosted service.

**Limitations**

- Spam patterns change over time, and the model may not generalize to other languages, regions, or newer messages.
- Short or ambiguous messages can be misclassified; false positives can hide legitimate messages.
- The saved pickle files must match the preprocessing and vectorizer expected by the app. Only load pickle files from a trusted source.
- The app scripts are prototypes and do not provide production security, monitoring, or deployment configuration.
