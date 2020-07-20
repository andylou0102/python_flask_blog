from flask import (Blueprint, render_template, url_for,
                    redirect, flash, request)
from blog import db, bcrypt, mail
from blog.model import User, Post
from blog.users.forms import (RegistrationForm, LoginForm, AccountUpdateForm,
                            RequestResetForm, ResetPasswordForm, ContectForm)
from flask_login import login_user, current_user, login_required, logout_user
from blog.users.func import save_picture, send_reset_email
from flask_mail import Message

users = Blueprint('users', __name__)

@users.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("註冊完成! 可以開始登入", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form = form, title = "Register")

@users.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("登入失敗. 請檢查信箱和密碼是否正確", "danger")
    return render_template("login.html", form = form, title = "Login")

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('個人資料更新完成', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', form = form, image_file = image_file, title = 'Account')

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('信件已送出. 請前往信箱查看', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form = form, title = 'Reset Password')

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('密碼更新完成. 可以開始登入', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form = form, title = 'Reset Password')

@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
                .order_by(Post.date.desc())\
                .paginate(page=page, per_page=6)
    return render_template('user_posts.html', posts = posts, user = user)

@users.route('/contect', methods = ['GET', 'POST'])
def contect():
    form = ContectForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone_number = form.phone_number.data
        msg = form.message.data

        message = Message('Hi! '+ name, sender='noreply@gmail.com', recipients=[email])
        message.body = f'''{msg} 
            my phone number is(+886){phone_number}, you can direct contecting me by phone call.'''
        mail.send(message)

        flash("傳送完成，收到會盡速回覆，謝謝!", "success")
        return redirect(url_for("users.contect"))
    return render_template("contect.html", form = form, title = "Contect")