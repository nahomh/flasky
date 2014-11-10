from flask import Flask, render_template, session, redirect, url_for, flash
from flask import request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form #class form
from wtforms import StringField, SubmitField #fields 
from wtforms.validators import Required #param required
from flask.ext.sqlalchemy import SQLAlchemy 
from flask.ext.script import Shell #adding a shell context
from flask.ext.migrate import Migrate, MigrateCommand
import os




app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_a_test_string' #CSRF protection --> should be stored in an enviornment variable rather than embedded in the actual code

#initializations
manager=Manager(app) #initiate manager for server
bootstrap=Bootstrap(app) #initiate bootstrap for styling
moment=Moment(app) #initiate moment for time
db=SQLAlchemy(app) #initiate db

migrate=Migrate(app,db) #initiate migrations


#adding data abstraction layer using sqlalchemy 
basedir = os.path.abspath(os.path.dirname(__file__)) #db location
app.config['SQLALCHEMY_DATABASE_URI'] =\
 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#models for db
class Role(db.Model):
	__tablename__='roles'
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(64), unique=True)
	#relationships
	users=db.relationship('User', backref='role',lazy='dynamic')

	def __repr_(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__='users'
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(64),unique=True,index=True)
	role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))


	def __repr__(self):
 		return '<User %r>' % self.username



#Forms
class NameForm(Form):
	name=StringField("What is your name?",validators=[Required()])
	Submit=SubmitField('Submit')


#Routes
@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
 		user = User.query.filter_by(username=form.name.data).first()
 		if user is None:
 			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
		else:
 			session['known'] = True
 		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
 	return render_template('index.html',
 form = form, name = session.get('name'),
 known = session.get('known', False))

#The code below doesn't work due to the fact that the information
# @app.route('/', methods=['GET', 'POST']) #need to specift post otherwise defaulted to get requests only
# def index():
#  name = None
#  form = NameForm()
#  if form.validate_on_submit():
#  	name = form.name.data
#  	form.name.data = ''
#  return render_template('index.html', form=form, name=name) #need Post/ Redirect/Get pattern here in order to not send another post request at the refresh button. 


@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)


#custom routes for error handeling 
@app.errorhandler(404)
def page_not_found(e):
 return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500

#adding a shell context
def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)


#commands
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand) #expose migration commands


#Application start
if __name__ == '__main__':
	manager.run()




#In order to call a template you need to import the render_template functionality

#url_for(params) -> used for dynamic routing and organization of routes