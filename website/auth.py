from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
import re


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect the user if they are already logged in
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('auth.adminPanel'))
        else:
            return redirect(url_for('views.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                if user.is_admin:
                    flash('Logged in successfully Admin!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('auth.adminPanel'))
                else:
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.index'))
            else:
                flash('Wrong username or password.', category='error')
        else:
            flash('This account does not exist.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


def send_welcome_email(user):
    msg = Message('Registered Successfully',
                  sender='noreply@headmouseweb.com', recipients=[user.email])
    msg.body = f'''Welcome to Headmouse Web, {user.firstName}!

 You have successfully registered with your account. You can now log in to your account using your credentials.
'''
    from . import mail
    mail.send(msg)


@auth.route('/adminPanel')
# @login_required
def adminPanel():
    if not current_user.is_authenticated:
        flash('Please log in as an admin to access this page!', category='error')
        return redirect(url_for('auth.login'))
    elif not isinstance(current_user, User) or not current_user.is_admin:
        flash('You are not authorized to view this page.', category='error')
        return redirect(url_for('views.index'))
    else:
        return render_template("admin.html", users=User.query, user=current_user)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect the user if they are already logged in
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('auth.adminPanel'))
        else:
            return redirect(url_for('views.index'))

    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        country = request.form.get('country')
        gender = request.form.get('gender')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email is already linked to an account!', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')

        elif not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            flash('Invalid email format. Please enter a valid email!',
                  category='error')

        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')

        elif len(lastName) < 2:
            flash('Last name must be greater than 1 character.', category='error')

        elif not re.match("^[A-Za-z]+$", firstName):
            flash('First name should contain only letters', category='error')

        elif not re.match("^[A-Za-z]+$", lastName):
            flash('Last name should contain only letters', category='error')

        elif password != password2:
            flash('Passwords do not match.', category='error')

        elif " " in password:
            flash('Password should not contain spaces', category='error')

        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')

        else:
            # add user to database
            new_user = User(email=email, firstName=firstName.replace(" ", ""), lastName=lastName.replace(" ", ""), password=generate_password_hash(
                password, method='sha256'), country=country, gender=gender)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            send_welcome_email(new_user)
            flash('Account created successfully!', category='success')

            return redirect(url_for('views.index'))
    return render_template("register.html", user=current_user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@headmouseweb.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.resetPassword', token=token, _external=True)}
This link will expire in 5 minutes.
If you did not make this request then simply ignore this email and no changes will be made.
'''
    from . import mail
    mail.send(msg)


@auth.route('/requestResetPassword', methods=['GET', 'POST'])
def requestResetPassword():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        if request.method == 'POST':
            email = request.form.get('email')

            user = User.query.filter_by(email=email).first()
            if user:
                # send email with reset password link
                send_reset_email(user)
                flash('Email sent with instructions!', category='success')
                return redirect(url_for('auth.login'))
            else:
                flash('Email does not exist.', category='error')
        return render_template("requestPassword.html", user=current_user)


@auth.route('/resetPassword/<token>', methods=['GET', 'POST'])
def resetPassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', category='error')
        return redirect(url_for('auth.requestResetPassword'))
    else:
        if request.method == 'POST':
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            if user:
                if password != confirm_password:
                    flash('Passwords don\'t match.', category='error')

                elif len(password) == 0 or len(confirm_password) == 0:
                    flash('Please enter a password.',
                          category='error')

                elif " " in password:
                    flash('Password should not contain spaces', category='error')

                elif len(password) < 7:
                    flash('Password must be at least 7 characters.',
                          category='error')

                else:
                    hashed_password = generate_password_hash(
                        password, method='sha256')
                    user.password = hashed_password
                    db.session.commit()
                    flash('Your password has been updated!', category='success')
                    return redirect(url_for('auth.login'))
        return render_template("resetPassword.html", user=current_user)


def password_changed(user):
    msg = Message('Password Changed',
                  sender='noreply@headmouseweb.com', recipients=[user.email])
    msg.body = f'''Hi {user.firstName},

 You have successfully changed your account password. If you did not make this change, please contact us immediately.
'''
    from . import mail
    mail.send(msg)


@auth.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    if request.method == 'POST':
        currentPassword = request.form.get('currentPassword')
        newPassword = request.form.get('newPassword')
        confirmNewPassword = request.form.get('confirmNewPassword')

        if check_password_hash(current_user.password, currentPassword):
            if newPassword != confirmNewPassword:
                flash('Passwords don\'t match.', category='error')

            elif len(newPassword) == 0 or len(confirmNewPassword) == 0:
                flash('Please enter a password.', category='error')

            elif " " in newPassword:
                flash('Password should not contain spaces', category='error')

            elif len(newPassword) < 7:
                flash('Password must be at least 7 characters.', category='error')

            else:
                hashed_password = generate_password_hash(
                    newPassword, method='sha256')
                current_user.password = hashed_password
                db.session.commit()
                password_changed(current_user)
                flash('Password changed successfully!', category='success')

                return redirect(url_for('views.userProfile'))
        else:
            flash(
                'Incorrect password, please enter your current account password.', category='error')

    return render_template("changePassword.html", user=current_user)
