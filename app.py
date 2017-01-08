# usr/bin/python -tt
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
import logging
from logging import Formatter, FileHandler
from forms import *
from models import *
import os
import json
import glob
from werkzeug.security import check_password_hash
import youtube_dl

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Automatically tear down SQLAlchemy.
#
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

#----------------------------------------------------------------------------#
# Controllers/Routes
#----------------------------------------------------------------------------#


@app.route('/')
def home():
	return render_template('pages/home.html')

@app.route('/player')
def player():
	return render_template('pages/player.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)

	if (request.method == "POST"):
		userName = request.form["name"]
		password = request.form["password"]

		client = User.query.filter_by(username = userName).first()
		# If our database query came up empty...
		if (client is None):
			# Deny their ass and make them try again!
			flash("Could not find the specified user!", "error")
			return redirect(url_for("login"))

		if (check_password_hash(client.password, password)):
			login_user(client)
			flash("Logged in successfully")
			return redirect(url_for("submit"))
		else:
			flash("Invalid username and password combination!", "error")
			return redirect(url_for("login"))

	return render_template("forms/login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)

	if request.method == 'GET':
		return render_template('forms/register.html', form=form)

	#Checks if passwords and confirmation are the same
	if (request.form['password'] != request.form['confirm']):
		flash("Password confirmation mismatch", "error")
		return render_template('forms/register.html', form=form)
	#If matches, puts in DB
	else:
		user = User(request.form['name'], request.form['password'])
		db.session.add(user)
		db.session.commit()
		flash("Sucessfully made user")
		return redirect(url_for('login'))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
	form = PostForm(request.form)
	if request.method == 'POST':
		info = get_info(request.form['url'])
		fileName = (info['title']+ "-" +info['uploader']+".mp3")
		post = Posting(request.form['url'], info['title'], info['uploader'], fileName, current_user.id, current_user.username)
		db.session.add(post)
		db.session.commit()
		flash("Submitted Successfully")
		return redirect(url_for('posts'))
	return render_template('forms/submit.html', form=form)


@app.route('/posts', methods=['GET'])
def posts():
	posts = Posting.query.order_by(Posting.id)
	return render_template('pages/post.html', posts=posts)

@app.route('/post/<int:page_id>')
def page(page_id):
	count = Posting.query.order_by(Posting.id).count()
	if (page_id > count) or (page_id == 0):
		return render_template('errors/404.html'), 404
	post = Posting.query.filter_by(id=page_id).first()
	get_song(post.url)
	return render_template('pages/posting_player.html', post=post)

@app.route('/user')
@login_required
def user():
	user = User.query.filter_by(id=current_user.id).first()
	posts = Posting.query.filter_by(user_id=current_user.id)
	return render_template('pages/user.html', user=user, posts=posts)

@app.route('/user/<int:user_id>')
def user_page(user_id):
	count = User.query.order_by(User.id).count()
	if (user_id > count) or (user_id == 0) :
		return render_template('errors/404.html'), 404
	user = User.query.filter_by(id=user_id).first()
	posts = Posting.query.filter_by(user_id=user_id)
	return render_template('pages/user.html', user=user, posts=posts)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("Logged out successfully")
	return redirect(url_for('home'))

#Error handlers.

@app.errorhandler(500)
def internal_error(error):
	return render_template('errors/500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
	return render_template('errors/404.html'), 404

if not app.debug:
	file_handler = FileHandler('error.log')
	file_handler.setFormatter(
		Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
	)
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('errors')

#YouTube DL Script by Elias
def get_song(url):
	options = {
		'format':'bestaudio/best',
		'extractaudio':True,
		'audioformat':'mp3',
		'outtmpl': 'tmp/%(title)s-%(uploader)s.%(ext)s',
		'noplaylist': True,
		'nocheckcertificate':True,
		'postprocessors': [{
			'key':'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '128',
		}]
	}
	with youtube_dl.YoutubeDL(options) as ydl:
		ydl.download([url])

def get_info(url):
	data = {}
	ydl = youtube_dl.YoutubeDL()
	with ydl:
		data = ydl.extract_info(url, download=False)
	return data

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
	app.run()

# Uncomment if you want to specify post
'''
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
'''
