import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download stopwords
nltk.download("stopwords", quiet=True)

# Initialize once
stopwords_set = set(stopwords.words("english"))
ps = PorterStemmer()


def preprocess_plot(text: str) -> str:

    # 1. Remove special characters and numbers
    text = re.sub(pattern="[^a-zA-Z]", repl=" ", string=text)

    # 2. Convert to lowercase and remove extra spaces
    text = text.lower()
    text = " ".join(text.split())

    # 3. Remove stopwords
    words = text.split()
    words = [word for word in words if word not in stopwords_set]
    text = " ".join(words)

    # 4. Apply stemming
    words = text.split()
    words = [ps.stem(word) for word in words]
    text = " ".join(words)

    return text