from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)

class NameForm(Form):
 name = StringField('What is your name?', validators=[Required()])
 submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
 form = NameForm()
 if form.validate_on_submit():
  session['name'] = form.name.data
  return redirect(url_for('index'))
 return render_template('index.html', form=form, name=session.get('name'))


if __name__ == '__main__':
 app.run(port=80)
