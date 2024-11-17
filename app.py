import pickle
import streamlit as st
import requests

def fetch_movie_details(movie_title):
    url = f"https://www.omdbapi.com/?t={movie_title}&apikey=526b109a"
    response = requests.get(url, timeout=10)
    data = response.json()
    return data

def fetch_poster(movie_title):
    data = fetch_movie_details(movie_title)
    if 'Poster' in data and data['Poster'] != 'N/A':
        return data['Poster'], data
    else:
        return None, data

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    movie_details = []
    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title
        poster, details = fetch_poster(movie_title)
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movie_title)
        movie_details.append(details)

    return recommended_movie_names, recommended_movie_posters, movie_details

st.set_page_config(page_title="Movie Recommender System", page_icon="🎬", layout="wide")

# Center the header title using custom HTML and CSS
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 3em;
            color: #d50000;
            font-weight: bold;
        }
    </style>
    <div class="title">
        🎥 Movie Recommender System
    </div>
""", unsafe_allow_html=True)

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    with st.spinner('Fetching recommendations...'):
        recommended_movie_names, recommended_movie_posters, movie_details = recommend(selected_movie)
    
    st.subheader(f"Recommendations for {selected_movie}:")
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    for idx, col in enumerate(columns):
        with col:
            st.text(recommended_movie_names[idx])
            if recommended_movie_posters[idx]:
                st.image(recommended_movie_posters[idx])
            else:
                st.text("Poster not available")
            
            # Display additional movie details
            if 'Genre' in movie_details[idx]:
                st.caption(f"Genre: {movie_details[idx]['Genre']}")
            if 'Director' in movie_details[idx]:
                st.caption(f"Director: {movie_details[idx]['Director']}")
            if 'imdbRating' in movie_details[idx]:
                st.caption(f"IMDb Rating: {movie_details[idx]['imdbRating']}⭐")
            if 'Plot' in movie_details[idx]:
                with st.expander("Plot Summary"):
                    st.write(movie_details[idx]['Plot'])
