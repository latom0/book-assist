from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import requests
import time
from dotenv import load_dotenv
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app, resources={r"/upload": {"origins": "http://localhost:3000"}})

API_URL = "https://www.googleapis.com/books/v1/volumes"

load_dotenv()
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

book_cache = {}

def get_book_data(book_title):
    try:
        params = {
            "q": book_title, 
            "maxResults": 1,
            "key": API_KEY  
        }
        response = requests.get(API_URL, params=params)
        response.raise_for_status() 

        data = response.json()
        if "items" not in data:
            return None

        item = data["items"][0]
        volume_info = item.get("volumeInfo", {})

        book_details = {
            "title": volume_info.get("title", "Unknown Title"),
            "author": ", ".join(volume_info.get("authors", ["Unknown Author"])),
            "genre": ", ".join(volume_info.get("categories", ["Unknown Genre"])),
            "summary": volume_info.get("description", "No description available.")
        }

        return book_details
    except requests.RequestException as e:
        print(f"Error fetching book data: {e}")
        return None

def recommend_books_content(books_df, book_title):
    if book_title not in books_df["title"].values:
        return []

    books_df["features"] = books_df["genre"] + " " + books_df["author"] + " " + books_df["summary"]
    
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(books_df["features"])
    
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    try:
        idx = books_df[books_df["title"] == book_title].index[0]
    except IndexError:
        return []

    scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:6]

    return books_df.iloc[[i[0] for i in scores]][["title", "author", "genre"]].values.tolist()

def recommend_books_collaborative(user_id, ratings_df):
    reader = Reader(rating_scale=(1, 5))

    if len(ratings_df) < 10:
        return []

    data = Dataset.load_from_df(ratings_df[["user_id", "book_title", "rating"]], reader)
    trainset, testset = train_test_split(data, test_size=0.2)
    
    model = SVD()
    model.fit(trainset)

    all_books = data.build_full_trainset().all_items()
    book_titles = {i: data.build_full_trainset().to_raw_iid(i) for i in data.build_full_trainset().all_items()}


    recommendations = [
        (book_titles[book], model.predict(user_id, book_titles[book]).est)
        for book in all_books
    ]

    recommendations.sort(key=lambda x: x[1], reverse=True)

    return [rec[0] for rec in recommendations[:5]]

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        file_path = "user_preferences.csv"
        file.save(file_path)

        # Load the uploaded file into a DataFrame
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading file: {e}")
            return jsonify({"error": f"Error reading file: {e}"}), 400

        # Step 1: Get book details from Google Books API
        book_data = []
        for book in df["book_title"]:
            details = get_book_data(book)
            if details:
                book_data.append(details)
            time.sleep(1) 

        books_df = pd.DataFrame(book_data)

        # Step 2: Fetch additional books from Google Books API based on genre
        extra_books = []
        for genre in books_df["genre"].unique():
            params = {
                "q": f"subject:{genre}",  
                "maxResults": 5,
                "key": API_KEY
            }
            response = requests.get(API_URL, params=params)

            if response.status_code == 200:
                data = response.json()
                if "items" in data:
                    for item in data["items"]:
                        volume_info = item.get("volumeInfo", {})
                        extra_books.append({
                            "title": volume_info.get("title", "Unknown Title"),
                            "author": ", ".join(volume_info.get("authors", ["Unknown Author"])),
                            "genre": ", ".join(volume_info.get("categories", ["Unknown Genre"])),
                            "summary": volume_info.get("description", "No description available.")
                        })

            time.sleep(1)  # Avoid rate-limiting

        extra_books_df = pd.DataFrame(extra_books)

        # Step 3: Combine CSV books + Google Books API books
        full_books_df = pd.concat([books_df, extra_books_df], ignore_index=True)

        # Step 4: Get content-based recommendations
        hybrid_recommendations = set()
        for book in df["book_title"]:
            content_recs = recommend_books_content(full_books_df, book)
            hybrid_recommendations.update([rec[0] for rec in content_recs])

        return jsonify({"message": "File uploaded successfully", "recommendations": list(hybrid_recommendations)})
    
    except Exception as e:
        print(f"Internal server error: {e}")
        return jsonify({"error": f"Internal server error: {e}"}), 500

    
if __name__ == "__main__":
    app.run(debug=True)