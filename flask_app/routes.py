from flask import render_template, flash, redirect, url_for, request
from flask_bcrypt import check_password_hash
from flask_app import app, db, crypt, forms, database_model as dm
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import secrets
import os


post_data_1 = [{'title': "Blog-1", 'desc': 'The first blog.', 'author': 'Deepankar', 'date_posted': '12th june'},
             {'title': "Blog-2", 'desc': 'The 2nd blog.', 'author': 'alien', 'date_posted': '11th june'}]


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", post_data_1 = post_data_1)


@app.route('/about')
def about():
    return render_template("about.html", title = "About Page")


@app.route('/register', methods=['GET', 'POST'])
def register():
    # if user is already logged in then it will not allow
    # the user to sign up again.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.RegistrationForm()

    # validate_on_submit() . This function returns True if the
    # form has been both submitted (i.e. if the HTTP method is PUT or POST)
    # and validated by the validators we defined in forms.py.
    if form.validate_on_submit():
        hashed_pass = crypt.generate_password_hash(form.password.data).decode("utf-8")
        user = dm.User(username= form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Now you can Log In.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    # if user is already logged in then it will not allow
    # the user to login again.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = forms.User.query.filter_by(email = form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash('You are logged in successfully', 'success')

            next_page = request.args.get('next', None)
            if next_page:
                return redirect(url_for(next_page[1:]))
            else:
                return redirect(url_for('home'))
        else:
            flash('Wrong email or password entered. Try Again', 'danger')
    return render_template("login.html",title = "Login Page", form=form)


# Creating log_out route.
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = forms.UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User details updated successfully.', 'success')
        return redirect(url_for('account'))

    # to fill the updated form with values already present
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Personal Profile", image_file = image_file, form = form)
