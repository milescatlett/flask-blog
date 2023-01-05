import os
from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mailman import Mail, EmailMessage
import db
import cr

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
app = Flask(__name__, instance_path=project_root, template_folder=template_path, static_folder=static_path)

UPLOAD_FOLDER = os.path.join(project_root, 'uploads')

app.config.update(
    SECRET_KEY=cr.secret_key,
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    MAIL_SERVER=cr.mail_server,
    MAIL_PORT=465,
    MAIL_USERNAME=cr.mail_username,
    MAIL_PASSWORD=cr.mail_password,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
)

mail = Mail(app)


@app.route('/')
def home():
    data = db.get_portfolio()
    return render_template('home.html', data=data)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:
        if request.method == 'POST':
            title = request.form['title']
            slug = db.check_slug(title)
            body = request.form['body']
            keywords = request.form['keywords']
            emgithub = request.form['emgithub']
            youtube = request.form['youtube']
            p_type = request.form['p_type']
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = '/uploads/' + filename
            db.submit_post(slug, title, body, image_path, emgithub, youtube, p_type, keywords)
        data = db.get_all()
        return render_template('dashboard.html', data=data)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "loggedin" in session:
        return redirect(url_for('dashboard'))
    else:
        msg = ''
        if 'loggedin' not in session:
            msg = 'You are not logged in.'
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            data = db.get_users()
            for i in range(len(data)):
                if data[i][0] == email and check_password_hash(data[i][1], password):
                    account = [data[i][0], data[i][1], data[i][2]]
                    session['id'] = account[2]
                    session['email'] = account[0]
                    session['loggedin'] = True
                    msg += "You've successfully logged in."
                    return redirect(url_for('dashboard'))
                else:
                    msg += "Sorry, that's the wrong info."
        return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        password_two = request.form['password_two']
        if password != password_two:
            msg = 'Passwords do not match!'
        else:
            hashed_password = generate_password_hash(password)
            db.add_user(fullname, email, hashed_password)
            msg = 'Thank you, ' + fullname + ', you have been registered. Please check your email.'
            email_msg = EmailMessage(
                'Thank You for Registering',
                'You have successfully registered your account. Please go to https://trlblzr.dev/login to log in.',
                'info@trlblzr.dev',
                ['milescatlett@gmail.com'],
                headers={'Message-ID': 'foo'},
            )
            email_msg.send()
    return render_template('register.html', msg=msg)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/blog')
def blog():
    articles = db.get_article()
    return render_template('articles.html', data=articles)


@app.route('/portfolio')
def portfolio():
    portfolio = db.get_portfolio()
    return render_template('portfolio.html', data=portfolio)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/blog/<slug>')
def article(slug):
    article = db.get_article_by_slug(slug)
    return render_template('article.html', article=article)


@app.route('/portfolio/<slug>')
def entry(slug):
    entry = db.get_article_by_slug(slug)
    return render_template('entry.html', entry=entry)


@app.route('/dashboard/<slug>', methods=['GET', 'POST'])
def update(slug):
    if 'loggedin' in session:
        fpath = request.full_path
        post = db.get_article_by_slug(slug)
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            keywords = request.form['keywords']
            emgithub = request.form['emgithub']
            youtube = request.form['youtube']
            p_type = request.form['p_type']
            try:
                file = request.files['file']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = '/uploads/' + filename
            except:
                image_path = post[0][5]
            db.update_post(slug, title, body, image_path, emgithub, youtube, p_type, keywords)
            return redirect(fpath)
        return render_template('create.html', post=post[0], fpath=fpath)
    else:
        return redirect(url_for('login'))


application = app


if __name__ == '__main__':
    app.run()
