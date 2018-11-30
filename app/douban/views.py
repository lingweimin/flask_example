from flask import render_template
from ..main import main
from ..models.douban import Movie

@main.route('/douban')
def get_movies():
    movies = Movie.query.order_by(Movie.release.desc(), Movie.rate.desc())
    return render_template('douban/index.html', movies=movies)
