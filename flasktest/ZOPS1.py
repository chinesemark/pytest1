from flask import Flask
from flask import request
from flask import redirect
from flask import make_response
from flask import render_template

from flask_bootstrap import Bootstrap

from datetime import datetime
from flask_moment import Moment

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)

bootstrap = Bootstrap(app)

moment = Moment(app)


app.config['SECRET_KEY'] = 'hard to guess string'



class NameForm(FlaskForm):
 name = StringField('What is your name?', validators=[DataRequired()])
 id  = StringField(validators=[DataRequired()])
 submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
 name = None
 id = None
 form = NameForm()
 if form.validate_on_submit():
  name = form.name.data
  id = form.id.data
  form.name.data = ''
 return render_template('index.html', form=form, name=name,id=id)

 #return redirect('http://www.bing.com')

@app.route('/user/<name>')
def user(name):
 return  render_template ('user.html', name = name)


@app.errorhandler(404)
def internal_server_error(e):
 return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500


if __name__ == '__main__':
 app.run(debug=True)

