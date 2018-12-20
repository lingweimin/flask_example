from flask import render_template
from ..main import main


@main.route('/quotes')
def get_movies():
    return render_template('quotes/index.html')
