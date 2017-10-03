from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap

from datetime import datetime
from flask_moment import Moment
app = Flask(__name__)



bootstrap = Bootstrap(app)

moment = Moment(app)


app.config['SECRET_KEY'] = 'hard to guess string'
class NameForm(FlaskForm):
 name = StringField('What is your name?', validators=[DataRequired()])
 submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
 name= None
 form = NameForm()
 if form.validate_on_submit():
  name = form.name.data
 #return redirect(url_for('index'))
 return render_template('index.html', form=form, name=name)


if __name__ == '__main__':
 app.run(port=80)
