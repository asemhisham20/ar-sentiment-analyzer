import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import ISRIStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from flask import Flask, request, jsonify

nltk.download('punkt')
app = Flask(__name__)

def tokenize_and_stem(text):
    stemmer = ISRIStemmer()
    return ' '.join([stemmer.stem(token) for token in word_tokenize(text)])


def load_and_train_model(file_path):
    dataset = pd.read_csv(file_path)
    dataset['processed_review'] = dataset['review'].apply(tokenize_and_stem)

    vectorizer = CountVectorizer()
    x_vectorized = vectorizer.fit_transform(dataset['processed_review'])

    classifier = MultinomialNB()
    classifier.fit(x_vectorized, dataset['rating'])

    return vectorizer, classifier


def predict_rating(vectorizer, classifier, review):
    review = tokenize_and_stem(review)

    input_vectorized = vectorizer.transform([review])

    predicted_rating = classifier.predict(input_vectorized)[0]
    return predicted_rating


def get_rating(review):
    vectorizer, classifier = load_and_train_model('customer_reviews.csv')

    predicted_rating = predict_rating(vectorizer, classifier, review)
    return predicted_rating

@app.route('/review', methods=['POST'])
def post_endpoint():
    data = request.json

    return jsonify(str(get_rating(data['review'])))

if __name__ == '__main__':
    app.run(debug=True)