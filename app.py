import streamlit as st
import pickle
import pandas as pd
import requests


API_KEY = '4e68409f72f1d0840bb15137fcb7a2e6'

import time


def fetch_poster(movie_id):
    """Fetch movie poster URL safely with retry mechanism"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    for attempt in range(3):  # retry up to 3 times
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"
                else:
                    return None
            else:
                st.warning(f"TMDB returned status {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            if attempt < 2:
                time.sleep(1.5)  # wait before retry
            else:
                # st.error(f"Error fetching poster after 3 tries: {e}")
                return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for j in movies_list:
        movie_id = movies.iloc[j[0]].movie_id
        recommended_movies.append(movies.iloc[j[0]].title)
        poster = fetch_poster(movie_id)
        recommended_movies_posters.append(poster if poster else "https://via.placeholder.com/500x750?text=No+Image")
        print("Poster URL:", poster)

    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)




import gdown
import os
import pickle

# Download the file from Google Drive if not already downloaded
if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/file/d/19yx2QNQk0w1_GDYz4xAlqozaRJsgExCF/view?usp=drive_link"
    gdown.download(url, "similarity.pkl", quiet=False)

# Load it (read in binary mode)
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
