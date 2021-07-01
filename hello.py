# author : lobotijo
from flask import  Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import  Migrate
from datetime import datetime

# create flask instance
app = Flask(__name__)

#add sqlite database													

#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
#MysqlDataBase
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://ades:admin123@localhost/flaskblog'
#secret key
app.config['SECRET_KEY']="lobotijo"

#initial database
db= SQLAlchemy(app)
migrate = Migrate(app,db)

#create model
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False, unique=True)
	favorite_color = db.Column(db.String(15))
	date_added= db.Column(db.DateTime, default=datetime.utcnow)

	#Create A String
	def __repr__(self):
		return '<Name %r>' % self.name

@app.route('/delete/<int:id>')
def delete(id):
	user_to_delete = Users.query.get_or_404(id)
	name = None
	form = UserForm()

	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("User Delete successfully")
		our_users = Users.query.order_by(Users.date_added)
		return render_template('add_user.html', 
		form=form, 
		name=name, 
		our_users= our_users)
	except:
		flash("Problem Delete User, Try again,..")
		return render_template('add_user.html', 
		form=form, 
		name=name, 
		our_users= our_users)

# create form class
class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	favorite_color = StringField("Favorite Color")
	submit = SubmitField("Submit")

# updateuser
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
	form = UserForm()
	name_to_update= Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name= request.form['name']		
		name_to_update.email= request.form['email']
		name_to_update.favorite_color= request.form['favorite_color']
		try:
			db.session.commit()
			flash("User update successfully!")
			return render_template("update.html",form=form,name_to_update=name_to_update)
		except :
			flash("User update Error try again,.. !")
			return render_template("update.html",form=form,name_to_update=name_to_update)
	else:
		return render_template("update.html",form=form,name_to_update=name_to_update)

class NameForm(FlaskForm):
	name = StringField("What your Name ", validators=[DataRequired()])
	submit = SubmitField("Submit")


# def index():
# 	return "<h1>Hello Flask</h1>"

# create route
@app.route('/user/add', methods=['GET','POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
			db.session.add(user);
			db.session.commit()
		name = form.name.data
		form.name.data=''
		form.email.data=''
		form.favorite_color.data=''
		flash('User added successfully')
	our_users = Users.query.order_by(Users.date_added)
	return render_template('add_user.html', 
		form=form,
		name=name,
		our_users= our_users	
		)

@app.route('/')
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

# create name page`
@app.route('/name', methods=['GET', 'POST'])
def name():
	name= None
	form= NameForm()
	# validate form
	if form.validate_on_submit():
		name= form.name.data
		form.name.data = ''
		flash("Form Submit Successfully")

	return render_template("name.html",
	name=name,
	form=form)
