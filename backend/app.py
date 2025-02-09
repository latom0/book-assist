from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import requests
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

app = Flask(__name__)
CORS(app)  

API_URL = "https://www.googleapis.com/books/v1/volumes"

def get_book_data(book_title):
    params = {"q": book_title, "maxResults": 1}
    response = requests.get(API_URL, params=params)

    if response.status_code != 200:
        return None
    
    data = response.json()
    if "items" not in data:
        return None
    
    item = data["items"][0]
    volume_info = item.get("volumeInfo", {})
    
    return {
        "title": volume_info.get("title", "Unknown Title"),
        "author": ", ".join(volume_info.get("authors", ["Unknown Author"])),
        "genre": ", ".join(volume_info.get("categories", ["Unknown Genre"])),
        "summary": volume_info.get("description", "No description available.")
    }

def recommend_books_content(books_df, book_title):
    if book_title not in books_df["title"].values:
        return []
    
    books_df["features"] = books_df["genre"] + " " + books_df["author"] + " " + books_df["summary"]
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(books_df["features"])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    idx = books_df[books_df["title"] == book_title].index[0]
    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
    
    return books_df.iloc[[i[0] for i in scores]][["title", "author", "genre"]].values.tolist()

def recommend_books_collaborative(user_id, ratings_df):
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings_df[["user_id", "book_title", "rating"]], reader)
    
    trainset, testset = train_test_split(data, test_size=0.2)
    model = SVD()
    model.fit(trainset)
    
    predictions = model.test(testset)
    accuracy.rmse(predictions)

    all_books = data.build_full_trainset().all_items()
    book_titles = data.build_full_trainset().to_raw_iid
    
    recommendations = [(book_titles[book], model.predict(user_id, book_titles[book]).est) for book in all_books]
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    return [rec[0] for rec in recommendations[:5]]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file_path = "user_preferences.csv"
            file.save(file_path)

            user_prefs = pd.read_csv(file_path)

            book_data = []
            for book in user_prefs["book_title"]:
                details = get_book_data(book)
                if details:
                    book_data.append(details)
                time.sleep(1)
            
            books_df = pd.DataFrame(book_data)

            hybrid_recommendations = set()
            
            for book in user_prefs["book_title"]:
                content_recs = recommend_books_content(books_df, book)
                hybrid_recommendations.update([rec[0] for rec in content_recs])
            
            collab_recs = recommend_books_collaborative(1, user_prefs)
            hybrid_recommendations.update(collab_recs)

            return render_template("index.html", recommendations=list(hybrid_recommendations))
    
    return render_template("index.html", recommendations=[])

if __name__ == "__main__":
    app.run(debug=True)
