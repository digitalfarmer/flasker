# author : lobotijo
from flask import  Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# create flask instance
app = Flask(__name__)
app.config['SECRET_KEY']="lobotijo"

# create form class
class NameForm(FlaskForm):
	name = StringField("What's Your Name", validators=[DataRequired()])
	submit = SubmitField("Submit")


# create route
@app.route('/')
# def index():
# 	return "<h1>Hello Flask</h1>"

def index():
	first_name = 'Ades'
	pframework=['Flask','Django','Pyramid','Keras','pyTorch', 32]
	return render_template("index.html", first_name=first_name, pframework=pframework)

@app.route('/user/<name>')
def user(name):
	return render_template("user.html", user_name=name)

# create custom error page


# create invalid route
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# internal server error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500

# create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
	name= None
	form= NameForm()
	# validate form
	if form.validate_on_submit():
		name= form.name.data
		form.name.data = ''
	return render_template("name.html",
	name=name,
	form=form)
