from flask import Flask  , render_template  , request 
import pickle
import pandas as pd
from patsy import dmatrices
import requests

movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9f94ba1be62276745b2d383655dc5dec&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_name.append(movies.iloc[i[0]].title)
        
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies_name,recommended_movies_poster


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recommend', methods=['GET', 'POST'])
def recommend_handler():
    movie_list = movies['title'].values
    status=False
    if request.method == 'POST':
        try:
            if request.form:
                movies_name = request.form.get('movies')
                print(movies_name)
                recommended_movies_name, recommended_movies_poster = recommend(movies_name)
                print(recommended_movies_name)
                print(recommended_movies_poster)
                status=True
                return render_template("recommend.html", movies_name=recommended_movies_name , poster=recommended_movies_poster,movie_list=movie_list , status=status)

        except Exception as e:
            error = {'error': e}
            return render_template("recommend.html" ,error=error, movie_list=movie_list, status=status)

    else:
        return render_template("recommend.html", movie_list=movie_list,status=status)




if __name__ == '__main__':
    app.run(debug=True)