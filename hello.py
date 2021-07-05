# author : lobotijo
from flask import  Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import  Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import  date

from wtforms.widgets.core import TextArea

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

# Create Blog post Model
class Posts(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(255))
	content=db.Column(db.Text)
	author=db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug=db.Column(db.String(255))

#create a POSTS from 
class PostsForm(FlaskForm):
	title=StringField("Title", validators=[DataRequired()])
	content=StringField("Content", validators=[DataRequired()], widget=TextArea())
	author= StringField("Author", validators=[DataRequired()])
	slug=StringField("Slug", validators=[DataRequired()])
	submit=SubmitField("Submit")

#add POST 
@app.route('/add-post', methods=['POST', 'GET'])
def add_post():
	form=PostsForm()
	
	if form.validate_on_submit():
		post = Posts(title=form.title.data,content=form.content.data,author=form.author.data,slug=form.slug.data)
		form.title.data=''
		form.content.data=''
		form.author.data=''
		form.slug.data=''

		#add data to database
		db.session.add(post)
		db.session.commit()
		# return a message
		flash("Blog is created successfully")
		#redirect to webpage
	return render_template('add_post.html', form=form)

#route api
@app.route('/date')
def get_current_date():
	return { "Date": date.today()}

#create model
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False, unique=True)
	favorite_color = db.Column(db.String(15))
	date_added= db.Column(db.DateTime, default=datetime.utcnow)
	#do some 'context' : {'default_order_id' : self.order_id},
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError('Password is not readable, Try again')
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
		
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

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
	password_hash=PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Password must be Match')])
	password_hash2=PasswordField("Confirm Password")
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

# password form
class PasswordForm(FlaskForm):
	email = StringField("email ", validators=[DataRequired()])
	password_hash = PasswordField("password ", validators=[DataRequired()])
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
			#hash 'context' : {'default_order_id' : self.order_id},
			hash_pw= generate_password_hash(form.password_hash.data, "sha256")
			user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hash_pw)
			db.session.add(user);
			db.session.commit()
		name = form.name.data
		form.name.data=''
		form.email.data=''
		form.favorite_color.data=''
		form.password_hash.data=''
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

# create test_pw`
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
	email= None
	password=None
	pw_to_check=None
	passed=None,
	form= PasswordForm()
	# validate form
	if form.validate_on_submit():
		email= form.email.data
		password= form.password_hash.data
		#clear form
		form.email.data = ''
		form.password_hash.data = ''
		#flash("Form Submit Successfully")
		pw_to_check= Users.query.filter_by(email=email).first()

		# check hash password
		passed=check_password_hash(pw_to_check.password_hash, password)

	return render_template("test_pw.html",
	email=email,
	password=password,
	pw_to_check=pw_to_check,
	passed=passed,
	form=form)


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
