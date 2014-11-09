from flask import Flask, render_template, session, redirect, url_for, flash
from flask import request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form #class form
from wtforms import StringField, SubmitField #fields 
from wtforms.validators import Required #param required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_a_test_string' #CSRF protection --> should be stored in an enviornment variable rather than embedded in the actual code

manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)

#Forms
class NameForm(Form):
	name=StringField("What is your name?",validators=[Required()])
	Submit=SubmitField('Submit')


#Routes
@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
 	if form.validate_on_submit():
 		old_name = session.get('name')
 		if old_name is not None and old_name != form.name.data:
 			flash('Looks like you have changed your name!')
		session['name'] = form.name.data
		form.name.data = ''
 		return redirect(url_for('index'))
	return render_template('index.html', form = form, name = session.get('name'))


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


#custom error handeling 

@app.errorhandler(404)
def page_not_found(e):
 return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500


#Application start
if __name__ == '__main__':
	manager.run()




#In order to call a template you need to import the render_template functionality

#url_for(params) -> used for dynamic routing and organization of routes