# import os
# import pickle
# import pandas as pd
# import requests
# import streamlit as st

# base_path = os.path.dirname(__file__)

# movies_path = os.path.join(base_path, "movies.pkl")
# similarity_path = os.path.join(base_path, "similarity.pkl")

# try:
#     movies_list = pickle.load(open(movies_path, 'rb'))
#     similarity = pickle.load(open(similarity_path, "rb"))
# except FileNotFoundError:
#     st.error("Required files `movies.pkl` and `similarity.pkl` are not found in the script's directory. Please add them and restart the app.")
#     st.stop()

# # TMDB API Key
# API_KEY = "94e24b34c4f78c900d6408fe80c4aaf8"

# # Function to fetch movie details
# def fetch_movie_details(movie_title):
#     url = "https://api.themoviedb.org/3/search/movie"
#     params = {
#         "api_key": API_KEY,
#         "query": movie_title
#     }
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         if data["results"]:
#             movie_data = data["results"][0]
#             poster_path = movie_data.get("poster_path")
#             overview = movie_data.get("overview", "Description not available.")
#             poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
#             return poster_url, overview
#     return None, "Description not available."

# # Recommendation function
# def recommend(selected_movie_name):
#     movie_index = movies_list[movies_list['title'] == selected_movie_name].index[0]
#     distances = similarity[movie_index]
#     movies_list['similarity'] = distances
#     recommended_movies = movies_list.sort_values(by='similarity', ascending=False)[1:6]
#     return recommended_movies['title'].values

# # Streamlit app
# st.title("Movie Recommender System")

# selected_movie_name = st.selectbox(
#     "Select a movie of your choice",
#     movies_list["title"].values
# )

# if st.button("Recommend"):
#     recommendations = recommend(selected_movie_name)
#     st.write("Recommended Movies:")
    
#     for title in recommendations:
#         poster, description = fetch_movie_details(title)
#         col1, col2 = st.columns([1, 2])
#         with col1:
#             if poster:
#                 st.image(poster, use_container_width=True)
#             else:
#                 st.write("Poster not available")
#         with col2:
#             st.subheader(title)
#             st.write(description)


















































import os
import pickle
import pandas as pd
import requests
import streamlit as st

# Base path for locating required files
base_path = os.path.dirname(__file__)

movies_path = os.path.join(base_path, "movies.pkl")
similarity_path = os.path.join(base_path, "similarity.pkl")

# Load the movie data and similarity matrix
try:
    movies_list = pickle.load(open(movies_path, 'rb'))
    similarity = pickle.load(open(similarity_path, "rb"))
except FileNotFoundError:
    st.error("Required files `movies.pkl` and `similarity.pkl` are not found in the script's directory. Please add them and restart the app.")
    st.stop()

# TMDB API Key
API_KEY = "94e24b34c4f78c900d6408fe80c4aaf8"

# Function to fetch movie details
def fetch_movie_details(movie_title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": API_KEY,
        "query": movie_title
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            movie_data = data["results"][0]
            poster_path = movie_data.get("poster_path")
            overview = movie_data.get("overview", "Description not available.")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
            return poster_url, overview
    return None, "Description not available."

# Recommendation function
def recommend(selected_movie_name):
    movie_index = movies_list[movies_list['title'] == selected_movie_name].index[0]
    distances = similarity[movie_index]
    movies_list['similarity'] = distances
    recommended_movies = movies_list.sort_values(by='similarity', ascending=False)[1:10]
    return recommended_movies['title'].values

# Streamlit app
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie of your choice",
    movies_list["title"].values
)

if st.button("Recommend"):
    recommendations = recommend(selected_movie_name)
    st.write("Recommended Movies:")

    # Create rows with 3 columns per row
    for i in range(0, len(recommendations), 3):
        cols = st.columns(3)  # Create 3 columns
        for idx, title in enumerate(recommendations[i:i+3]):  # Process 3 movies at a time
            poster, description = fetch_movie_details(title)
            with cols[idx]:  # Assign content to the column
                if poster:
                    st.image(poster, use_container_width=True)
                else:
                    st.write("Poster not available")
                st.subheader(title)
                st.write(description)
