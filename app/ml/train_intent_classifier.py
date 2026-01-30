import os
import joblib
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

nltk.download('stopwords')
pt_stopwords = stopwords.words('portuguese')

DATASET_PATH = "app/data/emails_dataset_250.csv"
MODEL_PATH = "app/models/intent_classifier.joblib"

def load_dataset(path: str):
    df = pd.read_csv(path, sep=";")
    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("Dataset must contain 'text' and 'label' columns")
    return df["text"], df["label"]

def build_pipeline():
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            stop_words=pt_stopwords,
            ngram_range=(1, 3),
            max_df=0.8,
            min_df=1
        )),
        ("classifier", MultinomialNB(alpha=0.1))
    ])

def train():
    texts, labels = load_dataset(DATASET_PATH)

    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.15,
        random_state=42,
        stratify=labels
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    print(f"--- RELATÓRIO DE TREINAMENTO ---")
    print(f"Acurácia Final: {accuracy_score(y_test, predictions):.4f}")
    print(classification_report(y_test, predictions))

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Modelo exportado para: {MODEL_PATH}")

if __name__ == "__main__":
    train()