from tenacity import retry,wait_fixed,stop_after_attempt
import pickle as p
import streamlit as st
import requests as r

st.header("Movie Recommendation System Using Machine Learning")

# Function to fetch movie poster from TMDb
@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def fetch_poster(movie_id,retries=3):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=71b4aad1ba4567b150fcc24992459c45".format(movie_id)
    attempt=0
    while(attempt<retries):
        try:
            data = r.get(url)
            data = data.json()
            poster_path = data['poster_path']
            full_path = "http://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        except r.exceptions.Timeout:
            st.error(f"Request to fetch poster for movie {movie_id} timed out. Please try again.")
        except r.exceptions.RequestException as e:    
            st.error("Error fetching poster:{e}")
            raise e
    return None

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommanded_movies_name = []
    recommanded_movies_poster = []
    
    # Loop through the most similar movies (top 5)
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['id'] # Corrected line here
        recommanded_movies_poster.append(fetch_poster(movie_id))
        recommanded_movies_name.append(movies.iloc[i[0]]['title'])  # Use column name for accessing the title
    
    return recommanded_movies_name, recommanded_movies_poster

# Load pickled data
try:
    with open('artificats/movie_list.pkl', 'rb') as file:
        movies = p.load(file)
except Exception as e:
    st.error(f"Error loading movie list: {e}")
    movies = None

try:
    with open('artificats/similarity.pkl', 'rb') as file:
        similarity = p.load(file)
except Exception as e:
    st.error(f"Error loading similarity data: {e}")
    similarity = None

# Create movie list for the selectbox
if movies is not None:
    movies_list = movies['title'].values
else:
    st.error("Failed to load movie data. Please check the file and try again.")
# Streamlit UI: Movie selection
selected_movie = st.selectbox('Type or select a movie to get recommendations', movies_list)

# Show recommendations when the button is clicked
if st.button('Show Recommendation'):
    recommanded_movies_name, recommanded_movies_poster = recommend(selected_movie)
    
    # Layout for displaying recommended movies
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommanded_movies_name[0])
        st.image(recommanded_movies_poster[0])
    
    with col2:
        st.text(recommanded_movies_name[1])
        st.image(recommanded_movies_poster[1])
    
    with col3:
        st.text(recommanded_movies_name[2])
        st.image(recommanded_movies_poster[2])
    
    with col4:
        st.text(recommanded_movies_name[3])
        st.image(recommanded_movies_poster[3])
    
    with col5:
        st.text(recommanded_movies_name[4])
        st.image(recommanded_movies_poster[4])
