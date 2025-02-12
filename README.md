# Book Assist

An AI-powered book recommendation system that suggests books based on **content similarity** and **collaborative filtering**. Users upload a CSV file of books they've read, and the system recommends similar books using **Google Books API**, **TF-IDF**, and **SVD-based collaborative filtering**.

---

##  Features
-**Upload a book list** (CSV format)  
-**Content-based recommendations** (based on book genre, author, and summary)  
-**Collaborative filtering recommendations** (using user ratings & SVD algorithm)  
-**Fetches book details dynamically** from **Google Books API**  
-**Fully responsive UI** built with **React & Tailwind CSS**  
-**Flask backend** with ML-powered recommendations  

---

## Installation
### **1.** Clone the repository  
`git clone https://github.com/latom0/book-assist.git`  
`cd bookai`  

### **2.** Backend setup
Install dependencies:  
`cd backend`  
`pip install -r requirements.txt`  

Setup API key in `.env`  
`GOOGLE_BOOKS_API_KEY=your_api_key_here`  

Run the backend:  
`python app.py`

### **3.** frontend setup  
Install dependencies:  
`cd frontend`  
`npm install`  

Run the React app:  
`npm start`




