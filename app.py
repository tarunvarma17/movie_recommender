from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.validators import InputRequired

from func_test import square
from movie_methods import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "password123"

class RecForm(FlaskForm):
    username = StringField('username')
    submit = SubmitField('submit')

class PickForm(FlaskForm):
    start_year = IntegerField('start_year', default = 1900)
    end_year = IntegerField('end_year', default = 2020)
    genre = SelectField('genre', choices = [('Any', 'Any'), ('Action', 'Action'), ('Comedy', 'Comedy'), ('Crime', 'Crime'), ('Documentary', 'Documentary'), ('Drama', 'Drama'), ('History', 'History'), ('Horror', 'Horror'), ('Music', 'Musical'), ('Mystery', 'Mystery'), ('Romance', 'Romance'), ('Thriller', 'Thriller')])
    eng_only = BooleanField('eng_only')
    anim = BooleanField('anim')
    submit = SubmitField('submit')
    

@app.route('/form', methods = ['GET', 'POST'])
def form():
    form = RecForm()
    
    if form.validate_on_submit():
       
        user_movie = form.username.data.title()
        user_index = get_index_from_title(user_movie)
        orig_title = get_title_from_index(user_index)
        user_dir = get_dir_from_index(user_index)
        return render_template("form.html", form = form, uname = form.username.data, rec_list = content_rec(user_movie), orig_title = orig_title, director = user_dir, dir_list = same_director(user_movie))
    return render_template("form.html", form = form)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/pick', methods = ['GET', 'POST'])
def pick():
    form = PickForm()

    if form.validate_on_submit():
        sy = form.start_year.data

        ey = form.end_year.data
        genre = form.genre.data
        eng = form.eng_only.data
        anim = form.anim.data
        return render_template("pick.html", form = form, picklist = rec_crit(sy, ey, genre, eng, anim), genre = genre, eng = eng, anim = anim)
    return render_template("pick.html", form = form)

if __name__ == "__main__":
    app.run(debug = True)
