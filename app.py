# app.py
import pickle
import pandas as pd
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch movie poster using movie ID
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key="Your_API_KEY"&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

# Function to get movie recommendations
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Home page route
@app.route('/')
def home():
    return render_template('index.html', movie_names=movies['title'].values)

# Recommendation route
@app.route('/recommend', methods=['POST'])
def get_recommendations():
    selected_movie_name = request.form['selected_movie']
    names, posters = recommend(selected_movie_name)
    return render_template('recommendations.html', names=names, posters=posters)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
