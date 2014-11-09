from flask import Flask, render_template
from flask import request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime

app = Flask(__name__)
manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)

@app.route('/index')
def index():
	return render_template('index.html',current_time=datetime.utcnow())


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

if __name__ == '__main__':
	manager.run()




#In order to call a template you need to import the render_template functionality

#url_for(params) -> used for dynamic routing and organization of routes